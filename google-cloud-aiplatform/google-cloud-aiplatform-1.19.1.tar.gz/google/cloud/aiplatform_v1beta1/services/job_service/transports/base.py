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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union
import pkg_resources

import google.auth  # type: ignore
import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.aiplatform_v1beta1.types import batch_prediction_job
from google.cloud.aiplatform_v1beta1.types import (
    batch_prediction_job as gca_batch_prediction_job,
)
from google.cloud.aiplatform_v1beta1.types import custom_job
from google.cloud.aiplatform_v1beta1.types import custom_job as gca_custom_job
from google.cloud.aiplatform_v1beta1.types import data_labeling_job
from google.cloud.aiplatform_v1beta1.types import (
    data_labeling_job as gca_data_labeling_job,
)
from google.cloud.aiplatform_v1beta1.types import hyperparameter_tuning_job
from google.cloud.aiplatform_v1beta1.types import (
    hyperparameter_tuning_job as gca_hyperparameter_tuning_job,
)
from google.cloud.aiplatform_v1beta1.types import job_service
from google.cloud.aiplatform_v1beta1.types import model_deployment_monitoring_job
from google.cloud.aiplatform_v1beta1.types import (
    model_deployment_monitoring_job as gca_model_deployment_monitoring_job,
)
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-aiplatform",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class JobServiceTransport(abc.ABC):
    """Abstract transport class for JobService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "aiplatform.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
        """

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

        # Save the scopes.
        self._scopes = scopes

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )
        elif credentials is None:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )
            # Don't apply audience if the credentials file passed from user.
            if hasattr(credentials, "with_gdch_audience"):
                credentials = credentials.with_gdch_audience(
                    api_audience if api_audience else host
                )

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_custom_job: gapic_v1.method.wrap_method(
                self.create_custom_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.get_custom_job: gapic_v1.method.wrap_method(
                self.get_custom_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.list_custom_jobs: gapic_v1.method.wrap_method(
                self.list_custom_jobs,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.delete_custom_job: gapic_v1.method.wrap_method(
                self.delete_custom_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.cancel_custom_job: gapic_v1.method.wrap_method(
                self.cancel_custom_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.create_data_labeling_job: gapic_v1.method.wrap_method(
                self.create_data_labeling_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.get_data_labeling_job: gapic_v1.method.wrap_method(
                self.get_data_labeling_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.list_data_labeling_jobs: gapic_v1.method.wrap_method(
                self.list_data_labeling_jobs,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.delete_data_labeling_job: gapic_v1.method.wrap_method(
                self.delete_data_labeling_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.cancel_data_labeling_job: gapic_v1.method.wrap_method(
                self.cancel_data_labeling_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.create_hyperparameter_tuning_job: gapic_v1.method.wrap_method(
                self.create_hyperparameter_tuning_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.get_hyperparameter_tuning_job: gapic_v1.method.wrap_method(
                self.get_hyperparameter_tuning_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.list_hyperparameter_tuning_jobs: gapic_v1.method.wrap_method(
                self.list_hyperparameter_tuning_jobs,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.delete_hyperparameter_tuning_job: gapic_v1.method.wrap_method(
                self.delete_hyperparameter_tuning_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.cancel_hyperparameter_tuning_job: gapic_v1.method.wrap_method(
                self.cancel_hyperparameter_tuning_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.create_batch_prediction_job: gapic_v1.method.wrap_method(
                self.create_batch_prediction_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.get_batch_prediction_job: gapic_v1.method.wrap_method(
                self.get_batch_prediction_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.list_batch_prediction_jobs: gapic_v1.method.wrap_method(
                self.list_batch_prediction_jobs,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.delete_batch_prediction_job: gapic_v1.method.wrap_method(
                self.delete_batch_prediction_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.cancel_batch_prediction_job: gapic_v1.method.wrap_method(
                self.cancel_batch_prediction_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.create_model_deployment_monitoring_job: gapic_v1.method.wrap_method(
                self.create_model_deployment_monitoring_job,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.search_model_deployment_monitoring_stats_anomalies: gapic_v1.method.wrap_method(
                self.search_model_deployment_monitoring_stats_anomalies,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.get_model_deployment_monitoring_job: gapic_v1.method.wrap_method(
                self.get_model_deployment_monitoring_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.list_model_deployment_monitoring_jobs: gapic_v1.method.wrap_method(
                self.list_model_deployment_monitoring_jobs,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.update_model_deployment_monitoring_job: gapic_v1.method.wrap_method(
                self.update_model_deployment_monitoring_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.delete_model_deployment_monitoring_job: gapic_v1.method.wrap_method(
                self.delete_model_deployment_monitoring_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.pause_model_deployment_monitoring_job: gapic_v1.method.wrap_method(
                self.pause_model_deployment_monitoring_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.resume_model_deployment_monitoring_job: gapic_v1.method.wrap_method(
                self.resume_model_deployment_monitoring_job,
                default_timeout=5.0,
                client_info=client_info,
            ),
        }

    def close(self):
        """Closes resources associated with the transport.

        .. warning::
             Only call this method if the transport is NOT shared
             with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def operations_client(self):
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def create_custom_job(
        self,
    ) -> Callable[
        [job_service.CreateCustomJobRequest],
        Union[gca_custom_job.CustomJob, Awaitable[gca_custom_job.CustomJob]],
    ]:
        raise NotImplementedError()

    @property
    def get_custom_job(
        self,
    ) -> Callable[
        [job_service.GetCustomJobRequest],
        Union[custom_job.CustomJob, Awaitable[custom_job.CustomJob]],
    ]:
        raise NotImplementedError()

    @property
    def list_custom_jobs(
        self,
    ) -> Callable[
        [job_service.ListCustomJobsRequest],
        Union[
            job_service.ListCustomJobsResponse,
            Awaitable[job_service.ListCustomJobsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_custom_job(
        self,
    ) -> Callable[
        [job_service.DeleteCustomJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_custom_job(
        self,
    ) -> Callable[
        [job_service.CancelCustomJobRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_data_labeling_job(
        self,
    ) -> Callable[
        [job_service.CreateDataLabelingJobRequest],
        Union[
            gca_data_labeling_job.DataLabelingJob,
            Awaitable[gca_data_labeling_job.DataLabelingJob],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_data_labeling_job(
        self,
    ) -> Callable[
        [job_service.GetDataLabelingJobRequest],
        Union[
            data_labeling_job.DataLabelingJob,
            Awaitable[data_labeling_job.DataLabelingJob],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_data_labeling_jobs(
        self,
    ) -> Callable[
        [job_service.ListDataLabelingJobsRequest],
        Union[
            job_service.ListDataLabelingJobsResponse,
            Awaitable[job_service.ListDataLabelingJobsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_data_labeling_job(
        self,
    ) -> Callable[
        [job_service.DeleteDataLabelingJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_data_labeling_job(
        self,
    ) -> Callable[
        [job_service.CancelDataLabelingJobRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_hyperparameter_tuning_job(
        self,
    ) -> Callable[
        [job_service.CreateHyperparameterTuningJobRequest],
        Union[
            gca_hyperparameter_tuning_job.HyperparameterTuningJob,
            Awaitable[gca_hyperparameter_tuning_job.HyperparameterTuningJob],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_hyperparameter_tuning_job(
        self,
    ) -> Callable[
        [job_service.GetHyperparameterTuningJobRequest],
        Union[
            hyperparameter_tuning_job.HyperparameterTuningJob,
            Awaitable[hyperparameter_tuning_job.HyperparameterTuningJob],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_hyperparameter_tuning_jobs(
        self,
    ) -> Callable[
        [job_service.ListHyperparameterTuningJobsRequest],
        Union[
            job_service.ListHyperparameterTuningJobsResponse,
            Awaitable[job_service.ListHyperparameterTuningJobsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_hyperparameter_tuning_job(
        self,
    ) -> Callable[
        [job_service.DeleteHyperparameterTuningJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_hyperparameter_tuning_job(
        self,
    ) -> Callable[
        [job_service.CancelHyperparameterTuningJobRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_batch_prediction_job(
        self,
    ) -> Callable[
        [job_service.CreateBatchPredictionJobRequest],
        Union[
            gca_batch_prediction_job.BatchPredictionJob,
            Awaitable[gca_batch_prediction_job.BatchPredictionJob],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_batch_prediction_job(
        self,
    ) -> Callable[
        [job_service.GetBatchPredictionJobRequest],
        Union[
            batch_prediction_job.BatchPredictionJob,
            Awaitable[batch_prediction_job.BatchPredictionJob],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_batch_prediction_jobs(
        self,
    ) -> Callable[
        [job_service.ListBatchPredictionJobsRequest],
        Union[
            job_service.ListBatchPredictionJobsResponse,
            Awaitable[job_service.ListBatchPredictionJobsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_batch_prediction_job(
        self,
    ) -> Callable[
        [job_service.DeleteBatchPredictionJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_batch_prediction_job(
        self,
    ) -> Callable[
        [job_service.CancelBatchPredictionJobRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_model_deployment_monitoring_job(
        self,
    ) -> Callable[
        [job_service.CreateModelDeploymentMonitoringJobRequest],
        Union[
            gca_model_deployment_monitoring_job.ModelDeploymentMonitoringJob,
            Awaitable[gca_model_deployment_monitoring_job.ModelDeploymentMonitoringJob],
        ],
    ]:
        raise NotImplementedError()

    @property
    def search_model_deployment_monitoring_stats_anomalies(
        self,
    ) -> Callable[
        [job_service.SearchModelDeploymentMonitoringStatsAnomaliesRequest],
        Union[
            job_service.SearchModelDeploymentMonitoringStatsAnomaliesResponse,
            Awaitable[
                job_service.SearchModelDeploymentMonitoringStatsAnomaliesResponse
            ],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_model_deployment_monitoring_job(
        self,
    ) -> Callable[
        [job_service.GetModelDeploymentMonitoringJobRequest],
        Union[
            model_deployment_monitoring_job.ModelDeploymentMonitoringJob,
            Awaitable[model_deployment_monitoring_job.ModelDeploymentMonitoringJob],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_model_deployment_monitoring_jobs(
        self,
    ) -> Callable[
        [job_service.ListModelDeploymentMonitoringJobsRequest],
        Union[
            job_service.ListModelDeploymentMonitoringJobsResponse,
            Awaitable[job_service.ListModelDeploymentMonitoringJobsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_model_deployment_monitoring_job(
        self,
    ) -> Callable[
        [job_service.UpdateModelDeploymentMonitoringJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_model_deployment_monitoring_job(
        self,
    ) -> Callable[
        [job_service.DeleteModelDeploymentMonitoringJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def pause_model_deployment_monitoring_job(
        self,
    ) -> Callable[
        [job_service.PauseModelDeploymentMonitoringJobRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def resume_model_deployment_monitoring_job(
        self,
    ) -> Callable[
        [job_service.ResumeModelDeploymentMonitoringJobRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest],
        Union[
            operations_pb2.ListOperationsResponse,
            Awaitable[operations_pb2.ListOperationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_operation(
        self,
    ) -> Callable[
        [operations_pb2.GetOperationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def wait_operation(
        self,
    ) -> Callable[
        [operations_pb2.WaitOperationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.SetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.GetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Union[
            iam_policy_pb2.TestIamPermissionsResponse,
            Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_location(
        self,
    ) -> Callable[
        [locations_pb2.GetLocationRequest],
        Union[locations_pb2.Location, Awaitable[locations_pb2.Location]],
    ]:
        raise NotImplementedError()

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest],
        Union[
            locations_pb2.ListLocationsResponse,
            Awaitable[locations_pb2.ListLocationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = ("JobServiceTransport",)
