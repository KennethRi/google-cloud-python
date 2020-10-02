# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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


from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.functions.v1",
    manifest={
        "CloudFunctionStatus",
        "CloudFunction",
        "SourceRepository",
        "HttpsTrigger",
        "EventTrigger",
        "FailurePolicy",
        "CreateFunctionRequest",
        "UpdateFunctionRequest",
        "GetFunctionRequest",
        "ListFunctionsRequest",
        "ListFunctionsResponse",
        "DeleteFunctionRequest",
        "CallFunctionRequest",
        "CallFunctionResponse",
        "GenerateUploadUrlRequest",
        "GenerateUploadUrlResponse",
        "GenerateDownloadUrlRequest",
        "GenerateDownloadUrlResponse",
    },
)


class CloudFunctionStatus(proto.Enum):
    r"""Describes the current stage of a deployment."""
    CLOUD_FUNCTION_STATUS_UNSPECIFIED = 0
    ACTIVE = 1
    OFFLINE = 2
    DEPLOY_IN_PROGRESS = 3
    DELETE_IN_PROGRESS = 4
    UNKNOWN = 5


class CloudFunction(proto.Message):
    r"""Describes a Cloud Function that contains user computation
    executed in response to an event. It encapsulate function and
    triggers configurations.

    Attributes:
        name (str):
            A user-defined name of the function. Function names must be
            unique globally and match pattern
            ``projects/*/locations/*/functions/*``
        description (str):
            User-provided description of a function.
        source_archive_url (str):
            The Google Cloud Storage URL, starting with
            gs://, pointing to the zip archive which
            contains the function.
        source_repository (~.gcf_functions.SourceRepository):
            **Beta Feature**

            The source repository where a function is hosted.
        source_upload_url (str):
            The Google Cloud Storage signed URL used for source
            uploading, generated by
            [google.cloud.functions.v1.GenerateUploadUrl][]
        https_trigger (~.gcf_functions.HttpsTrigger):
            An HTTPS endpoint type of source that can be
            triggered via URL.
        event_trigger (~.gcf_functions.EventTrigger):
            A source that fires events in response to a
            condition in another service.
        status (~.gcf_functions.CloudFunctionStatus):
            Output only. Status of the function
            deployment.
        entry_point (str):
            The name of the function (as defined in source code) that
            will be executed. Defaults to the resource name suffix, if
            not specified. For backward compatibility, if function with
            given name is not found, then the system will try to use
            function named "function". For Node.js this is name of a
            function exported by the module specified in
            ``source_location``.
        runtime (str):
            The runtime in which to run the function. Required when
            deploying a new function, optional when updating an existing
            function. For a complete list of possible choices, see the
            ```gcloud`` command
            reference </sdk/gcloud/reference/functions/deploy#--runtime>`__.
        timeout (~.duration.Duration):
            The function execution timeout. Execution is
            considered failed and can be terminated if the
            function is not completed at the end of the
            timeout period. Defaults to 60 seconds.
        available_memory_mb (int):
            The amount of memory in MB available for a
            function. Defaults to 256MB.
        service_account_email (str):
            The email of the function's service account. If empty,
            defaults to ``{project_id}@appspot.gserviceaccount.com``.
        update_time (~.timestamp.Timestamp):
            Output only. The last update timestamp of a
            Cloud Function.
        version_id (int):
            Output only. The version identifier of the
            Cloud Function. Each deployment attempt results
            in a new version of a function being created.
        labels (Sequence[~.gcf_functions.CloudFunction.LabelsEntry]):
            Labels associated with this Cloud Function.
        environment_variables (Sequence[~.gcf_functions.CloudFunction.EnvironmentVariablesEntry]):
            Environment variables that shall be available
            during function execution.
        network (str):
            The VPC Network that this cloud function can connect to. It
            can be either the fully-qualified URI, or the short name of
            the network resource. If the short network name is used, the
            network must belong to the same project. Otherwise, it must
            belong to a project within the same organization. The format
            of this field is either
            ``projects/{project}/global/networks/{network}`` or
            ``{network}``, where {project} is a project id where the
            network is defined, and {network} is the short name of the
            network.

            This field is mutually exclusive with ``vpc_connector`` and
            will be replaced by it.

            See `the VPC
            documentation <https://cloud.google.com/compute/docs/vpc>`__
            for more information on connecting Cloud projects.
        max_instances (int):
            The limit on the maximum number of function
            instances that may coexist at a given time.
        vpc_connector (str):
            The VPC Network Connector that this cloud function can
            connect to. It can be either the fully-qualified URI, or the
            short name of the network connector resource. The format of
            this field is ``projects/*/locations/*/connectors/*``

            This field is mutually exclusive with ``network`` field and
            will eventually replace it.

            See `the VPC
            documentation <https://cloud.google.com/compute/docs/vpc>`__
            for more information on connecting Cloud projects.
        vpc_connector_egress_settings (~.gcf_functions.CloudFunction.VpcConnectorEgressSettings):
            The egress settings for the connector,
            controlling what traffic is diverted through it.
        ingress_settings (~.gcf_functions.CloudFunction.IngressSettings):
            The ingress settings for the function,
            controlling what traffic can reach it.
        build_id (str):
            Output only. The Cloud Build ID of the latest
            successful deployment of the function.
    """

    class VpcConnectorEgressSettings(proto.Enum):
        r"""Available egress settings.

        This controls what traffic is diverted through the VPC Access
        Connector resource. By default PRIVATE_RANGES_ONLY will be used.
        """
        VPC_CONNECTOR_EGRESS_SETTINGS_UNSPECIFIED = 0
        PRIVATE_RANGES_ONLY = 1
        ALL_TRAFFIC = 2

    class IngressSettings(proto.Enum):
        r"""Available ingress settings.

        This controls what traffic can reach the function.

        If unspecified, ALLOW_ALL will be used.
        """
        INGRESS_SETTINGS_UNSPECIFIED = 0
        ALLOW_ALL = 1
        ALLOW_INTERNAL_ONLY = 2
        ALLOW_INTERNAL_AND_GCLB = 3

    name = proto.Field(proto.STRING, number=1)

    description = proto.Field(proto.STRING, number=2)

    source_archive_url = proto.Field(proto.STRING, number=3, oneof="source_code")

    source_repository = proto.Field(
        proto.MESSAGE, number=4, oneof="source_code", message="SourceRepository",
    )

    source_upload_url = proto.Field(proto.STRING, number=16, oneof="source_code")

    https_trigger = proto.Field(
        proto.MESSAGE, number=5, oneof="trigger", message="HttpsTrigger",
    )

    event_trigger = proto.Field(
        proto.MESSAGE, number=6, oneof="trigger", message="EventTrigger",
    )

    status = proto.Field(proto.ENUM, number=7, enum="CloudFunctionStatus",)

    entry_point = proto.Field(proto.STRING, number=8)

    runtime = proto.Field(proto.STRING, number=19)

    timeout = proto.Field(proto.MESSAGE, number=9, message=duration.Duration,)

    available_memory_mb = proto.Field(proto.INT32, number=10)

    service_account_email = proto.Field(proto.STRING, number=11)

    update_time = proto.Field(proto.MESSAGE, number=12, message=timestamp.Timestamp,)

    version_id = proto.Field(proto.INT64, number=14)

    labels = proto.MapField(proto.STRING, proto.STRING, number=15)

    environment_variables = proto.MapField(proto.STRING, proto.STRING, number=17)

    network = proto.Field(proto.STRING, number=18)

    max_instances = proto.Field(proto.INT32, number=20)

    vpc_connector = proto.Field(proto.STRING, number=22)

    vpc_connector_egress_settings = proto.Field(
        proto.ENUM, number=23, enum=VpcConnectorEgressSettings,
    )

    ingress_settings = proto.Field(proto.ENUM, number=24, enum=IngressSettings,)

    build_id = proto.Field(proto.STRING, number=27)


