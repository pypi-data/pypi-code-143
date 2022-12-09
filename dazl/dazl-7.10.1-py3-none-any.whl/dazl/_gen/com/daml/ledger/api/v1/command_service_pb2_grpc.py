# Copyright (c) 2017-2022 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# fmt: off
# isort: skip_file
# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import command_service_pb2 as com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class CommandServiceStub(object):
    """Command Service is able to correlate submitted commands with completion data, identify timeouts, and return contextual
    information with each tracking result. This supports the implementation of stateless clients.

    Note that submitted commands generally produce completion events as well, even in case a command gets rejected.
    For example, the participant MAY choose to produce a completion event for a rejection of a duplicate command.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SubmitAndWait = channel.unary_unary(
                '/com.daml.ledger.api.v1.CommandService/SubmitAndWait',
                request_serializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.SubmitAndWaitForTransactionId = channel.unary_unary(
                '/com.daml.ledger.api.v1.CommandService/SubmitAndWaitForTransactionId',
                request_serializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitRequest.SerializeToString,
                response_deserializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitForTransactionIdResponse.FromString,
                )
        self.SubmitAndWaitForTransaction = channel.unary_unary(
                '/com.daml.ledger.api.v1.CommandService/SubmitAndWaitForTransaction',
                request_serializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitRequest.SerializeToString,
                response_deserializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitForTransactionResponse.FromString,
                )
        self.SubmitAndWaitForTransactionTree = channel.unary_unary(
                '/com.daml.ledger.api.v1.CommandService/SubmitAndWaitForTransactionTree',
                request_serializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitRequest.SerializeToString,
                response_deserializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitForTransactionTreeResponse.FromString,
                )


class CommandServiceServicer(object):
    """Command Service is able to correlate submitted commands with completion data, identify timeouts, and return contextual
    information with each tracking result. This supports the implementation of stateless clients.

    Note that submitted commands generally produce completion events as well, even in case a command gets rejected.
    For example, the participant MAY choose to produce a completion event for a rejection of a duplicate command.
    """

    def SubmitAndWait(self, request, context):
        """Submits a single composite command and waits for its result.
        Propagates the gRPC error of failed submissions including Daml interpretation errors.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubmitAndWaitForTransactionId(self, request, context):
        """Submits a single composite command, waits for its result, and returns the transaction id.
        Propagates the gRPC error of failed submissions including Daml interpretation errors.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubmitAndWaitForTransaction(self, request, context):
        """Submits a single composite command, waits for its result, and returns the transaction.
        Propagates the gRPC error of failed submissions including Daml interpretation errors.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubmitAndWaitForTransactionTree(self, request, context):
        """Submits a single composite command, waits for its result, and returns the transaction tree.
        Propagates the gRPC error of failed submissions including Daml interpretation errors.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CommandServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SubmitAndWait': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitAndWait,
                    request_deserializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'SubmitAndWaitForTransactionId': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitAndWaitForTransactionId,
                    request_deserializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitRequest.FromString,
                    response_serializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitForTransactionIdResponse.SerializeToString,
            ),
            'SubmitAndWaitForTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitAndWaitForTransaction,
                    request_deserializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitRequest.FromString,
                    response_serializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitForTransactionResponse.SerializeToString,
            ),
            'SubmitAndWaitForTransactionTree': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitAndWaitForTransactionTree,
                    request_deserializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitRequest.FromString,
                    response_serializer=com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitForTransactionTreeResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.daml.ledger.api.v1.CommandService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CommandService(object):
    """Command Service is able to correlate submitted commands with completion data, identify timeouts, and return contextual
    information with each tracking result. This supports the implementation of stateless clients.

    Note that submitted commands generally produce completion events as well, even in case a command gets rejected.
    For example, the participant MAY choose to produce a completion event for a rejection of a duplicate command.
    """

    @staticmethod
    def SubmitAndWait(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.daml.ledger.api.v1.CommandService/SubmitAndWait',
            com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubmitAndWaitForTransactionId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.daml.ledger.api.v1.CommandService/SubmitAndWaitForTransactionId',
            com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitRequest.SerializeToString,
            com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitForTransactionIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubmitAndWaitForTransaction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.daml.ledger.api.v1.CommandService/SubmitAndWaitForTransaction',
            com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitRequest.SerializeToString,
            com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitForTransactionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubmitAndWaitForTransactionTree(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.daml.ledger.api.v1.CommandService/SubmitAndWaitForTransactionTree',
            com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitRequest.SerializeToString,
            com_dot_daml_dot_ledger_dot_api_dot_v1_dot_command__service__pb2.SubmitAndWaitForTransactionTreeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
