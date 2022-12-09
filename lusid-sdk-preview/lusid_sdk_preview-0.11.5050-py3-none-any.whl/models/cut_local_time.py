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


class CutLocalTime(object):
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
        'hours': 'int',
        'minutes': 'int'
    }

    attribute_map = {
        'hours': 'hours',
        'minutes': 'minutes'
    }

    required_map = {
        'hours': 'optional',
        'minutes': 'optional'
    }

    def __init__(self, hours=None, minutes=None, local_vars_configuration=None):  # noqa: E501
        """CutLocalTime - a model defined in OpenAPI"
        
        :param hours: 
        :type hours: int
        :param minutes: 
        :type minutes: int

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._hours = None
        self._minutes = None
        self.discriminator = None

        if hours is not None:
            self.hours = hours
        if minutes is not None:
            self.minutes = minutes

    @property
    def hours(self):
        """Gets the hours of this CutLocalTime.  # noqa: E501


        :return: The hours of this CutLocalTime.  # noqa: E501
        :rtype: int
        """
        return self._hours

    @hours.setter
    def hours(self, hours):
        """Sets the hours of this CutLocalTime.


        :param hours: The hours of this CutLocalTime.  # noqa: E501
        :type hours: int
        """

        self._hours = hours

    @property
    def minutes(self):
        """Gets the minutes of this CutLocalTime.  # noqa: E501


        :return: The minutes of this CutLocalTime.  # noqa: E501
        :rtype: int
        """
        return self._minutes

    @minutes.setter
    def minutes(self, minutes):
        """Sets the minutes of this CutLocalTime.


        :param minutes: The minutes of this CutLocalTime.  # noqa: E501
        :type minutes: int
        """

        self._minutes = minutes

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
        if not isinstance(other, CutLocalTime):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CutLocalTime):
            return True

        return self.to_dict() != other.to_dict()
