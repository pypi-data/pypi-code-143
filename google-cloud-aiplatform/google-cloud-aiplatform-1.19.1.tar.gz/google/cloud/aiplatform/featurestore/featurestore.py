# -*- coding: utf-8 -*-

# Copyright 2021 Google LLC
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

from typing import Dict, List, Optional, Sequence, Tuple, Union
import uuid

from google.auth import credentials as auth_credentials
from google.protobuf import field_mask_pb2

from google.cloud.aiplatform import base
from google.cloud.aiplatform.compat.types import (
    feature_selector as gca_feature_selector,
    featurestore as gca_featurestore,
    featurestore_service as gca_featurestore_service,
    io as gca_io,
)
from google.cloud.aiplatform import featurestore
from google.cloud.aiplatform import initializer
from google.cloud.aiplatform import utils
from google.cloud.aiplatform.utils import featurestore_utils, resource_manager_utils

from google.cloud import bigquery

_LOGGER = base.Logger(__name__)


class Featurestore(base.VertexAiResourceNounWithFutureManager):
    """Managed featurestore resource for Vertex AI."""

    client_class = utils.FeaturestoreClientWithOverride

    _resource_noun = "featurestores"
    _getter_method = "get_featurestore"
    _list_method = "list_featurestores"
    _delete_method = "delete_featurestore"
    _parse_resource_name_method = "parse_featurestore_path"
    _format_resource_name_method = "featurestore_path"

    @staticmethod
    def _resource_id_validator(resource_id: str):
        """Validates resource ID.

        Args:
            resource_id(str):
                The resource id to validate.
        """
        featurestore_utils.validate_id(resource_id)

    def __init__(
        self,
        featurestore_name: str,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
    ):
        """Retrieves an existing managed featurestore given a featurestore resource name or a featurestore ID.

        Example Usage:

            my_featurestore = aiplatform.Featurestore(
                featurestore_name='projects/123/locations/us-central1/featurestores/my_featurestore_id'
            )
            or
            my_featurestore = aiplatform.Featurestore(
                featurestore_name='my_featurestore_id'
            )

        Args:
            featurestore_name (str):
                Required. A fully-qualified featurestore resource name or a featurestore ID.
                Example: "projects/123/locations/us-central1/featurestores/my_featurestore_id"
                or "my_featurestore_id" when project and location are initialized or passed.
            project (str):
                Optional. Project to retrieve featurestore from. If not set, project
                set in aiplatform.init will be used.
            location (str):
                Optional. Location to retrieve featurestore from. If not set, location
                set in aiplatform.init will be used.
            credentials (auth_credentials.Credentials):
                Optional. Custom credentials to use to retrieve this Featurestore. Overrides
                credentials set in aiplatform.init.
        """

        super().__init__(
            project=project,
            location=location,
            credentials=credentials,
            resource_name=featurestore_name,
        )
        self._gca_resource = self._get_gca_resource(resource_name=featurestore_name)

    def get_entity_type(self, entity_type_id: str) -> "featurestore.EntityType":
        """Retrieves an existing managed entityType in this Featurestore.

        Args:
            entity_type_id (str):
                Required. The managed entityType resource ID in this Featurestore.
        Returns:
            featurestore.EntityType - The managed entityType resource object.
        """
        self.wait()
        return self._get_entity_type(entity_type_id=entity_type_id)

    def _get_entity_type(self, entity_type_id: str) -> "featurestore.EntityType":
        """Retrieves an existing managed entityType in this Featurestore.

        Args:
            entity_type_id (str):
                Required. The managed entityType resource ID in this Featurestore.
        Returns:
            featurestore.EntityType - The managed entityType resource object.
        """
        featurestore_name_components = self._parse_resource_name(self.resource_name)
        return featurestore.EntityType(
            entity_type_name=featurestore.EntityType._format_resource_name(
                project=featurestore_name_components["project"],
                location=featurestore_name_components["location"],
                featurestore=featurestore_name_components["featurestore"],
                entity_type=entity_type_id,
            )
        )

    def update(
        self,
        labels: Optional[Dict[str, str]] = None,
        request_metadata: Optional[Sequence[Tuple[str, str]]] = (),
        update_request_timeout: Optional[float] = None,
    ) -> "Featurestore":
        """Updates an existing managed featurestore resource.

        Example Usage:

            my_featurestore = aiplatform.Featurestore(
                featurestore_name='my_featurestore_id',
            )
            my_featurestore.update(
                labels={'update my key': 'update my value'},
            )

        Args:
            labels (Dict[str, str]):
                Optional. The labels with user-defined
                metadata to organize your Featurestores.
                Label keys and values can be no longer than 64
                characters (Unicode codepoints), can only
                contain lowercase letters, numeric characters,
                underscores and dashes. International characters
                are allowed.
                See https://goo.gl/xmQnxf for more information
                on and examples of labels. No more than 64 user
                labels can be associated with one Feature
                (System labels are excluded)."
                System reserved label keys are prefixed with
                "aiplatform.googleapis.com/" and are immutable.
            request_metadata (Sequence[Tuple[str, str]]):
                Optional. Strings which should be sent along with the request as metadata.
            update_request_timeout (float):
                Optional. The timeout for the update request in seconds.

        Returns:
            Featurestore - The updated featurestore resource object.
        """

        return self._update(
            labels=labels,
            request_metadata=request_metadata,
            update_request_timeout=update_request_timeout,
        )

    # TODO(b/206818784): Add enable_online_store and disable_online_store methods
    def update_online_store(
        self,
        fixed_node_count: int,
        request_metadata: Optional[Sequence[Tuple[str, str]]] = (),
        update_request_timeout: Optional[float] = None,
    ) -> "Featurestore":
        """Updates the online store of an existing managed featurestore resource.

        Example Usage:

            my_featurestore = aiplatform.Featurestore(
                featurestore_name='my_featurestore_id',
            )
            my_featurestore.update_online_store(
                fixed_node_count=2,
            )

        Args:
            fixed_node_count (int):
                Required. Config for online serving resources, can only update the node count to >= 1.
            request_metadata (Sequence[Tuple[str, str]]):
                Optional. Strings which should be sent along with the request as metadata.
            update_request_timeout (float):
                Optional. The timeout for the update request in seconds.

        Returns:
            Featurestore - The updated featurestore resource object.
        """
        return self._update(
            fixed_node_count=fixed_node_count,
            request_metadata=request_metadata,
            update_request_timeout=update_request_timeout,
        )

    def _update(
        self,
        labels: Optional[Dict[str, str]] = None,
        fixed_node_count: Optional[int] = None,
        request_metadata: Optional[Sequence[Tuple[str, str]]] = (),
        update_request_timeout: Optional[float] = None,
    ) -> "Featurestore":
        """Updates an existing managed featurestore resource.

        Args:
            labels (Dict[str, str]):
                Optional. The labels with user-defined
                metadata to organize your Featurestores.
                Label keys and values can be no longer than 64
                characters (Unicode codepoints), can only
                contain lowercase letters, numeric characters,
                underscores and dashes. International characters
                are allowed.
                See https://goo.gl/xmQnxf for more information
                on and examples of labels. No more than 64 user
                labels can be associated with one Feature
                (System labels are excluded)."
                System reserved label keys are prefixed with
                "aiplatform.googleapis.com/" and are immutable.
            fixed_node_count (int):
                Optional. Config for online serving resources, can only update the node count to >= 1.
            request_metadata (Sequence[Tuple[str, str]]):
                Optional. Strings which should be sent along with the request as metadata.
            update_request_timeout (float):
                Optional. The timeout for the update request in seconds.

        Returns:
            Featurestore - The updated featurestore resource object.
        """
        self.wait()
        update_mask = list()

        if labels:
            utils.validate_labels(labels)
            update_mask.append("labels")

        if fixed_node_count is not None:
            update_mask.append("online_serving_config.fixed_node_count")

        update_mask = field_mask_pb2.FieldMask(paths=update_mask)

        gapic_featurestore = gca_featurestore.Featurestore(
            name=self.resource_name,
            labels=labels,
            online_serving_config=gca_featurestore.Featurestore.OnlineServingConfig(
                fixed_node_count=fixed_node_count
            ),
        )

        _LOGGER.log_action_start_against_resource(
            "Updating",
            "featurestore",
            self,
        )

        update_featurestore_lro = self.api_client.update_featurestore(
            featurestore=gapic_featurestore,
            update_mask=update_mask,
            metadata=request_metadata,
            timeout=update_request_timeout,
        )

        _LOGGER.log_action_started_against_resource_with_lro(
            "Update", "featurestore", self.__class__, update_featurestore_lro
        )

        update_featurestore_lro.result()

        _LOGGER.log_action_completed_against_resource("featurestore", "updated", self)

        return self

    def list_entity_types(
        self,
        filter: Optional[str] = None,
        order_by: Optional[str] = None,
    ) -> List["featurestore.EntityType"]:
        """Lists existing managed entityType resources in this Featurestore.

        Example Usage:

            my_featurestore = aiplatform.Featurestore(
                featurestore_name='my_featurestore_id',
            )
            my_featurestore.list_entity_types()

        Args:
            filter (str):
                Optional. Lists the EntityTypes that match the filter expression. The
                following filters are supported:

                -  ``create_time``: Supports ``=``, ``!=``, ``<``, ``>``,
                   ``>=``, and ``<=`` comparisons. Values must be in RFC
                   3339 format.
                -  ``update_time``: Supports ``=``, ``!=``, ``<``, ``>``,
                   ``>=``, and ``<=`` comparisons. Values must be in RFC
                   3339 format.
                -  ``labels``: Supports key-value equality as well as key
                   presence.

                Examples:

                -  ``create_time > \"2020-01-31T15:30:00.000000Z\" OR update_time > \"2020-01-31T15:30:00.000000Z\"``
                   --> EntityTypes created or updated after
                   2020-01-31T15:30:00.000000Z.
                -  ``labels.active = yes AND labels.env = prod`` -->
                   EntityTypes having both (active: yes) and (env: prod)
                   labels.
                -  ``labels.env: *`` --> Any EntityType which has a label
                   with 'env' as the key.
            order_by (str):
                Optional. A comma-separated list of fields to order by, sorted in
                ascending order. Use "desc" after a field name for
                descending.

                Supported fields:

                -  ``entity_type_id``
                -  ``create_time``
                -  ``update_time``

        Returns:
            List[featurestore.EntityType] - A list of managed entityType resource objects.
        """
        self.wait()
        return featurestore.EntityType.list(
            featurestore_name=self.resource_name,
            filter=filter,
            order_by=order_by,
        )

    @base.optional_sync()
    def delete_entity_types(
        self,
        entity_type_ids: List[str],
        sync: bool = True,
        force: bool = False,
    ) -> None:
        """Deletes entity_type resources in this Featurestore given their entity_type IDs.
        WARNING: This deletion is permanent.

        Args:
            entity_type_ids (List[str]):
                Required. The list of entity_type IDs to be deleted.
            sync (bool):
                Optional. Whether to execute this deletion synchronously. If False, this method
                will be executed in concurrent Future and any downstream object will
                be immediately returned and synced when the Future has completed.
            force (bool):
                Optional. If force is set to True, all features in each entityType
                will be deleted prior to entityType deletion. Default is False.
        """
        entity_types = []
        for entity_type_id in entity_type_ids:
            entity_type = self._get_entity_type(entity_type_id=entity_type_id)
            entity_type.delete(force=force, sync=False)
            entity_types.append(entity_type)

        for entity_type in entity_types:
            entity_type.wait()

    @base.optional_sync()
    def delete(self, sync: bool = True, force: bool = False) -> None:
        """Deletes this Featurestore resource. If force is set to True,
        all entityTypes in this Featurestore will be deleted prior to featurestore deletion,
        and all features in each entityType will be deleted prior to each entityType deletion.

        WARNING: This deletion is permanent.

        Args:
            force (bool):
                If set to true, any EntityTypes and
                Features for this Featurestore will also
                be deleted. (Otherwise, the request will
                only work if the Featurestore has no
                EntityTypes.)
            sync (bool):
                Whether to execute this deletion synchronously. If False, this method
                will be executed in concurrent Future and any downstream object will
                be immediately returned and synced when the Future has completed.
        """
        _LOGGER.log_action_start_against_resource("Deleting", "", self)
        lro = getattr(self.api_client, self._delete_method)(
            name=self.resource_name, force=force
        )
        _LOGGER.log_action_started_against_resource_with_lro(
            "Delete", "", self.__class__, lro
        )
        lro.result()
        _LOGGER.log_action_completed_against_resource("deleted.", "", self)

    @classmethod
    @base.optional_sync()
    def create(
        cls,
        featurestore_id: str,
        online_store_fixed_node_count: Optional[int] = None,
        labels: Optional[Dict[str, str]] = None,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        request_metadata: Optional[Sequence[Tuple[str, str]]] = (),
        encryption_spec_key_name: Optional[str] = None,
        sync: bool = True,
        create_request_timeout: Optional[float] = None,
    ) -> "Featurestore":
        """Creates a Featurestore resource.

        Example Usage:

            my_featurestore = aiplatform.Featurestore.create(
                featurestore_id='my_featurestore_id',
            )

        Args:
            featurestore_id (str):
                Required. The ID to use for this Featurestore, which will
                become the final component of the Featurestore's resource
                name.

                This value may be up to 60 characters, and valid characters
                are ``[a-z0-9_]``. The first character cannot be a number.

                The value must be unique within the project and location.
            online_store_fixed_node_count (int):
                Optional. Config for online serving resources.
                When not specified, no fixed node count for online serving. The
                number of nodes will not scale automatically but
                can be scaled manually by providing different
                values when updating.
            labels (Dict[str, str]):
                Optional. The labels with user-defined
                metadata to organize your Featurestore.
                Label keys and values can be no longer than 64
                characters (Unicode codepoints), can only
                contain lowercase letters, numeric characters,
                underscores and dashes. International characters
                are allowed.
                See https://goo.gl/xmQnxf for more information
                on and examples of labels. No more than 64 user
                labels can be associated with one
                Featurestore(System labels are excluded)."
                System reserved label keys are prefixed with
                "aiplatform.googleapis.com/" and are immutable.
            project (str):
                Optional. Project to create EntityType in. If not set, project
                set in aiplatform.init will be used.
            location (str):
                Optional. Location to create EntityType in. If not set, location
                set in aiplatform.init will be used.
            credentials (auth_credentials.Credentials):
                Optional. Custom credentials to use to create EntityTypes. Overrides
                credentials set in aiplatform.init.
            request_metadata (Sequence[Tuple[str, str]]):
                Optional. Strings which should be sent along with the request as metadata.
            request_metadata (Sequence[Tuple[str, str]]):
                Optional. Strings which should be sent along with the request as metadata.
            encryption_spec (str):
                Optional. Customer-managed encryption key
                spec for data storage. If set, both of the
                online and offline data storage will be secured
                by this key.
            sync (bool):
                Optional. Whether to execute this creation synchronously. If False, this method
                will be executed in concurrent Future and any downstream object will
                be immediately returned and synced when the Future has completed.
            create_request_timeout (float):
                Optional. The timeout for the create request in seconds.

        Returns:
            Featurestore - Featurestore resource object

        """
        gapic_featurestore = gca_featurestore.Featurestore(
            online_serving_config=gca_featurestore.Featurestore.OnlineServingConfig(
                fixed_node_count=online_store_fixed_node_count
            )
        )

        if labels:
            utils.validate_labels(labels)
            gapic_featurestore.labels = labels

        if encryption_spec_key_name:
            gapic_featurestore.encryption_spec = (
                initializer.global_config.get_encryption_spec(
                    encryption_spec_key_name=encryption_spec_key_name
                )
            )

        api_client = cls._instantiate_client(location=location, credentials=credentials)

        created_featurestore_lro = api_client.create_featurestore(
            parent=initializer.global_config.common_location_path(
                project=project, location=location
            ),
            featurestore=gapic_featurestore,
            featurestore_id=featurestore_id,
            metadata=request_metadata,
            timeout=create_request_timeout,
        )

        _LOGGER.log_create_with_lro(cls, created_featurestore_lro)

        created_featurestore = created_featurestore_lro.result()

        _LOGGER.log_create_complete(cls, created_featurestore, "featurestore")

        featurestore_obj = cls(
            featurestore_name=created_featurestore.name,
            project=project,
            location=location,
            credentials=credentials,
        )

        return featurestore_obj

    def create_entity_type(
        self,
        entity_type_id: str,
        description: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        request_metadata: Optional[Sequence[Tuple[str, str]]] = (),
        sync: bool = True,
        create_request_timeout: Optional[float] = None,
    ) -> "featurestore.EntityType":
        """Creates an EntityType resource in this Featurestore.

        Example Usage:

            my_featurestore = aiplatform.Featurestore.create(
                featurestore_id='my_featurestore_id'
            )
            my_entity_type = my_featurestore.create_entity_type(
                entity_type_id='my_entity_type_id',
            )

        Args:
            entity_type_id (str):
                Required. The ID to use for the EntityType, which will
                become the final component of the EntityType's resource
                name.

                This value may be up to 60 characters, and valid characters
                are ``[a-z0-9_]``. The first character cannot be a number.

                The value must be unique within a featurestore.
            description (str):
                Optional. Description of the EntityType.
            labels (Dict[str, str]):
                Optional. The labels with user-defined
                metadata to organize your EntityTypes.
                Label keys and values can be no longer than 64
                characters (Unicode codepoints), can only
                contain lowercase letters, numeric characters,
                underscores and dashes. International characters
                are allowed.
                See https://goo.gl/xmQnxf for more information
                on and examples of labels. No more than 64 user
                labels can be associated with one EntityType
                (System labels are excluded)."
                System reserved label keys are prefixed with
                "aiplatform.googleapis.com/" and are immutable.
            request_metadata (Sequence[Tuple[str, str]]):
                Optional. Strings which should be sent along with the request as metadata.
            create_request_timeout (float):
                Optional. The timeout for the create request in seconds.
            sync (bool):
                Optional. Whether to execute this creation synchronously. If False, this method
                will be executed in concurrent Future and any downstream object will
                be immediately returned and synced when the Future has completed.

        Returns:
            featurestore.EntityType - EntityType resource object

        """
        self.wait()
        return featurestore.EntityType.create(
            entity_type_id=entity_type_id,
            featurestore_name=self.resource_name,
            description=description,
            labels=labels,
            request_metadata=request_metadata,
            sync=sync,
            create_request_timeout=create_request_timeout,
        )

    def _batch_read_feature_values(
        self,
        batch_read_feature_values_request: gca_featurestore_service.BatchReadFeatureValuesRequest,
        request_metadata: Optional[Sequence[Tuple[str, str]]] = (),
        serve_request_timeout: Optional[float] = None,
    ) -> "Featurestore":
        """Batch read Feature values from the Featurestore to a destination storage.

        Args:
            batch_read_feature_values_request (gca_featurestore_service.BatchReadFeatureValuesRequest):
                Required. Request of batch read feature values.
            request_metadata (Sequence[Tuple[str, str]]):
                Optional. Strings which should be sent along with the request as metadata.
            serve_request_timeout (float):
                Optional. The timeout for the serve request in seconds.

        Returns:
            Featurestore: The featurestore resource object batch read feature values from.
        """

        _LOGGER.log_action_start_against_resource(
            "Serving",
            "feature values",
            self,
        )

        batch_read_lro = self.api_client.batch_read_feature_values(
            request=batch_read_feature_values_request,
            metadata=request_metadata,
            timeout=serve_request_timeout,
        )

        _LOGGER.log_action_started_against_resource_with_lro(
            "Serve", "feature values", self.__class__, batch_read_lro
        )

        batch_read_lro.result()

        _LOGGER.log_action_completed_against_resource("feature values", "served", self)

        return self

    @staticmethod
    def _validate_and_get_read_instances(
        read_instances_uri: str,
    ) -> Union[gca_io.BigQuerySource, gca_io.CsvSource]:
        """Gets read_instances

        Args:
            read_instances_uri (str):
                Required. Read_instances_uri can be either BigQuery URI to an input table,
                or Google Cloud Storage URI to a csv file.

        Returns:
            Union[gca_io.BigQuerySource, gca_io.CsvSource]:
                BigQuery source or Csv source for read instances. The Csv source contains exactly 1 URI.

        Raises:
            ValueError if read_instances_uri does not start with 'bq://' or 'gs://'.
        """
        if not (
            read_instances_uri.startswith("bq://")
            or read_instances_uri.startswith("gs://")
        ):
            raise ValueError(
                "The read_instances_uri should be a single uri starts with either 'bq://' or 'gs://'."
            )

        if read_instances_uri.startswith("bq://"):
            return gca_io.BigQuerySource(input_uri=read_instances_uri)
        if read_instances_uri.startswith("gs://"):
            return gca_io.CsvSource(
                gcs_source=gca_io.GcsSource(uris=[read_instances_uri])
            )

    def _validate_and_get_batch_read_feature_values_request(
        self,
        featurestore_name: str,
        serving_feature_ids: Dict[str, List[str]],
        destination: Union[
            gca_io.BigQueryDestination,
            gca_io.CsvDestination,
            gca_io.TFRecordDestination,
        ],
        read_instances: Union[gca_io.BigQuerySource, gca_io.CsvSource],
        pass_through_fields: Optional[List[str]] = None,
        feature_destination_fields: Optional[Dict[str, str]] = None,
    ) -> gca_featurestore_service.BatchReadFeatureValuesRequest:
        """Validates and gets batch_read_feature_values_request

        Args:
            featurestore_name (str):
                Required. A fully-qualified featurestore resource name.
            serving_feature_ids (Dict[str, List[str]]):
                Required. A user defined dictionary to define the entity_types and their features for batch serve/read.
                The keys of the dictionary are the serving entity_type ids and
                the values are lists of serving feature ids in each entity_type.

                Example:
                    serving_feature_ids = {
                        'my_entity_type_id_1': ['feature_id_1_1', 'feature_id_1_2'],
                        'my_entity_type_id_2': ['feature_id_2_1', 'feature_id_2_2'],
                    }

            destination (Union[gca_io.BigQueryDestination, gca_io.CsvDestination, gca_io.TFRecordDestination]):
                Required. BigQuery destination, Csv destination or TFRecord destination.
            read_instances (Union[gca_io.BigQuerySource, gca_io.CsvSource]):
                Required. BigQuery source or Csv source for read instances.
                The Csv source must contain exactly 1 URI.
            pass_through_fields (List[str]):
                Optional. When not empty, the specified fields in the
                read_instances source will be joined as-is in the output,
                in addition to those fields from the Featurestore Entity.

                For BigQuery source, the type of the pass-through values
                will be automatically inferred. For CSV source, the
                pass-through values will be passed as opaque bytes.
            feature_destination_fields (Dict[str, str]):
                Optional. A user defined dictionary to map a feature's fully qualified resource name to
                its destination field name. If the destination field name is not defined,
                the feature ID will be used as its destination field name.

                Example:
                    feature_destination_fields = {
                        'projects/123/locations/us-central1/featurestores/fs_id/entityTypes/et_id1/features/f_id11': 'foo',
                        'projects/123/locations/us-central1/featurestores/fs_id/entityTypes/et_id2/features/f_id22': 'bar',
                     }

        Returns:
            gca_featurestore_service.BatchReadFeatureValuesRequest: batch read feature values request
        """
        featurestore_name_components = self._parse_resource_name(featurestore_name)

        feature_destination_fields = feature_destination_fields or {}

        entity_type_specs = []
        for entity_type_id, feature_ids in serving_feature_ids.items():
            destination_feature_settings = []
            for feature_id in feature_ids:
                feature_resource_name = featurestore.Feature._format_resource_name(
                    project=featurestore_name_components["project"],
                    location=featurestore_name_components["location"],
                    featurestore=featurestore_name_components["featurestore"],
                    entity_type=entity_type_id,
                    feature=feature_id,
                )

                feature_destination_field = feature_destination_fields.get(
                    feature_resource_name
                )
                if feature_destination_field:
                    destination_feature_setting_proto = (
                        gca_featurestore_service.DestinationFeatureSetting(
                            feature_id=feature_id,
                            destination_field=feature_destination_field,
                        )
                    )
                    destination_feature_settings.append(
                        destination_feature_setting_proto
                    )

            entity_type_spec = (
                gca_featurestore_service.BatchReadFeatureValuesRequest.EntityTypeSpec(
                    entity_type_id=entity_type_id,
                    feature_selector=gca_feature_selector.FeatureSelector(
                        id_matcher=gca_feature_selector.IdMatcher(ids=feature_ids)
                    ),
                    settings=destination_feature_settings or None,
                )
            )
            entity_type_specs.append(entity_type_spec)

        batch_read_feature_values_request = (
            gca_featurestore_service.BatchReadFeatureValuesRequest(
                featurestore=featurestore_name,
                entity_type_specs=entity_type_specs,
            )
        )

        if isinstance(destination, gca_io.BigQueryDestination):
            batch_read_feature_values_request.destination = (
                gca_featurestore_service.FeatureValueDestination(
                    bigquery_destination=destination
                )
            )
        elif isinstance(destination, gca_io.CsvDestination):
            batch_read_feature_values_request.destination = (
                gca_featurestore_service.FeatureValueDestination(
                    csv_destination=destination
                )
            )
        elif isinstance(destination, gca_io.TFRecordDestination):
            batch_read_feature_values_request.destination = (
                gca_featurestore_service.FeatureValueDestination(
                    tfrecord_destination=destination
                )
            )

        if isinstance(read_instances, gca_io.BigQuerySource):
            batch_read_feature_values_request.bigquery_read_instances = read_instances
        elif isinstance(read_instances, gca_io.CsvSource):
            batch_read_feature_values_request.csv_read_instances = read_instances

        if pass_through_fields is not None:
            batch_read_feature_values_request.pass_through_fields = [
                gca_featurestore_service.BatchReadFeatureValuesRequest.PassThroughField(
                    field_name=pass_through_field
                )
                for pass_through_field in pass_through_fields
            ]

        return batch_read_feature_values_request

    @base.optional_sync(return_input_arg="self")
    def batch_serve_to_bq(
        self,
        bq_destination_output_uri: str,
        serving_feature_ids: Dict[str, List[str]],
        read_instances_uri: str,
        pass_through_fields: Optional[List[str]] = None,
        feature_destination_fields: Optional[Dict[str, str]] = None,
        request_metadata: Optional[Sequence[Tuple[str, str]]] = (),
        serve_request_timeout: Optional[float] = None,
        sync: bool = True,
    ) -> "Featurestore":
        """Batch serves feature values to BigQuery destination

        Args:
            bq_destination_output_uri (str):
                Required. BigQuery URI to the detination table.

                Example:
                    'bq://project.dataset.table_name'

                It requires an existing BigQuery destination Dataset, under the same project as the Featurestore.

            serving_feature_ids (Dict[str, List[str]]):
                Required. A user defined dictionary to define the entity_types and their features for batch serve/read.
                The keys of the dictionary are the serving entity_type ids and
                the values are lists of serving feature ids in each entity_type.

                Example:
                    serving_feature_ids = {
                        'my_entity_type_id_1': ['feature_id_1_1', 'feature_id_1_2'],
                        'my_entity_type_id_2': ['feature_id_2_1', 'feature_id_2_2'],
                    }

            read_instances_uri (str):
                Required. Read_instances_uri can be either BigQuery URI to an input table,
                or Google Cloud Storage URI to a csv file.

                Example:
                    'bq://project.dataset.table_name'
                    or
                    "gs://my_bucket/my_file.csv"

                Each read instance should consist of exactly one read timestamp
                and one or more entity IDs identifying entities of the
                corresponding EntityTypes whose Features are requested.

                Each output instance contains Feature values of requested
                entities concatenated together as of the read time.

                An example read instance may be
                ``foo_entity_id, bar_entity_id, 2020-01-01T10:00:00.123Z``.

                An example output instance may be
                ``foo_entity_id, bar_entity_id, 2020-01-01T10:00:00.123Z, foo_entity_feature1_value, bar_entity_feature2_value``.

                Timestamp in each read instance must be millisecond-aligned.

                The columns can be in any order.

                Values in the timestamp column must use the RFC 3339 format,
                e.g. ``2012-07-30T10:43:17.123Z``.

            pass_through_fields (List[str]):
                Optional. When not empty, the specified fields in the
                read_instances source will be joined as-is in the output,
                in addition to those fields from the Featurestore Entity.

                For BigQuery source, the type of the pass-through values
                will be automatically inferred. For CSV source, the
                pass-through values will be passed as opaque bytes.

            feature_destination_fields (Dict[str, str]):
                Optional. A user defined dictionary to map a feature's fully qualified resource name to
                its destination field name. If the destination field name is not defined,
                the feature ID will be used as its destination field name.

                Example:
                    feature_destination_fields = {
                        'projects/123/locations/us-central1/featurestores/fs_id/entityTypes/et_id1/features/f_id11': 'foo',
                        'projects/123/locations/us-central1/featurestores/fs_id/entityTypes/et_id2/features/f_id22': 'bar',
                     }
            serve_request_timeout (float):
                Optional. The timeout for the serve request in seconds.
        Returns:
            Featurestore: The featurestore resource object batch read feature values from.

        Raises:
            NotFound: if the BigQuery destination Dataset does not exist.
            FailedPrecondition: if the BigQuery destination Dataset/Table is in a different project.
        """
        read_instances = self._validate_and_get_read_instances(read_instances_uri)

        batch_read_feature_values_request = (
            self._validate_and_get_batch_read_feature_values_request(
                featurestore_name=self.resource_name,
                serving_feature_ids=serving_feature_ids,
                destination=gca_io.BigQueryDestination(
                    output_uri=bq_destination_output_uri
                ),
                feature_destination_fields=feature_destination_fields,
                read_instances=read_instances,
                pass_through_fields=pass_through_fields,
            )
        )

        return self._batch_read_feature_values(
            batch_read_feature_values_request=batch_read_feature_values_request,
            request_metadata=request_metadata,
            serve_request_timeout=serve_request_timeout,
        )

    @base.optional_sync(return_input_arg="self")
    def batch_serve_to_gcs(
        self,
        gcs_destination_output_uri_prefix: str,
        gcs_destination_type: str,
        serving_feature_ids: Dict[str, List[str]],
        read_instances_uri: str,
        pass_through_fields: Optional[List[str]] = None,
        feature_destination_fields: Optional[Dict[str, str]] = None,
        request_metadata: Optional[Sequence[Tuple[str, str]]] = (),
        sync: bool = True,
        serve_request_timeout: Optional[float] = None,
    ) -> "Featurestore":
        """Batch serves feature values to GCS destination

        Args:
            gcs_destination_output_uri_prefix (str):
                Required. Google Cloud Storage URI to output
                directory. If the uri doesn't end with '/', a
                '/' will be automatically appended. The
                directory is created if it doesn't exist.

                Example:
                    "gs://bucket/path/to/prefix"

            gcs_destination_type (str):
                Required. The type of the destination files(s),
                the value of gcs_destination_type can only be either `csv`, or `tfrecord`.

                For CSV format. Array Feature value types are not allowed in CSV format.

                For TFRecord format.

                Below are the mapping from Feature value type in
                Featurestore to Feature value type in TFRecord:

                ::

                    Value type in Featurestore                 | Value type in TFRecord
                    DOUBLE, DOUBLE_ARRAY                       | FLOAT_LIST
                    INT64, INT64_ARRAY                         | INT64_LIST
                    STRING, STRING_ARRAY, BYTES                | BYTES_LIST
                    true -> byte_string("true"), false -> byte_string("false")
                    BOOL, BOOL_ARRAY (true, false)             | BYTES_LIST

            serving_feature_ids (Dict[str, List[str]]):
                Required. A user defined dictionary to define the entity_types and their features for batch serve/read.
                The keys of the dictionary are the serving entity_type ids and
                the values are lists of serving feature ids in each entity_type.

                Example:
                    serving_feature_ids = {
                        'my_entity_type_id_1': ['feature_id_1_1', 'feature_id_1_2'],
                        'my_entity_type_id_2': ['feature_id_2_1', 'feature_id_2_2'],
                    }

            read_instances_uri (str):
                Required. Read_instances_uri can be either BigQuery URI to an input table,
                or Google Cloud Storage URI to a csv file.

                Example:
                    'bq://project.dataset.table_name'
                    or
                    "gs://my_bucket/my_file.csv"

                Each read instance should consist of exactly one read timestamp
                and one or more entity IDs identifying entities of the
                corresponding EntityTypes whose Features are requested.

                Each output instance contains Feature values of requested
                entities concatenated together as of the read time.

                An example read instance may be
                ``foo_entity_id, bar_entity_id, 2020-01-01T10:00:00.123Z``.

                An example output instance may be
                ``foo_entity_id, bar_entity_id, 2020-01-01T10:00:00.123Z, foo_entity_feature1_value, bar_entity_feature2_value``.

                Timestamp in each read instance must be millisecond-aligned.

                The columns can be in any order.

                Values in the timestamp column must use the RFC 3339 format,
                e.g. ``2012-07-30T10:43:17.123Z``.

            pass_through_fields (List[str]):
                Optional. When not empty, the specified fields in the
                read_instances source will be joined as-is in the output,
                in addition to those fields from the Featurestore Entity.

                For BigQuery source, the type of the pass-through values
                will be automatically inferred. For CSV source, the
                pass-through values will be passed as opaque bytes.

            feature_destination_fields (Dict[str, str]):
                Optional. A user defined dictionary to map a feature's fully qualified resource name to
                its destination field name. If the destination field name is not defined,
                the feature ID will be used as its destination field name.

                Example:
                    feature_destination_fields = {
                        'projects/123/locations/us-central1/featurestores/fs_id/entityTypes/et_id1/features/f_id11': 'foo',
                        'projects/123/locations/us-central1/featurestores/fs_id/entityTypes/et_id2/features/f_id22': 'bar',
                     }
            serve_request_timeout (float):
                Optional. The timeout for the serve request in seconds.

        Returns:
            Featurestore: The featurestore resource object batch read feature values from.

        Raises:
            ValueError if gcs_destination_type is not supported.

        """
        destination = None
        if gcs_destination_type not in featurestore_utils.GCS_DESTINATION_TYPE:
            raise ValueError(
                "Only %s are supported gcs_destination_type, not `%s`. "
                % (
                    "`" + "`, `".join(featurestore_utils.GCS_DESTINATION_TYPE) + "`",
                    gcs_destination_type,
                )
            )

        gcs_destination = gca_io.GcsDestination(
            output_uri_prefix=gcs_destination_output_uri_prefix
        )
        if gcs_destination_type == "csv":
            destination = gca_io.CsvDestination(gcs_destination=gcs_destination)
        if gcs_destination_type == "tfrecord":
            destination = gca_io.TFRecordDestination(gcs_destination=gcs_destination)

        read_instances = self._validate_and_get_read_instances(read_instances_uri)

        batch_read_feature_values_request = (
            self._validate_and_get_batch_read_feature_values_request(
                featurestore_name=self.resource_name,
                serving_feature_ids=serving_feature_ids,
                destination=destination,
                feature_destination_fields=feature_destination_fields,
                read_instances=read_instances,
                pass_through_fields=pass_through_fields,
            )
        )

        return self._batch_read_feature_values(
            batch_read_feature_values_request=batch_read_feature_values_request,
            request_metadata=request_metadata,
            serve_request_timeout=serve_request_timeout,
        )

    def batch_serve_to_df(
        self,
        serving_feature_ids: Dict[str, List[str]],
        read_instances_df: "pd.DataFrame",  # noqa: F821 - skip check for undefined name 'pd'
        pass_through_fields: Optional[List[str]] = None,
        feature_destination_fields: Optional[Dict[str, str]] = None,
        request_metadata: Optional[Sequence[Tuple[str, str]]] = (),
        serve_request_timeout: Optional[float] = None,
        bq_dataset_id: Optional[str] = None,
    ) -> "pd.DataFrame":  # noqa: F821 - skip check for undefined name 'pd'
        """Batch serves feature values to pandas DataFrame

        Note:
            Calling this method will automatically create and delete a temporary
            bigquery dataset in the same GCP project, which will be used
            as the intermediary storage for batch serve feature values
            from featurestore to dataframe.

        Args:
            serving_feature_ids (Dict[str, List[str]]):
                Required. A user defined dictionary to define the entity_types and their features for batch serve/read.
                The keys of the dictionary are the serving entity_type ids and
                the values are lists of serving feature ids in each entity_type.

                Example:
                    serving_feature_ids = {
                        'my_entity_type_id_1': ['feature_id_1_1', 'feature_id_1_2'],
                        'my_entity_type_id_2': ['feature_id_2_1', 'feature_id_2_2'],
                    }

            read_instances_df (pd.DataFrame):
                Required. Read_instances_df is a pandas DataFrame containing the read instances.

                Each read instance should consist of exactly one read timestamp
                and one or more entity IDs identifying entities of the
                corresponding EntityTypes whose Features are requested.

                Each output instance contains Feature values of requested
                entities concatenated together as of the read time.

                An example read_instances_df may be
                    pd.DataFrame(
                        data=[
                            {
                                "my_entity_type_id_1": "my_entity_type_id_1_entity_1",
                                "my_entity_type_id_2": "my_entity_type_id_2_entity_1",
                                "timestamp": "2020-01-01T10:00:00.123Z"
                        ],
                    )

                An example batch_serve_output_df may be
                    pd.DataFrame(
                        data=[
                            {
                                "my_entity_type_id_1": "my_entity_type_id_1_entity_1",
                                "my_entity_type_id_2": "my_entity_type_id_2_entity_1",
                                "foo": "feature_id_1_1_feature_value",
                                "feature_id_1_2": "feature_id_1_2_feature_value",
                                "feature_id_2_1": "feature_id_2_1_feature_value",
                                "bar": "feature_id_2_2_feature_value",
                                "timestamp": "2020-01-01T10:00:00.123Z"
                        ],
                    )

                Timestamp in each read instance must be millisecond-aligned.

                The columns can be in any order.

                Values in the timestamp column must use the RFC 3339 format,
                e.g. ``2012-07-30T10:43:17.123Z``.

            pass_through_fields (List[str]):
                Optional. When not empty, the specified fields in the
                read_instances source will be joined as-is in the output,
                in addition to those fields from the Featurestore Entity.

                For BigQuery source, the type of the pass-through values
                will be automatically inferred. For CSV source, the
                pass-through values will be passed as opaque bytes.

            feature_destination_fields (Dict[str, str]):
                Optional. A user defined dictionary to map a feature's fully qualified resource name to
                its destination field name. If the destination field name is not defined,
                the feature ID will be used as its destination field name.

                Example:
                    feature_destination_fields = {
                        'projects/123/locations/us-central1/featurestores/fs_id/entityTypes/et_id1/features/f_id11': 'foo',
                        'projects/123/locations/us-central1/featurestores/fs_id/entityTypes/et_id2/features/f_id22': 'bar',
                     }
            serve_request_timeout (float):
                Optional. The timeout for the serve request in seconds.

            bq_dataset_id (str):
                Optional. The full dataset ID for the BigQuery dataset to use
                for temporarily staging data. If specified, caller must have
                `bigquery.tables.create` permissions for Dataset.

        Returns:
            pd.DataFrame: The pandas DataFrame containing feature values from batch serving.

        """
        try:
            from google.cloud import bigquery_storage
        except ImportError:
            raise ImportError(
                f"Google-Cloud-Bigquery-Storage is not installed. Please install google-cloud-bigquery-storage to use "
                f"{self.batch_serve_to_df.__name__}"
            )

        try:
            import pyarrow  # noqa: F401 - skip check for 'pyarrow' which is required when using 'google.cloud.bigquery'
        except ImportError:
            raise ImportError(
                f"Pyarrow is not installed. Please install pyarrow to use "
                f"{self.batch_serve_to_df.__name__}"
            )

        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                f"Pandas is not installed. Please install pandas to use "
                f"{self.batch_serve_to_df.__name__}"
            )

        bigquery_client = bigquery.Client(
            project=self.project, credentials=self.credentials
        )

        self.wait()
        featurestore_name_components = self._parse_resource_name(self.resource_name)

        # if user didn't specify BigQuery dataset, create an ephemeral one
        if bq_dataset_id is None:
            temp_bq_full_dataset_id = self._get_ephemeral_bq_full_dataset_id(
                featurestore_name_components["featurestore"],
                featurestore_name_components["project"],
            )
            temp_bq_dataset = self._create_ephemeral_bq_dataset(
                bigquery_client, temp_bq_full_dataset_id
            )
            temp_bq_batch_serve_table_name = "batch_serve"
            temp_bq_read_instances_table_name = "read_instances"

        # if user specified BigQuery dataset, create ephemeral tables
        else:
            temp_bq_full_dataset_id = bq_dataset_id
            temp_bq_dataset = bigquery.Dataset(dataset_ref=temp_bq_full_dataset_id)
            temp_bq_batch_serve_table_name = f"tmp_batch_serve_{uuid.uuid4()}".replace(
                "-", "_"
            )
            temp_bq_read_instances_table_name = (
                f"tmp_read_instances_{uuid.uuid4()}".replace("-", "_")
            )

        temp_bq_batch_serve_table_id = (
            f"{temp_bq_full_dataset_id}.{temp_bq_batch_serve_table_name}"
        )

        temp_bq_read_instances_table_id = (
            f"{temp_bq_full_dataset_id}.{temp_bq_read_instances_table_name}"
        )

        try:

            job = bigquery_client.load_table_from_dataframe(
                dataframe=read_instances_df,
                destination=temp_bq_read_instances_table_id,
            )
            job.result()

            self.batch_serve_to_bq(
                bq_destination_output_uri=f"bq://{temp_bq_batch_serve_table_id}",
                serving_feature_ids=serving_feature_ids,
                read_instances_uri=f"bq://{temp_bq_read_instances_table_id}",
                pass_through_fields=pass_through_fields,
                feature_destination_fields=feature_destination_fields,
                request_metadata=request_metadata,
                serve_request_timeout=serve_request_timeout,
            )

            bigquery_storage_read_client = bigquery_storage.BigQueryReadClient(
                credentials=self.credentials
            )
            read_session_proto = bigquery_storage_read_client.create_read_session(
                parent=f"projects/{self.project}",
                read_session=bigquery_storage.types.ReadSession(
                    table="projects/{project}/datasets/{dataset}/tables/{table}".format(
                        project=self.project,
                        dataset=temp_bq_dataset.dataset_id,
                        table=temp_bq_batch_serve_table_name,
                    ),
                    data_format=bigquery_storage.types.DataFormat.ARROW,
                ),
            )

            frames = []
            for stream in read_session_proto.streams:
                reader = bigquery_storage_read_client.read_rows(stream.name)
                for message in reader.rows().pages:
                    frames.append(message.to_dataframe())

        finally:
            # clean up: if user didn't specify dataset, delete ephemeral dataset
            if bq_dataset_id is None:
                bigquery_client.delete_dataset(
                    dataset=temp_bq_dataset.dataset_id,
                    delete_contents=True,
                )

            # clean up: if user specified BigQuery dataset, delete ephemeral tables
            else:
                bigquery_client.delete_table(temp_bq_batch_serve_table_id)
                bigquery_client.delete_table(temp_bq_read_instances_table_id)

        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(frames)

    def _get_ephemeral_bq_full_dataset_id(
        self, featurestore_id: str, project_number: str
    ) -> str:
        """Helper method to generate an id for an ephemeral dataset in BigQuery
        used to temporarily stage data.

        Args:
            featurestore_id (str):
                Required. The ID to use for this featurestore.
            project_number (str):
                Required. Project to retrieve featurestore from.
        Returns:
            str - full BigQuery dataset ID
        """
        temp_bq_dataset_name = f"temp_{featurestore_id}_{uuid.uuid4()}".replace(
            "-", "_"
        )

        project_id = resource_manager_utils.get_project_id(
            project_number=project_number,
            credentials=self.credentials,
        )

        return f"{project_id}.{temp_bq_dataset_name}"[:1024]

    def _create_ephemeral_bq_dataset(
        self, bigquery_client: bigquery.Client, dataset_id: str
    ) -> "bigquery.Dataset":
        """Helper method to create an ephemeral dataset in BigQuery used to
        temporarily stage data.

        Args:
            bigquery_client (bigquery.Client):
                Required. BigQuery client to use to generate the BigQuery dataset.
            dataset_id (str):
                Required. Identifier to use for the BigQuery dataset.
        Returns:
            bigquery.Dataset - new BigQuery dataset used to temporarily stage data
        """
        temp_bq_dataset = bigquery.Dataset(dataset_ref=dataset_id)
        temp_bq_dataset.location = self.location

        return bigquery_client.create_dataset(temp_bq_dataset)
