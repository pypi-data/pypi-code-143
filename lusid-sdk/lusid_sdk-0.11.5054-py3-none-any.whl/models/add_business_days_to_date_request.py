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


class AddBusinessDaysToDateRequest(object):
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
        'business_day_offset': 'int',
        'holiday_codes': 'list[str]',
        'start_date': 'datetime',
        'as_at': 'datetime'
    }

    attribute_map = {
        'business_day_offset': 'businessDayOffset',
        'holiday_codes': 'holidayCodes',
        'start_date': 'startDate',
        'as_at': 'asAt'
    }

    required_map = {
        'business_day_offset': 'required',
        'holiday_codes': 'required',
        'start_date': 'optional',
        'as_at': 'optional'
    }

    def __init__(self, business_day_offset=None, holiday_codes=None, start_date=None, as_at=None, local_vars_configuration=None):  # noqa: E501
        """AddBusinessDaysToDateRequest - a model defined in OpenAPI"
        
        :param business_day_offset:  (required)
        :type business_day_offset: int
        :param holiday_codes:  (required)
        :type holiday_codes: list[str]
        :param start_date: 
        :type start_date: datetime
        :param as_at: 
        :type as_at: datetime

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._business_day_offset = None
        self._holiday_codes = None
        self._start_date = None
        self._as_at = None
        self.discriminator = None

        self.business_day_offset = business_day_offset
        self.holiday_codes = holiday_codes
        if start_date is not None:
            self.start_date = start_date
        self.as_at = as_at

    @property
    def business_day_offset(self):
        """Gets the business_day_offset of this AddBusinessDaysToDateRequest.  # noqa: E501


        :return: The business_day_offset of this AddBusinessDaysToDateRequest.  # noqa: E501
        :rtype: int
        """
        return self._business_day_offset

    @business_day_offset.setter
    def business_day_offset(self, business_day_offset):
        """Sets the business_day_offset of this AddBusinessDaysToDateRequest.


        :param business_day_offset: The business_day_offset of this AddBusinessDaysToDateRequest.  # noqa: E501
        :type business_day_offset: int
        """
        if self.local_vars_configuration.client_side_validation and business_day_offset is None:  # noqa: E501
            raise ValueError("Invalid value for `business_day_offset`, must not be `None`")  # noqa: E501

        self._business_day_offset = business_day_offset

    @property
    def holiday_codes(self):
        """Gets the holiday_codes of this AddBusinessDaysToDateRequest.  # noqa: E501


        :return: The holiday_codes of this AddBusinessDaysToDateRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._holiday_codes

    @holiday_codes.setter
    def holiday_codes(self, holiday_codes):
        """Sets the holiday_codes of this AddBusinessDaysToDateRequest.


        :param holiday_codes: The holiday_codes of this AddBusinessDaysToDateRequest.  # noqa: E501
        :type holiday_codes: list[str]
        """
        if self.local_vars_configuration.client_side_validation and holiday_codes is None:  # noqa: E501
            raise ValueError("Invalid value for `holiday_codes`, must not be `None`")  # noqa: E501

        self._holiday_codes = holiday_codes

    @property
    def start_date(self):
        """Gets the start_date of this AddBusinessDaysToDateRequest.  # noqa: E501


        :return: The start_date of this AddBusinessDaysToDateRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this AddBusinessDaysToDateRequest.


        :param start_date: The start_date of this AddBusinessDaysToDateRequest.  # noqa: E501
        :type start_date: datetime
        """

        self._start_date = start_date

    @property
    def as_at(self):
        """Gets the as_at of this AddBusinessDaysToDateRequest.  # noqa: E501


        :return: The as_at of this AddBusinessDaysToDateRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._as_at

    @as_at.setter
    def as_at(self, as_at):
        """Sets the as_at of this AddBusinessDaysToDateRequest.


        :param as_at: The as_at of this AddBusinessDaysToDateRequest.  # noqa: E501
        :type as_at: datetime
        """

        self._as_at = as_at

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
        if not isinstance(other, AddBusinessDaysToDateRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AddBusinessDaysToDateRequest):
            return True

        return self.to_dict() != other.to_dict()
