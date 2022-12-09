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
import proto  # type: ignore

from google.cloud.aiplatform_v1.types import deployed_index_ref
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.aiplatform.v1",
    manifest={
        "Index",
        "IndexDatapoint",
        "IndexStats",
    },
)


class Index(proto.Message):
    r"""A representation of a collection of database items organized
    in a way that allows for approximate nearest neighbor (a.k.a
    ANN) algorithms search.

    Attributes:
        name (str):
            Output only. The resource name of the Index.
        display_name (str):
            Required. The display name of the Index.
            The name can be up to 128 characters long and
            can consist of any UTF-8 characters.
        description (str):
            The description of the Index.
        metadata_schema_uri (str):
            Immutable. Points to a YAML file stored on Google Cloud
            Storage describing additional information about the Index,
            that is specific to it. Unset if the Index does not have any
            additional information. The schema is defined as an OpenAPI
            3.0.2 `Schema
            Object <https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.2.md#schemaObject>`__.
            Note: The URI given on output will be immutable and probably
            different, including the URI scheme, than the one given on
            input. The output URI will point to a location where the
            user only has a read access.
        metadata (google.protobuf.struct_pb2.Value):
            An additional information about the Index; the schema of the
            metadata can be found in
            [metadata_schema][google.cloud.aiplatform.v1.Index.metadata_schema_uri].
        deployed_indexes (Sequence[google.cloud.aiplatform_v1.types.DeployedIndexRef]):
            Output only. The pointers to DeployedIndexes
            created from this Index. An Index can be only
            deleted if all its DeployedIndexes had been
            undeployed first.
        etag (str):
            Used to perform consistent read-modify-write
            updates. If not set, a blind "overwrite" update
            happens.
        labels (Mapping[str, str]):
            The labels with user-defined metadata to
            organize your Indexes.
            Label keys and values can be no longer than 64
            characters (Unicode codepoints), can only
            contain lowercase letters, numeric characters,
            underscores and dashes. International characters
            are allowed.
            See https://goo.gl/xmQnxf for more information
            and examples of labels.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this Index was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this Index was most recently
            updated. This also includes any update to the contents of
            the Index. Note that Operations working on this Index may
            have their
            [Operations.metadata.generic_metadata.update_time]
            [google.cloud.aiplatform.v1.GenericOperationMetadata.update_time]
            a little after the value of this timestamp, yet that does
            not mean their results are not already reflected in the
            Index. Result of any successfully completed Operation on the
            Index is reflected in it.
        index_stats (google.cloud.aiplatform_v1.types.IndexStats):
            Output only. Stats of the index resource.
        index_update_method (google.cloud.aiplatform_v1.types.Index.IndexUpdateMethod):
            Immutable. The update method to use with this Index. If not
            set, BATCH_UPDATE will be used by default.
    """

    class IndexUpdateMethod(proto.Enum):
        r"""The update method of an Index."""
        INDEX_UPDATE_METHOD_UNSPECIFIED = 0
        BATCH_UPDATE = 1
        STREAM_UPDATE = 2

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name = proto.Field(
        proto.STRING,
        number=2,
    )
    description = proto.Field(
        proto.STRING,
        number=3,
    )
    metadata_schema_uri = proto.Field(
        proto.STRING,
        number=4,
    )
    metadata = proto.Field(
        proto.MESSAGE,
        number=6,
        message=struct_pb2.Value,
    )
    deployed_indexes = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message=deployed_index_ref.DeployedIndexRef,
    )
    etag = proto.Field(
        proto.STRING,
        number=8,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=11,
        message=timestamp_pb2.Timestamp,
    )
    index_stats = proto.Field(
        proto.MESSAGE,
        number=14,
        message="IndexStats",
    )
    index_update_method = proto.Field(
        proto.ENUM,
        number=16,
        enum=IndexUpdateMethod,
    )


class IndexDatapoint(proto.Message):
    r"""A datapoint of Index.

    Attributes:
        datapoint_id (str):
            Required. Unique identifier of the datapoint.
        feature_vector (Sequence[float]):
            Required. Feature embedding vector. An array of numbers with
            the length of [NearestNeighborSearchConfig.dimensions].
        restricts (Sequence[google.cloud.aiplatform_v1.types.IndexDatapoint.Restriction]):
            Optional. List of Restrict of the datapoint,
            used to perform "restricted searches" where
            boolean rule are used to filter the subset of
            the database eligible for matching.
            See:
            https://cloud.google.com/vertex-ai/docs/matching-engine/filtering
        crowding_tag (google.cloud.aiplatform_v1.types.IndexDatapoint.CrowdingTag):
            Optional. CrowdingTag of the datapoint, the
            number of neighbors to return in each crowding
            can be configured during query.
    """

    class Restriction(proto.Message):
        r"""Restriction of a datapoint which describe its
        attributes(tokens) from each of several attribute
        categories(namespaces).

        Attributes:
            namespace (str):
                The namespace of this restriction. eg: color.
            allow_list (Sequence[str]):
                The attributes to allow in this namespace.
                eg: 'red'
            deny_list (Sequence[str]):
                The attributes to deny in this namespace. eg:
                'blue'
        """

        namespace = proto.Field(
            proto.STRING,
            number=1,
        )
        allow_list = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        deny_list = proto.RepeatedField(
            proto.STRING,
            number=3,
        )

    class CrowdingTag(proto.Message):
        r"""Crowding tag is a constraint on a neighbor list produced by nearest
        neighbor search requiring that no more than some value k' of the k
        neighbors returned have the same value of crowding_attribute.

        Attributes:
            crowding_attribute (str):
                The attribute value used for crowding. The maximum number of
                neighbors to return per crowding attribute value
                (per_crowding_attribute_num_neighbors) is configured
                per-query. This field is ignored if
                per_crowding_attribute_num_neighbors is larger than the
                total number of neighbors to return for a given query.
        """

        crowding_attribute = proto.Field(
            proto.STRING,
            number=1,
        )

    datapoint_id = proto.Field(
        proto.STRING,
        number=1,
    )
    feature_vector = proto.RepeatedField(
        proto.FLOAT,
        number=2,
    )
    restricts = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=Restriction,
    )
    crowding_tag = proto.Field(
        proto.MESSAGE,
        number=5,
        message=CrowdingTag,
    )


class IndexStats(proto.Message):
    r"""Stats of the Index.

    Attributes:
        vectors_count (int):
            Output only. The number of vectors in the
            Index.
        shards_count (int):
            Output only. The number of shards in the
            Index.
    """

    vectors_count = proto.Field(
        proto.INT64,
        number=1,
    )
    shards_count = proto.Field(
        proto.INT32,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
