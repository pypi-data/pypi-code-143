import contextlib
import inspect
import io
import json
import math
import queue
import sys
import typing
import warnings
from concurrent.futures import Future
from types import GeneratorType
from urllib.parse import unquote, urljoin

import anyio
import anyio.from_thread
import httpx
from anyio.streams.stapled import StapledObjectStream

from starlette._utils import is_async_callable
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.websockets import WebSocketDisconnect

if sys.version_info >= (3, 8):  # pragma: no cover
    from typing import TypedDict
else:  # pragma: no cover
    from typing_extensions import TypedDict

_PortalFactoryType = typing.Callable[
    [], typing.ContextManager[anyio.abc.BlockingPortal]
]

ASGIInstance = typing.Callable[[Receive, Send], typing.Awaitable[None]]
ASGI2App = typing.Callable[[Scope], ASGIInstance]
ASGI3App = typing.Callable[[Scope, Receive, Send], typing.Awaitable[None]]


_RequestData = typing.Mapping[str, typing.Union[str, typing.Iterable[str]]]


def _is_asgi3(app: typing.Union[ASGI2App, ASGI3App]) -> bool:
    if inspect.isclass(app):
        return hasattr(app, "__await__")
    return is_async_callable(app)


class _WrapASGI2:
    """
    Provide an ASGI3 interface onto an ASGI2 app.
    """

    def __init__(self, app: ASGI2App) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        instance = self.app(scope)
        await instance(receive, send)


class _AsyncBackend(TypedDict):
    backend: str
    backend_options: typing.Dict[str, typing.Any]


class _Upgrade(Exception):
    def __init__(self, session: "WebSocketTestSession") -> None:
        self.session = session


class WebSocketTestSession:
    def __init__(
        self,
        app: ASGI3App,
        scope: Scope,
        portal_factory: _PortalFactoryType,
    ) -> None:
        self.app = app
        self.scope = scope
        self.accepted_subprotocol = None
        self.portal_factory = portal_factory
        self._receive_queue: "queue.Queue[typing.Any]" = queue.Queue()
        self._send_queue: "queue.Queue[typing.Any]" = queue.Queue()
        self.extra_headers = None

    def __enter__(self) -> "WebSocketTestSession":
        self.exit_stack = contextlib.ExitStack()
        self.portal = self.exit_stack.enter_context(self.portal_factory())

        try:
            _: "Future[None]" = self.portal.start_task_soon(self._run)
            self.send({"type": "websocket.connect"})
            message = self.receive()
            self._raise_on_close(message)
        except Exception:
            self.exit_stack.close()
            raise
        self.accepted_subprotocol = message.get("subprotocol", None)
        self.extra_headers = message.get("headers", None)
        return self

    def __exit__(self, *args: typing.Any) -> None:
        try:
            self.close(1000)
        finally:
            self.exit_stack.close()
        while not self._send_queue.empty():
            message = self._send_queue.get()
            if isinstance(message, BaseException):
                raise message

    async def _run(self) -> None:
        """
        The sub-thread in which the websocket session runs.
        """
        scope = self.scope
        receive = self._asgi_receive
        send = self._asgi_send
        try:
            await self.app(scope, receive, send)
        except BaseException as exc:
            self._send_queue.put(exc)
            raise

    async def _asgi_receive(self) -> Message:
        while self._receive_queue.empty():
            await anyio.sleep(0)
        return self._receive_queue.get()

    async def _asgi_send(self, message: Message) -> None:
        self._send_queue.put(message)

    def _raise_on_close(self, message: Message) -> None:
        if message["type"] == "websocket.close":
            raise WebSocketDisconnect(
                message.get("code", 1000), message.get("reason", "")
            )

    def send(self, message: Message) -> None:
        self._receive_queue.put(message)

    def send_text(self, data: str) -> None:
        self.send({"type": "websocket.receive", "text": data})

    def send_bytes(self, data: bytes) -> None:
        self.send({"type": "websocket.receive", "bytes": data})

    def send_json(self, data: typing.Any, mode: str = "text") -> None:
        assert mode in ["text", "binary"]
        text = json.dumps(data)
        if mode == "text":
            self.send({"type": "websocket.receive", "text": text})
        else:
            self.send({"type": "websocket.receive", "bytes": text.encode("utf-8")})

    def close(self, code: int = 1000) -> None:
        self.send({"type": "websocket.disconnect", "code": code})

    def receive(self) -> Message:
        message = self._send_queue.get()
        if isinstance(message, BaseException):
            raise message
        return message

    def receive_text(self) -> str:
        message = self.receive()
        self._raise_on_close(message)
        return message["text"]

    def receive_bytes(self) -> bytes:
        message = self.receive()
        self._raise_on_close(message)
        return message["bytes"]

    def receive_json(self, mode: str = "text") -> typing.Any:
        assert mode in ["text", "binary"]
        message = self.receive()
        self._raise_on_close(message)
        if mode == "text":
            text = message["text"]
        else:
            text = message["bytes"].decode("utf-8")
        return json.loads(text)


