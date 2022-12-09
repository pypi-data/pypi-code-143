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


class TaxRule(object):
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
        'description': 'str',
        'rate': 'float',
        'match_criteria': 'list[MatchCriterion]',
        'links': 'list[Link]'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'rate': 'rate',
        'match_criteria': 'matchCriteria',
        'links': 'links'
    }

    required_map = {
        'name': 'required',
        'description': 'required',
        'rate': 'required',
        'match_criteria': 'required',
        'links': 'optional'
    }

    def __init__(self, name=None, description=None, rate=None, match_criteria=None, links=None, local_vars_configuration=None):  # noqa: E501
        """TaxRule - a model defined in OpenAPI"
        
        :param name:  A user-friendly name (required)
        :type name: str
        :param description:  A description for this rule (required)
        :type description: str
        :param rate:  The rate to be applied if all criteria are met (required)
        :type rate: float
        :param match_criteria:  A set of criteria to be met for this rule to be applied (required)
        :type match_criteria: list[lusid.MatchCriterion]
        :param links:  Collection of links.
        :type links: list[lusid.Link]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._description = None
        self._rate = None
        self._match_criteria = None
        self._links = None
        self.discriminator = None

        self.name = name
        self.description = description
        self.rate = rate
        self.match_criteria = match_criteria
        self.links = links

    @property
    def name(self):
        """Gets the name of this TaxRule.  # noqa: E501

        A user-friendly name  # noqa: E501

        :return: The name of this TaxRule.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TaxRule.

        A user-friendly name  # noqa: E501

        :param name: The name of this TaxRule.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 64):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', name)):  # noqa: E501
            raise ValueError(r"Invalid value for `name`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this TaxRule.  # noqa: E501

        A description for this rule  # noqa: E501

        :return: The description of this TaxRule.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this TaxRule.

        A description for this rule  # noqa: E501

        :param description: The description of this TaxRule.  # noqa: E501
        :type description: str
        """
        if self.local_vars_configuration.client_side_validation and description is None:  # noqa: E501
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 1024):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 0):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and not re.search(r'^[\s\S]*$', description)):  # noqa: E501
            raise ValueError(r"Invalid value for `description`, must be a follow pattern or equal to `/^[\s\S]*$/`")  # noqa: E501

        self._description = description

    @property
    def rate(self):
        """Gets the rate of this TaxRule.  # noqa: E501

        The rate to be applied if all criteria are met  # noqa: E501

        :return: The rate of this TaxRule.  # noqa: E501
        :rtype: float
        """
        return self._rate

    @rate.setter
    def rate(self, rate):
        """Sets the rate of this TaxRule.

        The rate to be applied if all criteria are met  # noqa: E501

        :param rate: The rate of this TaxRule.  # noqa: E501
        :type rate: float
        """
        if self.local_vars_configuration.client_side_validation and rate is None:  # noqa: E501
            raise ValueError("Invalid value for `rate`, must not be `None`")  # noqa: E501

        self._rate = rate

    @property
    def match_criteria(self):
        """Gets the match_criteria of this TaxRule.  # noqa: E501

        A set of criteria to be met for this rule to be applied  # noqa: E501

        :return: The match_criteria of this TaxRule.  # noqa: E501
        :rtype: list[lusid.MatchCriterion]
        """
        return self._match_criteria

    @match_criteria.setter
    def match_criteria(self, match_criteria):
        """Sets the match_criteria of this TaxRule.

        A set of criteria to be met for this rule to be applied  # noqa: E501

        :param match_criteria: The match_criteria of this TaxRule.  # noqa: E501
        :type match_criteria: list[lusid.MatchCriterion]
        """
        if self.local_vars_configuration.client_side_validation and match_criteria is None:  # noqa: E501
            raise ValueError("Invalid value for `match_criteria`, must not be `None`")  # noqa: E501

        self._match_criteria = match_criteria

    @property
    def links(self):
        """Gets the links of this TaxRule.  # noqa: E501

        Collection of links.  # noqa: E501

        :return: The links of this TaxRule.  # noqa: E501
        :rtype: list[lusid.Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this TaxRule.

        Collection of links.  # noqa: E501

        :param links: The links of this TaxRule.  # noqa: E501
        :type links: list[lusid.Link]
        """

        self._links = links

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
        if not isinstance(other, TaxRule):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TaxRule):
            return True

        return self.to_dict() != other.to_dict()
