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

from typing import Iterable, Optional, Union, Sequence, Dict, List

import abc
import copy
import datetime
import time

from google.cloud import storage
from google.cloud import bigquery

from google.auth import credentials as auth_credentials
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.rpc import status_pb2

from google.cloud import aiplatform
from google.cloud.aiplatform import base
from google.cloud.aiplatform.compat.types import (
    batch_prediction_job as gca_bp_job_compat,
    completion_stats as gca_completion_stats,
    custom_job as gca_custom_job_compat,
    explanation as gca_explanation_compat,
    encryption_spec as gca_encryption_spec_compat,
    io as gca_io_compat,
    job_state as gca_job_state,
    hyperparameter_tuning_job as gca_hyperparameter_tuning_job_compat,
    machine_resources as gca_machine_resources_compat,
    manual_batch_tuning_parameters as gca_manual_batch_tuning_parameters_compat,
    study as gca_study_compat,
    model_deployment_monitoring_job as gca_model_deployment_monitoring_job_compat,
)

from google.cloud.aiplatform.constants import base as constants
from google.cloud.aiplatform import initializer
from google.cloud.aiplatform import hyperparameter_tuning
from google.cloud.aiplatform import model_monitoring
from google.cloud.aiplatform import utils
from google.cloud.aiplatform.utils import console_utils
from google.cloud.aiplatform.utils import source_utils
from google.cloud.aiplatform.utils import worker_spec_utils

from google.cloud.aiplatform_v1.types import (
    batch_prediction_job as batch_prediction_job_v1,
)
from google.cloud.aiplatform_v1.types import custom_job as custom_job_v1

_LOGGER = base.Logger(__name__)

_JOB_COMPLETE_STATES = (
    gca_job_state.JobState.JOB_STATE_SUCCEEDED,
    gca_job_state.JobState.JOB_STATE_FAILED,
    gca_job_state.JobState.JOB_STATE_CANCELLED,
    gca_job_state.JobState.JOB_STATE_PAUSED,
)

_JOB_ERROR_STATES = (
    gca_job_state.JobState.JOB_STATE_FAILED,
    gca_job_state.JobState.JOB_STATE_CANCELLED,
)

# _block_until_complete wait times
_JOB_WAIT_TIME = 5  # start at five seconds
_LOG_WAIT_TIME = 5
_MAX_WAIT_TIME = 60 * 5  # 5 minute wait
_WAIT_TIME_MULTIPLIER = 2  # scale wait by 2 every iteration


class _Job(base.VertexAiStatefulResource):
    """Class that represents a general Job resource in Vertex AI.
    Cannot be directly instantiated.

    Serves as base class to specific Job types, i.e. BatchPredictionJob or
    DataLabelingJob to re-use shared functionality.

    Subclasses requires one class attribute:

    _getter_method (str): The name of JobServiceClient getter method for specific
    Job type, i.e. 'get_custom_job' for CustomJob
    _cancel_method (str): The name of the specific JobServiceClient cancel method
    _delete_method (str): The name of the specific JobServiceClient delete method
    """

    client_class = utils.JobClientWithOverride

    # Required by the done() method
    _valid_done_states = _JOB_COMPLETE_STATES

    def __init__(
        self,
        job_name: str,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
    ):
        """Retrieves Job subclass resource by calling a subclass-specific getter
        method.

        Args:
            job_name (str):
                Required. A fully-qualified job resource name or job ID.
                Example: "projects/123/locations/us-central1/batchPredictionJobs/456" or
                "456" when project, location and job_type are initialized or passed.
            project: Optional[str] = None,
                Optional. project to retrieve Job subclass from. If not set,
                project set in aiplatform.init will be used.
            location: Optional[str] = None,
                Optional. location to retrieve Job subclass from. If not set,
                location set in aiplatform.init will be used.
            credentials: Optional[auth_credentials.Credentials] = None,
                Custom credentials to use. If not set, credentials set in
                aiplatform.init will be used.
        """
        super().__init__(
            project=project,
            location=location,
            credentials=credentials,
            resource_name=job_name,
        )
        self._gca_resource = self._get_gca_resource(resource_name=job_name)

    @property
    def state(self) -> gca_job_state.JobState:
        """Fetch Job again and return the current JobState.

        Returns:
            state (job_state.JobState):
                Enum that describes the state of a Vertex AI job.
        """

        # Fetch the Job again for most up-to-date job state
        self._sync_gca_resource()

        return self._gca_resource.state

    @property
    def start_time(self) -> Optional[datetime.datetime]:
        """Time when the Job resource entered the `JOB_STATE_RUNNING` for the
        first time."""
        self._sync_gca_resource()
        return getattr(self._gca_resource, "start_time")

    @property
    def end_time(self) -> Optional[datetime.datetime]:
        """Time when the Job resource entered the `JOB_STATE_SUCCEEDED`,
        `JOB_STATE_FAILED`, or `JOB_STATE_CANCELLED` state."""
        self._sync_gca_resource()
        return getattr(self._gca_resource, "end_time")

    @property
    def error(self) -> Optional[status_pb2.Status]:
        """Detailed error info for this Job resource. Only populated when the
        Job's state is `JOB_STATE_FAILED` or `JOB_STATE_CANCELLED`."""
        self._sync_gca_resource()
        return getattr(self._gca_resource, "error")

    @property
    @abc.abstractmethod
    def _job_type(cls) -> str:
        """Job type."""
        pass

    @property
    @abc.abstractmethod
    def _cancel_method(cls) -> str:
        """Name of cancellation method for cancelling the specific job type."""
        pass

    def _dashboard_uri(self) -> Optional[str]:
        """Helper method to compose the dashboard uri where job can be
        viewed."""
        fields = self._parse_resource_name(self.resource_name)
        location = fields.pop("location")
        project = fields.pop("project")
        job = list(fields.values())[0]
        url = f"https://console.cloud.google.com/ai/platform/locations/{location}/{self._job_type}/{job}?project={project}"
        return url

    def _log_job_state(self):
        """Helper method to log job state."""
        _LOGGER.info(
            "%s %s current state:\n%s"
            % (
                self.__class__.__name__,
                self._gca_resource.name,
                self._gca_resource.state,
            )
        )

    def _block_until_complete(self):
        """Helper method to block and check on job until complete.

        Raises:
            RuntimeError: If job failed or cancelled.
        """

        log_wait = _LOG_WAIT_TIME

        previous_time = time.time()
        while self.state not in _JOB_COMPLETE_STATES:
            current_time = time.time()
            if current_time - previous_time >= log_wait:
                self._log_job_state()
                log_wait = min(log_wait * _WAIT_TIME_MULTIPLIER, _MAX_WAIT_TIME)
                previous_time = current_time
            time.sleep(_JOB_WAIT_TIME)

        self._log_job_state()

        # Error is only populated when the job state is
        # JOB_STATE_FAILED or JOB_STATE_CANCELLED.
        if self._gca_resource.state in _JOB_ERROR_STATES:
            raise RuntimeError("Job failed with:\n%s" % self._gca_resource.error)
        else:
            _LOGGER.log_action_completed_against_resource("run", "completed", self)

    @classmethod
    def list(
        cls,
        filter: Optional[str] = None,
        order_by: Optional[str] = None,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
    ) -> List[base.VertexAiResourceNoun]:
        """List all instances of this Job Resource.

        Example Usage:

        aiplatform.BatchPredictionJobs.list(
            filter='state="JOB_STATE_SUCCEEDED" AND display_name="my_job"',
        )

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

        Returns:
            List[VertexAiResourceNoun] - A list of Job resource objects.
        """

        return cls._list_with_local_order(
            filter=filter,
            order_by=order_by,
            project=project,
            location=location,
            credentials=credentials,
        )

    def cancel(self) -> None:
        """Cancels this Job.

        Success of cancellation is not guaranteed. Use `Job.state`
        property to verify if cancellation was successful.
        """

        _LOGGER.log_action_start_against_resource("Cancelling", "run", self)
        getattr(self.api_client, self._cancel_method)(name=self.resource_name)


