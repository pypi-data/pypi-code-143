# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.5052
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


class CustomEntityFieldDefinition(object):
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
        'lifetime': 'str',
        'type': 'str',
        'required': 'bool',
        'description': 'str'
    }

    attribute_map = {
        'name': 'name',
        'lifetime': 'lifetime',
        'type': 'type',
        'required': 'required',
        'description': 'description'
    }

    required_map = {
        'name': 'required',
        'lifetime': 'required',
        'type': 'required',
        'required': 'required',
        'description': 'optional'
    }

    def __init__(self, name=None, lifetime=None, type=None, required=None, description=None, local_vars_configuration=None):  # noqa: E501
        """CustomEntityFieldDefinition - a model defined in OpenAPI"
        
        :param name:  The name of the field. (required)
        :type name: str
        :param lifetime:  Describes how the field’s values can change over time. The available values are: “Perpetual”, “TimeVariant”. (required)
        :type lifetime: str
        :param type:  The value type for the field. Available values are: “String”, “Boolean”, “DateTime”, “Decimal”. (required)
        :type type: str
        :param required:  Whether the field is required or not. (required)
        :type required: bool
        :param description:  An optional description for the field.
        :type description: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._lifetime = None
        self._type = None
        self._required = None
        self._description = None
        self.discriminator = None

        self.name = name
        self.lifetime = lifetime
        self.type = type
        self.required = required
        self.description = description

    @property
    def name(self):
        """Gets the name of this CustomEntityFieldDefinition.  # noqa: E501

        The name of the field.  # noqa: E501

        :return: The name of this CustomEntityFieldDefinition.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CustomEntityFieldDefinition.

        The name of the field.  # noqa: E501

        :param name: The name of this CustomEntityFieldDefinition.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def lifetime(self):
        """Gets the lifetime of this CustomEntityFieldDefinition.  # noqa: E501

        Describes how the field’s values can change over time. The available values are: “Perpetual”, “TimeVariant”.  # noqa: E501

        :return: The lifetime of this CustomEntityFieldDefinition.  # noqa: E501
        :rtype: str
        """
        return self._lifetime

    @lifetime.setter
    def lifetime(self, lifetime):
        """Sets the lifetime of this CustomEntityFieldDefinition.

        Describes how the field’s values can change over time. The available values are: “Perpetual”, “TimeVariant”.  # noqa: E501

        :param lifetime: The lifetime of this CustomEntityFieldDefinition.  # noqa: E501
        :type lifetime: str
        """
        if self.local_vars_configuration.client_side_validation and lifetime is None:  # noqa: E501
            raise ValueError("Invalid value for `lifetime`, must not be `None`")  # noqa: E501

        self._lifetime = lifetime

    @property
    def type(self):
        """Gets the type of this CustomEntityFieldDefinition.  # noqa: E501

        The value type for the field. Available values are: “String”, “Boolean”, “DateTime”, “Decimal”.  # noqa: E501

        :return: The type of this CustomEntityFieldDefinition.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CustomEntityFieldDefinition.

        The value type for the field. Available values are: “String”, “Boolean”, “DateTime”, “Decimal”.  # noqa: E501

        :param type: The type of this CustomEntityFieldDefinition.  # noqa: E501
        :type type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def required(self):
        """Gets the required of this CustomEntityFieldDefinition.  # noqa: E501

        Whether the field is required or not.  # noqa: E501

        :return: The required of this CustomEntityFieldDefinition.  # noqa: E501
        :rtype: bool
        """
        return self._required

    @required.setter
    def required(self, required):
        """Sets the required of this CustomEntityFieldDefinition.

        Whether the field is required or not.  # noqa: E501

        :param required: The required of this CustomEntityFieldDefinition.  # noqa: E501
        :type required: bool
        """
        if self.local_vars_configuration.client_side_validation and required is None:  # noqa: E501
            raise ValueError("Invalid value for `required`, must not be `None`")  # noqa: E501

        self._required = required

    @property
    def description(self):
        """Gets the description of this CustomEntityFieldDefinition.  # noqa: E501

        An optional description for the field.  # noqa: E501

        :return: The description of this CustomEntityFieldDefinition.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CustomEntityFieldDefinition.

        An optional description for the field.  # noqa: E501

        :param description: The description of this CustomEntityFieldDefinition.  # noqa: E501
        :type description: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 512):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `512`")  # noqa: E501

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
        if not isinstance(other, CustomEntityFieldDefinition):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CustomEntityFieldDefinition):
            return True

        return self.to_dict() != other.to_dict()
