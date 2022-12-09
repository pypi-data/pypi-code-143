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


class TransitionEventAllOf(object):
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
        'announcement_date': 'datetime',
        'ex_date': 'datetime',
        'record_date': 'datetime',
        'payment_date': 'datetime',
        'input_transition': 'InputTransition',
        'output_transitions': 'list[OutputTransition]',
        'instrument_event_type': 'str'
    }

    attribute_map = {
        'announcement_date': 'announcementDate',
        'ex_date': 'exDate',
        'record_date': 'recordDate',
        'payment_date': 'paymentDate',
        'input_transition': 'inputTransition',
        'output_transitions': 'outputTransitions',
        'instrument_event_type': 'instrumentEventType'
    }

    required_map = {
        'announcement_date': 'optional',
        'ex_date': 'optional',
        'record_date': 'optional',
        'payment_date': 'optional',
        'input_transition': 'optional',
        'output_transitions': 'optional',
        'instrument_event_type': 'required'
    }

    def __init__(self, announcement_date=None, ex_date=None, record_date=None, payment_date=None, input_transition=None, output_transitions=None, instrument_event_type=None, local_vars_configuration=None):  # noqa: E501
        """TransitionEventAllOf - a model defined in OpenAPI"
        
        :param announcement_date:  The announcement date of the corporate action
        :type announcement_date: datetime
        :param ex_date:  The ex date of the corporate action
        :type ex_date: datetime
        :param record_date:  The record date of the corporate action
        :type record_date: datetime
        :param payment_date:  The payment date of the corporate action
        :type payment_date: datetime
        :param input_transition: 
        :type input_transition: lusid.InputTransition
        :param output_transitions:  The resulting transitions from this event
        :type output_transitions: list[lusid.OutputTransition]
        :param instrument_event_type:  The Type of Event. The available values are: TransitionEvent, InformationalEvent, OpenEvent, CloseEvent, StockSplitEvent, BondDefaultEvent, CashDividendEvent, AmortisationEvent, CashFlowEvent, ExerciseEvent, ResetEvent (required)
        :type instrument_event_type: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._announcement_date = None
        self._ex_date = None
        self._record_date = None
        self._payment_date = None
        self._input_transition = None
        self._output_transitions = None
        self._instrument_event_type = None
        self.discriminator = None

        if announcement_date is not None:
            self.announcement_date = announcement_date
        if ex_date is not None:
            self.ex_date = ex_date
        if record_date is not None:
            self.record_date = record_date
        if payment_date is not None:
            self.payment_date = payment_date
        if input_transition is not None:
            self.input_transition = input_transition
        self.output_transitions = output_transitions
        self.instrument_event_type = instrument_event_type

    @property
    def announcement_date(self):
        """Gets the announcement_date of this TransitionEventAllOf.  # noqa: E501

        The announcement date of the corporate action  # noqa: E501

        :return: The announcement_date of this TransitionEventAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._announcement_date

    @announcement_date.setter
    def announcement_date(self, announcement_date):
        """Sets the announcement_date of this TransitionEventAllOf.

        The announcement date of the corporate action  # noqa: E501

        :param announcement_date: The announcement_date of this TransitionEventAllOf.  # noqa: E501
        :type announcement_date: datetime
        """

        self._announcement_date = announcement_date

    @property
    def ex_date(self):
        """Gets the ex_date of this TransitionEventAllOf.  # noqa: E501

        The ex date of the corporate action  # noqa: E501

        :return: The ex_date of this TransitionEventAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._ex_date

    @ex_date.setter
    def ex_date(self, ex_date):
        """Sets the ex_date of this TransitionEventAllOf.

        The ex date of the corporate action  # noqa: E501

        :param ex_date: The ex_date of this TransitionEventAllOf.  # noqa: E501
        :type ex_date: datetime
        """

        self._ex_date = ex_date

    @property
    def record_date(self):
        """Gets the record_date of this TransitionEventAllOf.  # noqa: E501

        The record date of the corporate action  # noqa: E501

        :return: The record_date of this TransitionEventAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._record_date

    @record_date.setter
    def record_date(self, record_date):
        """Sets the record_date of this TransitionEventAllOf.

        The record date of the corporate action  # noqa: E501

        :param record_date: The record_date of this TransitionEventAllOf.  # noqa: E501
        :type record_date: datetime
        """

        self._record_date = record_date

    @property
    def payment_date(self):
        """Gets the payment_date of this TransitionEventAllOf.  # noqa: E501

        The payment date of the corporate action  # noqa: E501

        :return: The payment_date of this TransitionEventAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._payment_date

    @payment_date.setter
    def payment_date(self, payment_date):
        """Sets the payment_date of this TransitionEventAllOf.

        The payment date of the corporate action  # noqa: E501

        :param payment_date: The payment_date of this TransitionEventAllOf.  # noqa: E501
        :type payment_date: datetime
        """

        self._payment_date = payment_date

    @property
    def input_transition(self):
        """Gets the input_transition of this TransitionEventAllOf.  # noqa: E501


        :return: The input_transition of this TransitionEventAllOf.  # noqa: E501
        :rtype: lusid.InputTransition
        """
        return self._input_transition

    @input_transition.setter
    def input_transition(self, input_transition):
        """Sets the input_transition of this TransitionEventAllOf.


        :param input_transition: The input_transition of this TransitionEventAllOf.  # noqa: E501
        :type input_transition: lusid.InputTransition
        """

        self._input_transition = input_transition

    @property
    def output_transitions(self):
        """Gets the output_transitions of this TransitionEventAllOf.  # noqa: E501

        The resulting transitions from this event  # noqa: E501

        :return: The output_transitions of this TransitionEventAllOf.  # noqa: E501
        :rtype: list[lusid.OutputTransition]
        """
        return self._output_transitions

    @output_transitions.setter
    def output_transitions(self, output_transitions):
        """Sets the output_transitions of this TransitionEventAllOf.

        The resulting transitions from this event  # noqa: E501

        :param output_transitions: The output_transitions of this TransitionEventAllOf.  # noqa: E501
        :type output_transitions: list[lusid.OutputTransition]
        """

        self._output_transitions = output_transitions

    @property
    def instrument_event_type(self):
        """Gets the instrument_event_type of this TransitionEventAllOf.  # noqa: E501

        The Type of Event. The available values are: TransitionEvent, InformationalEvent, OpenEvent, CloseEvent, StockSplitEvent, BondDefaultEvent, CashDividendEvent, AmortisationEvent, CashFlowEvent, ExerciseEvent, ResetEvent  # noqa: E501

        :return: The instrument_event_type of this TransitionEventAllOf.  # noqa: E501
        :rtype: str
        """
        return self._instrument_event_type

    @instrument_event_type.setter
    def instrument_event_type(self, instrument_event_type):
        """Sets the instrument_event_type of this TransitionEventAllOf.

        The Type of Event. The available values are: TransitionEvent, InformationalEvent, OpenEvent, CloseEvent, StockSplitEvent, BondDefaultEvent, CashDividendEvent, AmortisationEvent, CashFlowEvent, ExerciseEvent, ResetEvent  # noqa: E501

        :param instrument_event_type: The instrument_event_type of this TransitionEventAllOf.  # noqa: E501
        :type instrument_event_type: str
        """
        if self.local_vars_configuration.client_side_validation and instrument_event_type is None:  # noqa: E501
            raise ValueError("Invalid value for `instrument_event_type`, must not be `None`")  # noqa: E501
        allowed_values = ["TransitionEvent", "InformationalEvent", "OpenEvent", "CloseEvent", "StockSplitEvent", "BondDefaultEvent", "CashDividendEvent", "AmortisationEvent", "CashFlowEvent", "ExerciseEvent", "ResetEvent"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and instrument_event_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `instrument_event_type` ({0}), must be one of {1}"  # noqa: E501
                .format(instrument_event_type, allowed_values)
            )

        self._instrument_event_type = instrument_event_type

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
        if not isinstance(other, TransitionEventAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TransitionEventAllOf):
            return True

        return self.to_dict() != other.to_dict()
