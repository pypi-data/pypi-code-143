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
from elabapi_python.api.todolist_api import TodolistApi  # noqa: E501
from elabapi_python.rest import ApiException


class TestTodolistApi(unittest.TestCase):
    """TodolistApi unit test stubs"""

    def setUp(self):
        self.api = TodolistApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_todoitem(self):
        """Test case for delete_todoitem

        Delete a todoitem.  # noqa: E501
        """
        pass

    def test_patch_todoitem(self):
        """Test case for patch_todoitem

        Actions on a todoitem.   # noqa: E501
        """
        pass

    def test_post_todolist(self):
        """Test case for post_todolist

        Create a todo item  # noqa: E501
        """
        pass

    def test_read_todoitem(self):
        """Test case for read_todoitem

        Read a todo entry.  # noqa: E501
        """
        pass

    def test_read_todolist(self):
        """Test case for read_todolist

        Read all todoitems.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
