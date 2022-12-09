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


class ScreenRecordingHeatmapUrl(object):
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
        'histogram_data': 'list[int]',
        'histogram_interval': 'str',
        'histogram_start_dts': 'str',
        'page_rank': 'int',
        'session_count': 'int',
        'url': 'str'
    }

    attribute_map = {
        'histogram_data': 'histogram_data',
        'histogram_interval': 'histogram_interval',
        'histogram_start_dts': 'histogram_start_dts',
        'page_rank': 'page_rank',
        'session_count': 'session_count',
        'url': 'url'
    }

    def __init__(self, histogram_data=None, histogram_interval=None, histogram_start_dts=None, page_rank=None, session_count=None, url=None):  # noqa: E501
        """ScreenRecordingHeatmapUrl - a model defined in Swagger"""  # noqa: E501

        self._histogram_data = None
        self._histogram_interval = None
        self._histogram_start_dts = None
        self._page_rank = None
        self._session_count = None
        self._url = None
        self.discriminator = None

        if histogram_data is not None:
            self.histogram_data = histogram_data
        if histogram_interval is not None:
            self.histogram_interval = histogram_interval
        if histogram_start_dts is not None:
            self.histogram_start_dts = histogram_start_dts
        if page_rank is not None:
            self.page_rank = page_rank
        if session_count is not None:
            self.session_count = session_count
        if url is not None:
            self.url = url

    @property
    def histogram_data(self):
        """Gets the histogram_data of this ScreenRecordingHeatmapUrl.  # noqa: E501


        :return: The histogram_data of this ScreenRecordingHeatmapUrl.  # noqa: E501
        :rtype: list[int]
        """
        return self._histogram_data

    @histogram_data.setter
    def histogram_data(self, histogram_data):
        """Sets the histogram_data of this ScreenRecordingHeatmapUrl.


        :param histogram_data: The histogram_data of this ScreenRecordingHeatmapUrl.  # noqa: E501
        :type: list[int]
        """

        self._histogram_data = histogram_data

    @property
    def histogram_interval(self):
        """Gets the histogram_interval of this ScreenRecordingHeatmapUrl.  # noqa: E501


        :return: The histogram_interval of this ScreenRecordingHeatmapUrl.  # noqa: E501
        :rtype: str
        """
        return self._histogram_interval

    @histogram_interval.setter
    def histogram_interval(self, histogram_interval):
        """Sets the histogram_interval of this ScreenRecordingHeatmapUrl.


        :param histogram_interval: The histogram_interval of this ScreenRecordingHeatmapUrl.  # noqa: E501
        :type: str
        """

        self._histogram_interval = histogram_interval

    @property
    def histogram_start_dts(self):
        """Gets the histogram_start_dts of this ScreenRecordingHeatmapUrl.  # noqa: E501


        :return: The histogram_start_dts of this ScreenRecordingHeatmapUrl.  # noqa: E501
        :rtype: str
        """
        return self._histogram_start_dts

    @histogram_start_dts.setter
    def histogram_start_dts(self, histogram_start_dts):
        """Sets the histogram_start_dts of this ScreenRecordingHeatmapUrl.


        :param histogram_start_dts: The histogram_start_dts of this ScreenRecordingHeatmapUrl.  # noqa: E501
        :type: str
        """

        self._histogram_start_dts = histogram_start_dts

    @property
    def page_rank(self):
        """Gets the page_rank of this ScreenRecordingHeatmapUrl.  # noqa: E501


        :return: The page_rank of this ScreenRecordingHeatmapUrl.  # noqa: E501
        :rtype: int
        """
        return self._page_rank

    @page_rank.setter
    def page_rank(self, page_rank):
        """Sets the page_rank of this ScreenRecordingHeatmapUrl.


        :param page_rank: The page_rank of this ScreenRecordingHeatmapUrl.  # noqa: E501
        :type: int
        """

        self._page_rank = page_rank

    @property
    def session_count(self):
        """Gets the session_count of this ScreenRecordingHeatmapUrl.  # noqa: E501


        :return: The session_count of this ScreenRecordingHeatmapUrl.  # noqa: E501
        :rtype: int
        """
        return self._session_count

    @session_count.setter
    def session_count(self, session_count):
        """Sets the session_count of this ScreenRecordingHeatmapUrl.


        :param session_count: The session_count of this ScreenRecordingHeatmapUrl.  # noqa: E501
        :type: int
        """

        self._session_count = session_count

    @property
    def url(self):
        """Gets the url of this ScreenRecordingHeatmapUrl.  # noqa: E501


        :return: The url of this ScreenRecordingHeatmapUrl.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this ScreenRecordingHeatmapUrl.


        :param url: The url of this ScreenRecordingHeatmapUrl.  # noqa: E501
        :type: str
        """

        self._url = url

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
        if issubclass(ScreenRecordingHeatmapUrl, dict):
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
        if not isinstance(other, ScreenRecordingHeatmapUrl):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
