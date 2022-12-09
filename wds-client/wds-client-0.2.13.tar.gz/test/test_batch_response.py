# coding: utf-8

"""
    Workspace Data Service

    This page lists both current and proposed APIs. The proposed APIs which have not yet been implemented are marked as deprecated. This is incongruous, but by using the deprecated flag, we can force swagger-ui to display those endpoints differently.  Error codes and responses for proposed APIs are likely to change as we gain more clarity on their implementation.  As of v0.2, all APIs are subject to change without notice.   # noqa: E501

    The version of the OpenAPI document: v0.2
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import wds_client
from wds_client.models.batch_response import BatchResponse  # noqa: E501
from wds_client.rest import ApiException

class TestBatchResponse(unittest.TestCase):
    """BatchResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test BatchResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = wds_client.models.batch_response.BatchResponse()  # noqa: E501
        if include_optional :
            return BatchResponse(
                message = '0', 
                records_modified = 56
            )
        else :
            return BatchResponse(
                message = '0',
                records_modified = 56,
        )

    def testBatchResponse(self):
        """Test BatchResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
