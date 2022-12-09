"""
    Ory APIs

    Documentation for all public and administrative Ory APIs. Administrative APIs can only be accessed with a valid Personal Access Token. Public APIs are mostly used in browsers.   # noqa: E501

    The version of the OpenAPI document: v1.1.0
    Contact: support@ory.sh
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import ory_client
from ory_client.model.o_auth2_client import OAuth2Client
from ory_client.model.o_auth2_consent_request_open_id_connect_context import OAuth2ConsentRequestOpenIDConnectContext
from ory_client.model.string_slice_json_format import StringSliceJSONFormat
globals()['OAuth2Client'] = OAuth2Client
globals()['OAuth2ConsentRequestOpenIDConnectContext'] = OAuth2ConsentRequestOpenIDConnectContext
globals()['StringSliceJSONFormat'] = StringSliceJSONFormat
from ory_client.model.o_auth2_login_request import OAuth2LoginRequest


class TestOAuth2LoginRequest(unittest.TestCase):
    """OAuth2LoginRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testOAuth2LoginRequest(self):
        """Test OAuth2LoginRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = OAuth2LoginRequest()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
