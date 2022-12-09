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


__protobuf__ = proto.module(
    package="google.cloud.aiplatform.v1",
    manifest={
        "FeaturestoreMonitoringConfig",
    },
)


class FeaturestoreMonitoringConfig(proto.Message):
    r"""Configuration of how features in Featurestore are monitored.

    Attributes:
        snapshot_analysis (google.cloud.aiplatform_v1.types.FeaturestoreMonitoringConfig.SnapshotAnalysis):
            The config for Snapshot Analysis Based
            Feature Monitoring.
        import_features_analysis (google.cloud.aiplatform_v1.types.FeaturestoreMonitoringConfig.ImportFeaturesAnalysis):
            The config for ImportFeatures Analysis Based
            Feature Monitoring.
        numerical_threshold_config (google.cloud.aiplatform_v1.types.FeaturestoreMonitoringConfig.ThresholdConfig):
            Threshold for numerical features of anomaly detection. This
            is shared by all objectives of Featurestore Monitoring for
            numerical features (i.e. Features with type
            ([Feature.ValueType][google.cloud.aiplatform.v1.Feature.ValueType])
            DOUBLE or INT64).
        categorical_threshold_config (google.cloud.aiplatform_v1.types.FeaturestoreMonitoringConfig.ThresholdConfig):
            Threshold for categorical features of anomaly detection.
            This is shared by all types of Featurestore Monitoring for
            categorical features (i.e. Features with type
            ([Feature.ValueType][google.cloud.aiplatform.v1.Feature.ValueType])
            BOOL or STRING).
    """

    class SnapshotAnalysis(proto.Message):
        r"""Configuration of the Featurestore's Snapshot Analysis Based
        Monitoring. This type of analysis generates statistics for each
        Feature based on a snapshot of the latest feature value of each
        entities every monitoring_interval.

        Attributes:
            disabled (bool):
                The monitoring schedule for snapshot analysis. For
                EntityType-level config: unset / disabled = true indicates
                disabled by default for Features under it; otherwise by
                default enable snapshot analysis monitoring with
                monitoring_interval for Features under it. Feature-level
                config: disabled = true indicates disabled regardless of the
                EntityType-level config; unset monitoring_interval indicates
                going with EntityType-level config; otherwise run snapshot
                analysis monitoring with monitoring_interval regardless of
                the EntityType-level config. Explicitly Disable the snapshot
                analysis based monitoring.
            monitoring_interval_days (int):
                Configuration of the snapshot analysis based monitoring
                pipeline running interval. The value indicates number of
                days. If both
                [FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days][google.cloud.aiplatform.v1.FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days]
                and
                [FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval][]
                are set when creating/updating EntityTypes/Features,
                [FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days][google.cloud.aiplatform.v1.FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days]
                will be used.
            staleness_days (int):
                Customized export features time window for
                snapshot analysis. Unit is one day. Default
                value is 3 weeks. Minimum value is 1 day.
                Maximum value is 4000 days.
        """

        disabled = proto.Field(
            proto.BOOL,
            number=1,
        )
        monitoring_interval_days = proto.Field(
            proto.INT32,
            number=3,
        )
        staleness_days = proto.Field(
            proto.INT32,
            number=4,
        )

    class ImportFeaturesAnalysis(proto.Message):
        r"""Configuration of the Featurestore's ImportFeature Analysis Based
        Monitoring. This type of analysis generates statistics for values of
        each Feature imported by every [ImportFeatureValues][] operation.

        Attributes:
            state (google.cloud.aiplatform_v1.types.FeaturestoreMonitoringConfig.ImportFeaturesAnalysis.State):
                Whether to enable / disable / inherite
                default hebavior for import features analysis.
            anomaly_detection_baseline (google.cloud.aiplatform_v1.types.FeaturestoreMonitoringConfig.ImportFeaturesAnalysis.Baseline):
                The baseline used to do anomaly detection for
                the statistics generated by import features
                analysis.
        """

        class State(proto.Enum):
            r"""The state defines whether to enable ImportFeature analysis."""
            STATE_UNSPECIFIED = 0
            DEFAULT = 1
            ENABLED = 2
            DISABLED = 3

        class Baseline(proto.Enum):
            r"""Defines the baseline to do anomaly detection for feature values
            imported by each [ImportFeatureValues][] operation.
            """
            BASELINE_UNSPECIFIED = 0
            LATEST_STATS = 1
            MOST_RECENT_SNAPSHOT_STATS = 2
            PREVIOUS_IMPORT_FEATURES_STATS = 3

        state = proto.Field(
            proto.ENUM,
            number=1,
            enum="FeaturestoreMonitoringConfig.ImportFeaturesAnalysis.State",
        )
        anomaly_detection_baseline = proto.Field(
            proto.ENUM,
            number=2,
            enum="FeaturestoreMonitoringConfig.ImportFeaturesAnalysis.Baseline",
        )

    class ThresholdConfig(proto.Message):
        r"""The config for Featurestore Monitoring threshold.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            value (float):
                Specify a threshold value that can trigger
                the alert. 1. For categorical feature, the
                distribution distance is calculated by
                L-inifinity norm.
                2. For numerical feature, the distribution
                distance is calculated by Jensen–Shannon
                divergence. Each feature must have a non-zero
                threshold if they need to be monitored.
                Otherwise no alert will be triggered for that
                feature.

                This field is a member of `oneof`_ ``threshold``.
        """

        value = proto.Field(
            proto.DOUBLE,
            number=1,
            oneof="threshold",
        )

    snapshot_analysis = proto.Field(
        proto.MESSAGE,
        number=1,
        message=SnapshotAnalysis,
    )
    import_features_analysis = proto.Field(
        proto.MESSAGE,
        number=2,
        message=ImportFeaturesAnalysis,
    )
    numerical_threshold_config = proto.Field(
        proto.MESSAGE,
        number=3,
        message=ThresholdConfig,
    )
    categorical_threshold_config = proto.Field(
        proto.MESSAGE,
        number=4,
        message=ThresholdConfig,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
