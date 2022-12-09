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


class PromptActionRequest(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "actor",
            "verb",
        }
        
        class properties:
        
            @staticmethod
            def actor() -> typing.Type['PromptActionActorRequest']:
                return PromptActionActorRequest
            
            
            class verb(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 255
                    min_length = 1
        
            @staticmethod
            def action_object() -> typing.Type['PromptActionObjectRequest']:
                return PromptActionObjectRequest
        
            @staticmethod
            def target() -> typing.Type['PromptActionTargetRequest']:
                return PromptActionTargetRequest
            public = schemas.BoolSchema
            
            
            class description(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'description':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            timestamp = schemas.DateTimeSchema
            __annotations__ = {
                "actor": actor,
                "verb": verb,
                "action_object": action_object,
                "target": target,
                "public": public,
                "description": description,
                "timestamp": timestamp,
            }
    
    actor: 'PromptActionActorRequest'
    verb: MetaOapg.properties.verb
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["actor"]) -> 'PromptActionActorRequest': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["verb"]) -> MetaOapg.properties.verb: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["action_object"]) -> 'PromptActionObjectRequest': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["target"]) -> 'PromptActionTargetRequest': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["public"]) -> MetaOapg.properties.public: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["timestamp"]) -> MetaOapg.properties.timestamp: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["actor", "verb", "action_object", "target", "public", "description", "timestamp", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["actor"]) -> 'PromptActionActorRequest': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["verb"]) -> MetaOapg.properties.verb: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["action_object"]) -> typing.Union['PromptActionObjectRequest', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["target"]) -> typing.Union['PromptActionTargetRequest', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["public"]) -> typing.Union[MetaOapg.properties.public, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["timestamp"]) -> typing.Union[MetaOapg.properties.timestamp, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["actor", "verb", "action_object", "target", "public", "description", "timestamp", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        actor: 'PromptActionActorRequest',
        verb: typing.Union[MetaOapg.properties.verb, str, ],
        action_object: typing.Union['PromptActionObjectRequest', schemas.Unset] = schemas.unset,
        target: typing.Union['PromptActionTargetRequest', schemas.Unset] = schemas.unset,
        public: typing.Union[MetaOapg.properties.public, bool, schemas.Unset] = schemas.unset,
        description: typing.Union[MetaOapg.properties.description, None, str, schemas.Unset] = schemas.unset,
        timestamp: typing.Union[MetaOapg.properties.timestamp, str, datetime, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'PromptActionRequest':
        return super().__new__(
            cls,
            *args,
            actor=actor,
            verb=verb,
            action_object=action_object,
            target=target,
            public=public,
            description=description,
            timestamp=timestamp,
            _configuration=_configuration,
            **kwargs,
        )

from frontrunner_python_sdk.model.prompt_action_actor_request import PromptActionActorRequest
from frontrunner_python_sdk.model.prompt_action_object_request import PromptActionObjectRequest
from frontrunner_python_sdk.model.prompt_action_target_request import PromptActionTargetRequest
