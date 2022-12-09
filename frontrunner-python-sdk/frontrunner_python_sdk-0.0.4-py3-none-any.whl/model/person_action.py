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


class PersonAction(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "pk",
        }
        
        class properties:
            pk = schemas.IntSchema
            class_name = schemas.StrSchema
            
            
            class first_name(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 50
            
            
            class last_name(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 50
            
            
            class dob(
                schemas.DateBase,
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                class MetaOapg:
                    format = 'date'
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, str, date, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'dob':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "pk": pk,
                "class_name": class_name,
                "first_name": first_name,
                "last_name": last_name,
                "dob": dob,
            }
    
    pk: MetaOapg.properties.pk
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pk"]) -> MetaOapg.properties.pk: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["class_name"]) -> MetaOapg.properties.class_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["first_name"]) -> MetaOapg.properties.first_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_name"]) -> MetaOapg.properties.last_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["dob"]) -> MetaOapg.properties.dob: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["pk", "class_name", "first_name", "last_name", "dob", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pk"]) -> MetaOapg.properties.pk: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["class_name"]) -> typing.Union[MetaOapg.properties.class_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["first_name"]) -> typing.Union[MetaOapg.properties.first_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_name"]) -> typing.Union[MetaOapg.properties.last_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["dob"]) -> typing.Union[MetaOapg.properties.dob, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["pk", "class_name", "first_name", "last_name", "dob", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        pk: typing.Union[MetaOapg.properties.pk, decimal.Decimal, int, ],
        class_name: typing.Union[MetaOapg.properties.class_name, str, schemas.Unset] = schemas.unset,
        first_name: typing.Union[MetaOapg.properties.first_name, str, schemas.Unset] = schemas.unset,
        last_name: typing.Union[MetaOapg.properties.last_name, str, schemas.Unset] = schemas.unset,
        dob: typing.Union[MetaOapg.properties.dob, None, str, date, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'PersonAction':
        return super().__new__(
            cls,
            *args,
            pk=pk,
            class_name=class_name,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            _configuration=_configuration,
            **kwargs,
        )
