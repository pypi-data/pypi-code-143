# -*- coding: utf-8 -*-

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import abc
from concurrent import futures
import datetime
import functools
import inspect
import logging
import re
import sys
import threading
import time
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Iterable,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from google.api_core import operation
from google.api_core import retry
from google.auth import credentials as auth_credentials
from google.cloud.aiplatform import initializer
from google.cloud.aiplatform import utils
from google.cloud.aiplatform.compat.types import (
    encryption_spec as gca_encryption_spec,
)
from google.cloud.aiplatform.constants import base as base_constants
import proto

from google.protobuf import field_mask_pb2 as field_mask
from google.protobuf import json_format

# This is the default retry callback to be used with get methods.
_DEFAULT_RETRY = retry.Retry()


class Logger:
    """Logging wrapper class with high level helper methods."""

    def __init__(self, name: str):
        """Initializes logger with optional name.

        Args:
            name (str): Name to associate with logger.
        """
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        self._logger.addHandler(handler)

    def log_create_with_lro(
        self,
        cls: Type["VertexAiResourceNoun"],
        lro: Optional[operation.Operation] = None,
    ):
        """Logs create event with LRO.

        Args:
            cls (VertexAiResourceNoun):
                Vertex AI Resource Noun class that is being created.
            lro (operation.Operation):
                Optional. Backing LRO for creation.
        """
        self._logger.info(f"Creating {cls.__name__}")

        if lro:
            self._logger.info(
                f"Create {cls.__name__} backing LRO: {lro.operation.name}"
            )

    def log_create_complete(
        self,
        cls: Type["VertexAiResourceNoun"],
        resource: proto.Message,
        variable_name: str,
    ):
        """Logs create event is complete.

        Will also include code snippet to instantiate resource in SDK.

        Args:
            cls (VertexAiResourceNoun):
                Vertex AI Resource Noun class that is being created.
            resource (proto.Message):
                Vertex AI Resource proto.Message
            variable_name (str): Name of variable to use for code snippet
        """
        self._logger.info(f"{cls.__name__} created. Resource name: {resource.name}")
        self._logger.info(f"To use this {cls.__name__} in another session:")
        self._logger.info(
            f"{variable_name} = aiplatform.{cls.__name__}('{resource.name}')"
        )

    def log_create_complete_with_getter(
        self,
        cls: Type["VertexAiResourceNoun"],
        resource: proto.Message,
        variable_name: str,
    ):
        """Logs create event is complete.

        Will also include code snippet to instantiate resource in SDK.

        Args:
            cls (VertexAiResourceNoun):
                Vertex AI Resource Noun class that is being created.
            resource (proto.Message):
                Vertex AI Resource proto.Message
            variable_name (str): Name of variable to use for code snippet
        """
        self._logger.info(f"{cls.__name__} created. Resource name: {resource.name}")
        self._logger.info(f"To use this {cls.__name__} in another session:")
        self._logger.info(
            f"{variable_name} = aiplatform.{cls.__name__}.get('{resource.name}')"
        )

    def log_action_start_against_resource(
        self, action: str, noun: str, resource_noun_obj: "VertexAiResourceNoun"
    ):
        """Logs intention to start an action against a resource.

        Args:
            action (str): Action to complete against the resource ie: "Deploying". Can be empty string.
            noun (str): Noun the action acts on against the resource. Can be empty string.
            resource_noun_obj (VertexAiResourceNoun):
                Resource noun object the action is acting against.
        """
        self._logger.info(
            f"{action} {resource_noun_obj.__class__.__name__} {noun}: {resource_noun_obj.resource_name}"
        )

    def log_action_started_against_resource_with_lro(
        self,
        action: str,
        noun: str,
        cls: Type["VertexAiResourceNoun"],
        lro: operation.Operation,
    ):
        """Logs an action started against a resource with lro.

        Args:
            action (str): Action started against resource. ie: "Deploy". Can be empty string.
            noun (str): Noun the action acts on against the resource. Can be empty string.
            cls (VertexAiResourceNoun):
                Resource noun object the action is acting against.
            lro (operation.Operation): Backing LRO for action.
        """
        self._logger.info(
            f"{action} {cls.__name__} {noun} backing LRO: {lro.operation.name}"
        )

    def log_action_completed_against_resource(
        self, noun: str, action: str, resource_noun_obj: "VertexAiResourceNoun"
    ):
        """Logs action completed against resource.

        Args:
            noun (str): Noun the action acts on against the resource. Can be empty string.
            action (str): Action started against resource. ie: "Deployed". Can be empty string.
            resource_noun_obj (VertexAiResourceNoun):
                Resource noun object the action is acting against
        """
        self._logger.info(
            f"{resource_noun_obj.__class__.__name__} {noun} {action}. Resource name: {resource_noun_obj.resource_name}"
        )

    def __getattr__(self, attr: str):
        """Forward remainder of logging to underlying logger."""
        return getattr(self._logger, attr)


_LOGGER = Logger(__name__)