class BatchPredictionJob(_Job):

    _resource_noun = "batchPredictionJobs"
    _getter_method = "get_batch_prediction_job"
    _list_method = "list_batch_prediction_jobs"
    _cancel_method = "cancel_batch_prediction_job"
    _delete_method = "delete_batch_prediction_job"
    _job_type = "batch-predictions"
    _parse_resource_name_method = "parse_batch_prediction_job_path"
    _format_resource_name_method = "batch_prediction_job_path"

    def __init__(
        self,
        batch_prediction_job_name: str,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
    ):
        """Retrieves a BatchPredictionJob resource and instantiates its
        representation.

        Args:
            batch_prediction_job_name (str):
                Required. A fully-qualified BatchPredictionJob resource name or ID.
                Example: "projects/.../locations/.../batchPredictionJobs/456" or
                "456" when project and location are initialized or passed.
            project: Optional[str] = None,
                Optional. project to retrieve BatchPredictionJob from. If not set,
                project set in aiplatform.init will be used.
            location: Optional[str] = None,
                Optional. location to retrieve BatchPredictionJob from. If not set,
                location set in aiplatform.init will be used.
            credentials: Optional[auth_credentials.Credentials] = None,
                Custom credentials to use. If not set, credentials set in
                aiplatform.init will be used.
        """

        super().__init__(
            job_name=batch_prediction_job_name,
            project=project,
            location=location,
            credentials=credentials,
        )

    @property
    def output_info(
        self,
    ) -> Optional[batch_prediction_job_v1.BatchPredictionJob.OutputInfo]:
        """Information describing the output of this job, including output location
        into which prediction output is written.

        This is only available for batch prediction jobs that have run successfully.
        """
        self._assert_gca_resource_is_available()
        return self._gca_resource.output_info

    @property
    def partial_failures(self) -> Optional[Sequence[status_pb2.Status]]:
        """Partial failures encountered. For example, single files that can't be read.
        This field never exceeds 20 entries. Status details fields contain standard
        GCP error details."""
        self._assert_gca_resource_is_available()
        return getattr(self._gca_resource, "partial_failures")

    @property
    def completion_stats(self) -> Optional[gca_completion_stats.CompletionStats]:
        """Statistics on completed and failed prediction instances."""
        self._assert_gca_resource_is_available()
        return getattr(self._gca_resource, "completion_stats")

    @classmethod
    def create(
        cls,
        # TODO(b/223262536): Make the job_display_name parameter optional in the next major release
        job_display_name: str,
        model_name: Union[str, "aiplatform.Model"],
        instances_format: str = "jsonl",
        predictions_format: str = "jsonl",
        gcs_source: Optional[Union[str, Sequence[str]]] = None,
        bigquery_source: Optional[str] = None,
        gcs_destination_prefix: Optional[str] = None,
        bigquery_destination_prefix: Optional[str] = None,
        model_parameters: Optional[Dict] = None,
        machine_type: Optional[str] = None,
        accelerator_type: Optional[str] = None,
        accelerator_count: Optional[int] = None,
        starting_replica_count: Optional[int] = None,
        max_replica_count: Optional[int] = None,
        generate_explanation: Optional[bool] = False,
        explanation_metadata: Optional["aiplatform.explain.ExplanationMetadata"] = None,
        explanation_parameters: Optional[
            "aiplatform.explain.ExplanationParameters"
        ] = None,
        labels: Optional[Dict[str, str]] = None,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        encryption_spec_key_name: Optional[str] = None,
        sync: bool = True,
        create_request_timeout: Optional[float] = None,
        batch_size: Optional[int] = None,
        model_monitoring_objective_config: Optional[
            "aiplatform.model_monitoring.ObjectiveConfig"
        ] = None,
        model_monitoring_alert_config: Optional[
            "aiplatform.model_monitoring.AlertConfig"
        ] = None,
        analysis_instance_schema_uri: Optional[str] = None,
    ) -> "BatchPredictionJob":
        """Create a batch prediction job.

        Args:
            job_display_name (str):
                Required. The user-defined name of the BatchPredictionJob.
                The name can be up to 128 characters long and can be consist
                of any UTF-8 characters.
            model_name (Union[str, aiplatform.Model]):
                Required. A fully-qualified model resource name or model ID.
                Example: "projects/123/locations/us-central1/models/456" or
                "456" when project and location are initialized or passed.
                May optionally contain a version ID or alias in
                {model_name}@{version} form.

                Or an instance of aiplatform.Model.
            instances_format (str):
                Required. The format in which instances are provided. Must be one
                of the formats listed in `Model.supported_input_storage_formats`.
                Default is "jsonl" when using `gcs_source`. If a `bigquery_source`
                is provided, this is overridden to "bigquery".
            predictions_format (str):
                Required. The format in which Vertex AI outputs the
                predictions, must be one of the formats specified in
                `Model.supported_output_storage_formats`.
                Default is "jsonl" when using `gcs_destination_prefix`. If a
                `bigquery_destination_prefix` is provided, this is overridden to
                "bigquery".
            gcs_source (Optional[Sequence[str]]):
                Google Cloud Storage URI(-s) to your instances to run
                batch prediction on. They must match `instances_format`.

            bigquery_source (Optional[str]):
                BigQuery URI to a table, up to 2000 characters long. For example:
                `bq://projectId.bqDatasetId.bqTableId`
            gcs_destination_prefix (Optional[str]):
                The Google Cloud Storage location of the directory where the
                output is to be written to. In the given directory a new
                directory is created. Its name is
                ``prediction-<model-display-name>-<job-create-time>``, where
                timestamp is in YYYY-MM-DDThh:mm:ss.sssZ ISO-8601 format.
                Inside of it files ``predictions_0001.<extension>``,
                ``predictions_0002.<extension>``, ...,
                ``predictions_N.<extension>`` are created where
                ``<extension>`` depends on chosen ``predictions_format``,
                and N may equal 0001 and depends on the total number of
                successfully predicted instances. If the Model has both
                ``instance`` and ``prediction`` schemata defined then each such
                file contains predictions as per the ``predictions_format``.
                If prediction for any instance failed (partially or
                completely), then an additional ``errors_0001.<extension>``,
                ``errors_0002.<extension>``,..., ``errors_N.<extension>``
                files are created (N depends on total number of failed
                predictions). These files contain the failed instances, as
                per their schema, followed by an additional ``error`` field
                which as value has ```google.rpc.Status`` <Status>`__
                containing only ``code`` and ``message`` fields.
            bigquery_destination_prefix (Optional[str]):
                The BigQuery project or dataset location where the output is
                to be written to. If project is provided, a new dataset is
                created with name
                ``prediction_<model-display-name>_<job-create-time>`` where
                is made BigQuery-dataset-name compatible (for example, most
                special characters become underscores), and timestamp is in
                YYYY_MM_DDThh_mm_ss_sssZ "based on ISO-8601" format. In the
                dataset two tables will be created, ``predictions``, and
                ``errors``. If the Model has both
                [instance][google.cloud.aiplatform.v1.PredictSchemata.instance_schema_uri]
                and
                [prediction][google.cloud.aiplatform.v1.PredictSchemata.parameters_schema_uri]
                schemata defined then the tables have columns as follows:
                The ``predictions`` table contains instances for which the
                prediction succeeded, it has columns as per a concatenation
                of the Model's instance and prediction schemata. The
                ``errors`` table contains rows for which the prediction has
                failed, it has instance columns, as per the instance schema,
                followed by a single "errors" column, which as values has
                [google.rpc.Status][google.rpc.Status] represented as a
                STRUCT, and containing only ``code`` and ``message``.
            model_parameters (Optional[Dict]):
                The parameters that govern the predictions. The schema of
                the parameters may be specified via the Model's `parameters_schema_uri`.
            machine_type (Optional[str]):
                The type of machine for running batch prediction on
                dedicated resources. Not specifying machine type will result in
                batch prediction job being run with automatic resources.
            accelerator_type (Optional[str]):
                The type of accelerator(s) that may be attached
                to the machine as per `accelerator_count`. Only used if
                `machine_type` is set.
            accelerator_count (Optional[int]):
                The number of accelerators to attach to the
                `machine_type`. Only used if `machine_type` is set.
            starting_replica_count (Optional[int]):
                The number of machine replicas used at the start of the batch
                operation. If not set, Vertex AI decides starting number, not
                greater than `max_replica_count`. Only used if `machine_type` is
                set.
            max_replica_count (Optional[int]):
                The maximum number of machine replicas the batch operation may
                be scaled to. Only used if `machine_type` is set.
                Default is 10.
            generate_explanation (bool):
                Optional. Generate explanation along with the batch prediction
                results. This will cause the batch prediction output to include
                explanations based on the `prediction_format`:
                    - `bigquery`: output includes a column named `explanation`. The value
                        is a struct that conforms to the [aiplatform.gapic.Explanation] object.
                    - `jsonl`: The JSON objects on each line include an additional entry
                        keyed `explanation`. The value of the entry is a JSON object that
                        conforms to the [aiplatform.gapic.Explanation] object.
                    - `csv`: Generating explanations for CSV format is not supported.
            explanation_metadata (aiplatform.explain.ExplanationMetadata):
                Optional. Explanation metadata configuration for this BatchPredictionJob.
                Can be specified only if `generate_explanation` is set to `True`.

                This value overrides the value of `Model.explanation_metadata`.
                All fields of `explanation_metadata` are optional in the request. If
                a field of the `explanation_metadata` object is not populated, the
                corresponding field of the `Model.explanation_metadata` object is inherited.
                For more details, see `Ref docs <http://tinyurl.com/1igh60kt>`
            explanation_parameters (aiplatform.explain.ExplanationParameters):
                Optional. Parameters to configure explaining for Model's predictions.
                Can be specified only if `generate_explanation` is set to `True`.

                This value overrides the value of `Model.explanation_parameters`.
                All fields of `explanation_parameters` are optional in the request. If
                a field of the `explanation_parameters` object is not populated, the
                corresponding field of the `Model.explanation_parameters` object is inherited.
                For more details, see `Ref docs <http://tinyurl.com/1an4zake>`
            labels (Dict[str, str]):
                Optional. The labels with user-defined metadata to organize your
                BatchPredictionJobs. Label keys and values can be no longer than
                64 characters (Unicode codepoints), can only contain lowercase
                letters, numeric characters, underscores and dashes.
                International characters are allowed. See https://goo.gl/xmQnxf
                for more information and examples of labels.
            credentials (Optional[auth_credentials.Credentials]):
                Custom credentials to use to create this batch prediction
                job. Overrides credentials set in aiplatform.init.
            encryption_spec_key_name (Optional[str]):
                Optional. The Cloud KMS resource identifier of the customer
                managed encryption key used to protect the job. Has the
                form:
                ``projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key``.
                The key needs to be in the same region as where the compute
                resource is created.

                If this is set, then all
                resources created by the BatchPredictionJob will
                be encrypted with the provided encryption key.

                Overrides encryption_spec_key_name set in aiplatform.init.
            sync (bool):
                Whether to execute this method synchronously. If False, this method
                will be executed in concurrent Future and any downstream object will
                be immediately returned and synced when the Future has completed.
            create_request_timeout (float):
                Optional. The timeout for the create request in seconds.
            batch_size (int):
                Optional. The number of the records (e.g. instances) of the operation given in each batch
                to a machine replica. Machine type, and size of a single record should be considered
                when setting this parameter, higher value speeds up the batch operation's execution,
                but too high value will result in a whole batch not fitting in a machine's memory,
                and the whole operation will fail.
                The default value is 64.
            model_monitoring_objective_config (aiplatform.model_monitoring.ObjectiveConfig):
                Optional. The objective config for model monitoring. Passing this parameter enables
                monitoring on the model associated with this batch prediction job.
            model_monitoring_alert_config (aiplatform.model_monitoring.EmailAlertConfig):
                Optional. Configures how model monitoring alerts are sent to the user. Right now
                only email alert is supported.
            analysis_instance_schema_uri (str):
                Optional. Only applicable if model_monitoring_objective_config is also passed.
                This parameter specifies the YAML schema file uri describing the format of a single
                instance that you want Tensorflow Data Validation (TFDV) to
                analyze. If this field is empty, all the feature data types are
                inferred from predict_instance_schema_uri, meaning that TFDV
                will use the data in the exact format as prediction request/response.
                If there are any data type differences between predict instance
                and TFDV instance, this field can be used to override the schema.
                For models trained with Vertex AI, this field must be set as all the
                fields in predict instance formatted as string.
        Returns:
            (jobs.BatchPredictionJob):
                Instantiated representation of the created batch prediction job.
        """
        if not job_display_name:
            job_display_name = cls._generate_display_name()

        utils.validate_display_name(job_display_name)

        if labels:
            utils.validate_labels(labels)

        if isinstance(model_name, str):
            model_name = utils.full_resource_name(
                resource_name=model_name,
                resource_noun="models",
                parse_resource_name_method=aiplatform.Model._parse_resource_name,
                format_resource_name_method=aiplatform.Model._format_resource_name,
                project=project,
                location=location,
                resource_id_validator=super()._revisioned_resource_id_validator,
            )

        # Raise error if both or neither source URIs are provided
        if bool(gcs_source) == bool(bigquery_source):
            raise ValueError(
                "Please provide either a gcs_source or bigquery_source, "
                "but not both."
            )

        # Raise error if both or neither destination prefixes are provided
        if bool(gcs_destination_prefix) == bool(bigquery_destination_prefix):
            raise ValueError(
                "Please provide either a gcs_destination_prefix or "
                "bigquery_destination_prefix, but not both."
            )

        # Raise error if unsupported instance format is provided
        if instances_format not in constants.BATCH_PREDICTION_INPUT_STORAGE_FORMATS:
            raise ValueError(
                f"{predictions_format} is not an accepted instances format "
                f"type. Please choose from: {constants.BATCH_PREDICTION_INPUT_STORAGE_FORMATS}"
            )

        # Raise error if unsupported prediction format is provided
        if predictions_format not in constants.BATCH_PREDICTION_OUTPUT_STORAGE_FORMATS:
            raise ValueError(
                f"{predictions_format} is not an accepted prediction format "
                f"type. Please choose from: {constants.BATCH_PREDICTION_OUTPUT_STORAGE_FORMATS}"
            )
        # TODO(b/242108750): remove temporary re-import statements once model monitoring for batch prediction is GA
        if model_monitoring_objective_config:
            from google.cloud.aiplatform.compat.types import (
                io_v1beta1 as gca_io_compat,
                batch_prediction_job_v1beta1 as gca_bp_job_compat,
                model_monitoring_v1beta1 as gca_model_monitoring_compat,
            )
        else:
            from google.cloud.aiplatform.compat.types import (
                io as gca_io_compat,
                batch_prediction_job as gca_bp_job_compat,
            )
        gapic_batch_prediction_job = gca_bp_job_compat.BatchPredictionJob()

        # Required Fields
        gapic_batch_prediction_job.display_name = job_display_name

        input_config = gca_bp_job_compat.BatchPredictionJob.InputConfig()
        output_config = gca_bp_job_compat.BatchPredictionJob.OutputConfig()

        if bigquery_source:
            input_config.instances_format = "bigquery"
            input_config.bigquery_source = gca_io_compat.BigQuerySource()
            input_config.bigquery_source.input_uri = bigquery_source
        else:
            input_config.instances_format = instances_format
            input_config.gcs_source = gca_io_compat.GcsSource(
                uris=gcs_source if type(gcs_source) == list else [gcs_source]
            )

        if bigquery_destination_prefix:
            output_config.predictions_format = "bigquery"
            output_config.bigquery_destination = gca_io_compat.BigQueryDestination()

            bq_dest_prefix = bigquery_destination_prefix

            if not bq_dest_prefix.startswith("bq://"):
                bq_dest_prefix = f"bq://{bq_dest_prefix}"

            output_config.bigquery_destination.output_uri = bq_dest_prefix
        else:
            output_config.predictions_format = predictions_format
            output_config.gcs_destination = gca_io_compat.GcsDestination(
                output_uri_prefix=gcs_destination_prefix
            )

        gapic_batch_prediction_job.input_config = input_config
        gapic_batch_prediction_job.output_config = output_config

        # Optional Fields
        gapic_batch_prediction_job.encryption_spec = (
            initializer.global_config.get_encryption_spec(
                encryption_spec_key_name=encryption_spec_key_name
            )
        )

        if model_parameters:
            gapic_batch_prediction_job.model_parameters = model_parameters

        # Custom Compute
        if machine_type:

            machine_spec = gca_machine_resources_compat.MachineSpec()
            machine_spec.machine_type = machine_type
            machine_spec.accelerator_type = accelerator_type
            machine_spec.accelerator_count = accelerator_count

            dedicated_resources = gca_machine_resources_compat.BatchDedicatedResources()

            dedicated_resources.machine_spec = machine_spec
            dedicated_resources.starting_replica_count = starting_replica_count
            dedicated_resources.max_replica_count = max_replica_count

            gapic_batch_prediction_job.dedicated_resources = dedicated_resources

            manual_batch_tuning_parameters = (
                gca_manual_batch_tuning_parameters_compat.ManualBatchTuningParameters()
            )
            manual_batch_tuning_parameters.batch_size = batch_size

            gapic_batch_prediction_job.manual_batch_tuning_parameters = (
                manual_batch_tuning_parameters
            )

        # User Labels
        gapic_batch_prediction_job.labels = labels

        # Explanations
        if generate_explanation:
            gapic_batch_prediction_job.generate_explanation = generate_explanation

        if explanation_metadata or explanation_parameters:
            gapic_batch_prediction_job.explanation_spec = (
                gca_explanation_compat.ExplanationSpec(
                    metadata=explanation_metadata, parameters=explanation_parameters
                )
            )

        # Model Monitoring
        if model_monitoring_objective_config:
            if model_monitoring_objective_config.drift_detection_config:
                _LOGGER.info(
                    "Drift detection config is currently not supported for monitoring models associated with batch prediction jobs."
                )
            if model_monitoring_objective_config.explanation_config:
                _LOGGER.info(
                    "XAI config is currently not supported for monitoring models associated with batch prediction jobs."
                )
            gapic_batch_prediction_job.model_monitoring_config = (
                gca_model_monitoring_compat.ModelMonitoringConfig(
                    objective_configs=[
                        model_monitoring_objective_config.as_proto(config_for_bp=True)
                    ],
                    alert_config=model_monitoring_alert_config.as_proto(
                        config_for_bp=True
                    ),
                    analysis_instance_schema_uri=analysis_instance_schema_uri,
                )
            )

        empty_batch_prediction_job = cls._empty_constructor(
            project=project,
            location=location,
            credentials=credentials,
        )

        return cls._create(
            empty_batch_prediction_job=empty_batch_prediction_job,
            model_or_model_name=model_name,
            gca_batch_prediction_job=gapic_batch_prediction_job,
            generate_explanation=generate_explanation,
            sync=sync,
            create_request_timeout=create_request_timeout,
        )
        # TODO(b/242108750): remove temporary re-import statements once model monitoring for batch prediction is GA
        from google.cloud.aiplatform.compat.types import (
            io as gca_io_compat,
            batch_prediction_job as gca_bp_job_compat,
        )

    @classmethod
    @base.optional_sync(return_input_arg="empty_batch_prediction_job")
    def _create(
        cls,
        empty_batch_prediction_job: "BatchPredictionJob",
        model_or_model_name: Union[str, "aiplatform.Model"],
        gca_batch_prediction_job: gca_bp_job_compat.BatchPredictionJob,
        generate_explanation: bool,
        sync: bool = True,
        create_request_timeout: Optional[float] = None,
    ) -> "BatchPredictionJob":
        """Create a batch prediction job.

        Args:
            empty_batch_prediction_job (BatchPredictionJob):
                Required. BatchPredictionJob without _gca_resource populated.
            model_or_model_name (Union[str, aiplatform.Model]):
                Required. Required. A fully-qualified model resource name or
                an instance of aiplatform.Model. If a resource name, it may
                optionally contain a version ID or alias in
                {model_name}@{version} form.
            gca_batch_prediction_job (gca_bp_job.BatchPredictionJob):
                Required. a batch prediction job proto for creating a batch prediction job on Vertex AI.
            generate_explanation (bool):
                Required. Generate explanation along with the batch prediction
                results.
            create_request_timeout (float):
                Optional. The timeout for the create request in seconds.
        Returns:
            (jobs.BatchPredictionJob):
                Instantiated representation of the created batch prediction job.

        Raises:
            ValueError:
                If no or multiple source or destinations are provided. Also, if
                provided instances_format or predictions_format are not supported
                by Vertex AI.
        """

        parent = initializer.global_config.common_location_path(
            project=empty_batch_prediction_job.project,
            location=empty_batch_prediction_job.location,
        )

        model_resource_name = (
            model_or_model_name
            if isinstance(model_or_model_name, str)
            else model_or_model_name.versioned_resource_name
        )

        gca_batch_prediction_job.model = model_resource_name

        api_client = empty_batch_prediction_job.api_client

        _LOGGER.log_create_with_lro(cls)

        gca_batch_prediction_job = api_client.create_batch_prediction_job(
            parent=parent,
            batch_prediction_job=gca_batch_prediction_job,
            timeout=create_request_timeout,
        )

        empty_batch_prediction_job._gca_resource = gca_batch_prediction_job

        batch_prediction_job = empty_batch_prediction_job

        _LOGGER.log_create_complete(cls, batch_prediction_job._gca_resource, "bpj")

        _LOGGER.info(
            "View Batch Prediction Job:\n%s" % batch_prediction_job._dashboard_uri()
        )

        batch_prediction_job._block_until_complete()

        return batch_prediction_job

    def iter_outputs(
        self, bq_max_results: Optional[int] = 100
    ) -> Union[Iterable[storage.Blob], Iterable[bigquery.table.RowIterator]]:
        """Returns an Iterable object to traverse the output files, either a
        list of GCS Blobs or a BigQuery RowIterator depending on the output
        config set when the BatchPredictionJob was created.

        Args:
            bq_max_results: Optional[int] = 100
                Limit on rows to retrieve from prediction table in BigQuery dataset.
                Only used when retrieving predictions from a bigquery_destination_prefix.
                Default is 100.

        Returns:
            Union[Iterable[storage.Blob], Iterable[bigquery.table.RowIterator]]:
                Either a list of GCS Blob objects within the prediction output
                directory or an iterable BigQuery RowIterator with predictions.

        Raises:
            RuntimeError:
                If BatchPredictionJob is in a JobState other than SUCCEEDED,
                since outputs cannot be retrieved until the Job has finished.
            NotImplementedError:
                If BatchPredictionJob succeeded and output_info does not have a
                GCS or BQ output provided.
        """

        self._assert_gca_resource_is_available()

        if self.state != gca_job_state.JobState.JOB_STATE_SUCCEEDED:
            raise RuntimeError(
                f"Cannot read outputs until BatchPredictionJob has succeeded, "
                f"current state: {self._gca_resource.state}"
            )

        output_info = self._gca_resource.output_info

        # GCS Destination, return Blobs
        if output_info.gcs_output_directory:

            # Build a Storage Client using the same credentials as JobServiceClient
            storage_client = storage.Client(
                project=self.project,
                credentials=self.api_client._transport._credentials,
            )

            gcs_bucket, gcs_prefix = utils.extract_bucket_and_prefix_from_gcs_path(
                output_info.gcs_output_directory
            )

            blobs = storage_client.list_blobs(gcs_bucket, prefix=gcs_prefix)

            return blobs

        # BigQuery Destination, return RowIterator
        elif output_info.bigquery_output_dataset:

            # Format of `bigquery_output_dataset` from service is `bq://projectId.bqDatasetId`
            bq_dataset = output_info.bigquery_output_dataset
            bq_table = output_info.bigquery_output_table

            if not bq_table:
                raise RuntimeError(
                    "A BigQuery table with predictions was not found, this "
                    f"might be due to errors. Visit {self._dashboard_uri()} for details."
                )

            if bq_dataset.startswith("bq://"):
                bq_dataset = bq_dataset[5:]

            # Build a BigQuery Client using the same credentials as JobServiceClient
            bq_client = bigquery.Client(
                project=self.project,
                credentials=self.api_client._transport._credentials,
            )

            row_iterator = bq_client.list_rows(
                table=f"{bq_dataset}.{bq_table}", max_results=bq_max_results
            )

            return row_iterator

        # Unknown Destination type
        else:
            raise NotImplementedError(
                f"Unsupported batch prediction output location, here are details"
                f"on your prediction output:\n{output_info}"
            )

    def wait_for_resource_creation(self) -> None:
        """Waits until resource has been created."""
        self._wait_for_resource_creation()


