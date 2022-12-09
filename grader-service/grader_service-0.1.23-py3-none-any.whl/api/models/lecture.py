# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from grader_service.api.models.base_model_ import Model
from grader_service.api import util


class Lecture(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None, code=None, complete=False):  # noqa: E501
        """Lecture - a model defined in OpenAPI

        :param id: The id of this Lecture.  # noqa: E501
        :type id: int
        :param name: The name of this Lecture.  # noqa: E501
        :type name: str
        :param code: The code of this Lecture.  # noqa: E501
        :type code: str
        :param complete: The complete of this Lecture.  # noqa: E501
        :type complete: bool
        """
        self.openapi_types = {
            'id': int,
            'name': str,
            'code': str,
            'complete': bool
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'code': 'code',
            'complete': 'complete'
        }

        self._id = id
        self._name = name
        self._code = code
        self._complete = complete

    @classmethod
    def from_dict(cls, dikt) -> 'Lecture':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Lecture of this Lecture.  # noqa: E501
        :rtype: Lecture
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Lecture.


        :return: The id of this Lecture.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Lecture.


        :param id: The id of this Lecture.
        :type id: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Lecture.


        :return: The name of this Lecture.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Lecture.


        :param name: The name of this Lecture.
        :type name: str
        """

        self._name = name

    @property
    def code(self):
        """Gets the code of this Lecture.


        :return: The code of this Lecture.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this Lecture.


        :param code: The code of this Lecture.
        :type code: str
        """

        self._code = code

    @property
    def complete(self):
        """Gets the complete of this Lecture.


        :return: The complete of this Lecture.
        :rtype: bool
        """
        return self._complete

    @complete.setter
    def complete(self, complete):
        """Sets the complete of this Lecture.


        :param complete: The complete of this Lecture.
        :type complete: bool
        """

        self._complete = complete
