# coding: utf-8

"""
    eLabFTW REST API v2 Documentation

    Some description of the api.  # noqa: E501

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class UnfinishedStep(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'int',
        'title': 'str',
        'steps': 'list[str]'
    }

    attribute_map = {
        'id': 'id',
        'title': 'title',
        'steps': 'steps'
    }

    def __init__(self, id=None, title=None, steps=None):  # noqa: E501
        """UnfinishedStep - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._title = None
        self._steps = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if title is not None:
            self.title = title
        if steps is not None:
            self.steps = steps

    @property
    def id(self):
        """Gets the id of this UnfinishedStep.  # noqa: E501


        :return: The id of this UnfinishedStep.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UnfinishedStep.


        :param id: The id of this UnfinishedStep.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def title(self):
        """Gets the title of this UnfinishedStep.  # noqa: E501


        :return: The title of this UnfinishedStep.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this UnfinishedStep.


        :param title: The title of this UnfinishedStep.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def steps(self):
        """Gets the steps of this UnfinishedStep.  # noqa: E501


        :return: The steps of this UnfinishedStep.  # noqa: E501
        :rtype: list[str]
        """
        return self._steps

    @steps.setter
    def steps(self, steps):
        """Sets the steps of this UnfinishedStep.


        :param steps: The steps of this UnfinishedStep.  # noqa: E501
        :type: list[str]
        """

        self._steps = steps

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(UnfinishedStep, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UnfinishedStep):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