class _RunnableJob(_Job):
    """ABC to interface job as a runnable training class."""

    def __init__(
        self,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
    ):
        """Initializes job with project, location, and api_client.

        Args:
            project(str): Project of the resource noun.
            location(str): The location of the resource noun.
            credentials(google.auth.credentials.Credentials): Optional. custom
                credentials to use when accessing interacting with resource noun.
        """

        base.VertexAiResourceNounWithFutureManager.__init__(
            self, project=project, location=location, credentials=credentials
        )

        self._parent = aiplatform.initializer.global_config.common_location_path(
            project=project, location=location
        )

        self._logged_web_access_uris = set()

    @classmethod
    def _empty_constructor(
        cls,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        resource_name: Optional[str] = None,
    ) -> "_RunnableJob":
        """Initializes with all attributes set to None.

        The attributes should be populated after a future is complete. This allows
        scheduling of additional API calls before the resource is created.

        Args:
            project (str): Optional. Project of the resource noun.
            location (str): Optional. The location of the resource noun.
            credentials(google.auth.credentials.Credentials):
                Optional. custom credentials to use when accessing interacting with
                resource noun.
            resource_name(str): Optional. A fully-qualified resource name or ID.
        Returns:
            An instance of this class with attributes set to None.
        """
        self = super()._empty_constructor(
            project=project,
            location=location,
            credentials=credentials,
            resource_name=resource_name,
        )

        self._logged_web_access_uris = set()
        return self

    @property
    def web_access_uris(self) -> Dict[str, Union[str, Dict[str, str]]]:
        """Fetch the runnable job again and return the latest web access uris.

        Returns:
            (Dict[str, Union[str, Dict[str, str]]]):
                Web access uris of the runnable job.
        """

        # Fetch the Job again for most up-to-date web access uris
        self._sync_gca_resource()
        return self._get_web_access_uris()

    @abc.abstractmethod
    def _get_web_access_uris(self):
        """Helper method to get the web access uris of the runnable job"""
        pass

    @abc.abstractmethod
    def _log_web_access_uris(self):
        """Helper method to log the web access uris of the runnable job"""
        pass

    def _block_until_complete(self):
        """Helper method to block and check on runnable job until complete.

        Raises:
            RuntimeError: If job failed or cancelled.
        """

        log_wait = _LOG_WAIT_TIME

        previous_time = time.time()
        while self.state not in _JOB_COMPLETE_STATES:
            current_time = time.time()
            if current_time - previous_time >= _LOG_WAIT_TIME:
                self._log_job_state()
                log_wait = min(log_wait * _WAIT_TIME_MULTIPLIER, _MAX_WAIT_TIME)
                previous_time = current_time
            self._log_web_access_uris()
            time.sleep(_JOB_WAIT_TIME)

        self._log_job_state()

        # Error is only populated when the job state is
        # JOB_STATE_FAILED or JOB_STATE_CANCELLED.
        if self._gca_resource.state in _JOB_ERROR_STATES:
            raise RuntimeError("Job failed with:\n%s" % self._gca_resource.error)
        else:
            _LOGGER.log_action_completed_against_resource("run", "completed", self)

    @abc.abstractmethod
    def run(self) -> None:
        pass

    @classmethod
    def get(
        cls,
        resource_name: str,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
    ) -> "_RunnableJob":
        """Get a Vertex AI Job for the given resource_name.

        Args:
            resource_name (str):
                Required. A fully-qualified resource name or ID.
            project (str):
                Optional. project to retrieve dataset from. If not set, project
                set in aiplatform.init will be used.
            location (str):
                Optional. location to retrieve dataset from. If not set, location
                set in aiplatform.init will be used.
            credentials (auth_credentials.Credentials):
                Custom credentials to use to upload this model. Overrides
                credentials set in aiplatform.init.

        Returns:
            A Vertex AI Job.
        """
        self = cls._empty_constructor(
            project=project,
            location=location,
            credentials=credentials,
            resource_name=resource_name,
        )

        self._gca_resource = self._get_gca_resource(resource_name=resource_name)

        return self

    def wait_for_resource_creation(self) -> None:
        """Waits until resource has been created."""
        self._wait_for_resource_creation()


