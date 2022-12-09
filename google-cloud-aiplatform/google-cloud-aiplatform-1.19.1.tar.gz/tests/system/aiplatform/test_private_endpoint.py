# -*- coding: utf-8 -*-

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import pytest

from google.cloud import aiplatform

from tests.system.aiplatform import e2e_base

# permanent_custom_mnist_model
_MODEL_ID = "6430031960164270080"
_PRIVATE_ENDPOINT_NETWORK = "projects/580378083368/global/networks/private-endpoint-vpc"


@pytest.mark.usefixtures("tear_down_resources")
class TestPrivateEndpoint(e2e_base.TestEndToEnd):

    _temp_prefix = "temp_vertex_sdk_e2e"

    def test_create_deploy_delete_private_endpoint(self, shared_state):
        # Collection of resources generated by this test, to be deleted during teardown
        shared_state["resources"] = []

        aiplatform.init(
            project=e2e_base._PROJECT,
            location=e2e_base._LOCATION,
        )

        private_endpoint = aiplatform.PrivateEndpoint.create(
            display_name=self._make_display_name("private_endpoint_test"),
            network=_PRIVATE_ENDPOINT_NETWORK,
        )
        shared_state["resources"].append(private_endpoint)

        # Verify that the retrieved private Endpoint is the same
        my_private_endpoint = aiplatform.PrivateEndpoint(
            endpoint_name=private_endpoint.resource_name
        )
        assert private_endpoint.resource_name == my_private_endpoint.resource_name
        assert private_endpoint.display_name == my_private_endpoint.display_name

        # Verify the endpoint is in the private Endpoint list
        list_private_endpoint = aiplatform.PrivateEndpoint.list()
        assert private_endpoint.resource_name in [
            private_endpoint.resource_name for private_endpoint in list_private_endpoint
        ]

        # Retrieve permanent model, deploy to private Endpoint, then undeploy
        my_model = aiplatform.Model(model_name=_MODEL_ID)

        my_private_endpoint.deploy(model=my_model)
        assert my_private_endpoint._gca_resource.deployed_models

        deployed_model_id = my_private_endpoint.list_models()[0].id
        my_private_endpoint.undeploy(deployed_model_id=deployed_model_id)
        assert not my_private_endpoint._gca_resource.deployed_models
