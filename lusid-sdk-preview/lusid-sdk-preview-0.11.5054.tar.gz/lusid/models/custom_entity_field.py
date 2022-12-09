# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.5054
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


class CustomEntityField(object):
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
        'name': 'str',
        'value': 'object',
        'effective_from': 'datetime',
        'effective_until': 'datetime'
    }

    attribute_map = {
        'name': 'name',
        'value': 'value',
        'effective_from': 'effectiveFrom',
        'effective_until': 'effectiveUntil'
    }

    required_map = {
        'name': 'required',
        'value': 'required',
        'effective_from': 'optional',
        'effective_until': 'optional'
    }

    def __init__(self, name=None, value=None, effective_from=None, effective_until=None, local_vars_configuration=None):  # noqa: E501
        """CustomEntityField - a model defined in OpenAPI"
        
        :param name:  The name of the field in the custom entity type definition. (required)
        :type name: str
        :param value:  The value for the field. (required)
        :type value: object
        :param effective_from:  The effective datetime from which the field's value is valid. For timeVariant fields, this defaults to the beginning of time.
        :type effective_from: datetime
        :param effective_until:  The effective datetime until which the field's value is valid. If not supplied, the value will be valid indefinitely or until the next “effectiveFrom” date of the field.
        :type effective_until: datetime

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._value = None
        self._effective_from = None
        self._effective_until = None
        self.discriminator = None

        self.name = name
        self.value = value
        self.effective_from = effective_from
        self.effective_until = effective_until

    @property
    def name(self):
        """Gets the name of this CustomEntityField.  # noqa: E501

        The name of the field in the custom entity type definition.  # noqa: E501

        :return: The name of this CustomEntityField.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CustomEntityField.

        The name of the field in the custom entity type definition.  # noqa: E501

        :param name: The name of this CustomEntityField.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def value(self):
        """Gets the value of this CustomEntityField.  # noqa: E501

        The value for the field.  # noqa: E501

        :return: The value of this CustomEntityField.  # noqa: E501
        :rtype: object
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this CustomEntityField.

        The value for the field.  # noqa: E501

        :param value: The value of this CustomEntityField.  # noqa: E501
        :type value: object
        """
        if self.local_vars_configuration.client_side_validation and value is None:  # noqa: E501
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value

    @property
    def effective_from(self):
        """Gets the effective_from of this CustomEntityField.  # noqa: E501

        The effective datetime from which the field's value is valid. For timeVariant fields, this defaults to the beginning of time.  # noqa: E501

        :return: The effective_from of this CustomEntityField.  # noqa: E501
        :rtype: datetime
        """
        return self._effective_from

    @effective_from.setter
    def effective_from(self, effective_from):
        """Sets the effective_from of this CustomEntityField.

        The effective datetime from which the field's value is valid. For timeVariant fields, this defaults to the beginning of time.  # noqa: E501

        :param effective_from: The effective_from of this CustomEntityField.  # noqa: E501
        :type effective_from: datetime
        """

        self._effective_from = effective_from

    @property
    def effective_until(self):
        """Gets the effective_until of this CustomEntityField.  # noqa: E501

        The effective datetime until which the field's value is valid. If not supplied, the value will be valid indefinitely or until the next “effectiveFrom” date of the field.  # noqa: E501

        :return: The effective_until of this CustomEntityField.  # noqa: E501
        :rtype: datetime
        """
        return self._effective_until

    @effective_until.setter
    def effective_until(self, effective_until):
        """Sets the effective_until of this CustomEntityField.

        The effective datetime until which the field's value is valid. If not supplied, the value will be valid indefinitely or until the next “effectiveFrom” date of the field.  # noqa: E501

        :param effective_until: The effective_until of this CustomEntityField.  # noqa: E501
        :type effective_until: datetime
        """

        self._effective_until = effective_until

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
        if not isinstance(other, CustomEntityField):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CustomEntityField):
            return True

        return self.to_dict() != other.to_dict()