class DataLabelingJob(_Job):
    _resource_noun = "dataLabelingJobs"
    _getter_method = "get_data_labeling_job"
    _list_method = "list_data_labeling_jobs"
    _cancel_method = "cancel_data_labeling_job"
    _delete_method = "delete_data_labeling_job"
    _job_type = "labeling-tasks"
    _parse_resource_name_method = "parse_data_labeling_job_path"
    _format_resource_name_method = "data_labeling_job_path"
    pass


class CustomJob(_RunnableJob):
    """Vertex AI Custom Job."""

    _resource_noun = "customJobs"
    _getter_method = "get_custom_job"
    _list_method = "list_custom_jobs"
    _cancel_method = "cancel_custom_job"
    _delete_method = "delete_custom_job"
    _parse_resource_name_method = "parse_custom_job_path"
    _format_resource_name_method = "custom_job_path"
    _job_type = "training"

    def __init__(
        self,
        # TODO(b/223262536): Make display_name parameter fully optional in next major release
        display_name: str,
        worker_pool_specs: Union[List[Dict], List[custom_job_v1.WorkerPoolSpec]],
        base_output_dir: Optional[str] = None,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        labels: Optional[Dict[str, str]] = None,
        encryption_spec_key_name: Optional[str] = None,
        staging_bucket: Optional[str] = None,
    ):
        """Constructs a Custom Job with Worker Pool Specs.

        ```
        Example usage:
        worker_pool_specs = [
                {
                    "machine_spec": {
                        "machine_type": "n1-standard-4",
                        "accelerator_type": "NVIDIA_TESLA_K80",
                        "accelerator_count": 1,
                    },
                    "replica_count": 1,
                    "container_spec": {
                        "image_uri": container_image_uri,
                        "command": [],
                        "args": [],
                    },
                }
            ]

        my_job = aiplatform.CustomJob(
            display_name='my_job',
            worker_pool_specs=worker_pool_specs,
            labels={'my_key': 'my_value'},
        )

        my_job.run()
        ```


        For more information on configuring worker pool specs please visit:
        https://cloud.google.com/ai-platform-unified/docs/training/create-custom-job


        Args:
            display_name (str):
                Required. The user-defined name of the HyperparameterTuningJob.
                The name can be up to 128 characters long and can be consist
                of any UTF-8 characters.
            worker_pool_specs (Union[List[Dict], List[aiplatform.gapic.WorkerPoolSpec]]):
                Required. The spec of the worker pools including machine type and Docker image.
                Can provided as a list of dictionaries or list of WorkerPoolSpec proto messages.
            base_output_dir (str):
                Optional. GCS output directory of job. If not provided a
                timestamped directory in the staging directory will be used.
            project (str):
                Optional.Project to run the custom job in. Overrides project set in aiplatform.init.
            location (str):
                Optional.Location to run the custom job in. Overrides location set in aiplatform.init.
            credentials (auth_credentials.Credentials):
                Optional.Custom credentials to use to run call custom job service. Overrides
                credentials set in aiplatform.init.
            labels (Dict[str, str]):
                Optional. The labels with user-defined metadata to
                organize CustomJobs.
                Label keys and values can be no longer than 64
                characters (Unicode codepoints), can only
                contain lowercase letters, numeric characters,
                underscores and dashes. International characters
                are allowed.
                See https://goo.gl/xmQnxf for more information
                and examples of labels.
            encryption_spec_key_name (str):
                Optional.Customer-managed encryption key name for a
                CustomJob. If this is set, then all resources
                created by the CustomJob will be encrypted with
                the provided encryption key.
            staging_bucket (str):
                Optional. Bucket for produced custom job artifacts. Overrides
                staging_bucket set in aiplatform.init.

        Raises:
            RuntimeError: If staging bucket was not set using aiplatform.init and a staging
            bucket was not passed in.
        """

        super().__init__(project=project, location=location, credentials=credentials)

        staging_bucket = staging_bucket or initializer.global_config.staging_bucket

        if not staging_bucket:
            raise RuntimeError(
                "staging_bucket should be passed to CustomJob constructor or "
                "should be set using aiplatform.init(staging_bucket='gs://my-bucket')"
            )

        if labels:
            utils.validate_labels(labels)

        # default directory if not given
        base_output_dir = base_output_dir or utils._timestamped_gcs_dir(
            staging_bucket, "aiplatform-custom-job"
        )

        if not display_name:
            display_name = self.__class__._generate_display_name()

        self._gca_resource = gca_custom_job_compat.CustomJob(
            display_name=display_name,
            job_spec=gca_custom_job_compat.CustomJobSpec(
                worker_pool_specs=worker_pool_specs,
                base_output_directory=gca_io_compat.GcsDestination(
                    output_uri_prefix=base_output_dir
                ),
            ),
            labels=labels,
            encryption_spec=initializer.global_config.get_encryption_spec(
                encryption_spec_key_name=encryption_spec_key_name
            ),
        )

    @property
    def network(self) -> Optional[str]:
        """The full name of the Google Compute Engine
        [network](https://cloud.google.com/vpc/docs/vpc#networks) to which this
        CustomJob should be peered.

        Takes the format `projects/{project}/global/networks/{network}`. Where
        {project} is a project number, as in `12345`, and {network} is a network name.

        Private services access must already be configured for the network. If left
        unspecified, the CustomJob is not peered with any network.
        """
        self._assert_gca_resource_is_available()
        return self._gca_resource.job_spec.network

    def _get_web_access_uris(self) -> Dict[str, str]:
        """Helper method to get the web access uris of the custom job

        Returns:
            (Dict[str, str]):
                Web access uris of the custom job.
        """
        return dict(self._gca_resource.web_access_uris)

    def _log_web_access_uris(self):
        """Helper method to log the web access uris of the custom job"""

        for worker, uri in self._get_web_access_uris().items():
            if uri not in self._logged_web_access_uris:
                _LOGGER.info(
                    "%s %s access the interactive shell terminals for the custom job:\n%s:\n%s"
                    % (
                        self.__class__.__name__,
                        self._gca_resource.name,
                        worker,
                        uri,
                    ),
                )
                self._logged_web_access_uris.add(uri)

    @classmethod
    def from_local_script(
        cls,
        # TODO(b/223262536): Make display_name parameter fully optional in next major release
        display_name: str,
        script_path: str,
        container_uri: str,
        args: Optional[Sequence[str]] = None,
        requirements: Optional[Sequence[str]] = None,
        environment_variables: Optional[Dict[str, str]] = None,
        replica_count: int = 1,
        machine_type: str = "n1-standard-4",
        accelerator_type: str = "ACCELERATOR_TYPE_UNSPECIFIED",
        accelerator_count: int = 0,
        boot_disk_type: str = "pd-ssd",
        boot_disk_size_gb: int = 100,
        reduction_server_replica_count: int = 0,
        reduction_server_machine_type: Optional[str] = None,
        reduction_server_container_uri: Optional[str] = None,
        base_output_dir: Optional[str] = None,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        labels: Optional[Dict[str, str]] = None,
        encryption_spec_key_name: Optional[str] = None,
        staging_bucket: Optional[str] = None,
    ) -> "CustomJob":
        """Configures a custom job from a local script.

        Example usage:
        ```
        job = aiplatform.CustomJob.from_local_script(
            display_name="my-custom-job",
            script_path="training_script.py",
            container_uri="gcr.io/cloud-aiplatform/training/tf-cpu.2-2:latest",
            requirements=["gcsfs==0.7.1"],
            replica_count=1,
            args=['--dataset', 'gs://my-bucket/my-dataset',
            '--model_output_uri', 'gs://my-bucket/model']
            labels={'my_key': 'my_value'},
        )

        job.run()
        ```

        Args:
            display_name (str):
                Required. The user-defined name of this CustomJob.
            script_path (str):
                Required. Local path to training script.
            container_uri (str):
                Required. Uri of the training container image to use for custom job.
                Support images in Artifact Registry, Container Registry, or Docker Hub.
                Vertex AI provides a wide range of executor images with pre-installed
                packages to meet users' various use cases. See the list of `pre-built containers
                for training <https://cloud.google.com/vertex-ai/docs/training/pre-built-containers>`.
                If not using image from this list, please make sure python3 and pip3 are installed in your container.
            args (Optional[Sequence[str]]):
                Optional. Command line arguments to be passed to the Python task.
            requirements (Sequence[str]):
                Optional. List of python packages dependencies of script.
            environment_variables (Dict[str, str]):
                Optional. Environment variables to be passed to the container.
                Should be a dictionary where keys are environment variable names
                and values are environment variable values for those names.
                At most 10 environment variables can be specified.
                The Name of the environment variable must be unique.

                environment_variables = {
                    'MY_KEY': 'MY_VALUE'
                }
            replica_count (int):
                Optional. The number of worker replicas. If replica count = 1 then one chief
                replica will be provisioned. If replica_count > 1 the remainder will be
                provisioned as a worker replica pool.
            machine_type (str):
                Optional. The type of machine to use for training.
            accelerator_type (str):
                Optional. Hardware accelerator type. One of ACCELERATOR_TYPE_UNSPECIFIED,
                NVIDIA_TESLA_K80, NVIDIA_TESLA_P100, NVIDIA_TESLA_V100, NVIDIA_TESLA_P4,
                NVIDIA_TESLA_T4
            accelerator_count (int):
                Optional. The number of accelerators to attach to a worker replica.
            boot_disk_type (str):
                Optional. Type of the boot disk, default is `pd-ssd`.
                Valid values: `pd-ssd` (Persistent Disk Solid State Drive) or
                `pd-standard` (Persistent Disk Hard Disk Drive).
            boot_disk_size_gb (int):
                Optional. Size in GB of the boot disk, default is 100GB.
                boot disk size must be within the range of [100, 64000].
            reduction_server_replica_count (int):
                The number of reduction server replicas, default is 0.
            reduction_server_machine_type (str):
                Optional. The type of machine to use for reduction server.
            reduction_server_container_uri (str):
                Optional. The Uri of the reduction server container image.
                See details: https://cloud.google.com/vertex-ai/docs/training/distributed-training#reduce_training_time_with_reduction_server
            base_output_dir (str):
                Optional. GCS output directory of job. If not provided a
                timestamped directory in the staging directory will be used.
            project (str):
                Optional. Project to run the custom job in. Overrides project set in aiplatform.init.
            location (str):
                Optional. Location to run the custom job in. Overrides location set in aiplatform.init.
            credentials (auth_credentials.Credentials):
                Optional. Custom credentials to use to run call custom job service. Overrides
                credentials set in aiplatform.init.
            labels (Dict[str, str]):
                Optional. The labels with user-defined metadata to
                organize CustomJobs.
                Label keys and values can be no longer than 64
                characters (Unicode codepoints), can only
                contain lowercase letters, numeric characters,
                underscores and dashes. International characters
                are allowed.
                See https://goo.gl/xmQnxf for more information
                and examples of labels.
            encryption_spec_key_name (str):
                Optional. Customer-managed encryption key name for a
                CustomJob. If this is set, then all resources
                created by the CustomJob will be encrypted with
                the provided encryption key.
            staging_bucket (str):
                Optional. Bucket for produced custom job artifacts. Overrides
                staging_bucket set in aiplatform.init.

        Raises:
            RuntimeError: If staging bucket was not set using aiplatform.init and a staging
            bucket was not passed in.
        """

        project = project or initializer.global_config.project
        location = location or initializer.global_config.location
        staging_bucket = staging_bucket or initializer.global_config.staging_bucket

        if not staging_bucket:
            raise RuntimeError(
                "staging_bucket should be passed to CustomJob.from_local_script or "
                "should be set using aiplatform.init(staging_bucket='gs://my-bucket')"
            )

        if labels:
            utils.validate_labels(labels)

        worker_pool_specs = (
            worker_spec_utils._DistributedTrainingSpec.chief_worker_pool(
                replica_count=replica_count,
                machine_type=machine_type,
                accelerator_count=accelerator_count,
                accelerator_type=accelerator_type,
                boot_disk_type=boot_disk_type,
                boot_disk_size_gb=boot_disk_size_gb,
                reduction_server_replica_count=reduction_server_replica_count,
                reduction_server_machine_type=reduction_server_machine_type,
            ).pool_specs
        )

        python_packager = source_utils._TrainingScriptPythonPackager(
            script_path=script_path, requirements=requirements
        )

        package_gcs_uri = python_packager.package_and_copy_to_gcs(
            gcs_staging_dir=staging_bucket,
            project=project,
            credentials=credentials,
        )

        for spec_order, spec in enumerate(worker_pool_specs):

            if not spec:
                continue

            if (
                spec_order == worker_spec_utils._SPEC_ORDERS["server_spec"]
                and reduction_server_replica_count > 0
            ):
                spec["container_spec"] = {
                    "image_uri": reduction_server_container_uri,
                }
            ## check if the container is pre-built
            elif ("docker.pkg.dev/vertex-ai/" in container_uri) or (
                "gcr.io/cloud-aiplatform/" in container_uri
            ):
                spec["python_package_spec"] = {
                    "executor_image_uri": container_uri,
                    "python_module": python_packager.module_name,
                    "package_uris": [package_gcs_uri],
                }

                if args:
                    spec["python_package_spec"]["args"] = args

                if environment_variables:
                    spec["python_package_spec"]["env"] = [
                        {"name": key, "value": value}
                        for key, value in environment_variables.items()
                    ]
            else:
                command = [
                    "sh",
                    "-c",
                    "pip install --upgrade pip && "
                    + f"pip3 install -q --user {package_gcs_uri} && ".replace(
                        "gs://", "/gcs/"
                    )
                    + f"python3 -m {python_packager.module_name}",
                ]

                spec["container_spec"] = {
                    "image_uri": container_uri,
                    "command": command,
                }

                if args:
                    spec["container_spec"]["args"] = args

                if environment_variables:
                    spec["container_spec"]["env"] = [
                        {"name": key, "value": value}
                        for key, value in environment_variables.items()
                    ]

        return cls(
            display_name=display_name,
            worker_pool_specs=worker_pool_specs,
            base_output_dir=base_output_dir,
            project=project,
            location=location,
            credentials=credentials,
            labels=labels,
            encryption_spec_key_name=encryption_spec_key_name,
            staging_bucket=staging_bucket,
        )

    def run(
        self,
        service_account: Optional[str] = None,
        network: Optional[str] = None,
        timeout: Optional[int] = None,
        restart_job_on_worker_restart: bool = False,
        enable_web_access: bool = False,
        tensorboard: Optional[str] = None,
        sync: bool = True,
        create_request_timeout: Optional[float] = None,
    ) -> None:
        """Run this configured CustomJob.

        Args:
            service_account (str):
                Optional. Specifies the service account for workload run-as account.
                Users submitting jobs must have act-as permission on this run-as account.
            network (str):
                Optional. The full name of the Compute Engine network to which the job
                should be peered. For example, projects/12345/global/networks/myVPC.
                Private services access must already be configured for the network.
                If left unspecified, the network set in aiplatform.init will be used.
                Otherwise, the job is not peered with any network.
            timeout (int):
                The maximum job running time in seconds. The default is 7 days.
            restart_job_on_worker_restart (bool):
                Restarts the entire CustomJob if a worker
                gets restarted. This feature can be used by
                distributed training jobs that are not resilient
                to workers leaving and joining a job.
            enable_web_access (bool):
                Whether you want Vertex AI to enable interactive shell access
                to training containers.
                https://cloud.google.com/vertex-ai/docs/training/monitor-debug-interactive-shell
            tensorboard (str):
                Optional. The name of a Vertex AI
                [Tensorboard][google.cloud.aiplatform.v1beta1.Tensorboard]
                resource to which this CustomJob will upload Tensorboard
                logs. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}``

                The training script should write Tensorboard to following Vertex AI environment
                variable:

                AIP_TENSORBOARD_LOG_DIR

                `service_account` is required with provided `tensorboard`.
                For more information on configuring your service account please visit:
                https://cloud.google.com/vertex-ai/docs/experiments/tensorboard-training
            sync (bool):
                Whether to execute this method synchronously. If False, this method
                will unblock and it will be executed in a concurrent Future.
            create_request_timeout (float):
                Optional. The timeout for the create request in seconds.
        """
        network = network or initializer.global_config.network

        self._run(
            service_account=service_account,
            network=network,
            timeout=timeout,
            restart_job_on_worker_restart=restart_job_on_worker_restart,
            enable_web_access=enable_web_access,
            tensorboard=tensorboard,
            sync=sync,
            create_request_timeout=create_request_timeout,
        )

    @base.optional_sync()
    def _run(
        self,
        service_account: Optional[str] = None,
        network: Optional[str] = None,
        timeout: Optional[int] = None,
        restart_job_on_worker_restart: bool = False,
        enable_web_access: bool = False,
        tensorboard: Optional[str] = None,
        sync: bool = True,
        create_request_timeout: Optional[float] = None,
    ) -> None:
        """Helper method to ensure network synchronization and to run the configured CustomJob.

        Args:
            service_account (str):
                Optional. Specifies the service account for workload run-as account.
                Users submitting jobs must have act-as permission on this run-as account.
            network (str):
                Optional. The full name of the Compute Engine network to which the job
                should be peered. For example, projects/12345/global/networks/myVPC.
                Private services access must already be configured for the network.
            timeout (int):
                The maximum job running time in seconds. The default is 7 days.
            restart_job_on_worker_restart (bool):
                Restarts the entire CustomJob if a worker
                gets restarted. This feature can be used by
                distributed training jobs that are not resilient
                to workers leaving and joining a job.
            enable_web_access (bool):
                Whether you want Vertex AI to enable interactive shell access
                to training containers.
                https://cloud.google.com/vertex-ai/docs/training/monitor-debug-interactive-shell
            tensorboard (str):
                Optional. The name of a Vertex AI
                [Tensorboard][google.cloud.aiplatform.v1beta1.Tensorboard]
                resource to which this CustomJob will upload Tensorboard
                logs. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}``

                The training script should write Tensorboard to following Vertex AI environment
                variable:

                AIP_TENSORBOARD_LOG_DIR

                `service_account` is required with provided `tensorboard`.
                For more information on configuring your service account please visit:
                https://cloud.google.com/vertex-ai/docs/experiments/tensorboard-training
            sync (bool):
                Whether to execute this method synchronously. If False, this method
                will unblock and it will be executed in a concurrent Future.
            create_request_timeout (float):
                Optional. The timeout for the create request in seconds.
        """
        if service_account:
            self._gca_resource.job_spec.service_account = service_account

        if network:
            self._gca_resource.job_spec.network = network

        if timeout or restart_job_on_worker_restart:
            timeout = duration_pb2.Duration(seconds=timeout) if timeout else None
            self._gca_resource.job_spec.scheduling = gca_custom_job_compat.Scheduling(
                timeout=timeout,
                restart_job_on_worker_restart=restart_job_on_worker_restart,
            )

        if enable_web_access:
            self._gca_resource.job_spec.enable_web_access = enable_web_access

        if tensorboard:
            self._gca_resource.job_spec.tensorboard = tensorboard

        _LOGGER.log_create_with_lro(self.__class__)

        self._gca_resource = self.api_client.create_custom_job(
            parent=self._parent,
            custom_job=self._gca_resource,
            timeout=create_request_timeout,
        )

        _LOGGER.log_create_complete_with_getter(
            self.__class__, self._gca_resource, "custom_job"
        )

        _LOGGER.info("View Custom Job:\n%s" % self._dashboard_uri())

        if tensorboard:
            _LOGGER.info(
                "View Tensorboard:\n%s"
                % console_utils.custom_job_tensorboard_console_uri(
                    tensorboard, self.resource_name
                )
            )

        self._block_until_complete()

    @property
    def job_spec(self):
        return self._gca_resource.job_spec