class FutureManager(metaclass=abc.ABCMeta):
    """Tracks concurrent futures against this object."""

    def __init__(self):
        self.__latest_future_lock = threading.Lock()

        # Always points to the latest future. All submitted futures will always
        # form a dependency on the latest future.
        self.__latest_future = None

        # Caches Exception of any executed future. Once one exception occurs
        # all additional futures should fail and any additional invocations will block.
        self._exception = None

    def _raise_future_exception(self):
        """Raises exception if one of the object's futures has raised."""
        with self.__latest_future_lock:
            if self._exception:
                raise self._exception

    def _complete_future(self, future: futures.Future):
        """Checks for exception of future and removes the pointer if it's still
        latest.

        Args:
            future (futures.Future): Required. A future to complete.
        """

        with self.__latest_future_lock:
            try:
                future.result()  # raises
            except Exception as e:
                self._exception = e

            if self.__latest_future is future:
                self.__latest_future = None

    def _are_futures_done(self) -> bool:
        """Helper method to check to all futures are complete.

        Returns:
            True if no latest future.
        """
        with self.__latest_future_lock:
            return self.__latest_future is None

    def wait(self):
        """Helper method that blocks until all futures are complete."""
        future = self.__latest_future
        if future:
            futures.wait([future], return_when=futures.FIRST_EXCEPTION)

        self._raise_future_exception()

    @property
    def _latest_future(self) -> Optional[futures.Future]:
        """Get the latest future if it exists."""
        with self.__latest_future_lock:
            return self.__latest_future

    @_latest_future.setter
    def _latest_future(self, future: Optional[futures.Future]):
        """Optionally set the latest future and add a complete_future
        callback."""
        with self.__latest_future_lock:
            self.__latest_future = future
        if future:
            future.add_done_callback(self._complete_future)

    def _submit(
        self,
        method: Callable[..., Any],
        args: Sequence[Any],
        kwargs: Dict[str, Any],
        additional_dependencies: Optional[Sequence[futures.Future]] = None,
        callbacks: Optional[Sequence[Callable[[futures.Future], Any]]] = None,
        internal_callbacks: Iterable[Callable[[Any], Any]] = None,
    ) -> futures.Future:
        """Submit a method as a future against this object.

        Args:
            method (Callable): Required. The method to submit.
            args (Sequence): Required. The arguments to call the method with.
            kwargs (dict): Required. The keyword arguments to call the method with.
            additional_dependencies (Optional[Sequence[futures.Future]]):
                Optional. Additional dependent futures to wait on before executing
                method. Note: No validation is done on the dependencies.
            callbacks (Optional[Sequence[Callable[[futures.Future], Any]]]):
                Optional. Additional Future callbacks to execute once this created
                Future is complete.

        Returns:
            future (Future): Future of the submitted method call.
        """

        def wait_for_dependencies_and_invoke(
            deps: Sequence[futures.Future],
            method: Callable[..., Any],
            args: Sequence[Any],
            kwargs: Dict[str, Any],
            internal_callbacks: Iterable[Callable[[Any], Any]],
        ) -> Any:
            """Wrapper method to wait on any dependencies before submitting
            method.

            Args:
                deps (Sequence[futures.Future]):
                    Required. Dependent futures to wait on before executing method.
                    Note: No validation is done on the dependencies.
                method (Callable): Required. The method to submit.
                args (Sequence[Any]): Required. The arguments to call the method with.
                kwargs (Dict[str, Any]):
                    Required. The keyword arguments to call the method with.
                internal_callbacks: (Callable[[Any], Any]):
                    Callbacks that take the result of method.
            """

            for future in set(deps):
                future.result()

            result = method(*args, **kwargs)

            # call callbacks from within future
            if internal_callbacks:
                for callback in internal_callbacks:
                    callback(result)

            return result

        # Retrieves any dependencies from arguments.
        deps = [
            arg._latest_future
            for arg in list(args) + list(kwargs.values())
            if isinstance(arg, FutureManager)
        ]

        # Retrieves exceptions and raises
        # if any upstream dependency has an exception
        exceptions = [
            arg._exception
            for arg in list(args) + list(kwargs.values())
            if isinstance(arg, FutureManager) and arg._exception
        ]

        if exceptions:
            raise exceptions[0]

        # filter out objects that do not have pending tasks
        deps = [dep for dep in deps if dep]

        if additional_dependencies:
            deps.extend(additional_dependencies)

        with self.__latest_future_lock:

            # form a dependency on the latest future of this object
            if self.__latest_future:
                deps.append(self.__latest_future)

            self.__latest_future = initializer.global_pool.submit(
                wait_for_dependencies_and_invoke,
                deps=deps,
                method=method,
                args=args,
                kwargs=kwargs,
                internal_callbacks=internal_callbacks,
            )

            future = self.__latest_future

        # Clean up callback captures exception as well as removes future.
        # May execute immediately and take lock.

        future.add_done_callback(self._complete_future)

        if callbacks:
            for c in callbacks:
                future.add_done_callback(c)

        return future

    @classmethod
    @abc.abstractmethod
    def _empty_constructor(cls) -> "FutureManager":
        """Should construct object with all non FutureManager attributes as
        None."""
        pass

    @abc.abstractmethod
    def _sync_object_with_future_result(self, result: "FutureManager"):
        """Should sync the object from _empty_constructor with result of
        future."""

    def __repr__(self) -> str:
        if self._exception:
            return f"{object.__repr__(self)} failed with {str(self._exception)}"

        if self.__latest_future:
            return f"{object.__repr__(self)} is waiting for upstream dependencies to complete."

        return object.__repr__(self)


