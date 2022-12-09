# coding: utf-8

"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ConversationCannedMessage(object):
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
        'canned_message': 'str',
        'conversation_canned_message_oid': 'int',
        'conversation_department_oids': 'list[str]',
        'short_code': 'str'
    }

    attribute_map = {
        'canned_message': 'canned_message',
        'conversation_canned_message_oid': 'conversation_canned_message_oid',
        'conversation_department_oids': 'conversation_department_oids',
        'short_code': 'short_code'
    }

    def __init__(self, canned_message=None, conversation_canned_message_oid=None, conversation_department_oids=None, short_code=None):  # noqa: E501
        """ConversationCannedMessage - a model defined in Swagger"""  # noqa: E501

        self._canned_message = None
        self._conversation_canned_message_oid = None
        self._conversation_department_oids = None
        self._short_code = None
        self.discriminator = None

        if canned_message is not None:
            self.canned_message = canned_message
        if conversation_canned_message_oid is not None:
            self.conversation_canned_message_oid = conversation_canned_message_oid
        if conversation_department_oids is not None:
            self.conversation_department_oids = conversation_department_oids
        if short_code is not None:
            self.short_code = short_code

    @property
    def canned_message(self):
        """Gets the canned_message of this ConversationCannedMessage.  # noqa: E501


        :return: The canned_message of this ConversationCannedMessage.  # noqa: E501
        :rtype: str
        """
        return self._canned_message

    @canned_message.setter
    def canned_message(self, canned_message):
        """Sets the canned_message of this ConversationCannedMessage.


        :param canned_message: The canned_message of this ConversationCannedMessage.  # noqa: E501
        :type: str
        """

        self._canned_message = canned_message

    @property
    def conversation_canned_message_oid(self):
        """Gets the conversation_canned_message_oid of this ConversationCannedMessage.  # noqa: E501


        :return: The conversation_canned_message_oid of this ConversationCannedMessage.  # noqa: E501
        :rtype: int
        """
        return self._conversation_canned_message_oid

    @conversation_canned_message_oid.setter
    def conversation_canned_message_oid(self, conversation_canned_message_oid):
        """Sets the conversation_canned_message_oid of this ConversationCannedMessage.


        :param conversation_canned_message_oid: The conversation_canned_message_oid of this ConversationCannedMessage.  # noqa: E501
        :type: int
        """

        self._conversation_canned_message_oid = conversation_canned_message_oid

    @property
    def conversation_department_oids(self):
        """Gets the conversation_department_oids of this ConversationCannedMessage.  # noqa: E501


        :return: The conversation_department_oids of this ConversationCannedMessage.  # noqa: E501
        :rtype: list[str]
        """
        return self._conversation_department_oids

    @conversation_department_oids.setter
    def conversation_department_oids(self, conversation_department_oids):
        """Sets the conversation_department_oids of this ConversationCannedMessage.


        :param conversation_department_oids: The conversation_department_oids of this ConversationCannedMessage.  # noqa: E501
        :type: list[str]
        """

        self._conversation_department_oids = conversation_department_oids

    @property
    def short_code(self):
        """Gets the short_code of this ConversationCannedMessage.  # noqa: E501


        :return: The short_code of this ConversationCannedMessage.  # noqa: E501
        :rtype: str
        """
        return self._short_code

    @short_code.setter
    def short_code(self, short_code):
        """Sets the short_code of this ConversationCannedMessage.


        :param short_code: The short_code of this ConversationCannedMessage.  # noqa: E501
        :type: str
        """

        self._short_code = short_code

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
        if issubclass(ConversationCannedMessage, dict):
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
        if not isinstance(other, ConversationCannedMessage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