_SEARCH_ALGORITHM_TO_PROTO_VALUE = {
    "random": gca_study_compat.StudySpec.Algorithm.RANDOM_SEARCH,
    "grid": gca_study_compat.StudySpec.Algorithm.GRID_SEARCH,
    None: gca_study_compat.StudySpec.Algorithm.ALGORITHM_UNSPECIFIED,
}

_MEASUREMENT_SELECTION_TO_PROTO_VALUE = {
    "best": gca_study_compat.StudySpec.MeasurementSelectionType.BEST_MEASUREMENT,
    "last": gca_study_compat.StudySpec.MeasurementSelectionType.LAST_MEASUREMENT,
}


class HyperparameterTuningJob(_RunnableJob):
    """Vertex AI Hyperparameter Tuning Job."""

    _resource_noun = "hyperparameterTuningJobs"
    _getter_method = "get_hyperparameter_tuning_job"
    _list_method = "list_hyperparameter_tuning_jobs"
    _cancel_method = "cancel_hyperparameter_tuning_job"
    _delete_method = "delete_hyperparameter_tuning_job"
    _parse_resource_name_method = "parse_hyperparameter_tuning_job_path"
    _format_resource_name_method = "hyperparameter_tuning_job_path"
    _job_type = "training"

    def __init__(
        self,
        # TODO(b/223262536): Make display_name parameter fully optional in next major release
        display_name: str,
        custom_job: CustomJob,
        metric_spec: Dict[str, str],
        parameter_spec: Dict[str, hyperparameter_tuning._ParameterSpec],
        max_trial_count: int,
        parallel_trial_count: int,
        max_failed_trial_count: int = 0,
        search_algorithm: Optional[str] = None,
        measurement_selection: Optional[str] = "best",
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        labels: Optional[Dict[str, str]] = None,
        encryption_spec_key_name: Optional[str] = None,
    ):
        """
        Configures a HyperparameterTuning Job.

        Example usage:

        ```
        from google.cloud.aiplatform import hyperparameter_tuning as hpt

        worker_pool_specs = [
                {
                    "machine_spec": {
                        "machine_type": "n1-standard-4",
                        "accelerator_type": "NVIDIA_TESLA_K80",
                        "accelerator_count": 1,
                    },
                    "replica_count": 1,
                    "container_spec": {
                        "image_uri": container_image_uri,
                        "command": [],
                        "args": [],
                    },
                }
            ]

        custom_job = aiplatform.CustomJob(
            display_name='my_job',
            worker_pool_specs=worker_pool_specs,
            labels={'my_key': 'my_value'},
        )


        hp_job = aiplatform.HyperparameterTuningJob(
            display_name='hp-test',
            custom_job=job,
            metric_spec={
                'loss': 'minimize',
            },
            parameter_spec={
                'lr': hpt.DoubleParameterSpec(min=0.001, max=0.1, scale='log'),
                'units': hpt.IntegerParameterSpec(min=4, max=128, scale='linear'),
                'activation': hpt.CategoricalParameterSpec(values=['relu', 'selu']),
                'batch_size': hpt.DiscreteParameterSpec(values=[128, 256], scale='linear')
            },
            max_trial_count=128,
            parallel_trial_count=8,
            labels={'my_key': 'my_value'},
            )

        hp_job.run()

        print(hp_job.trials)
        ```


        For more information on using hyperparameter tuning please visit:
        https://cloud.google.com/ai-platform-unified/docs/training/using-hyperparameter-tuning

        Args:
            display_name (str):
                Required. The user-defined name of the HyperparameterTuningJob.
                The name can be up to 128 characters long and can be consist
                of any UTF-8 characters.
            custom_job (aiplatform.CustomJob):
                Required. Configured CustomJob. The worker pool spec from this custom job
                applies to the CustomJobs created in all the trials.
            metric_spec: Dict[str, str]
                Required. Dictionary representing metrics to optimize. The dictionary key is the metric_id,
                which is reported by your training job, and the dictionary value is the
                optimization goal of the metric('minimize' or 'maximize'). example:

                metric_spec = {'loss': 'minimize', 'accuracy': 'maximize'}

            parameter_spec (Dict[str, hyperparameter_tuning._ParameterSpec]):
                Required. Dictionary representing parameters to optimize. The dictionary key is the metric_id,
                which is passed into your training job as a command line key word argument, and the
                dictionary value is the parameter specification of the metric.


                from google.cloud.aiplatform import hyperparameter_tuning as hpt

                parameter_spec={
                    'decay': hpt.DoubleParameterSpec(min=1e-7, max=1, scale='linear'),
                    'learning_rate': hpt.DoubleParameterSpec(min=1e-7, max=1, scale='linear')
                    'batch_size': hpt.DiscreteParamterSpec(values=[4, 8, 16, 32, 64, 128], scale='linear')
                }

                Supported parameter specifications can be found until aiplatform.hyperparameter_tuning.
                These parameter specification are currently supported:
                DoubleParameterSpec, IntegerParameterSpec, CategoricalParameterSpace, DiscreteParameterSpec

            max_trial_count (int):
                Required. The desired total number of Trials.
            parallel_trial_count (int):
                Required. The desired number of Trials to run in parallel.
            max_failed_trial_count (int):
                Optional. The number of failed Trials that need to be
                seen before failing the HyperparameterTuningJob.
                If set to 0, Vertex AI decides how many Trials
                must fail before the whole job fails.
            search_algorithm (str):
                The search algorithm specified for the Study.
                Accepts one of the following:
                    `None` - If you do not specify an algorithm, your job uses
                    the default Vertex AI algorithm. The default algorithm
                    applies Bayesian optimization to arrive at the optimal
                    solution with a more effective search over the parameter space.

                    'grid' - A simple grid search within the feasible space. This
                    option is particularly useful if you want to specify a quantity
                    of trials that is greater than the number of points in the
                    feasible space. In such cases, if you do not specify a grid
                    search, the Vertex AI default algorithm may generate duplicate
                    suggestions. To use grid search, all parameter specs must be
                    of type `IntegerParameterSpec`, `CategoricalParameterSpace`,
                    or `DiscreteParameterSpec`.

                    'random' - A simple random search within the feasible space.
            measurement_selection (str):
                This indicates which measurement to use if/when the service
                automatically selects the final measurement from previously reported
                intermediate measurements.

                Accepts: 'best', 'last'

                Choose this based on two considerations:
                A) Do you expect your measurements to monotonically improve? If so,
                choose 'last'. On the other hand, if you're in a situation
                where your system can "over-train" and you expect the performance to
                get better for a while but then start declining, choose
                'best'. B) Are your measurements significantly noisy
                and/or irreproducible? If so, 'best' will tend to be
                over-optimistic, and it may be better to choose 'last'. If
                both or neither of (A) and (B) apply, it doesn't matter which
                selection type is chosen.
            project (str):
                Optional. Project to run the HyperparameterTuningjob in. Overrides project set in aiplatform.init.
            location (str):
                Optional. Location to run the HyperparameterTuning in. Overrides location set in aiplatform.init.
            credentials (auth_credentials.Credentials):
                Optional. Custom credentials to use to run call HyperparameterTuning service. Overrides
                credentials set in aiplatform.init.
            labels (Dict[str, str]):
                Optional. The labels with user-defined metadata to
                organize HyperparameterTuningJobs.
                Label keys and values can be no longer than 64
                characters (Unicode codepoints), can only
                contain lowercase letters, numeric characters,
                underscores and dashes. International characters
                are allowed.
                See https://goo.gl/xmQnxf for more information
                and examples of labels.
            encryption_spec_key_name (str):
                Optional. Customer-managed encryption key options for a
                HyperparameterTuningJob. If this is set, then
                all resources created by the
                HyperparameterTuningJob will be encrypted with
                the provided encryption key.
        """
        super().__init__(project=project, location=location, credentials=credentials)

        metrics = [
            gca_study_compat.StudySpec.MetricSpec(
                metric_id=metric_id, goal=goal.upper()
            )
            for metric_id, goal in metric_spec.items()
        ]

        parameters = [
            parameter._to_parameter_spec(parameter_id=parameter_id)
            for parameter_id, parameter in parameter_spec.items()
        ]

        study_spec = gca_study_compat.StudySpec(
            metrics=metrics,
            parameters=parameters,
            algorithm=_SEARCH_ALGORITHM_TO_PROTO_VALUE[search_algorithm],
            measurement_selection_type=_MEASUREMENT_SELECTION_TO_PROTO_VALUE[
                measurement_selection
            ],
        )

        if not display_name:
            display_name = self.__class__._generate_display_name()

        self._gca_resource = (
            gca_hyperparameter_tuning_job_compat.HyperparameterTuningJob(
                display_name=display_name,
                study_spec=study_spec,
                max_trial_count=max_trial_count,
                parallel_trial_count=parallel_trial_count,
                max_failed_trial_count=max_failed_trial_count,
                trial_job_spec=copy.deepcopy(custom_job.job_spec),
                labels=labels,
                encryption_spec=initializer.global_config.get_encryption_spec(
                    encryption_spec_key_name=encryption_spec_key_name
                ),
            )
        )

    @property
    def network(self) -> Optional[str]:
        """The full name of the Google Compute Engine
        [network](https://cloud.google.com/vpc/docs/vpc#networks) to which this
        HyperparameterTuningJob should be peered.

        Takes the format `projects/{project}/global/networks/{network}`. Where
        {project} is a project number, as in `12345`, and {network} is a network name.

        Private services access must already be configured for the network. If left
        unspecified, the HyperparameterTuningJob is not peered with any network.
        """
        self._assert_gca_resource_is_available()
        return getattr(self._gca_resource.trial_job_spec, "network")

    def _get_web_access_uris(self) -> Dict[str, Dict[str, str]]:
        """Helper method to get the web access uris of the hyperparameter job

        Returns:
            (Dict[str, Dict[str, str]]):
                Web access uris of the hyperparameter job.
        """
        web_access_uris = dict()
        for trial in self.trials:
            web_access_uris[trial.id] = web_access_uris.get(trial.id, dict())
            for worker, uri in trial.web_access_uris.items():
                web_access_uris[trial.id][worker] = uri
        return web_access_uris

    def _log_web_access_uris(self):
        """Helper method to log the web access uris of the hyperparameter job"""

        for trial_id, trial_web_access_uris in self._get_web_access_uris().items():
            for worker, uri in trial_web_access_uris.items():
                if uri not in self._logged_web_access_uris:
                    _LOGGER.info(
                        "%s %s access the interactive shell terminals for trial - %s:\n%s:\n%s"
                        % (
                            self.__class__.__name__,
                            self._gca_resource.name,
                            trial_id,
                            worker,
                            uri,
                        ),
                    )
                    self._logged_web_access_uris.add(uri)

    def run(
        self,
        service_account: Optional[str] = None,
        network: Optional[str] = None,
        timeout: Optional[int] = None,  # seconds
        restart_job_on_worker_restart: bool = False,
        enable_web_access: bool = False,
        tensorboard: Optional[str] = None,
        sync: bool = True,
        create_request_timeout: Optional[float] = None,
    ) -> None:
        """Run this configured CustomJob.

        Args:
            service_account (str):
                Optional. Specifies the service account for workload run-as account.
                Users submitting jobs must have act-as permission on this run-as account.
            network (str):
                Optional. The full name of the Compute Engine network to which the job
                should be peered. For example, projects/12345/global/networks/myVPC.
                Private services access must already be configured for the network.
                If left unspecified, the network set in aiplatform.init will be used.
                Otherwise, the job is not peered with any network.
            timeout (int):
                Optional. The maximum job running time in seconds. The default is 7 days.
            restart_job_on_worker_restart (bool):
                Restarts the entire CustomJob if a worker
                gets restarted. This feature can be used by
                distributed training jobs that are not resilient
                to workers leaving and joining a job.
            enable_web_access (bool):
                Whether you want Vertex AI to enable interactive shell access
                to training containers.
                https://cloud.google.com/vertex-ai/docs/training/monitor-debug-interactive-shell
            tensorboard (str):
                Optional. The name of a Vertex AI
                [Tensorboard][google.cloud.aiplatform.v1beta1.Tensorboard]
                resource to which this CustomJob will upload Tensorboard
                logs. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}``

                The training script should write Tensorboard to following Vertex AI environment
                variable:

                AIP_TENSORBOARD_LOG_DIR

                `service_account` is required with provided `tensorboard`.
                For more information on configuring your service account please visit:
                https://cloud.google.com/vertex-ai/docs/experiments/tensorboard-training
            sync (bool):
                Whether to execute this method synchronously. If False, this method
                will unblock and it will be executed in a concurrent Future.
            create_request_timeout (float):
                Optional. The timeout for the create request in seconds.
        """
        network = network or initializer.global_config.network

        self._run(
            service_account=service_account,
            network=network,
            timeout=timeout,
            restart_job_on_worker_restart=restart_job_on_worker_restart,
            enable_web_access=enable_web_access,
            tensorboard=tensorboard,
            sync=sync,
            create_request_timeout=create_request_timeout,
        )

    @base.optional_sync()
    def _run(
        self,
        service_account: Optional[str] = None,
        network: Optional[str] = None,
        timeout: Optional[int] = None,  # seconds
        restart_job_on_worker_restart: bool = False,
        enable_web_access: bool = False,
        tensorboard: Optional[str] = None,
        sync: bool = True,
        create_request_timeout: Optional[float] = None,
    ) -> None:
        """Helper method to ensure network synchronization and to run the configured CustomJob.

        Args:
            service_account (str):
                Optional. Specifies the service account for workload run-as account.
                Users submitting jobs must have act-as permission on this run-as account.
            network (str):
                Optional. The full name of the Compute Engine network to which the job
                should be peered. For example, projects/12345/global/networks/myVPC.
                Private services access must already be configured for the network.
            timeout (int):
                Optional. The maximum job running time in seconds. The default is 7 days.
            restart_job_on_worker_restart (bool):
                Restarts the entire CustomJob if a worker
                gets restarted. This feature can be used by
                distributed training jobs that are not resilient
                to workers leaving and joining a job.
            enable_web_access (bool):
                Whether you want Vertex AI to enable interactive shell access
                to training containers.
                https://cloud.google.com/vertex-ai/docs/training/monitor-debug-interactive-shell
            tensorboard (str):
                Optional. The name of a Vertex AI
                [Tensorboard][google.cloud.aiplatform.v1beta1.Tensorboard]
                resource to which this CustomJob will upload Tensorboard
                logs. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}``

                The training script should write Tensorboard to following Vertex AI environment
                variable:

                AIP_TENSORBOARD_LOG_DIR

                `service_account` is required with provided `tensorboard`.
                For more information on configuring your service account please visit:
                https://cloud.google.com/vertex-ai/docs/experiments/tensorboard-training
            sync (bool):
                Whether to execute this method synchronously. If False, this method
                will unblock and it will be executed in a concurrent Future.
            create_request_timeout (float):
                Optional. The timeout for the create request in seconds.
        """
        if service_account:
            self._gca_resource.trial_job_spec.service_account = service_account

        if network:
            self._gca_resource.trial_job_spec.network = network

        if timeout or restart_job_on_worker_restart:
            duration = duration_pb2.Duration(seconds=timeout) if timeout else None
            self._gca_resource.trial_job_spec.scheduling = (
                gca_custom_job_compat.Scheduling(
                    timeout=duration,
                    restart_job_on_worker_restart=restart_job_on_worker_restart,
                )
            )

        if enable_web_access:
            self._gca_resource.trial_job_spec.enable_web_access = enable_web_access

        if tensorboard:
            self._gca_resource.trial_job_spec.tensorboard = tensorboard

        _LOGGER.log_create_with_lro(self.__class__)

        self._gca_resource = self.api_client.create_hyperparameter_tuning_job(
            parent=self._parent,
            hyperparameter_tuning_job=self._gca_resource,
            timeout=create_request_timeout,
        )

        _LOGGER.log_create_complete_with_getter(
            self.__class__, self._gca_resource, "hpt_job"
        )

        _LOGGER.info("View HyperparameterTuningJob:\n%s" % self._dashboard_uri())

        if tensorboard:
            _LOGGER.info(
                "View Tensorboard:\n%s"
                % console_utils.custom_job_tensorboard_console_uri(
                    tensorboard, self.resource_name
                )
            )

        self._block_until_complete()

    @property
    def trials(self) -> List[gca_study_compat.Trial]:
        self._assert_gca_resource_is_available()
        return list(self._gca_resource.trials)


