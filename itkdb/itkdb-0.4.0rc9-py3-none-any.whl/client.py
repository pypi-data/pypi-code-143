from __future__ import annotations

import logging
from functools import partial
from io import BytesIO

import itkdb

from . import exceptions, models, utilities
from .core import Session
from .responses import PagedResponse

log = logging.getLogger(__name__)


class Client(Session):
    limit = -1

    def __init__(self, use_eos=False, **kwargs):
        self._use_eos = use_eos
        super().__init__(**kwargs)

    def request(self, method, url, *args, **kwargs):
        self.limit = kwargs.pop("limit", -1)

        response = super(Session, self).request(method, url, *args, **kwargs)
        return self._response_handler(response)

    def _handle_warnings(self, data):
        warnings = data.pop("uuAppErrorMap", {})
        try:
            for key, message in warnings.items():
                log.warning(f"{key}: {message}")
        except AttributeError:
            # it's a string like:
            #   'uuAppErrorMap': '#<UuApp::Oidc::Session:0x00561d53890118>'
            log.warning(f"{warnings}")

    def upload_to_eos(self, response, *args, eos_file_details=None, **kwargs):
        log.info("I was able to get a token to upload to EOS. Let me upload.")
        try:
            response.raise_for_status()
        except BaseException:
            log.warning("Something went wrong with uploading to EOS.")
            return response

        # see _request_handler for this information
        fn, fp, ft, fh = eos_file_details

        token_request = response.json()

        chain = str(itkdb.data / "CERN_chain.pem")
        url = utilities.merge_url_query_params(
            token_request["url"], {"authz": token_request["token"]}
        )

        headers = {"Content-Type": ft}
        headers.update(fh)

        response = super().put(url, data=fp, verify=chain, headers=headers)

    def _request_handler(self, request):
        if request.url == self._normalize_url("/itkdbPoisonPillTest"):
            request.url = self._normalize_url("/poison")
        elif request.url == self._normalize_url("/createComponentAttachment"):
            if not self.use_eos:
                return

            fn, fp, ft, fh = utilities.get_file_components(request.files)

            if not utilities.is_image(fn, fp) and not utilities.is_largefile(fn, fp):
                return

            log.info(
                "It looks like you're attaching an image or large file, I will try to put it on EOS for you."
            )

            # update headers
            fh = fh or {}
            request.headers.update(fh)

            ft = ft = utilities.get_mimetype(fn, fp)

            details = {
                "type": "component",
                "id": request.data["component"],
                "title": request.data["title"],
                "description": request.data["description"],
                "filesize": utilities.get_filesize(fn, fp),
            }

            leftover = {
                k: v
                for k, v in request.data.items()
                if k not in ["component", "title", "description"]
            }

            if leftover:
                log.warning(f"Ignoring user-specified data={leftover}")

            request.json = details
            request.data = None
            request.files = None
            request.hooks["response"] = [
                partial(self.upload_to_eos, eos_file_details=(fn, fp, ft, fh))
            ]
            request.url = self._normalize_url("requestUploadEosFile")
        elif request.url == self._normalize_url("/createTestRunAttachment"):
            if not self.use_eos:
                return

            fn, fp, ft, fh = utilities.get_file_components(request.files)

            if not utilities.is_image(fn, fp) and not utilities.is_largefile(fn, fp):
                return

            log.info(
                "It looks like you're attaching an image or large file, I will try to put it on EOS for you."
            )

            # update headers
            fh = fh or {}
            request.headers.update(fh)

            ft = ft = utilities.get_mimetype(fn, fp)

            details = {
                "type": "testRun",
                "id": request.data["testRun"],
                "title": request.data["title"],
                "description": request.data["description"],
                "filesize": utilities.get_filesize(fn, fp),
            }

            leftover = {
                k: v
                for k, v in request.data.items()
                if k not in ["component", "title", "description"]
            }

            if leftover:
                log.warning(f"Ignoring user-specified data={leftover}")

            request.json = details
            request.data = None
            request.files = None
            request.hooks["response"] = [
                partial(self.upload_to_eos, eos_file_details=(fn, fp, ft, fh))
            ]
            request.url = self._normalize_url("requestUploadEosFile")
        elif request.url == self._normalize_url("/createShipmentAttachment"):
            if not self.use_eos:
                return

            fn, fp, ft, fh = utilities.get_file_components(request.files)

            if not utilities.is_image(fn, fp) and not utilities.is_largefile(fn, fp):
                return

            log.info(
                "It looks like you're attaching an image or large file, I will try to put it on EOS for you."
            )

            # update headers
            request.headers.update(fh)

            details = {
                "type": "shipment",
                "id": request.data["shipment"],
                "title": request.data["title"],
                "description": request.data["description"],
                "filesize": utilities.get_filesize(fn, fp),
            }

            leftover = {
                k: v
                for k, v in request.data.items()
                if k not in ["component", "title", "description"]
            }

            if leftover:
                log.warning(f"Ignoring user-specified data={leftover}")

            request.json = details
            request.data = None
            request.files = None
            request.hooks["response"] = [
                partial(self.upload_to_eos, eos_file_details=(fn, fp, ft, fh))
            ]
            request.url = self._normalize_url("requestUploadEosFile")

    def _response_handler(self, response):
        # sometimes we don't get content-type, so make sure it's a string at least
        content_type = response.headers.get("content-type")
        if content_type is None:
            return response

        if content_type == "application/octet-stream":
            fp = BytesIO(response.content)
            content_type = utilities.get_mimetype(None, fp) or content_type
            response.headers["content-type"] = content_type

        if content_type.startswith("application/json"):
            if response.headers.get("content-length") == "0":
                return {}

            try:
                data = response.json()
                self._handle_warnings(data)
            except ValueError as err:
                raise exceptions.BadJSON(response) from err

            limit = self.limit
            self.limit = -1  # reset the limit again
            if "pageItemList" in data:
                return PagedResponse(super(), response, limit=limit, key="pageItemList")
            elif "itemList" in data:
                pageInfo = data.get("pageInfo", None)
                if pageInfo and (
                    pageInfo["pageIndex"] * pageInfo["pageSize"] < pageInfo["total"]
                ):
                    return PagedResponse(super(), response, limit=limit, key="itemList")
                return data["itemList"]
            elif "testRunList" in data:
                return data["testRunList"]
            elif "dtoSample" in data:
                return data["dtoSample"]
            else:
                return data
        elif content_type.startswith("image/"):
            return models.Image.from_response(response)
        elif content_type.startswith("text/"):
            return models.Text.from_response(response)
        elif content_type.startswith("text"):
            return models.Text.from_response(response)
        elif content_type == "application/zip":
            return models.ZipFile.from_response(response)
        else:
            log.warning(f"Do not know how to handle Content-Type: {content_type:s}.")
            return response

    def prepare_request(self, request):
        request.url = self._normalize_url(request.url)
        self._request_handler(request)
        return super().prepare_request(request)

    @property
    def use_eos(self):
        return self._use_eos