class SourceRepository(proto.Message):
    r"""Describes SourceRepository, used to represent parameters
    related to source repository where a function is hosted.

    Attributes:
        url (str):
            The URL pointing to the hosted repository where the function
            is defined. There are supported Cloud Source Repository URLs
            in the following formats:

            To refer to a specific commit:
            ``https://source.developers.google.com/projects/*/repos/*/revisions/*/paths/*``
            To refer to a moveable alias (branch):
            ``https://source.developers.google.com/projects/*/repos/*/moveable-aliases/*/paths/*``
            In particular, to refer to HEAD use ``master`` moveable
            alias. To refer to a specific fixed alias (tag):
            ``https://source.developers.google.com/projects/*/repos/*/fixed-aliases/*/paths/*``

            You may omit ``paths/*`` if you want to use the main
            directory.
        deployed_url (str):
            Output only. The URL pointing to the hosted
            repository where the function were defined at
            the time of deployment. It always points to a
            specific commit in the format described above.
    """

    url = proto.Field(proto.STRING, number=1)

    deployed_url = proto.Field(proto.STRING, number=2)


class HttpsTrigger(proto.Message):
    r"""Describes HttpsTrigger, could be used to connect web hooks to
    function.

    Attributes:
        url (str):
            Output only. The deployed url for the
            function.
    """

    url = proto.Field(proto.STRING, number=1)