class _TestClientTransport(httpx.BaseTransport):
    def __init__(
        self,
        app: ASGI3App,
        portal_factory: _PortalFactoryType,
        raise_server_exceptions: bool = True,
        root_path: str = "",
    ) -> None:
        self.app = app
        self.raise_server_exceptions = raise_server_exceptions
        self.root_path = root_path
        self.portal_factory = portal_factory

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        scheme = request.url.scheme
        netloc = request.url.netloc.decode(encoding="ascii")
        path = request.url.path
        raw_path = request.url.raw_path
        query = request.url.query.decode(encoding="ascii")

        default_port = {"http": 80, "ws": 80, "https": 443, "wss": 443}[scheme]

        if ":" in netloc:
            host, port_string = netloc.split(":", 1)
            port = int(port_string)
        else:
            host = netloc
            port = default_port

        # Include the 'host' header.
        if "host" in request.headers:
            headers: typing.List[typing.Tuple[bytes, bytes]] = []
        elif port == default_port:  # pragma: no cover
            headers = [(b"host", host.encode())]
        else:  # pragma: no cover
            headers = [(b"host", (f"{host}:{port}").encode())]

        # Include other request headers.
        headers += [
            (key.lower().encode(), value.encode())
            for key, value in request.headers.items()
        ]

        scope: typing.Dict[str, typing.Any]

        if scheme in {"ws", "wss"}:
            subprotocol = request.headers.get("sec-websocket-protocol", None)
            if subprotocol is None:
                subprotocols: typing.Sequence[str] = []
            else:
                subprotocols = [value.strip() for value in subprotocol.split(",")]
            scope = {
                "type": "websocket",
                "path": unquote(path),
                "raw_path": raw_path,
                "root_path": self.root_path,
                "scheme": scheme,
                "query_string": query.encode(),
                "headers": headers,
                "client": ["testclient", 50000],
                "server": [host, port],
                "subprotocols": subprotocols,
            }
            session = WebSocketTestSession(self.app, scope, self.portal_factory)
            raise _Upgrade(session)

        scope = {
            "type": "http",
            "http_version": "1.1",
            "method": request.method,
            "path": unquote(path),
            "raw_path": raw_path,
            "root_path": self.root_path,
            "scheme": scheme,
            "query_string": query.encode(),
            "headers": headers,
            "client": ["testclient", 50000],
            "server": [host, port],
            "extensions": {"http.response.template": {}},
        }

        request_complete = False
        response_started = False
        response_complete: anyio.Event
        raw_kwargs: typing.Dict[str, typing.Any] = {"stream": io.BytesIO()}
        template = None
        context = None

        async def receive() -> Message:
            nonlocal request_complete

            if request_complete:
                if not response_complete.is_set():
                    await response_complete.wait()
                return {"type": "http.disconnect"}

            body = request.read()
            if isinstance(body, str):
                body_bytes: bytes = body.encode("utf-8")  # pragma: no cover
            elif body is None:
                body_bytes = b""  # pragma: no cover
            elif isinstance(body, GeneratorType):
                try:  # pragma: no cover
                    chunk = body.send(None)
                    if isinstance(chunk, str):
                        chunk = chunk.encode("utf-8")
                    return {"type": "http.request", "body": chunk, "more_body": True}
                except StopIteration:  # pragma: no cover
                    request_complete = True
                    return {"type": "http.request", "body": b""}
            else:
                body_bytes = body

            request_complete = True
            return {"type": "http.request", "body": body_bytes}

        async def send(message: Message) -> None:
            nonlocal raw_kwargs, response_started, template, context

            if message["type"] == "http.response.start":
                assert (
                    not response_started
                ), 'Received multiple "http.response.start" messages.'
                raw_kwargs["status_code"] = message["status"]
                raw_kwargs["headers"] = [
                    (key.decode(), value.decode())
                    for key, value in message.get("headers", [])
                ]
                response_started = True
            elif message["type"] == "http.response.body":
                assert (
                    response_started
                ), 'Received "http.response.body" without "http.response.start".'
                assert (
                    not response_complete.is_set()
                ), 'Received "http.response.body" after response completed.'
                body = message.get("body", b"")
                more_body = message.get("more_body", False)
                if request.method != "HEAD":
                    raw_kwargs["stream"].write(body)
                if not more_body:
                    raw_kwargs["stream"].seek(0)
                    response_complete.set()
            elif message["type"] == "http.response.template":
                template = message["template"]
                context = message["context"]

        try:
            with self.portal_factory() as portal:
                response_complete = portal.call(anyio.Event)
                portal.call(self.app, scope, receive, send)
        except BaseException as exc:
            if self.raise_server_exceptions:
                raise exc

        if self.raise_server_exceptions:
            assert response_started, "TestClient did not receive any response."
        elif not response_started:
            raw_kwargs = {
                "status_code": 500,
                "headers": [],
                "stream": io.BytesIO(),
            }

        raw_kwargs["stream"] = httpx.ByteStream(raw_kwargs["stream"].read())

        response = httpx.Response(**raw_kwargs, request=request)
        if template is not None:
            response.template = template  # type: ignore[attr-defined]
            response.context = context  # type: ignore[attr-defined]
        return response


