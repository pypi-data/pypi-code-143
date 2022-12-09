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
    package="google.cloud.aiplatform.v1beta1.schema.predict.prediction",
    manifest={
        "TimeSeriesForecastingPredictionResult",
    },
)


class TimeSeriesForecastingPredictionResult(proto.Message):
    r"""Prediction output format for Time Series Forecasting.

    Attributes:
        value (float):
            The regression value.
    """

    value = proto.Field(
        proto.FLOAT,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
