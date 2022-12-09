# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
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
    Database module
    ~~~~~~~~~~~~~~~

"""

from ..common.dbi import *

from .dos import *

from .t_private import PrivateKeyTable
from .t_meta import MetaTable
from .t_document import DocumentTable
from .t_user import UserTable
from .t_group import GroupTable

from .t_message import ReliableMessageTable
from .t_cipherkey import CipherKeyTable

from .t_login import LoginTable
from .t_provider import ProviderTable

from .account import AccountDatabase
from .message import MessageDatabase
from .session import SessionDatabase


__all__ = [
    #
    #   DBI
    #
    'PrivateKeyDBI', 'MetaDBI', 'DocumentDBI',
    'UserDBI', 'GroupDBI',
    'AccountDBI',

    'ReliableMessageDBI', 'CipherKeyDBI',
    'MessageDBI',

    'LoginDBI', 'ProviderDBI',
    'SessionDBI',

    #
    #   DOS
    #
    'Storage',
    'PrivateKeyStorage', 'MetaStorage', 'DocumentStorage',
    'UserStorage', 'GroupStorage',
    'LoginStorage',

    #
    #   Table
    #
    'PrivateKeyTable', 'MetaTable', 'DocumentTable',
    'UserTable', 'GroupTable',
    'ReliableMessageTable', 'CipherKeyTable',
    'LoginTable', 'ProviderTable',

    #
    #   Database
    #
    'AccountDatabase',
    'MessageDatabase',
    'SessionDatabase',
]