class VertexAiResourceNoun(metaclass=abc.ABCMeta):
    """Base class the Vertex AI resource nouns.

    Subclasses require two class attributes:

    client_class: The client to instantiate to interact with this resource noun.

    Subclass is required to populate private attribute _gca_resource which is the
    service representation of the resource noun.
    """

    @property
    @classmethod
    @abc.abstractmethod
    def client_class(cls) -> Type[utils.VertexAiServiceClientWithOverride]:
        """Client class required to interact with resource with optional
        overrides."""
        pass

    @property
    @classmethod
    @abc.abstractmethod
    def _getter_method(cls) -> str:
        """Name of getter method of client class for retrieving the
        resource."""
        pass

    @property
    @classmethod
    @abc.abstractmethod
    def _delete_method(cls) -> str:
        """Name of delete method of client class for deleting the resource."""
        pass

    @property
    @classmethod
    @abc.abstractmethod
    def _resource_noun(cls) -> str:
        """Resource noun."""
        pass

    @property
    @classmethod
    @abc.abstractmethod
    def _parse_resource_name_method(cls) -> str:
        """Method name on GAPIC client to parse a resource name."""
        pass

    @property
    @classmethod
    @abc.abstractmethod
    def _format_resource_name_method(self) -> str:
        """Method name on GAPIC client to format a resource name."""
        pass

    # Override this value with staticmethod
    # to use custom resource id validators per resource
    _resource_id_validator: Optional[Callable[[str], None]] = None

    @staticmethod
    def _revisioned_resource_id_validator(
        resource_id: str,
    ) -> None:
        """Some revisioned resource names can have '@' in them
        to separate the resource ID from the revision ID.
        Thus, they need their own resource id validator.
        See https://google.aip.dev/162

        Args:
            resource_id(str): A resource ID for a resource type that accepts revision syntax.
                See https://google.aip.dev/162.
        Raises:
            ValueError: If a `resource_id` doesn't conform to appropriate revision syntax.
        """
        if not re.compile(r"^[\w-]+@?[\w-]+$").match(resource_id):
            raise ValueError(f"Resource {resource_id} is not a valid resource ID.")

    def __init__(
        self,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        resource_name: Optional[str] = None,
    ):
        """Initializes class with project, location, and api_client.

        Args:
            project(str): Project of the resource noun.
            location(str): The location of the resource noun.
            credentials(google.auth.credentials.Credentials): Optional custom
                credentials to use when accessing interacting with resource noun.
            resource_name(str): A fully-qualified resource name or ID.
        """

        if resource_name:
            project, location = self._get_and_validate_project_location(
                resource_name=resource_name, project=project, location=location
            )

        self.project = project or initializer.global_config.project
        self.location = location or initializer.global_config.location
        self.credentials = credentials or initializer.global_config.credentials

        appended_user_agent = None
        if base_constants.USER_AGENT_SDK_COMMAND:
            appended_user_agent = [
                f"sdk_command/{base_constants.USER_AGENT_SDK_COMMAND}"
            ]
            # Reset the value for the USER_AGENT_SDK_COMMAND to avoid counting future unrelated api calls.
            base_constants.USER_AGENT_SDK_COMMAND = ""

        self.api_client = self._instantiate_client(
            location=self.location,
            credentials=self.credentials,
            appended_user_agent=appended_user_agent,
        )

    @classmethod
    def _instantiate_client(
        cls,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        appended_user_agent: Optional[List[str]] = None,
    ) -> utils.VertexAiServiceClientWithOverride:
        """Helper method to instantiate service client for resource noun.

        Args:
            location (str): The location of the resource noun.
            credentials (google.auth.credentials.Credentials):
                Optional custom credentials to use when accessing interacting with
                resource noun.
            appended_user_agent (List[str]):
                Optional. User agent appended in the client info. If more than one,
                it will be separated by spaces.
        Returns:
            client (utils.VertexAiServiceClientWithOverride):
                Initialized service client for this service noun with optional overrides.
        """
        return initializer.global_config.create_client(
            client_class=cls.client_class,
            credentials=credentials,
            location_override=location,
            appended_user_agent=appended_user_agent,
        )

    @classmethod
    def _parse_resource_name(cls, resource_name: str) -> Dict[str, str]:
        """
        Parses resource name into its component segments.

        Args:
            resource_name: Resource name of this resource.
        Returns:
            Dictionary of component segments.
        """
        # gets the underlying wrapped gapic client class
        return getattr(
            cls.client_class.get_gapic_client_class(), cls._parse_resource_name_method
        )(resource_name)

    @classmethod
    def _format_resource_name(cls, **kwargs: str) -> str:
        """
        Formats a resource name using its component segments.

        Args:
            **kwargs: Resource name parts. Singular and snake case. ie:
            format_resource_name(
                project='my-project',
                location='us-central1'
            )
        Returns:
            Resource name.
        """
        # gets the underlying wrapped gapic client class
        return getattr(
            cls.client_class.get_gapic_client_class(), cls._format_resource_name_method
        )(**kwargs)

    def _get_and_validate_project_location(
        self,
        resource_name: str,
        project: Optional[str] = None,
        location: Optional[str] = None,
    ) -> Tuple[str, str]:

        """Validate the project and location for the resource.

        Args:
            resource_name(str): Required. A fully-qualified resource name or ID.
            project(str): Project of the resource noun.
            location(str): The location of the resource noun.

        Raises:
            RuntimeError: If location is different from resource location
        """

        fields = self._parse_resource_name(resource_name)

        if not fields:
            return project, location

        if location and fields["location"] != location:
            raise RuntimeError(
                f"location {location} is provided, but different from "
                f"the resource location {fields['location']}"
            )

        return fields["project"], fields["location"]

    def _get_gca_resource(
        self,
        resource_name: str,
        parent_resource_name_fields: Optional[Dict[str, str]] = None,
    ) -> proto.Message:
        """Returns GAPIC service representation of client class resource.

        Args:
            resource_name (str): Required. A fully-qualified resource name or ID.
            parent_resource_name_fields (Dict[str,str]):
                Optional. Mapping of parent resource name key to values. These
                will be used to compose the resource name if only resource ID is given.
                Should not include project and location.
        """
        resource_name = utils.full_resource_name(
            resource_name=resource_name,
            resource_noun=self._resource_noun,
            parse_resource_name_method=self._parse_resource_name,
            format_resource_name_method=self._format_resource_name,
            project=self.project,
            location=self.location,
            parent_resource_name_fields=parent_resource_name_fields,
            resource_id_validator=self._resource_id_validator,
        )

        return getattr(self.api_client, self._getter_method)(
            name=resource_name, retry=_DEFAULT_RETRY
        )

    def _sync_gca_resource(self):
        """Sync GAPIC service representation of client class resource."""

        self._gca_resource = self._get_gca_resource(resource_name=self.resource_name)

    @property
    def name(self) -> str:
        """Name of this resource."""
        self._assert_gca_resource_is_available()
        return self._gca_resource.name.split("/")[-1]

    @property
    def _project_tuple(self) -> Tuple[Optional[str], Optional[str]]:
        """Returns the tuple of project id and project inferred from the local instance.

        Another option is to use resource_manager_utils but requires the caller have resource manager
        get role.
        """
        # we may not have the project if project inferred from the resource name
        maybe_project_id = self.project
        if self._gca_resource is not None and self._gca_resource.name:
            project_no = self._parse_resource_name(self._gca_resource.name)["project"]
        else:
            project_no = None

        if maybe_project_id == project_no:
            return (None, project_no)
        else:
            return (maybe_project_id, project_no)

    @property
    def resource_name(self) -> str:
        """Full qualified resource name."""
        self._assert_gca_resource_is_available()
        return self._gca_resource.name

    @property
    def display_name(self) -> str:
        """Display name of this resource."""
        self._assert_gca_resource_is_available()
        return self._gca_resource.display_name

    @property
    def create_time(self) -> datetime.datetime:
        """Time this resource was created."""
        self._assert_gca_resource_is_available()
        return self._gca_resource.create_time

    @property
    def update_time(self) -> datetime.datetime:
        """Time this resource was last updated."""
        self._sync_gca_resource()
        return self._gca_resource.update_time

    @property
    def encryption_spec(self) -> Optional[gca_encryption_spec.EncryptionSpec]:
        """Customer-managed encryption key options for this Vertex AI resource.

        If this is set, then all resources created by this Vertex AI resource will
        be encrypted with the provided encryption key.
        """
        self._assert_gca_resource_is_available()
        return getattr(self._gca_resource, "encryption_spec")

    @property
    def labels(self) -> Dict[str, str]:
        """User-defined labels containing metadata about this resource.

        Read more about labels at https://goo.gl/xmQnxf
        """
        self._assert_gca_resource_is_available()
        return dict(self._gca_resource.labels)

    @property
    def gca_resource(self) -> proto.Message:
        """The underlying resource proto representation."""
        self._assert_gca_resource_is_available()
        return self._gca_resource

    @property
    def _resource_is_available(self) -> bool:
        """Returns True if GCA resource has been created and is available, otherwise False"""
        try:
            self._assert_gca_resource_is_available()
            return True
        except RuntimeError:
            return False

    def _assert_gca_resource_is_available(self) -> None:
        """Helper method to raise when property is not accessible.

        Raises:
            RuntimeError: If _gca_resource is has not been created.
        """
        if self._gca_resource is None:
            raise RuntimeError(
                f"{self.__class__.__name__} resource has not been created"
            )

    def __repr__(self) -> str:
        return f"{object.__repr__(self)} \nresource name: {self.resource_name}"

    def to_dict(self) -> Dict[str, Any]:
        """Returns the resource proto as a dictionary."""
        return json_format.MessageToDict(self._gca_resource._pb)

    @classmethod
    def _generate_display_name(cls, prefix: Optional[str] = None) -> str:
        """Returns a display name containing class name and time string."""
        if not prefix:
            prefix = cls.__name__
        return prefix + " " + datetime.datetime.now().isoformat(sep=" ")


