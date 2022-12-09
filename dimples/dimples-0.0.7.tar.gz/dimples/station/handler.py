# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

"""
    Request Handler
    ~~~~~~~~~~~~~~~

    Handler for each connection
"""

import socket
import traceback
from socketserver import StreamRequestHandler
from typing import Tuple

from ..utils import Logging, Runner
from ..common import CommonPacker

from ..server import ServerSession, SessionCenter
from ..server import ServerMessenger
from ..server import ServerProcessor
from ..server import DefaultFilter

from .shared import GlobalVariable


def create_messenger(remote: Tuple[str, int], sock: socket.socket) -> ServerMessenger:
    shared = GlobalVariable()
    facebook = shared.facebook
    # 1. create session with SessionDB
    session = ServerSession(remote=remote, sock=sock, database=shared.sdb)
    # 2. create messenger with session and MessageDB
    messenger = ServerMessenger(session=session, facebook=facebook, database=shared.mdb)
    # 3. create packer, processor, filter for messenger
    #    they have weak references to session, facebook & messenger
    messenger.packer = CommonPacker(facebook=facebook, messenger=messenger)
    messenger.processor = ServerProcessor(facebook=facebook, messenger=messenger)
    messenger.filter = DefaultFilter(session=session, facebook=facebook)
    # 4. set weak reference messenger in session
    session.messenger = messenger
    return messenger


class RequestHandler(StreamRequestHandler, Logging):

    def __init__(self, request, client_address, server):
        self.__messenger = create_messenger(remote=client_address, sock=request)
        # call 'setup()', 'handle()', 'finish()'
        super().__init__(request=request, client_address=client_address, server=server)

    @property
    def messenger(self) -> ServerMessenger:
        return self.__messenger

    # Override
    def setup(self):
        super().setup()
        try:
            session = self.messenger.session
            center = SessionCenter()
            center.add_session(session=session)
            self.info(msg='client connected: %s' % session)
            assert isinstance(session, Runner), 'session error: %s' % session
            session.setup()
        except Exception as error:
            self.error(msg='setup request handler error: %s' % error)
            traceback.print_exc()

    # Override
    def finish(self):
        try:
            session = self.messenger.session
            self.info(msg='client disconnected: %s' % session)
            center = SessionCenter()
            center.remove_session(session=session)
            assert isinstance(session, Runner), 'session error: %s' % session
            session.finish()
            self.__messenger = None
        except Exception as error:
            self.error(msg='finish request handler error: %s' % error)
            traceback.print_exc()
        super().finish()

    """
        DIM Request Handler
    """

    # Override
    def handle(self):
        super().handle()
        try:
            self.info(msg='session started: %s' % str(self.client_address))
            session = self.messenger.session
            assert isinstance(session, Runner), 'session error: %s' % session
            session.handle()
            self.info(msg='session finished: %s' % str(self.client_address))
        except Exception as error:
            self.error(msg='request handler error: %s' % error)
            traceback.print_exc()
