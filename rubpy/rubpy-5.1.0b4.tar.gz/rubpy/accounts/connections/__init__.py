from websockets import connect, ConnectionClosed
from json import dumps, loads
from random import choice, randint
from ...crypto import Crypto

__all__ = (
    'Connections',
    'WebSocket',
)

class Connections:
    def __init__(self):
        pass

    async def get(self, session, url, headers=None):
        while True:
            async with session.get(url, headers=headers) as response:
                if response.ok:
                    return await response.json()
                else:
                    continue

    async def post(self, session, url=f'https://messengerg2c{randint(1, 11)}.iranlms.ir/', json=None, data=None, headers=None):
        while True:
            if json:
                async with session.post(url, json=json) as response:
                    if response.ok:
                        return await response.json()
                    else:
                        continue
            else:
                async with session.post(url, data=data, headers=headers) as response:
                    if response.ok:
                        return await response.json()
                    else:
                        continue

    async def getdcmess(self, session, ws=False):
        response = await self.get(session=session, url='https://getdcmess.iranlms.ir/')
        if ws:
            return list(response.get('data').get('socket').values())
        else:
            return list(response.get('data').get('API').values())

class WebSocket:
    __slots__ = (
        'auth',
        'crypto',
        'connections',
        'session',
    )

    def __init__(self, auth, session):
        self.auth = auth
        self.crypto = Crypto(auth)
        self.connections = Connections()
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excpets):
        exit(excpets)

    async def handSnake(self):
        data = {
            'api_version': '5',
            'auth': self.auth,
            'method': 'handShake',
        }
        wss = await self.connections.getdcmess(self.session, ws=True)

        async for websocket in connect(choice(wss)):
            try:
                await websocket.send(dumps(data))
                while True:
                    await websocket.send(('{}'))
                    data = await websocket.recv()
                    if data != '{"status":"OK","status_det":"OK"}':
                        yield loads(data)
                    else: continue
            except ConnectionClosed: continue

    async def updatesHandler(self, chat_updates=False, message_updates=True, show_notifications=False):
        async for message in self.handSnake():
            if message.get('type') == 'messenger':
                data = loads(self.crypto.decrypt(message.get('data_enc')))
                if message_updates and chat_updates and show_notifications:
                    yield message
                elif message_updates:
                    if 'message_updates' in data:
                        for i in data.get('message_updates'):
                            yield i
                elif chat_updates:
                    if 'chat_updates' in data:
                        for i in data.get('chat_updates'):
                            yield i
                elif show_notifications:
                    if 'show_notifications' in data:
                        for i in data.get('show_notifications'):
                            yield i