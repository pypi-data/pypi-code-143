# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.5050
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class UpsertPersonRequest(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'identifiers': 'dict(str, ModelProperty)',
        'properties': 'dict(str, list[ModelProperty])',
        'display_name': 'str',
        'description': 'str'
    }

    attribute_map = {
        'identifiers': 'identifiers',
        'properties': 'properties',
        'display_name': 'displayName',
        'description': 'description'
    }

    required_map = {
        'identifiers': 'required',
        'properties': 'optional',
        'display_name': 'required',
        'description': 'optional'
    }

    def __init__(self, identifiers=None, properties=None, display_name=None, description=None, local_vars_configuration=None):  # noqa: E501
        """UpsertPersonRequest - a model defined in OpenAPI"
        
        :param identifiers:  The identifiers the person will be upserted with.The provided keys should be idTypeScope, idTypeCode, code (required)
        :type identifiers: dict[str, lusid.ModelProperty]
        :param properties:  A set of properties associated to the Person. There can be multiple properties associated with a property key.
        :type properties: dict(str, list[ModelProperty])
        :param display_name:  The display name of the Person (required)
        :type display_name: str
        :param description:  The description of the Person
        :type description: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._identifiers = None
        self._properties = None
        self._display_name = None
        self._description = None
        self.discriminator = None

        self.identifiers = identifiers
        self.properties = properties
        self.display_name = display_name
        self.description = description

    @property
    def identifiers(self):
        """Gets the identifiers of this UpsertPersonRequest.  # noqa: E501

        The identifiers the person will be upserted with.The provided keys should be idTypeScope, idTypeCode, code  # noqa: E501

        :return: The identifiers of this UpsertPersonRequest.  # noqa: E501
        :rtype: dict[str, lusid.ModelProperty]
        """
        return self._identifiers

    @identifiers.setter
    def identifiers(self, identifiers):
        """Sets the identifiers of this UpsertPersonRequest.

        The identifiers the person will be upserted with.The provided keys should be idTypeScope, idTypeCode, code  # noqa: E501

        :param identifiers: The identifiers of this UpsertPersonRequest.  # noqa: E501
        :type identifiers: dict[str, lusid.ModelProperty]
        """
        if self.local_vars_configuration.client_side_validation and identifiers is None:  # noqa: E501
            raise ValueError("Invalid value for `identifiers`, must not be `None`")  # noqa: E501

        self._identifiers = identifiers

    @property
    def properties(self):
        """Gets the properties of this UpsertPersonRequest.  # noqa: E501

        A set of properties associated to the Person. There can be multiple properties associated with a property key.  # noqa: E501

        :return: The properties of this UpsertPersonRequest.  # noqa: E501
        :rtype: dict(str, list[ModelProperty])
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this UpsertPersonRequest.

        A set of properties associated to the Person. There can be multiple properties associated with a property key.  # noqa: E501

        :param properties: The properties of this UpsertPersonRequest.  # noqa: E501
        :type properties: dict(str, list[ModelProperty])
        """

        self._properties = properties

    @property
    def display_name(self):
        """Gets the display_name of this UpsertPersonRequest.  # noqa: E501

        The display name of the Person  # noqa: E501

        :return: The display_name of this UpsertPersonRequest.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this UpsertPersonRequest.

        The display name of the Person  # noqa: E501

        :param display_name: The display_name of this UpsertPersonRequest.  # noqa: E501
        :type display_name: str
        """
        if self.local_vars_configuration.client_side_validation and display_name is None:  # noqa: E501
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                display_name is not None and len(display_name) > 512):
            raise ValueError("Invalid value for `display_name`, length must be less than or equal to `512`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                display_name is not None and len(display_name) < 1):
            raise ValueError("Invalid value for `display_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._display_name = display_name

    @property
    def description(self):
        """Gets the description of this UpsertPersonRequest.  # noqa: E501

        The description of the Person  # noqa: E501

        :return: The description of this UpsertPersonRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpsertPersonRequest.

        The description of the Person  # noqa: E501

        :param description: The description of this UpsertPersonRequest.  # noqa: E501
        :type description: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 512):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `512`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 0):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")  # noqa: E501

        self._description = description

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpsertPersonRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpsertPersonRequest):
            return True

        return self.to_dict() != other.to_dict()