def optional_sync(
    construct_object_on_arg: Optional[str] = None,
    return_input_arg: Optional[str] = None,
    bind_future_to_self: bool = True,
):
    """Decorator for VertexAiResourceNounWithFutureManager with optional sync
    support.

    Methods with this decorator should include a "sync" argument that defaults to
    True. If called with sync=False this decorator will launch the method as a
    concurrent Future in a separate Thread.

    Note that this is only robust enough to support our current end to end patterns
    and may not be suitable for new patterns.

    Args:
        construct_object_on_arg (str):
            Optional. If provided, will only construct output object if arg is present.
            Example: If custom training does not produce a model.
        return_input_arg (str):
            Optional. If provided will return passed in argument instead of
            constructing.
            Example: Model.deploy(Endpoint) returns the passed in Endpoint
        bind_future_to_self (bool):
            Whether to add this future to the calling object.
            Example: Model.deploy(Endpoint) would be set to False because we only
            want the deployment Future to be associated with Endpoint.
    """

    def optional_run_in_thread(method: Callable[..., Any]):
        """Optionally run this method concurrently in separate Thread.

        Args:
            method (Callable[..., Any]): Method to optionally run in separate Thread.
        """

        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            """Wraps method."""
            sync = kwargs.pop("sync", True)
            bound_args = inspect.signature(method).bind(*args, **kwargs)
            self = bound_args.arguments.get("self")
            calling_object_latest_future = None

            # check to see if this object has any exceptions
            if self:
                calling_object_latest_future = self._latest_future
                self._raise_future_exception()

            # if sync then wait for any Futures to complete and execute
            if sync:
                if self:
                    VertexAiResourceNounWithFutureManager.wait(self)
                return method(*args, **kwargs)

            # callbacks to call within the Future (in same Thread)
            internal_callbacks = []
            # callbacks to add to the Future (may or may not be in same Thread)
            callbacks = []
            # additional Future dependencies to capture
            dependencies = []

            # all methods should have type signatures
            return_type = get_annotation_class(
                inspect.getfullargspec(method).annotations["return"]
            )

            # object produced by the method
            returned_object = bound_args.arguments.get(return_input_arg)

            # is a classmethod that creates the object and returns it
            if args and inspect.isclass(args[0]):

                # assumes class in classmethod is the resource noun
                returned_object = (
                    args[0]._empty_constructor()
                    if not returned_object
                    else returned_object
                )
                self = returned_object

            else:  # instance method
                # if we're returning an input object
                if returned_object and returned_object is not self:

                    # make sure the input object doesn't have any exceptions
                    # from previous futures
                    returned_object._raise_future_exception()

                    # if the future will be associated with both the returned object
                    # and calling object then we need to add additional callback
                    # to remove the future from the returned object

                # if we need to construct a new empty returned object
                should_construct = not returned_object and bound_args.arguments.get(
                    construct_object_on_arg, not construct_object_on_arg
                )

                if should_construct:
                    if return_type is not None:
                        returned_object = return_type._empty_constructor()

                # if the future will be associated with both the returned object
                # and calling object then we need to add additional callback
                # to remove the future from the returned object
                if returned_object and bind_future_to_self:
                    callbacks.append(returned_object._complete_future)

            if returned_object:
                # sync objects after future completes
                internal_callbacks.append(
                    returned_object._sync_object_with_future_result
                )

            # If the future is not associated with the calling object
            # then the return object future needs to form a dependency on the
            # the latest future in the calling object.
            if not bind_future_to_self:
                if calling_object_latest_future:
                    dependencies.append(calling_object_latest_future)
                self = returned_object

            future = self._submit(
                method=method,
                callbacks=callbacks,
                internal_callbacks=internal_callbacks,
                additional_dependencies=dependencies,
                args=[],
                kwargs=bound_args.arguments,
            )

            # if the calling object is the one that submitted then add it's future
            # to the returned object
            if returned_object and returned_object is not self:
                returned_object._latest_future = future

            return returned_object

        return wrapper

    return optional_run_in_thread


