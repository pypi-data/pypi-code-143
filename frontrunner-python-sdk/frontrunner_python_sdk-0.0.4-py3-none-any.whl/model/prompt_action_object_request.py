# coding: utf-8

"""
    FrontRunner API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from frontrunner_python_sdk import schemas  # noqa: F401


class PromptActionObjectRequest(
    schemas.ComposedSchema,
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        @staticmethod
        def discriminator():
            return {
                'class_name': {
                    'Broadcast': BroadcastActionRequest,
                    'BroadcastActionRequest': BroadcastActionRequest,
                    'Person': PersonActionRequest,
                    'PersonActionRequest': PersonActionRequest,
                    'TenantUserProfile': UserProfileActionRequest,
                    'UserProfileActionRequest': UserProfileActionRequest,
                    'Vendor': VendorActionRequest,
                    'VendorActionRequest': VendorActionRequest,
                }
            }
        
        @classmethod
        @functools.lru_cache()
        def any_of(cls):
            # we need this here to make our import statements work
            # we must store _composed_schemas in here so the code is only run
            # when we invoke this method. If we kept this at the class
            # level we would get an error because the class level
            # code would be run when this module is imported, and these composed
            # classes don't exist yet because their module has not finished
            # loading
            return [
                UserProfileActionRequest,
                VendorActionRequest,
                PersonActionRequest,
                BroadcastActionRequest,
            ]


    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'PromptActionObjectRequest':
        return super().__new__(
            cls,
            *args,
            _configuration=_configuration,
            **kwargs,
        )

from frontrunner_python_sdk.model.broadcast_action_request import BroadcastActionRequest
from frontrunner_python_sdk.model.person_action_request import PersonActionRequest
from frontrunner_python_sdk.model.user_profile_action_request import UserProfileActionRequest
from frontrunner_python_sdk.model.vendor_action_request import VendorActionRequest