class TestClient(httpx.Client):
    __test__ = False
    task: "Future[None]"
    portal: typing.Optional[anyio.abc.BlockingPortal] = None

    def __init__(
        self,
        app: ASGIApp,
        base_url: str = "http://testserver",
        raise_server_exceptions: bool = True,
        root_path: str = "",
        backend: str = "asyncio",
        backend_options: typing.Optional[typing.Dict[str, typing.Any]] = None,
        cookies: httpx._client.CookieTypes = None,
        headers: typing.Dict[str, str] = None,
    ) -> None:
        self.async_backend = _AsyncBackend(
            backend=backend, backend_options=backend_options or {}
        )
        if _is_asgi3(app):
            app = typing.cast(ASGI3App, app)
            asgi_app = app
        else:
            app = typing.cast(ASGI2App, app)  # type: ignore[assignment]
            asgi_app = _WrapASGI2(app)  # type: ignore[arg-type]
        self.app = asgi_app
        transport = _TestClientTransport(
            self.app,
            portal_factory=self._portal_factory,
            raise_server_exceptions=raise_server_exceptions,
            root_path=root_path,
        )
        if headers is None:
            headers = {}
        headers.setdefault("user-agent", "testclient")
        super().__init__(
            app=self.app,
            base_url=base_url,
            headers=headers,
            transport=transport,
            follow_redirects=True,
            cookies=cookies,
        )

    @contextlib.contextmanager
    def _portal_factory(self) -> typing.Generator[anyio.abc.BlockingPortal, None, None]:
        if self.portal is not None:
            yield self.portal
        else:
            with anyio.from_thread.start_blocking_portal(
                **self.async_backend
            ) as portal:
                yield portal

    def _choose_redirect_arg(
        self,
        follow_redirects: typing.Optional[bool],
        allow_redirects: typing.Optional[bool],
    ) -> typing.Union[bool, httpx._client.UseClientDefault]:
        redirect: typing.Union[
            bool, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT
        if allow_redirects is not None:
            message = (
                "The `allow_redirects` argument is deprecated. "
                "Use `follow_redirects` instead."
            )
            warnings.warn(message, DeprecationWarning)
            redirect = allow_redirects
        if follow_redirects is not None:
            redirect = follow_redirects
        elif allow_redirects is not None and follow_redirects is not None:
            raise RuntimeError(  # pragma: no cover
                "Cannot use both `allow_redirects` and `follow_redirects`."
            )
        return redirect

    def request(  # type: ignore[override]
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: typing.Optional[httpx._types.RequestContent] = None,
        data: typing.Optional[_RequestData] = None,
        files: typing.Optional[httpx._types.RequestFiles] = None,
        json: typing.Any = None,
        params: typing.Optional[httpx._types.QueryParamTypes] = None,
        headers: typing.Optional[httpx._types.HeaderTypes] = None,
        cookies: typing.Optional[httpx._types.CookieTypes] = None,
        auth: typing.Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        follow_redirects: typing.Optional[bool] = None,
        allow_redirects: typing.Optional[bool] = None,
        timeout: typing.Union[
            httpx._client.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        extensions: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> httpx.Response:
        url = self.base_url.join(url)
        redirect = self._choose_redirect_arg(follow_redirects, allow_redirects)
        return super().request(
            method,
            url,
            content=content,
            data=data,  # type: ignore[arg-type]
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=redirect,
            timeout=timeout,
            extensions=extensions,
        )

    def get(  # type: ignore[override]
        self,
        url: httpx._types.URLTypes,
        *,
        params: typing.Optional[httpx._types.QueryParamTypes] = None,
        headers: typing.Optional[httpx._types.HeaderTypes] = None,
        cookies: typing.Optional[httpx._types.CookieTypes] = None,
        auth: typing.Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        follow_redirects: typing.Optional[bool] = None,
        allow_redirects: typing.Optional[bool] = None,
        timeout: typing.Union[
            httpx._client.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        extensions: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> httpx.Response:
        redirect = self._choose_redirect_arg(follow_redirects, allow_redirects)
        return super().get(
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=redirect,
            timeout=timeout,
            extensions=extensions,
        )

    def options(  # type: ignore[override]
        self,
        url: httpx._types.URLTypes,
        *,
        params: typing.Optional[httpx._types.QueryParamTypes] = None,
        headers: typing.Optional[httpx._types.HeaderTypes] = None,
        cookies: typing.Optional[httpx._types.CookieTypes] = None,
        auth: typing.Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        follow_redirects: typing.Optional[bool] = None,
        allow_redirects: typing.Optional[bool] = None,
        timeout: typing.Union[
            httpx._client.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        extensions: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> httpx.Response:
        redirect = self._choose_redirect_arg(follow_redirects, allow_redirects)
        return super().options(
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=redirect,
            timeout=timeout,
            extensions=extensions,
        )

    def head(  # type: ignore[override]
        self,
        url: httpx._types.URLTypes,
        *,
        params: typing.Optional[httpx._types.QueryParamTypes] = None,
        headers: typing.Optional[httpx._types.HeaderTypes] = None,
        cookies: typing.Optional[httpx._types.CookieTypes] = None,
        auth: typing.Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        follow_redirects: typing.Optional[bool] = None,
        allow_redirects: typing.Optional[bool] = None,
        timeout: typing.Union[
            httpx._client.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        extensions: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> httpx.Response:
        redirect = self._choose_redirect_arg(follow_redirects, allow_redirects)
        return super().head(
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=redirect,
            timeout=timeout,
            extensions=extensions,
        )

    def post(  # type: ignore[override]
        self,
        url: httpx._types.URLTypes,
        *,
        content: typing.Optional[httpx._types.RequestContent] = None,
        data: typing.Optional[_RequestData] = None,
        files: typing.Optional[httpx._types.RequestFiles] = None,
        json: typing.Any = None,
        params: typing.Optional[httpx._types.QueryParamTypes] = None,
        headers: typing.Optional[httpx._types.HeaderTypes] = None,
        cookies: typing.Optional[httpx._types.CookieTypes] = None,
        auth: typing.Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        follow_redirects: typing.Optional[bool] = None,
        allow_redirects: typing.Optional[bool] = None,
        timeout: typing.Union[
            httpx._client.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        extensions: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> httpx.Response:
        redirect = self._choose_redirect_arg(follow_redirects, allow_redirects)
        return super().post(
            url,
            content=content,
            data=data,  # type: ignore[arg-type]
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=redirect,
            timeout=timeout,
            extensions=extensions,
        )

    def put(  # type: ignore[override]
        self,
        url: httpx._types.URLTypes,
        *,
        content: typing.Optional[httpx._types.RequestContent] = None,
        data: typing.Optional[_RequestData] = None,
        files: typing.Optional[httpx._types.RequestFiles] = None,
        json: typing.Any = None,
        params: typing.Optional[httpx._types.QueryParamTypes] = None,
        headers: typing.Optional[httpx._types.HeaderTypes] = None,
        cookies: typing.Optional[httpx._types.CookieTypes] = None,
        auth: typing.Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        follow_redirects: typing.Optional[bool] = None,
        allow_redirects: typing.Optional[bool] = None,
        timeout: typing.Union[
            httpx._client.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        extensions: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> httpx.Response:
        redirect = self._choose_redirect_arg(follow_redirects, allow_redirects)
        return super().put(
            url,
            content=content,
            data=data,  # type: ignore[arg-type]
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=redirect,
            timeout=timeout,
            extensions=extensions,
        )

    def patch(  # type: ignore[override]
        self,
        url: httpx._types.URLTypes,
        *,
        content: typing.Optional[httpx._types.RequestContent] = None,
        data: typing.Optional[_RequestData] = None,
        files: typing.Optional[httpx._types.RequestFiles] = None,
        json: typing.Any = None,
        params: typing.Optional[httpx._types.QueryParamTypes] = None,
        headers: typing.Optional[httpx._types.HeaderTypes] = None,
        cookies: typing.Optional[httpx._types.CookieTypes] = None,
        auth: typing.Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        follow_redirects: typing.Optional[bool] = None,
        allow_redirects: typing.Optional[bool] = None,
        timeout: typing.Union[
            httpx._client.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        extensions: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> httpx.Response:
        redirect = self._choose_redirect_arg(follow_redirects, allow_redirects)
        return super().patch(
            url,
            content=content,
            data=data,  # type: ignore[arg-type]
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=redirect,
            timeout=timeout,
            extensions=extensions,
        )

    def delete(  # type: ignore[override]
        self,
        url: httpx._types.URLTypes,
        *,
        params: typing.Optional[httpx._types.QueryParamTypes] = None,
        headers: typing.Optional[httpx._types.HeaderTypes] = None,
        cookies: typing.Optional[httpx._types.CookieTypes] = None,
        auth: typing.Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        follow_redirects: typing.Optional[bool] = None,
        allow_redirects: typing.Optional[bool] = None,
        timeout: typing.Union[
            httpx._client.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx._client.USE_CLIENT_DEFAULT,
        extensions: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> httpx.Response:
        redirect = self._choose_redirect_arg(follow_redirects, allow_redirects)
        return super().delete(
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=redirect,
            timeout=timeout,
            extensions=extensions,
        )

    def websocket_connect(
        self, url: str, subprotocols: typing.Sequence[str] = None, **kwargs: typing.Any
    ) -> typing.Any:
        url = urljoin("ws://testserver", url)
        headers = kwargs.get("headers", {})
        headers.setdefault("connection", "upgrade")
        headers.setdefault("sec-websocket-key", "testserver==")
        headers.setdefault("sec-websocket-version", "13")
        if subprotocols is not None:
            headers.setdefault("sec-websocket-protocol", ", ".join(subprotocols))
        kwargs["headers"] = headers
        try:
            super().request("GET", url, **kwargs)
        except _Upgrade as exc:
            session = exc.session
        else:
            raise RuntimeError("Expected WebSocket upgrade")  # pragma: no cover

        return session

    def __enter__(self) -> "TestClient":
        with contextlib.ExitStack() as stack:
            self.portal = portal = stack.enter_context(
                anyio.from_thread.start_blocking_portal(**self.async_backend)
            )

            @stack.callback
            def reset_portal() -> None:
                self.portal = None

            self.stream_send = StapledObjectStream(
                *anyio.create_memory_object_stream(math.inf)
            )
            self.stream_receive = StapledObjectStream(
                *anyio.create_memory_object_stream(math.inf)
            )
            self.task = portal.start_task_soon(self.lifespan)
            portal.call(self.wait_startup)

            @stack.callback
            def wait_shutdown() -> None:
                portal.call(self.wait_shutdown)

            self.exit_stack = stack.pop_all()

        return self

    def __exit__(self, *args: typing.Any) -> None:
        self.exit_stack.close()

    async def lifespan(self) -> None:
        scope = {"type": "lifespan"}
        try:
            await self.app(scope, self.stream_receive.receive, self.stream_send.send)
        finally:
            await self.stream_send.send(None)

    async def wait_startup(self) -> None:
        await self.stream_receive.send({"type": "lifespan.startup"})

        async def receive() -> typing.Any:
            message = await self.stream_send.receive()
            if message is None:
                self.task.result()
            return message

        message = await receive()
        assert message["type"] in (
            "lifespan.startup.complete",
            "lifespan.startup.failed",
        )
        if message["type"] == "lifespan.startup.failed":
            await receive()

    async def wait_shutdown(self) -> None:
        async def receive() -> typing.Any:
            message = await self.stream_send.receive()
            if message is None:
                self.task.result()
            return message

        async with self.stream_send:
            await self.stream_receive.send({"type": "lifespan.shutdown"})
            message = await receive()
            assert message["type"] in (
                "lifespan.shutdown.complete",
                "lifespan.shutdown.failed",
            )
            if message["type"] == "lifespan.shutdown.failed":
                await receive()
