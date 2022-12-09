"""
    Fastly API

    Via the Fastly API you can perform any of the operations that are possible within the management console,  including creating services, domains, and backends, configuring rules or uploading your own application code, as well as account operations such as user administration and billing reports. The API is organized into collections of endpoints that allow manipulation of objects related to Fastly services and accounts. For the most accurate and up-to-date API reference content, visit our [Developer Hub](https://developer.fastly.com/reference/api/)   # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: oss@fastly.com
"""


import re  # noqa: F401
import sys  # noqa: F401

from fastly.api_client import ApiClient, Endpoint as _Endpoint
from fastly.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from fastly.model.waf_firewall import WafFirewall
from fastly.model.waf_firewall_response import WafFirewallResponse
from fastly.model.waf_firewalls_response import WafFirewallsResponse


class WafFirewallsApi(object):
    """NOTE: This class is auto generated.
    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.create_waf_firewall_endpoint = _Endpoint(
            settings={
                'response_type': (WafFirewallResponse,),
                'auth': [
                    'token'
                ],
                'endpoint_path': '/waf/firewalls',
                'operation_id': 'create_waf_firewall',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'waf_firewall',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'waf_firewall':
                        (WafFirewall,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'waf_firewall': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/vnd.api+json'
                ],
                'content_type': [
                    'application/vnd.api+json'
                ]
            },
            api_client=api_client
        )
        self.delete_waf_firewall_endpoint = _Endpoint(
            settings={
                'response_type': None,
                'auth': [
                    'token'
                ],
                'endpoint_path': '/waf/firewalls/{firewall_id}',
                'operation_id': 'delete_waf_firewall',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'firewall_id',
                    'waf_firewall',
                ],
                'required': [
                    'firewall_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'firewall_id':
                        (str,),
                    'waf_firewall':
                        (WafFirewall,),
                },
                'attribute_map': {
                    'firewall_id': 'firewall_id',
                },
                'location_map': {
                    'firewall_id': 'path',
                    'waf_firewall': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )
        self.get_waf_firewall_endpoint = _Endpoint(
            settings={
                'response_type': (WafFirewallResponse,),
                'auth': [
                    'token'
                ],
                'endpoint_path': '/waf/firewalls/{firewall_id}',
                'operation_id': 'get_waf_firewall',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'firewall_id',
                    'filter_service_version_number',
                    'include',
                ],
                'required': [
                    'firewall_id',
                ],
                'nullable': [
                ],
                'enum': [
                    'include',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('include',): {

                        "WAF_FIREWALL_VERSIONS": "waf_firewall_versions"
                    },
                },
                'openapi_types': {
                    'firewall_id':
                        (str,),
                    'filter_service_version_number':
                        (str,),
                    'include':
                        (str,),
                },
                'attribute_map': {
                    'firewall_id': 'firewall_id',
                    'filter_service_version_number': 'filter[service_version_number]',
                    'include': 'include',
                },
                'location_map': {
                    'firewall_id': 'path',
                    'filter_service_version_number': 'query',
                    'include': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/vnd.api+json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.list_waf_firewalls_endpoint = _Endpoint(
            settings={
                'response_type': (WafFirewallsResponse,),
                'auth': [
                    'token'
                ],
                'endpoint_path': '/waf/firewalls',
                'operation_id': 'list_waf_firewalls',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'page_number',
                    'page_size',
                    'filter_service_id',
                    'filter_service_version_number',
                    'include',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                    'include',
                ],
                'validation': [
                    'page_size',
                ]
            },
            root_map={
                'validations': {
                    ('page_size',): {

                        'inclusive_maximum': 100,
                        'inclusive_minimum': 1,
                    },
                },
                'allowed_values': {
                    ('include',): {

                        "WAF_FIREWALL_VERSIONS": "waf_firewall_versions"
                    },
                },
                'openapi_types': {
                    'page_number':
                        (int,),
                    'page_size':
                        (int,),
                    'filter_service_id':
                        (str,),
                    'filter_service_version_number':
                        (str,),
                    'include':
                        (str,),
                },
                'attribute_map': {
                    'page_number': 'page[number]',
                    'page_size': 'page[size]',
                    'filter_service_id': 'filter[service_id]',
                    'filter_service_version_number': 'filter[service_version_number]',
                    'include': 'include',
                },
                'location_map': {
                    'page_number': 'query',
                    'page_size': 'query',
                    'filter_service_id': 'query',
                    'filter_service_version_number': 'query',
                    'include': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/vnd.api+json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.update_waf_firewall_endpoint = _Endpoint(
            settings={
                'response_type': (WafFirewallResponse,),
                'auth': [
                    'token'
                ],
                'endpoint_path': '/waf/firewalls/{firewall_id}',
                'operation_id': 'update_waf_firewall',
                'http_method': 'PATCH',
                'servers': None,
            },
            params_map={
                'all': [
                    'firewall_id',
                    'waf_firewall',
                ],
                'required': [
                    'firewall_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'firewall_id':
                        (str,),
                    'waf_firewall':
                        (WafFirewall,),
                },
                'attribute_map': {
                    'firewall_id': 'firewall_id',
                },
                'location_map': {
                    'firewall_id': 'path',
                    'waf_firewall': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/vnd.api+json'
                ],
                'content_type': [
                    'application/vnd.api+json'
                ]
            },
            api_client=api_client
        )

    def create_waf_firewall(
        self,
        **kwargs
    ):
        """Create a firewall  # noqa: E501

        Create a firewall object for a particular service and service version using a defined `prefetch_condition` and `response`. If the `prefetch_condition` or the `response` is missing from the request body, Fastly will generate a default object on your service.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.create_waf_firewall(async_req=True)
        >>> result = thread.get()


        Keyword Args:
            waf_firewall (WafFirewall): [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            WafFirewallResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        return self.create_waf_firewall_endpoint.call_with_http_info(**kwargs)

    def delete_waf_firewall(
        self,
        firewall_id,
        **kwargs
    ):
        """Delete a firewall  # noqa: E501

        Delete the firewall object for a particular service and service version.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_waf_firewall(firewall_id, async_req=True)
        >>> result = thread.get()

        Args:
            firewall_id (str): Alphanumeric string identifying a WAF Firewall.

        Keyword Args:
            waf_firewall (WafFirewall): [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            None
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['firewall_id'] = \
            firewall_id
        return self.delete_waf_firewall_endpoint.call_with_http_info(**kwargs)

    def get_waf_firewall(
        self,
        firewall_id,
        **kwargs
    ):
        """Get a firewall  # noqa: E501

        Get a specific firewall object.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_waf_firewall(firewall_id, async_req=True)
        >>> result = thread.get()

        Args:
            firewall_id (str): Alphanumeric string identifying a WAF Firewall.

        Keyword Args:
            filter_service_version_number (str): Limit the results returned to a specific service version.. [optional]
            include (str): Include related objects. Optional.. [optional] if omitted the server will use the default value of "waf_firewall_versions"
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            WafFirewallResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['firewall_id'] = \
            firewall_id
        return self.get_waf_firewall_endpoint.call_with_http_info(**kwargs)

    def list_waf_firewalls(
        self,
        **kwargs
    ):
        """List firewalls  # noqa: E501

        List all firewall objects.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.list_waf_firewalls(async_req=True)
        >>> result = thread.get()


        Keyword Args:
            page_number (int): Current page.. [optional]
            page_size (int): Number of records per page.. [optional] if omitted the server will use the default value of 20
            filter_service_id (str): Limit the results returned to a specific service.. [optional]
            filter_service_version_number (str): Limit the results returned to a specific service version.. [optional]
            include (str): Include related objects. Optional.. [optional] if omitted the server will use the default value of "waf_firewall_versions"
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            WafFirewallsResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        return self.list_waf_firewalls_endpoint.call_with_http_info(**kwargs)

    def update_waf_firewall(
        self,
        firewall_id,
        **kwargs
    ):
        """Update a firewall  # noqa: E501

        Update a firewall object for a particular service and service version. Specifying a `service_version_number` is required.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.update_waf_firewall(firewall_id, async_req=True)
        >>> result = thread.get()

        Args:
            firewall_id (str): Alphanumeric string identifying a WAF Firewall.

        Keyword Args:
            waf_firewall (WafFirewall): [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            WafFirewallResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['firewall_id'] = \
            firewall_id
        return self.update_waf_firewall_endpoint.call_with_http_info(**kwargs)

