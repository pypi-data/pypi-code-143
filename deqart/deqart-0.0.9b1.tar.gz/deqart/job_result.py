import datetime
from io import BytesIO

import numpy as np
from dateutil.parser import parse

from .exceptions import DeqartStatevectorTooLarge
from .http_adapter import HTTP_SESSION_WITH_TIMEOUT_AND_RETRY


class JobResult:
    """This class contains information from a job run on quantum hardware or
    quantum simulators. Mainly it contains the resulting statevector from the
    run. It might contain only partial information, such as job name,
    when dq.run() is called with `asynchronous=true`."""

    def __init__(self, data):
        #  "PENDING" | "QUEUED" |"RUNNING" | "TERMINATED" | "CANCELED" | "NOT_ENOUGH_FUNDS" | "COMPLETED"
        self.run_status = data.get("run_status")
        self.job_id = data.get("job_id")
        self.job_name = data.get("job_name")
        self.results_path = data.get("results_path")
        self.top_100_results = data.get("top_100_results")
        self.num_qubits = data.get("num_qubits")
        self.circuit = data.get("qc")
        self.tags = data.get("tags")

        self.created_on = data.get("created_on")

        self.queue_start = data.get("queue_start")
        if self.queue_start is not None:
            self.queue_start = parse(self.queue_start)

        self.run_start = data.get("run_start")
        if self.run_start is not None:
            self.run_start = parse(self.run_start)

        self.run_end = data.get("run_end")
        if self.run_end is not None:
            self.run_end = parse(self.run_end)

        if self.queue_start is not None and self.run_start is not None:
            self.queue_time_ms = int(
                (self.run_start - self.queue_start) / datetime.timedelta(milliseconds=1)
            )
        else:
            self.queue_time_ms = None

        if self.run_start is not None and self.run_end is not None:
            self.run_time_ms = round(
                (self.run_end - self.run_start) / datetime.timedelta(milliseconds=1)
            )
        else:
            self.run_time_ms = None

        self.error_message = data.get("error_message")

        self.cost = data.get("cost")
        if self.cost is not None:
            self.cost /= 100.0
        self._metadata = None
        self._statevector = None

    def get_statevector(self):
        if self._statevector is None:
            response = HTTP_SESSION_WITH_TIMEOUT_AND_RETRY.get(
                self.results_path + "statevector.txt"
            )
            if response.ok:
                data = response.content
                self._statevector = np.loadtxt(BytesIO(data), dtype=np.complex_)
        if not self._statevector is None:
            return self._statevector
        else:
            raise DeqartStatevectorTooLarge(self.num_qubits)

    def get_counts(self):
        if self.results_path is None:
            return None
        if self._metadata is None:
            response = HTTP_SESSION_WITH_TIMEOUT_AND_RETRY.get(
                self.results_path + "metadata.json"
            )
            self._metadata = response.json()
        if "counts" not in self._metadata:
            raise RuntimeError("The job result metadata doesn't contain counts.")
        return self._metadata["counts"]

    def __str__(self):
        return f"Job ID: {self.job_id}, name: {self.job_name}, run status: {self.run_status}, queue time (ms): {self.queue_time_ms}, run time (ms): {self.run_time_ms}, cost ($): {self.cost}, num qubits: {self.num_qubits}, error_message: {self.error_message}"