class EventTrigger(proto.Message):
    r"""Describes EventTrigger, used to request events be sent from
    another service.

    Attributes:
        event_type (str):
            Required. The type of event to observe. For example:
            ``providers/cloud.storage/eventTypes/object.change`` and
            ``providers/cloud.pubsub/eventTypes/topic.publish``.

            Event types match pattern ``providers/*/eventTypes/*.*``.
            The pattern contains:

            1. namespace: For example, ``cloud.storage`` and
               ``google.firebase.analytics``.
            2. resource type: The type of resource on which event
               occurs. For example, the Google Cloud Storage API
               includes the type ``object``.
            3. action: The action that generates the event. For example,
               action for a Google Cloud Storage Object is 'change'.
               These parts are lower case.
        resource (str):
            Required. The resource(s) from which to observe events, for
            example, ``projects/_/buckets/myBucket``.

            Not all syntactically correct values are accepted by all
            services. For example:

            1. The authorization model must support it. Google Cloud
               Functions only allows EventTriggers to be deployed that
               observe resources in the same project as the
               ``CloudFunction``.
            2. The resource type must match the pattern expected for an
               ``event_type``. For example, an ``EventTrigger`` that has
               an ``event_type`` of "google.pubsub.topic.publish" should
               have a resource that matches Google Cloud Pub/Sub topics.

            Additionally, some services may support short names when
            creating an ``EventTrigger``. These will always be returned
            in the normalized "long" format.

            See each *service's* documentation for supported formats.
        service (str):
            The hostname of the service that should be observed.

            If no string is provided, the default service implementing
            the API will be used. For example,
            ``storage.googleapis.com`` is the default for all event
            types in the ``google.storage`` namespace.
        failure_policy (~.gcf_functions.FailurePolicy):
            Specifies policy for failed executions.
    """

    event_type = proto.Field(proto.STRING, number=1)

    resource = proto.Field(proto.STRING, number=2)

    service = proto.Field(proto.STRING, number=3)

    failure_policy = proto.Field(proto.MESSAGE, number=5, message="FailurePolicy",)


class FailurePolicy(proto.Message):
    r"""Describes the policy in case of function's execution failure.
    If empty, then defaults to ignoring failures (i.e. not retrying
    them).

    Attributes:
        retry (~.gcf_functions.FailurePolicy.Retry):
            If specified, then the function will be
            retried in case of a failure.
    """

    class Retry(proto.Message):
        r"""Describes the retry policy in case of function's execution
        failure. A function execution will be retried on any failure. A
        failed execution will be retried up to 7 days with an
        exponential backoff (capped at 10 seconds).
        Retried execution is charged as any other execution.
        """

    retry = proto.Field(proto.MESSAGE, number=1, oneof="action", message=Retry,)


class CreateFunctionRequest(proto.Message):
    r"""Request for the ``CreateFunction`` method.

    Attributes:
        location (str):
            Required. The project and location in which the function
            should be created, specified in the format
            ``projects/*/locations/*``
        function (~.gcf_functions.CloudFunction):
            Required. Function to be created.
    """

    location = proto.Field(proto.STRING, number=1)

    function = proto.Field(proto.MESSAGE, number=2, message=CloudFunction,)


class UpdateFunctionRequest(proto.Message):
    r"""Request for the ``UpdateFunction`` method.

    Attributes:
        function (~.gcf_functions.CloudFunction):
            Required. New version of the function.
        update_mask (~.field_mask.FieldMask):
            Required list of fields to be updated in this
            request.
    """

    function = proto.Field(proto.MESSAGE, number=1, message=CloudFunction,)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class GetFunctionRequest(proto.Message):
    r"""Request for the ``GetFunction`` method.

    Attributes:
        name (str):
            Required. The name of the function which
            details should be obtained.
    """

    name = proto.Field(proto.STRING, number=1)


