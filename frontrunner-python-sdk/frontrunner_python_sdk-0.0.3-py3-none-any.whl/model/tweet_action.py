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


class TweetAction(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "id",
            "url",
        }
        
        class properties:
            
            
            class id(
                schemas.Int64Schema
            ):
            
            
                class MetaOapg:
                    format = 'int64'
                    inclusive_maximum = 9223372036854775807
                    inclusive_minimum = 0
            
            
            class url(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    format = 'uri'
                    max_length = 200
            class_name = schemas.StrSchema
            
            
            class text(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 280
            __annotations__ = {
                "id": id,
                "url": url,
                "class_name": class_name,
                "text": text,
            }
    
    id: MetaOapg.properties.id
    url: MetaOapg.properties.url
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["url"]) -> MetaOapg.properties.url: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["class_name"]) -> MetaOapg.properties.class_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["text"]) -> MetaOapg.properties.text: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "url", "class_name", "text", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["url"]) -> MetaOapg.properties.url: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["class_name"]) -> typing.Union[MetaOapg.properties.class_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["text"]) -> typing.Union[MetaOapg.properties.text, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "url", "class_name", "text", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        id: typing.Union[MetaOapg.properties.id, decimal.Decimal, int, ],
        url: typing.Union[MetaOapg.properties.url, str, ],
        class_name: typing.Union[MetaOapg.properties.class_name, str, schemas.Unset] = schemas.unset,
        text: typing.Union[MetaOapg.properties.text, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'TweetAction':
        return super().__new__(
            cls,
            *args,
            id=id,
            url=url,
            class_name=class_name,
            text=text,
            _configuration=_configuration,
            **kwargs,
        )
