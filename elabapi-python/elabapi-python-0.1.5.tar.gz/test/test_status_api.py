# coding: utf-8

"""
    eLabFTW REST API v2 Documentation

    Some description of the api.  # noqa: E501

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import elabapi_python
from elabapi_python.api.status_api import StatusApi  # noqa: E501
from elabapi_python.rest import ApiException


class TestStatusApi(unittest.TestCase):
    """StatusApi unit test stubs"""

    def setUp(self):
        self.api = StatusApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_status(self):
        """Test case for delete_status

        Delete a status.  # noqa: E501
        """
        pass

    def test_patch_status(self):
        """Test case for patch_status

        Modify a status.  # noqa: E501
        """
        pass

    def test_post_team_one_status(self):
        """Test case for post_team_one_status

        Create a new status.  # noqa: E501
        """
        pass

    def test_read_team_one_status(self):
        """Test case for read_team_one_status

        Read a status.  # noqa: E501
        """
        pass

    def test_read_team_status(self):
        """Test case for read_team_status

        Read status of a team.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