class ListFunctionsRequest(proto.Message):
    r"""Request for the ``ListFunctions`` method.

    Attributes:
        parent (str):
            The project and location from which the function should be
            listed, specified in the format ``projects/*/locations/*``
            If you want to list functions in all locations, use "-" in
            place of a location. When listing functions in all
            locations, if one or more location(s) are unreachable, the
            response will contain functions from all reachable locations
            along with the names of any unreachable locations.
        page_size (int):
            Maximum number of functions to return per
            call.
        page_token (str):
            The value returned by the last ``ListFunctionsResponse``;
            indicates that this is a continuation of a prior
            ``ListFunctions`` call, and that the system should return
            the next page of data.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListFunctionsResponse(proto.Message):
    r"""Response for the ``ListFunctions`` method.

    Attributes:
        functions (Sequence[~.gcf_functions.CloudFunction]):
            The functions that match the request.
        next_page_token (str):
            If not empty, indicates that there may be more functions
            that match the request; this value should be passed in a new
            [google.cloud.functions.v1.ListFunctionsRequest][google.cloud.functions.v1.ListFunctionsRequest]
            to get more functions.
        unreachable (Sequence[str]):
            Locations that could not be reached. The
            response does not include any functions from
            these locations.
    """

    @property
    def raw_page(self):
        return self

    functions = proto.RepeatedField(proto.MESSAGE, number=1, message=CloudFunction,)

    next_page_token = proto.Field(proto.STRING, number=2)

    unreachable = proto.RepeatedField(proto.STRING, number=3)


class DeleteFunctionRequest(proto.Message):
    r"""Request for the ``DeleteFunction`` method.

    Attributes:
        name (str):
            Required. The name of the function which
            should be deleted.
    """

    name = proto.Field(proto.STRING, number=1)


class CallFunctionRequest(proto.Message):
    r"""Request for the ``CallFunction`` method.

    Attributes:
        name (str):
            Required. The name of the function to be
            called.
        data (str):
            Required. Input to be passed to the function.
    """

    name = proto.Field(proto.STRING, number=1)

    data = proto.Field(proto.STRING, number=2)


class CallFunctionResponse(proto.Message):
    r"""Response of ``CallFunction`` method.

    Attributes:
        execution_id (str):
            Execution id of function invocation.
        result (str):
            Result populated for successful execution of
            synchronous function. Will not be populated if
            function does not return a result through
            context.
        error (str):
            Either system or user-function generated
            error. Set if execution was not successful.
    """

    execution_id = proto.Field(proto.STRING, number=1)

    result = proto.Field(proto.STRING, number=2)

    error = proto.Field(proto.STRING, number=3)


class GenerateUploadUrlRequest(proto.Message):
    r"""Request of ``GenerateSourceUploadUrl`` method.

    Attributes:
        parent (str):
            The project and location in which the Google Cloud Storage
            signed URL should be generated, specified in the format
            ``projects/*/locations/*``.
    """

    parent = proto.Field(proto.STRING, number=1)


class GenerateUploadUrlResponse(proto.Message):
    r"""Response of ``GenerateSourceUploadUrl`` method.

    Attributes:
        upload_url (str):
            The generated Google Cloud Storage signed URL
            that should be used for a function source code
            upload. The uploaded file should be a zip
            archive which contains a function.
    """

    upload_url = proto.Field(proto.STRING, number=1)


class GenerateDownloadUrlRequest(proto.Message):
    r"""Request of ``GenerateDownloadUrl`` method.

    Attributes:
        name (str):
            The name of function for which source code
            Google Cloud Storage signed URL should be
            generated.
        version_id (int):
            The optional version of function. If not set,
            default, current version is used.
    """

    name = proto.Field(proto.STRING, number=1)

    version_id = proto.Field(proto.UINT64, number=2)


class GenerateDownloadUrlResponse(proto.Message):
    r"""Response of ``GenerateDownloadUrl`` method.

    Attributes:
        download_url (str):
            The generated Google Cloud Storage signed URL
            that should be used for function source code
            download.
    """

    download_url = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
