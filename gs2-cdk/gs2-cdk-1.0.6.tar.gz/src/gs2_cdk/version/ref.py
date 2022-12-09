# Copyright 2016 Game Server Services, Inc. or its affiliates. All Rights
# Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from __future__ import annotations
from .model import *
from .stamp_sheet import *

from typing import List


class NamespaceRef:
    namespace_name: str

    def __init__(
            self,
            namespace_name: str,
    ):
        self.namespace_name = namespace_name

    def current_version_master(
            self,
    ) -> CurrentVersionMasterRef:
        return CurrentVersionMasterRef(
            namespace_name=self.namespace_name,
        )

    def version_model(
            self,
            version_name: str,
    ) -> VersionModelRef:
        return VersionModelRef(
            namespace_name=self.namespace_name,
            version_name=version_name,
        )

    def version_model_master(
            self,
            version_name: str,
    ) -> VersionModelMasterRef:
        return VersionModelMasterRef(
            namespace_name=self.namespace_name,
            version_name=version_name,
        )

    def grn(self) -> str:
        return Join(
            ':',
            [
                'grn',
                'gs2',
                GetAttr.region().str(),
                GetAttr.owner_id().str(),
                'version',
                self.namespace_name,
            ],
        ).str()


class VersionModelMasterRef:
    namespace_name: str
    version_name: str

    def __init__(
            self,
            namespace_name: str,
            version_name: str,
    ):
        self.namespace_name = namespace_name
        self.version_name = version_name

    def grn(self) -> str:
        return Join(
            ':',
            [
                'grn',
                'gs2',
                GetAttr.region().str(),
                GetAttr.owner_id().str(),
                'version',
                self.namespace_name,
                'model',
                'version',
                self.version_name,
            ],
        ).str()


class VersionModelRef:
    namespace_name: str
    version_name: str

    def __init__(
            self,
            namespace_name: str,
            version_name: str,
    ):
        self.namespace_name = namespace_name
        self.version_name = version_name

    def grn(self) -> str:
        return Join(
            ':',
            [
                'grn',
                'gs2',
                GetAttr.region().str(),
                GetAttr.owner_id().str(),
                'version',
                self.namespace_name,
                'model',
                'version',
                self.version_name,
            ],
        ).str()


class CurrentVersionMasterRef:
    namespace_name: str

    def __init__(
            self,
            namespace_name: str,
    ):
        self.namespace_name = namespace_name

    def grn(self) -> str:
        return Join(
            ':',
            [
                'grn',
                'gs2',
                GetAttr.region().str(),
                GetAttr.owner_id().str(),
                'version',
                self.namespace_name,
            ],
        ).str()
