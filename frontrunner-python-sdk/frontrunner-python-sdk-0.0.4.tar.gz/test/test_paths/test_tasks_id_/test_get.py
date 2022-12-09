# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

import unittest
from unittest.mock import patch

import urllib3

import frontrunner_python_sdk
from frontrunner_python_sdk.paths.tasks_id_ import get  # noqa: E501
from frontrunner_python_sdk import configuration, schemas, api_client

from .. import ApiTestMixin


class TestTasksId(ApiTestMixin, unittest.TestCase):
    """
    TasksId unit test stubs
    """
    _configuration = configuration.Configuration()

    def setUp(self):
        used_api_client = api_client.ApiClient(configuration=self._configuration)
        self.api = get.ApiForget(api_client=used_api_client)  # noqa: E501

    def tearDown(self):
        pass

    response_status = 201




if __name__ == '__main__':
    unittest.main()