class VertexAiResourceNounWithFutureManager(VertexAiResourceNoun, FutureManager):
    """Allows optional asynchronous calls to this Vertex AI Resource
    Nouns."""

    def __init__(
        self,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        resource_name: Optional[str] = None,
    ):
        """Initializes class with project, location, and api_client.

        Args:
            project (str): Optional. Project of the resource noun.
            location (str): Optional. The location of the resource noun.
            credentials(google.auth.credentials.Credentials):
                Optional. custom credentials to use when accessing interacting with
                resource noun.
            resource_name(str): A fully-qualified resource name or ID.
        """
        VertexAiResourceNoun.__init__(
            self,
            project=project,
            location=location,
            credentials=credentials,
            resource_name=resource_name,
        )
        FutureManager.__init__(self)

    @classmethod
    def _empty_constructor(
        cls,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        resource_name: Optional[str] = None,
    ) -> "VertexAiResourceNounWithFutureManager":
        """Initializes with all attributes set to None.

        The attributes should be populated after a future is complete. This allows
        scheduling of additional API calls before the resource is created.

        Args:
            project (str): Optional. Project of the resource noun.
            location (str): Optional. The location of the resource noun.
            credentials(google.auth.credentials.Credentials):
                Optional. custom credentials to use when accessing interacting with
                resource noun.
            resource_name(str): A fully-qualified resource name or ID.
        Returns:
            An instance of this class with attributes set to None.
        """
        self = cls.__new__(cls)
        VertexAiResourceNoun.__init__(
            self,
            project=project,
            location=location,
            credentials=credentials,
            resource_name=resource_name,
        )
        FutureManager.__init__(self)
        self._gca_resource = None
        return self

    def _sync_object_with_future_result(
        self, result: "VertexAiResourceNounWithFutureManager"
    ):
        """Populates attributes from a Future result to this object.

        Args:
            result: VertexAiResourceNounWithFutureManager
                Required. Result of future with same type as this object.
        """
        sync_attributes = [
            "project",
            "location",
            "api_client",
            "_gca_resource",
            "credentials",
        ]
        optional_sync_attributes = [
            "_prediction_client",
            "_authorized_session",
            "_raw_predict_request_url",
        ]

        for attribute in sync_attributes:
            setattr(self, attribute, getattr(result, attribute))

        for attribute in optional_sync_attributes:
            value = getattr(result, attribute, None)
            if value:
                setattr(self, attribute, value)

    @classmethod
    def _construct_sdk_resource_from_gapic(
        cls,
        gapic_resource: proto.Message,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
    ) -> VertexAiResourceNoun:
        """Given a GAPIC resource object, return the SDK representation.

        Args:
            gapic_resource (proto.Message):
                A GAPIC representation of a Vertex AI resource, usually
                retrieved by a get_* or in a list_* API call.
            project (str):
                Optional. Project to construct SDK object from. If not set,
                project set in aiplatform.init will be used.
            location (str):
                Optional. Location to construct SDK object from. If not set,
                location set in aiplatform.init will be used.
            credentials (auth_credentials.Credentials):
                Optional. Custom credentials to use to construct SDK object.
                Overrides credentials set in aiplatform.init.

        Returns:
            VertexAiResourceNoun:
                An initialized SDK object that represents GAPIC type.
        """
        sdk_resource = cls._empty_constructor(
            project=project, location=location, credentials=credentials
        )
        sdk_resource._gca_resource = gapic_resource
        return sdk_resource

    # TODO(b/144545165): Improve documentation for list filtering once available
    # TODO(b/184910159): Expose `page_size` field in list method
    @classmethod
    def _list(
        cls,
        cls_filter: Callable[[proto.Message], bool] = lambda _: True,
        filter: Optional[str] = None,
        order_by: Optional[str] = None,
        read_mask: Optional[field_mask.FieldMask] = None,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        parent: Optional[str] = None,
    ) -> List[VertexAiResourceNoun]:
        """Private method to list all instances of this Vertex AI Resource,
        takes a `cls_filter` arg to filter to a particular SDK resource
        subclass.

        Args:
            cls_filter (Callable[[proto.Message], bool]):
                A function that takes one argument, a GAPIC resource, and returns
                a bool. If the function returns False, that resource will be
                excluded from the returned list. Example usage:
                cls_filter = lambda obj: obj.metadata in cls.valid_metadatas
            filter (str):
                Optional. An expression for filtering the results of the request.
                For field names both snake_case and camelCase are supported.
            order_by (str):
                Optional. A comma-separated list of fields to order by, sorted in
                ascending order. Use "desc" after a field name for descending.
                Supported fields: `display_name`, `create_time`, `update_time`
            read_mask (field_mask.FieldMask):
                Optional. A FieldMask with a list of strings passed via `paths`
                indicating which fields to return for each resource in the response.
                For example, passing
                field_mask.FieldMask(paths=["create_time", "update_time"])
                as `read_mask` would result in each returned VertexAiResourceNoun
                in the result list only having the "create_time" and
                "update_time" attributes.
            project (str):
                Optional. Project to retrieve list from. If not set, project
                set in aiplatform.init will be used.
            location (str):
                Optional. Location to retrieve list from. If not set, location
                set in aiplatform.init will be used.
            credentials (auth_credentials.Credentials):
                Optional. Custom credentials to use to retrieve list. Overrides
                credentials set in aiplatform.init.
            parent (str):
                Optional. The parent resource name if any to retrieve resource list from.

        Returns:
            List[VertexAiResourceNoun] - A list of SDK resource objects
        """
        if parent:
            parent_resources = utils.extract_project_and_location_from_parent(parent)
            if parent_resources:
                project, location = (
                    parent_resources["project"],
                    parent_resources["location"],
                )

        resource = cls._empty_constructor(
            project=project, location=location, credentials=credentials
        )

        # Fetch credentials once and re-use for all `_empty_constructor()` calls
        creds = resource.credentials

        resource_list_method = getattr(resource.api_client, resource._list_method)

        list_request = {
            "parent": parent
            or initializer.global_config.common_location_path(
                project=project, location=location
            ),
        }

        # `read_mask` is only passed from PipelineJob.list() for now
        if read_mask is not None:
            list_request["read_mask"] = read_mask

        if filter:
            list_request["filter"] = filter

        if order_by:
            list_request["order_by"] = order_by

        resource_list = resource_list_method(request=list_request) or []

        return [
            cls._construct_sdk_resource_from_gapic(
                gapic_resource, project=project, location=location, credentials=creds
            )
            for gapic_resource in resource_list
            if cls_filter(gapic_resource)
        ]

    @classmethod
    def _list_with_local_order(
        cls,
        cls_filter: Callable[[proto.Message], bool] = lambda _: True,
        filter: Optional[str] = None,
        order_by: Optional[str] = None,
        read_mask: Optional[field_mask.FieldMask] = None,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
    ) -> List[VertexAiResourceNoun]:
        """Private method to list all instances of this Vertex AI Resource,
        takes a `cls_filter` arg to filter to a particular SDK resource
        subclass. Provides client-side sorting when a list API doesn't support
        `order_by`.

        Args:
            cls_filter (Callable[[proto.Message], bool]):
                A function that takes one argument, a GAPIC resource, and returns
                a bool. If the function returns False, that resource will be
                excluded from the returned list. Example usage:
                cls_filter = lambda obj: obj.metadata in cls.valid_metadatas
            filter (str):
                Optional. An expression for filtering the results of the request.
                For field names both snake_case and camelCase are supported.
            order_by (str):
                Optional. A comma-separated list of fields to order by, sorted in
                ascending order. Use "desc" after a field name for descending.
                Supported fields: `display_name`, `create_time`, `update_time`
            read_mask (field_mask.FieldMask):
                Optional. A FieldMask with a list of strings passed via `paths`
                indicating which fields to return for each resource in the response.
                For example, passing
                field_mask.FieldMask(paths=["create_time", "update_time"])
                as `read_mask` would result in each returned VertexAiResourceNoun
                in the result list only having the "create_time" and
                "update_time" attributes.
            project (str):
                Optional. Project to retrieve list from. If not set, project
                set in aiplatform.init will be used.
            location (str):
                Optional. Location to retrieve list from. If not set, location
                set in aiplatform.init will be used.
            credentials (auth_credentials.Credentials):
                Optional. Custom credentials to use to retrieve list. Overrides
                credentials set in aiplatform.init.

        Returns:
            List[VertexAiResourceNoun] - A list of SDK resource objects
        """

        li = cls._list(
            cls_filter=cls_filter,
            filter=filter,
            order_by=None,  # This method will handle the ordering locally
            read_mask=read_mask,
            project=project,
            location=location,
            credentials=credentials,
        )

        if order_by:
            desc = "desc" in order_by
            order_by = order_by.replace("desc", "")
            order_by = order_by.split(",")

            li.sort(
                key=lambda x: tuple(getattr(x, field.strip()) for field in order_by),
                reverse=desc,
            )

        return li

    @classmethod
    def list(
        cls,
        filter: Optional[str] = None,
        order_by: Optional[str] = None,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        parent: Optional[str] = None,
    ) -> List[VertexAiResourceNoun]:
        """List all instances of this Vertex AI Resource.

        Example Usage:

        aiplatform.BatchPredictionJobs.list(
            filter='state="JOB_STATE_SUCCEEDED" AND display_name="my_job"',
        )

        aiplatform.Model.list(order_by="create_time desc, display_name")

        Args:
            filter (str):
                Optional. An expression for filtering the results of the request.
                For field names both snake_case and camelCase are supported.
            order_by (str):
                Optional. A comma-separated list of fields to order by, sorted in
                ascending order. Use "desc" after a field name for descending.
                Supported fields: `display_name`, `create_time`, `update_time`
            project (str):
                Optional. Project to retrieve list from. If not set, project
                set in aiplatform.init will be used.
            location (str):
                Optional. Location to retrieve list from. If not set, location
                set in aiplatform.init will be used.
            credentials (auth_credentials.Credentials):
                Optional. Custom credentials to use to retrieve list. Overrides
                credentials set in aiplatform.init.
            parent (str):
                Optional. The parent resource name if any to retrieve list from.

        Returns:
            List[VertexAiResourceNoun] - A list of SDK resource objects
        """

        return cls._list(
            filter=filter,
            order_by=order_by,
            project=project,
            location=location,
            credentials=credentials,
            parent=parent,
        )

    @optional_sync()
    def delete(self, sync: bool = True) -> None:
        """Deletes this Vertex AI resource. WARNING: This deletion is
        permanent.

        Args:
            sync (bool):
                Whether to execute this deletion synchronously. If False, this method
                will be executed in concurrent Future and any downstream object will
                be immediately returned and synced when the Future has completed.
        """
        _LOGGER.log_action_start_against_resource("Deleting", "", self)
        lro = getattr(self.api_client, self._delete_method)(name=self.resource_name)
        _LOGGER.log_action_started_against_resource_with_lro(
            "Delete", "", self.__class__, lro
        )
        lro.result()
        _LOGGER.log_action_completed_against_resource("deleted.", "", self)

    def __repr__(self) -> str:
        if self._gca_resource and self._resource_is_available:
            return VertexAiResourceNoun.__repr__(self)

        return FutureManager.__repr__(self)

    def _wait_for_resource_creation(self) -> None:
        """Wait until underlying resource is created.

        Currently this should only be used on subclasses that implement the construct then
        `run` pattern because the underlying sync=False implementation will not update
        downstream resource noun object's _gca_resource until the entire invoked method is complete.

        Ex:
        job = CustomTrainingJob()
        job.run(sync=False, ...)
        job._wait_for_resource_creation()
        Raises:
            RuntimeError: If the resource has not been scheduled to be created.
        """

        # If the user calls this but didn't actually invoke an API to create
        if self._are_futures_done() and not getattr(self._gca_resource, "name", None):
            self._raise_future_exception()
            raise RuntimeError(
                f"{self.__class__.__name__} resource is not scheduled to be created."
            )

        while not getattr(self._gca_resource, "name", None):
            # breaks out of loop if creation has failed async
            if self._are_futures_done() and not getattr(
                self._gca_resource, "name", None
            ):
                self._raise_future_exception()

            time.sleep(1)

    def _assert_gca_resource_is_available(self) -> None:
        """Helper method to raise when accessing properties that do not exist.

        Overrides VertexAiResourceNoun to provide a more informative exception if
        resource creation has failed asynchronously.

        Raises:
            RuntimeError: When resource has not been created.
        """
        if not getattr(self._gca_resource, "name", None):
            raise RuntimeError(
                f"{self.__class__.__name__} resource has not been created."
                + (
                    f" Resource failed with: {self._exception}"
                    if self._exception
                    else ""
                )
            )