class ModelDeploymentMonitoringJob(_Job):
    """Vertex AI Model Deployment Monitoring Job.

    This class should be used in conjunction with the Endpoint class
    in order to configure model monitoring for deployed models.
    """

    _resource_noun = "modelDeploymentMonitoringJobs"
    _getter_method = "get_model_deployment_monitoring_job"
    _list_method = "list_model_deployment_monitoring_jobs"
    _cancel_method = "cancel_model_deployment_monitoring_jobs"
    _delete_method = "delete_model_deployment_monitoring_job"
    _job_type = "model-deployment-monitoring"
    _parse_resource_name_method = "parse_model_deployment_monitoring_job_path"
    _format_resource_name_method = "model_deployment_monitoring_job_path"

    def __init__(
        self,
        model_deployment_monitoring_job_name: str,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
    ):
        """Initializer for ModelDeploymentMonitoringJob.

        Args:
            model_deployment_monitoring_job_name (str):
                Required. A fully-qualified ModelDeploymentMonitoringJob resource name or ID.
                Example: "projects/.../locations/.../modelDeploymentMonitoringJobs/456" or
                "456" when project and location are initialized or passed.
            project: (str),
                Optional. project to retrieve ModelDeploymentMonitoringJob from. If not set,
                project set in aiplatform.init will be used.
            location: (str),
                Optional. location to retrieve ModelDeploymentMonitoringJob from. If not set,
                location set in aiplatform.init will be used.
            credentials: (auth_credentials.Credentials),
                Optional. Custom credentials to use. If not set, credentials set in
                aiplatform.init will be used.
        """
        super().__init__(
            job_name=model_deployment_monitoring_job_name,
            project=project,
            location=location,
            credentials=credentials,
        )
        self._gca_resource = self._get_gca_resource(
            resource_name=model_deployment_monitoring_job_name
        )

    @classmethod
    def _parse_configs(
        cls,
        objective_configs: Union[
            model_monitoring.ObjectiveConfig,
            Dict[str, model_monitoring.ObjectiveConfig],
        ],
        endpoint: "aiplatform.Endpoint",
        deployed_model_ids: Optional[List[str]] = None,
    ) -> List[
        gca_model_deployment_monitoring_job_compat.ModelDeploymentMonitoringObjectiveConfig
    ]:
        """Helper function for matching objective configs with their corresponding models.

        Args:
            objective_configs (Union[model_monitoring.objective.ObjectiveConfig,
                Dict[str, model_monitoring.objective.ObjectiveConfig]):
                Required. A single config if it applies to all models, or a dictionary of
                model_id: model_monitoring.objective.ObjectiveConfig if
                different model IDs have different configs.
            endpoint (aiplatform.Endpoint):
                Required. A valid instance of aiplatforn.Endpoint to launch the MDM job on.
            deployed_model_ids (Optional[List[str]]):
                Optional. A list of deployed model IDs to apply the objective config to.
                Note that a model will have a deployed_model_id that is different from the
                uploaded model ID, and IDs in this list should consist of deployed model IDs
                on the same endpoint passed in the argument. If `objective_configs` is a dictionary,
                then this parameter is ignored. If `objective_configs` is an instance of
                `model_monitoring.ObjectiveConfig` and `deployed_model_ids` is a non-empty
                list of valid IDs, then the same objective config will apply to all models in this list.

        Returns:
            A List of ModelDeploymentMonitoringObjectiveConfig objects.

        Raises:
            ValueError, when the model IDs given are invalid.
            RuntimeError, when XAI is enabled on a model that doesn't have XAI parameters configured.
        """
        all_models = []
        xai_enabled = []
        for model in endpoint.list_models():
            all_models.append(model.id)
            if str(model.explanation_spec.parameters) != "":
                xai_enabled.append(model.id)

        all_configs = []

        ## when same objective config is applied to SOME or ALL models
        if deployed_model_ids is not None:
            if not all(model in all_models for model in deployed_model_ids):
                error_string = (
                    "Invalid model ID. The model ID must be one of ["
                    + ",".join(all_models)
                    + "]. Note that deployed model IDs are different from the uploaded model's ID"
                )
                raise ValueError(error_string)
            else:
                all_models = deployed_model_ids

        if isinstance(objective_configs, model_monitoring.ObjectiveConfig):
            for model in all_models:
                if (
                    model not in xai_enabled
                    and objective_configs.explanation_config is not None
                ):
                    raise RuntimeError(
                        "Invalid config for model ID %s. `explanation_config` should only be enabled if the model has `explanation_spec populated"
                        % model
                    )
                all_configs.append(
                    gca_model_deployment_monitoring_job_compat.ModelDeploymentMonitoringObjectiveConfig(
                        deployed_model_id=model,
                        objective_config=objective_configs.as_proto(),
                    )
                )

        ## when different objective configs are applied to EACH model
        else:
            if not all(model in all_models for model in objective_configs.keys()):
                error_string = (
                    "Invalid model ID. The model ID must be one of ["
                    + ",".join(all_models)
                    + "]. Note that deployed model IDs are different from the uploaded model's ID"
                )
                raise ValueError(error_string)
            for (deployed_model, objective_config) in objective_configs.items():
                if (
                    deployed_model not in xai_enabled
                    and objective_config.explanation_config is not None
                ):
                    raise RuntimeError(
                        "Invalid config for model ID %s. `explanation_config` should only be enabled if the model has `explanation_spec populated"
                        % deployed_model
                    )
                all_configs.append(
                    gca_model_deployment_monitoring_job_compat.ModelDeploymentMonitoringObjectiveConfig(
                        deployed_model_id=deployed_model,
                        objective_config=objective_config.as_proto(),
                    )
                )

        return all_configs

    @classmethod
    def create(
        cls,
        endpoint: Union[str, "aiplatform.Endpoint"],
        objective_configs: Optional[
            Union[
                model_monitoring.ObjectiveConfig,
                Dict[str, model_monitoring.ObjectiveConfig],
            ]
        ] = None,
        logging_sampling_strategy: Optional[model_monitoring.RandomSampleConfig] = None,
        schedule_config: Optional[model_monitoring.ScheduleConfig] = None,
        display_name: Optional[str] = None,
        deployed_model_ids: Optional[List[str]] = None,
        alert_config: Optional[model_monitoring.EmailAlertConfig] = None,
        predict_instance_schema_uri: Optional[str] = None,
        sample_predict_instance: Optional[str] = None,
        analysis_instance_schema_uri: Optional[str] = None,
        bigquery_tables_log_ttl: Optional[int] = None,
        stats_anomalies_base_directory: Optional[str] = None,
        enable_monitoring_pipeline_logs: Optional[bool] = None,
        labels: Optional[Dict[str, str]] = None,
        encryption_spec_key_name: Optional[str] = None,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
        create_request_timeout: Optional[float] = None,
    ) -> "ModelDeploymentMonitoringJob":
        """Creates and launches a model monitoring job.

        Args:
            endpoint (Union[str, "aiplatform.Endpoint"]):
                Required. Endpoint resource name or an instance of `aiplatform.Endpoint`. Format:
                ``projects/{project}/locations/{location}/endpoints/{endpoint}``

            objective_configs (Union[model_monitoring.ObjectiveConfig,
                Dict[str, model_monitoring.ObjectiveConfig]]):
                Required. A single config if it applies to all models, or a dictionary of
                model_id: model_monitoring.objective.ObjectiveConfig if
                different model IDs have different configs.

            logging_sampling_strategy (model_monitoring.sampling.RandomSampleConfig):
                Optional. Sample Strategy for logging.

            schedule_config (model_monitoring.schedule.ScheduleConfig):
                Optional. Configures model monitoring job scheduling interval in hours.
                This defines how often the monitoring jobs are triggered.

            display_name (str):
                Optional. The user-defined name of the
                ModelDeploymentMonitoringJob. The name can be up
                to 128 characters long and can be consist of any
                UTF-8 characters.
                Display name of a ModelDeploymentMonitoringJob.

            deployed_model_ids (List[str]):
                Optional. Use this argument to specify which deployed models to
                apply the objective config to. If left unspecified, the same config
                will be applied to all deployed models.

            alert_config (model_monitoring.alert.EmailAlertConfig):
                Optional. Configures how alerts are sent to the user. Right now
                only email alert is supported.

            predict_instance_schema_uri (str):
                Optional. YAML schema file uri describing the format of
                a single instance, which are given to format
                the Endpoint's prediction (and explanation). If
                not set, the schema will be generated from
                collected predict requests.

            sample_predict_instance (str):
                Optional. Sample Predict instance, same format as PredictionRequest.instances,
                this can be set as a replacement of predict_instance_schema_uri
                If not set, the schema will be generated from collected predict requests.

            analysis_instance_schema_uri (str):
                Optional. YAML schema file uri describing the format of a single
                instance that you want Tensorflow Data Validation (TFDV) to
                analyze. If this field is empty, all the feature data types are
                inferred from predict_instance_schema_uri, meaning that TFDV
                will use the data in the exact format as prediction request/response.
                If there are any data type differences between predict instance
                and TFDV instance, this field can be used to override the schema.
                For models trained with Vertex AI, this field must be set as all the
                fields in predict instance formatted as string.

            bigquery_tables_log_ttl (int):
                Optional. The TTL(time to live) of BigQuery tables in user projects
                which stores logs. A day is the basic unit of
                the TTL and we take the ceil of TTL/86400(a
                day). e.g. { second: 3600} indicates ttl = 1
                day.

            stats_anomalies_base_directory (str):
                Optional. Stats anomalies base folder path.

            enable_monitoring_pipeline_logs (bool):
                Optional. If true, the scheduled monitoring pipeline logs are sent to
                Google Cloud Logging, including pipeline status and
                anomalies detected. Please note the logs incur cost, which
                are subject to `Cloud Logging
                pricing <https://cloud.google.com/logging#pricing>`__.

            labels (Dict[str, str]):
                Optional. The labels with user-defined metadata to
                organize the ModelDeploymentMonitoringJob.
                Label keys and values can be no longer than 64
                characters (Unicode codepoints), can only
                contain lowercase letters, numeric characters,
                underscores and dashes. International characters
                are allowed. See https://goo.gl/xmQnxf for more information
                and examples of labels.

            encryption_spec_key_name (str):
                Optional. Customer-managed encryption key spec for a
                ModelDeploymentMonitoringJob. If set, this
                ModelDeploymentMonitoringJob and all
                sub-resources of this
                ModelDeploymentMonitoringJob will be secured by
                this key.

            create_request_timeout (int):
                Optional. Timeout in seconds for the model monitoring job creation request.

        Returns:
            An instance of ModelDeploymentMonitoringJob.
        """
        if not display_name:
            display_name = cls._generate_display_name()

        utils.validate_display_name(display_name)

        if labels:
            utils.validate_labels(labels)

        if stats_anomalies_base_directory:
            stats_anomalies_base_directory = gca_io_compat.GcsDestination(
                output_uri_prefix=stats_anomalies_base_directory
            )

        if encryption_spec_key_name:
            encryption_spec_key_name = gca_encryption_spec_compat.EncryptionSpec(
                kms_key_name=encryption_spec_key_name
            )

        if credentials is None and isinstance(endpoint, aiplatform.Endpoint):
            credentials = endpoint.credentials
        self = cls._empty_constructor(
            project=project, location=location, credentials=credentials
        )

        parent = initializer.global_config.common_location_path(
            project=self.project,
            location=self.location,
        )

        if isinstance(endpoint, str):
            endpoint = aiplatform.Endpoint(endpoint, project, location, credentials)

        mdm_objective_config_seq = cls._parse_configs(
            objective_configs,
            endpoint,
            deployed_model_ids,
        )

        gapic_mdm_job = (
            gca_model_deployment_monitoring_job_compat.ModelDeploymentMonitoringJob(
                display_name=display_name,
                endpoint=endpoint.resource_name,
                model_deployment_monitoring_objective_configs=mdm_objective_config_seq,
                logging_sampling_strategy=logging_sampling_strategy.as_proto(),
                model_deployment_monitoring_schedule_config=schedule_config.as_proto(),
                model_monitoring_alert_config=alert_config.as_proto(),
                predict_instance_schema_uri=predict_instance_schema_uri,
                analysis_instance_schema_uri=analysis_instance_schema_uri,
                sample_predict_instance=sample_predict_instance,
                stats_anomalies_base_directory=stats_anomalies_base_directory,
                enable_monitoring_pipeline_logs=enable_monitoring_pipeline_logs,
                labels=labels,
                encryption_spec=encryption_spec_key_name,
            )
        )

        _LOGGER.log_create_with_lro(cls)
        self._gca_resource = self.api_client.create_model_deployment_monitoring_job(
            parent=parent,
            model_deployment_monitoring_job=gapic_mdm_job,
            timeout=create_request_timeout,
        )

        _LOGGER.log_create_complete(cls, self._gca_resource, "mdm_job")

        _LOGGER.info(
            "View Model Deployment Monitoring Job:\n%s" % self._dashboard_uri()
        )

        return self

    @classmethod
    def cancel(cls):
        raise NotImplementedError(
            "Cancel method is not implemented because it is not applicable. A running model deployment monitoring job can be paused or deleted."
        )

    @property
    def end_time(self):
        _LOGGER.info(
            "Model deployment monitoring jobs do not have an end time since their inactive states are either PAUSED or PENDING."
        )
        return None

    def update(
        self,
        *,
        display_name: Optional[str] = None,
        schedule_config: Optional[model_monitoring.ScheduleConfig] = None,
        alert_config: Optional[model_monitoring.EmailAlertConfig] = None,
        logging_sampling_strategy: Optional[model_monitoring.RandomSampleConfig] = None,
        labels: Optional[Dict[str, str]] = None,
        bigquery_tables_log_ttl: Optional[int] = None,
        enable_monitoring_pipeline_logs: Optional[bool] = None,
        objective_configs: Optional[
            Union[
                model_monitoring.ObjectiveConfig,
                Dict[str, model_monitoring.ObjectiveConfig],
            ]
        ] = None,
        deployed_model_ids: Optional[List[str]] = None,
    ) -> "ModelDeploymentMonitoringJob":
        """Updates an existing ModelDeploymentMonitoringJob.

        Args:

            display_name (str):
                Optional. The user-defined name of the
                ModelDeploymentMonitoringJob. The name can be up
                to 128 characters long and can be consist of any
                UTF-8 characters.
                Display name of a ModelDeploymentMonitoringJob.

            schedule_config (model_monitoring.schedule.ScheduleConfig):
                Required. Configures model monitoring job scheduling interval in hours.
                This defines how often the monitoring jobs are triggered.
            alert_config (model_monitoring.alert.EmailAlertConfig):
                Optional. Configures how alerts are sent to the user. Right now
                only email alert is supported.
            logging_sampling_strategy (model_monitoring.sampling.RandomSampleConfig):
                Required. Sample Strategy for logging.

            labels (Dict[str, str]):
                Optional. The labels with user-defined metadata to
                organize the ModelDeploymentMonitoringJob.
                Label keys and values can be no longer than 64
                characters (Unicode codepoints), can only
                contain lowercase letters, numeric characters,
                underscores and dashes. International characters
                are allowed. See https://goo.gl/xmQnxf for more information
                and examples of labels.
            bigquery_tables_log_ttl (int):
                Optional. The number of days for which the logs are stored.
                The TTL(time to live) of BigQuery tables in user projects
                which stores logs. A day is the basic unit of
                the TTL and we take the ceil of TTL/86400(a
                day). e.g. { second: 3600} indicates ttl = 1
                day.

            enable_monitoring_pipeline_logs (bool):
                Optional. If true, the scheduled monitoring pipeline logs are sent to
                Google Cloud Logging, including pipeline status and
                anomalies detected. Please note the logs incur cost, which
                are subject to `Cloud Logging
                pricing <https://cloud.google.com/logging#pricing>`__.

            objective_configs (Union[
                Required. model_monitoring.objective.ObjectiveConfig,
                Dict[str, model_monitoring.objective.ObjectiveConfig]):
                A single config if it applies to all models, or a dictionary of
                model_id: model_monitoring.objective.ObjectiveConfig if
                different model IDs have different configs.

            deployed_model_ids (List[str]):
                Optional. Use this argument to specify which deployed models to
                apply the updated objective config to. If left unspecified, the same config
                will be applied to all deployed models.
        """
        self._sync_gca_resource()
        current_job = copy.deepcopy(self._gca_resource)
        update_mask: List[str] = []
        if display_name is not None:
            update_mask.append("display_name")
            current_job.display_name = display_name
        if schedule_config is not None:
            update_mask.append("model_deployment_monitoring_schedule_config")
            current_job.model_deployment_monitoring_schedule_config = (
                schedule_config.as_proto()
            )
        if alert_config is not None:
            update_mask.append("model_monitoring_alert_config")
            current_job.model_monitoring_alert_config = alert_config.as_proto()
        if logging_sampling_strategy is not None:
            update_mask.append("logging_sampling_strategy")
            current_job.logging_sampling_strategy = logging_sampling_strategy.as_proto()
        if labels is not None:
            update_mask.append("labels")
            current_job.labels = labels
        if bigquery_tables_log_ttl is not None:
            update_mask.append("log_ttl")
            current_job.log_ttl = duration_pb2.Duration(
                seconds=bigquery_tables_log_ttl * 86400
            )
        if enable_monitoring_pipeline_logs is not None:
            update_mask.append("enable_monitoring_pipeline_logs")
            current_job.enable_monitoring_pipeline_logs = (
                enable_monitoring_pipeline_logs
            )
        if objective_configs is not None:
            update_mask.append("model_deployment_monitoring_objective_configs")
            current_job.model_deployment_monitoring_objective_configs = (
                ModelDeploymentMonitoringJob._parse_configs(
                    objective_configs=objective_configs,
                    endpoint=aiplatform.Endpoint(
                        current_job.endpoint, credentials=self.credentials
                    ),
                    deployed_model_ids=deployed_model_ids,
                )
            )
        # TODO(b/254285776): add optional_sync support to model monitoring job
        lro = self.api_client.update_model_deployment_monitoring_job(
            model_deployment_monitoring_job=current_job,
            update_mask=field_mask_pb2.FieldMask(paths=update_mask),
        )
        self._gca_resource = lro.result()
        return self

    def pause(self) -> "ModelDeploymentMonitoringJob":
        """Pause a running MDM job."""
        self.api_client.pause_model_deployment_monitoring_job(
            name=self._gca_resource.name
        )
        return self

    def resume(self) -> "ModelDeploymentMonitoringJob":
        """Resumes a paused MDM job."""
        self.api_client.resume_model_deployment_monitoring_job(
            name=self._gca_resource.name
        )
        return self

    def delete(self) -> None:
        """Deletes an MDM job."""
        self.api_client.delete_model_deployment_monitoring_job(
            name=self._gca_resource.name
        )