def get_annotation_class(annotation: type) -> type:
    """Helper method to retrieve type annotation.

    Args:
        annotation (type): Type hint
    """
    # typing.Optional
    if getattr(annotation, "__origin__", None) is Union:
        return annotation.__args__[0]

    return annotation


class DoneMixin(abc.ABC):
    """An abstract class for implementing a done method, indicating
    whether a job has completed.

    """

    @abc.abstractmethod
    def done(self) -> bool:
        """Method indicating whether a job has completed."""
        pass


class StatefulResource(DoneMixin):
    """Extends DoneMixin to check whether a job returning a stateful resource has compted."""

    @property
    @abc.abstractmethod
    def state(self):
        """The current state of the job."""
        pass

    @property
    @classmethod
    @abc.abstractmethod
    def _valid_done_states(cls):
        """A set() containing all job states associated with a completed job."""
        pass

    def done(self) -> bool:
        """Method indicating whether a job has completed.

        Returns:
            True if the job has completed.
        """
        if self.state in self._valid_done_states:
            return True

        return False


class VertexAiStatefulResource(VertexAiResourceNounWithFutureManager, StatefulResource):
    """Extends StatefulResource to include a check for self._gca_resource."""

    def done(self) -> bool:
        """Method indicating whether a job has completed.

        Returns:
            True if the job has completed.
        """
        if self._gca_resource and self._gca_resource.name:
            return super().done()

        return False


# PreviewClass type variable
PreviewClass = TypeVar("PreviewClass", bound=VertexAiResourceNoun)


class PreviewMixin(abc.ABC):
    """An abstract class for adding preview functionality to certain classes.
    A child class that inherits from both this Mixin and another parent
    class allows the child class to introduce preview features.
    """

    @classmethod
    @property
    @abc.abstractmethod
    def _preview_class(cls: Type[PreviewClass]) -> Type[PreviewClass]:
        """Class that is currently in preview or has a preview feature.
        Class must have `resource_name` and `credentials` attributes.
        """
        pass

    @property
    def preview(self) -> PreviewClass:
        """Exposes features available in preview for this class."""
        if not hasattr(self, "_preview_instance"):
            self._preview_instance = self._preview_class(
                self.resource_name, credentials=self.credentials
            )

        return self._preview_instance
