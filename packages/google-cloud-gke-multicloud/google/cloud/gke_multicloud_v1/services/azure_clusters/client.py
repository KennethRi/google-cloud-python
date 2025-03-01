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
from collections import OrderedDict
import os
import re
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.gke_multicloud_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.gke_multicloud_v1.services.azure_clusters import pagers
from google.cloud.gke_multicloud_v1.types import (
    azure_resources,
    azure_service,
    common_resources,
)

from .transports.base import DEFAULT_CLIENT_INFO, AzureClustersTransport
from .transports.grpc import AzureClustersGrpcTransport
from .transports.grpc_asyncio import AzureClustersGrpcAsyncIOTransport
from .transports.rest import AzureClustersRestTransport


class AzureClustersClientMeta(type):
    """Metaclass for the AzureClusters client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[AzureClustersTransport]]
    _transport_registry["grpc"] = AzureClustersGrpcTransport
    _transport_registry["grpc_asyncio"] = AzureClustersGrpcAsyncIOTransport
    _transport_registry["rest"] = AzureClustersRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[AzureClustersTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class AzureClustersClient(metaclass=AzureClustersClientMeta):
    """The AzureClusters API provides a single centrally managed
    service to create and manage Anthos clusters that run on Azure
    infrastructure.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "gkemulticloud.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            AzureClustersClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            AzureClustersClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> AzureClustersTransport:
        """Returns the transport used by the client instance.

        Returns:
            AzureClustersTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def azure_client_path(
        project: str,
        location: str,
        azure_client: str,
    ) -> str:
        """Returns a fully-qualified azure_client string."""
        return "projects/{project}/locations/{location}/azureClients/{azure_client}".format(
            project=project,
            location=location,
            azure_client=azure_client,
        )

    @staticmethod
    def parse_azure_client_path(path: str) -> Dict[str, str]:
        """Parses a azure_client path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/azureClients/(?P<azure_client>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def azure_cluster_path(
        project: str,
        location: str,
        azure_cluster: str,
    ) -> str:
        """Returns a fully-qualified azure_cluster string."""
        return "projects/{project}/locations/{location}/azureClusters/{azure_cluster}".format(
            project=project,
            location=location,
            azure_cluster=azure_cluster,
        )

    @staticmethod
    def parse_azure_cluster_path(path: str) -> Dict[str, str]:
        """Parses a azure_cluster path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/azureClusters/(?P<azure_cluster>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def azure_node_pool_path(
        project: str,
        location: str,
        azure_cluster: str,
        azure_node_pool: str,
    ) -> str:
        """Returns a fully-qualified azure_node_pool string."""
        return "projects/{project}/locations/{location}/azureClusters/{azure_cluster}/azureNodePools/{azure_node_pool}".format(
            project=project,
            location=location,
            azure_cluster=azure_cluster,
            azure_node_pool=azure_node_pool,
        )

    @staticmethod
    def parse_azure_node_pool_path(path: str) -> Dict[str, str]:
        """Parses a azure_node_pool path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/azureClusters/(?P<azure_cluster>.+?)/azureNodePools/(?P<azure_node_pool>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def azure_server_config_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified azure_server_config string."""
        return "projects/{project}/locations/{location}/azureServerConfig".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_azure_server_config_path(path: str) -> Dict[str, str]:
        """Parses a azure_server_config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/azureServerConfig$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[Union[str, AzureClustersTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the azure clusters client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, AzureClustersTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
                NOTE: "rest" transport functionality is currently in a
                beta state (preview). We welcome your feedback via an
                issue in this library's source repository.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        client_options = cast(client_options_lib.ClientOptions, client_options)

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, AzureClustersTransport):
            # transport is a AzureClustersTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=client_options.api_audience,
            )

    def create_azure_client(
        self,
        request: Optional[Union[azure_service.CreateAzureClientRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        azure_client: Optional[azure_resources.AzureClient] = None,
        azure_client_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new
        [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
        resource on a given Google Cloud project and region.

        ``AzureClient`` resources hold client authentication information
        needed by the Anthos Multicloud API to manage Azure resources on
        your Azure subscription on your behalf.

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_create_azure_client():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                azure_client = gke_multicloud_v1.AzureClient()
                azure_client.tenant_id = "tenant_id_value"
                azure_client.application_id = "application_id_value"

                request = gke_multicloud_v1.CreateAzureClientRequest(
                    parent="parent_value",
                    azure_client=azure_client,
                    azure_client_id="azure_client_id_value",
                )

                # Make the request
                operation = client.create_azure_client(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.CreateAzureClientRequest, dict]):
                The request object. Request message for ``AzureClusters.CreateAzureClient``
                method.
            parent (str):
                Required. The parent location where this
                [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
                resource will be created.

                Location names are formatted as
                ``projects/<project-id>/locations/<region>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            azure_client (google.cloud.gke_multicloud_v1.types.AzureClient):
                Required. The specification of the
                [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
                to create.

                This corresponds to the ``azure_client`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            azure_client_id (str):
                Required. A client provided ID the resource. Must be
                unique within the parent resource.

                The provided ID will be part of the
                [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
                resource name formatted as
                ``projects/<project-id>/locations/<region>/azureClients/<client-id>``.

                Valid characters are ``/[a-z][0-9]-/``. Cannot be longer
                than 63 characters.

                This corresponds to the ``azure_client_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.gke_multicloud_v1.types.AzureClient` AzureClient resources hold client authentication information needed by the
                   Anthos Multi-Cloud API to manage Azure resources on
                   your Azure subscription.

                   When an
                   [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
                   is created, an AzureClient resource needs to be
                   provided and all operations on Azure resources
                   associated to that cluster will authenticate to Azure
                   services using the given client.

                   AzureClient resources are immutable and cannot be
                   modified upon creation.

                   Each AzureClient resource is bound to a single Azure
                   Active Directory Application and tenant.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, azure_client, azure_client_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.CreateAzureClientRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.CreateAzureClientRequest):
            request = azure_service.CreateAzureClientRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if azure_client is not None:
                request.azure_client = azure_client
            if azure_client_id is not None:
                request.azure_client_id = azure_client_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_azure_client]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            azure_resources.AzureClient,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_azure_client(
        self,
        request: Optional[Union[azure_service.GetAzureClientRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> azure_resources.AzureClient:
        r"""Describes a specific
        [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
        resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_get_azure_client():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GetAzureClientRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_azure_client(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.GetAzureClientRequest, dict]):
                The request object. Request message for ``AzureClusters.GetAzureClient``
                method.
            name (str):
                Required. The name of the
                [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
                resource to describe.

                [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
                names are formatted as
                ``projects/<project-id>/locations/<region>/azureClients/<client-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.AzureClient:
                AzureClient resources hold client authentication information needed by the
                   Anthos Multi-Cloud API to manage Azure resources on
                   your Azure subscription.

                   When an
                   [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
                   is created, an AzureClient resource needs to be
                   provided and all operations on Azure resources
                   associated to that cluster will authenticate to Azure
                   services using the given client.

                   AzureClient resources are immutable and cannot be
                   modified upon creation.

                   Each AzureClient resource is bound to a single Azure
                   Active Directory Application and tenant.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.GetAzureClientRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.GetAzureClientRequest):
            request = azure_service.GetAzureClientRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_azure_client]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_azure_clients(
        self,
        request: Optional[Union[azure_service.ListAzureClientsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAzureClientsPager:
        r"""Lists all
        [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
        resources on a given Google Cloud project and region.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_list_azure_clients():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.ListAzureClientsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_azure_clients(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.ListAzureClientsRequest, dict]):
                The request object. Request message for ``AzureClusters.ListAzureClients``
                method.
            parent (str):
                Required. The parent location which owns this collection
                of
                [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
                resources.

                Location names are formatted as
                ``projects/<project-id>/locations/<region>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud Platform resource
                names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.services.azure_clusters.pagers.ListAzureClientsPager:
                Response message for AzureClusters.ListAzureClients
                method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.ListAzureClientsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.ListAzureClientsRequest):
            request = azure_service.ListAzureClientsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_azure_clients]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAzureClientsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_azure_client(
        self,
        request: Optional[Union[azure_service.DeleteAzureClientRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a specific
        [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
        resource.

        If the client is used by one or more clusters, deletion will
        fail and a ``FAILED_PRECONDITION`` error will be returned.

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_delete_azure_client():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.DeleteAzureClientRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_azure_client(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.DeleteAzureClientRequest, dict]):
                The request object. Request message for ``AzureClusters.DeleteAzureClient``
                method.
            name (str):
                Required. The resource name the
                [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
                to delete.

                [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
                names are formatted as
                ``projects/<project-id>/locations/<region>/azureClients/<client-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.DeleteAzureClientRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.DeleteAzureClientRequest):
            request = azure_service.DeleteAzureClientRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_azure_client]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def create_azure_cluster(
        self,
        request: Optional[Union[azure_service.CreateAzureClusterRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        azure_cluster: Optional[azure_resources.AzureCluster] = None,
        azure_cluster_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new
        [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
        resource on a given Google Cloud Platform project and region.

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_create_azure_cluster():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                azure_cluster = gke_multicloud_v1.AzureCluster()
                azure_cluster.azure_region = "azure_region_value"
                azure_cluster.resource_group_id = "resource_group_id_value"
                azure_cluster.networking.virtual_network_id = "virtual_network_id_value"
                azure_cluster.networking.pod_address_cidr_blocks = ['pod_address_cidr_blocks_value1', 'pod_address_cidr_blocks_value2']
                azure_cluster.networking.service_address_cidr_blocks = ['service_address_cidr_blocks_value1', 'service_address_cidr_blocks_value2']
                azure_cluster.control_plane.version = "version_value"
                azure_cluster.control_plane.ssh_config.authorized_key = "authorized_key_value"
                azure_cluster.authorization.admin_users.username = "username_value"
                azure_cluster.fleet.project = "project_value"

                request = gke_multicloud_v1.CreateAzureClusterRequest(
                    parent="parent_value",
                    azure_cluster=azure_cluster,
                    azure_cluster_id="azure_cluster_id_value",
                )

                # Make the request
                operation = client.create_azure_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.CreateAzureClusterRequest, dict]):
                The request object. Request message for ``AzureClusters.CreateAzureCluster``
                method.
            parent (str):
                Required. The parent location where this
                [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
                resource will be created.

                Location names are formatted as
                ``projects/<project-id>/locations/<region>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            azure_cluster (google.cloud.gke_multicloud_v1.types.AzureCluster):
                Required. The specification of the
                [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
                to create.

                This corresponds to the ``azure_cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            azure_cluster_id (str):
                Required. A client provided ID the resource. Must be
                unique within the parent resource.

                The provided ID will be part of the
                [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
                resource name formatted as
                ``projects/<project-id>/locations/<region>/azureClusters/<cluster-id>``.

                Valid characters are ``/[a-z][0-9]-/``. Cannot be longer
                than 63 characters.

                This corresponds to the ``azure_cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.gke_multicloud_v1.types.AzureCluster`
                An Anthos cluster running on Azure.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, azure_cluster, azure_cluster_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.CreateAzureClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.CreateAzureClusterRequest):
            request = azure_service.CreateAzureClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if azure_cluster is not None:
                request.azure_cluster = azure_cluster
            if azure_cluster_id is not None:
                request.azure_cluster_id = azure_cluster_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_azure_cluster]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            azure_resources.AzureCluster,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_azure_cluster(
        self,
        request: Optional[Union[azure_service.UpdateAzureClusterRequest, dict]] = None,
        *,
        azure_cluster: Optional[azure_resources.AzureCluster] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates an
        [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_update_azure_cluster():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                azure_cluster = gke_multicloud_v1.AzureCluster()
                azure_cluster.azure_region = "azure_region_value"
                azure_cluster.resource_group_id = "resource_group_id_value"
                azure_cluster.networking.virtual_network_id = "virtual_network_id_value"
                azure_cluster.networking.pod_address_cidr_blocks = ['pod_address_cidr_blocks_value1', 'pod_address_cidr_blocks_value2']
                azure_cluster.networking.service_address_cidr_blocks = ['service_address_cidr_blocks_value1', 'service_address_cidr_blocks_value2']
                azure_cluster.control_plane.version = "version_value"
                azure_cluster.control_plane.ssh_config.authorized_key = "authorized_key_value"
                azure_cluster.authorization.admin_users.username = "username_value"
                azure_cluster.fleet.project = "project_value"

                request = gke_multicloud_v1.UpdateAzureClusterRequest(
                    azure_cluster=azure_cluster,
                )

                # Make the request
                operation = client.update_azure_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.UpdateAzureClusterRequest, dict]):
                The request object. Request message for ``AzureClusters.UpdateAzureCluster``
                method.
            azure_cluster (google.cloud.gke_multicloud_v1.types.AzureCluster):
                Required. The
                [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
                resource to update.

                This corresponds to the ``azure_cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Mask of fields to update. At least one path
                must be supplied in this field. The elements of the
                repeated paths field can only include these fields from
                [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]:

                -  ``description``.
                -  ``azureClient``.
                -  ``control_plane.version``.
                -  ``control_plane.vm_size``.
                -  ``annotations``.
                -  ``authorization.admin_users``.
                -  ``control_plane.root_volume.size_gib``.
                -  ``azure_services_authentication``.
                -  ``azure_services_authentication.tenant_id``.
                -  ``azure_services_authentication.application_id``.
                -  ``control_plane.proxy_config``.
                -  ``control_plane.proxy_config.resource_group_id``.
                -  ``control_plane.proxy_config.secret_id``.
                -  ``control_plane.ssh_config.authorized_key``.
                -  ``logging_config.component_config.enable_components``
                -  ``monitoring_config.managed_prometheus_config.enabled``.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.gke_multicloud_v1.types.AzureCluster`
                An Anthos cluster running on Azure.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([azure_cluster, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.UpdateAzureClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.UpdateAzureClusterRequest):
            request = azure_service.UpdateAzureClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if azure_cluster is not None:
                request.azure_cluster = azure_cluster
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_azure_cluster]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("azure_cluster.name", request.azure_cluster.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            azure_resources.AzureCluster,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_azure_cluster(
        self,
        request: Optional[Union[azure_service.GetAzureClusterRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> azure_resources.AzureCluster:
        r"""Describes a specific
        [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
        resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_get_azure_cluster():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GetAzureClusterRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_azure_cluster(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.GetAzureClusterRequest, dict]):
                The request object. Request message for ``AzureClusters.GetAzureCluster``
                method.
            name (str):
                Required. The name of the
                [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
                resource to describe.

                ``AzureCluster`` names are formatted as
                ``projects/<project-id>/locations/<region>/azureClusters/<cluster-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud Platform resource
                names.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.AzureCluster:
                An Anthos cluster running on Azure.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.GetAzureClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.GetAzureClusterRequest):
            request = azure_service.GetAzureClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_azure_cluster]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_azure_clusters(
        self,
        request: Optional[Union[azure_service.ListAzureClustersRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAzureClustersPager:
        r"""Lists all
        [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
        resources on a given Google Cloud project and region.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_list_azure_clusters():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.ListAzureClustersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_azure_clusters(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.ListAzureClustersRequest, dict]):
                The request object. Request message for ``AzureClusters.ListAzureClusters``
                method.
            parent (str):
                Required. The parent location which owns this collection
                of
                [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
                resources.

                Location names are formatted as
                ``projects/<project-id>/locations/<region>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud Platform resource
                names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.services.azure_clusters.pagers.ListAzureClustersPager:
                Response message for AzureClusters.ListAzureClusters
                method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.ListAzureClustersRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.ListAzureClustersRequest):
            request = azure_service.ListAzureClustersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_azure_clusters]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAzureClustersPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_azure_cluster(
        self,
        request: Optional[Union[azure_service.DeleteAzureClusterRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a specific
        [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
        resource.

        Fails if the cluster has one or more associated
        [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool]
        resources.

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_delete_azure_cluster():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.DeleteAzureClusterRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_azure_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.DeleteAzureClusterRequest, dict]):
                The request object. Request message for ``Clusters.DeleteAzureCluster``
                method.
            name (str):
                Required. The resource name the
                [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
                to delete.

                ``AzureCluster`` names are formatted as
                ``projects/<project-id>/locations/<region>/azureClusters/<cluster-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud Platform resource
                names.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.DeleteAzureClusterRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.DeleteAzureClusterRequest):
            request = azure_service.DeleteAzureClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_azure_cluster]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def generate_azure_access_token(
        self,
        request: Optional[
            Union[azure_service.GenerateAzureAccessTokenRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> azure_service.GenerateAzureAccessTokenResponse:
        r"""Generates a short-lived access token to authenticate to a given
        [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
        resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_generate_azure_access_token():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GenerateAzureAccessTokenRequest(
                    azure_cluster="azure_cluster_value",
                )

                # Make the request
                response = client.generate_azure_access_token(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.GenerateAzureAccessTokenRequest, dict]):
                The request object. Request message for
                ``AzureClusters.GenerateAzureAccessToken`` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.GenerateAzureAccessTokenResponse:
                Response message for
                AzureClusters.GenerateAzureAccessToken method.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.GenerateAzureAccessTokenRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.GenerateAzureAccessTokenRequest):
            request = azure_service.GenerateAzureAccessTokenRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.generate_azure_access_token
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("azure_cluster", request.azure_cluster),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_azure_node_pool(
        self,
        request: Optional[Union[azure_service.CreateAzureNodePoolRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        azure_node_pool: Optional[azure_resources.AzureNodePool] = None,
        azure_node_pool_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new
        [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool],
        attached to a given
        [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster].

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_create_azure_node_pool():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                azure_node_pool = gke_multicloud_v1.AzureNodePool()
                azure_node_pool.version = "version_value"
                azure_node_pool.config.ssh_config.authorized_key = "authorized_key_value"
                azure_node_pool.subnet_id = "subnet_id_value"
                azure_node_pool.autoscaling.min_node_count = 1489
                azure_node_pool.autoscaling.max_node_count = 1491
                azure_node_pool.max_pods_constraint.max_pods_per_node = 1798

                request = gke_multicloud_v1.CreateAzureNodePoolRequest(
                    parent="parent_value",
                    azure_node_pool=azure_node_pool,
                    azure_node_pool_id="azure_node_pool_id_value",
                )

                # Make the request
                operation = client.create_azure_node_pool(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.CreateAzureNodePoolRequest, dict]):
                The request object. Response message for
                ``AzureClusters.CreateAzureNodePool`` method.
            parent (str):
                Required. The
                [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
                resource where this node pool will be created.

                Location names are formatted as
                ``projects/<project-id>/locations/<region>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            azure_node_pool (google.cloud.gke_multicloud_v1.types.AzureNodePool):
                Required. The specification of the
                [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool]
                to create.

                This corresponds to the ``azure_node_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            azure_node_pool_id (str):
                Required. A client provided ID the resource. Must be
                unique within the parent resource.

                The provided ID will be part of the
                [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool]
                resource name formatted as
                ``projects/<project-id>/locations/<region>/azureClusters/<cluster-id>/azureNodePools/<node-pool-id>``.

                Valid characters are ``/[a-z][0-9]-/``. Cannot be longer
                than 63 characters.

                This corresponds to the ``azure_node_pool_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.gke_multicloud_v1.types.AzureNodePool`
                An Anthos node pool running on Azure.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, azure_node_pool, azure_node_pool_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.CreateAzureNodePoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.CreateAzureNodePoolRequest):
            request = azure_service.CreateAzureNodePoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if azure_node_pool is not None:
                request.azure_node_pool = azure_node_pool
            if azure_node_pool_id is not None:
                request.azure_node_pool_id = azure_node_pool_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_azure_node_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            azure_resources.AzureNodePool,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_azure_node_pool(
        self,
        request: Optional[Union[azure_service.UpdateAzureNodePoolRequest, dict]] = None,
        *,
        azure_node_pool: Optional[azure_resources.AzureNodePool] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates an
        [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_update_azure_node_pool():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                azure_node_pool = gke_multicloud_v1.AzureNodePool()
                azure_node_pool.version = "version_value"
                azure_node_pool.config.ssh_config.authorized_key = "authorized_key_value"
                azure_node_pool.subnet_id = "subnet_id_value"
                azure_node_pool.autoscaling.min_node_count = 1489
                azure_node_pool.autoscaling.max_node_count = 1491
                azure_node_pool.max_pods_constraint.max_pods_per_node = 1798

                request = gke_multicloud_v1.UpdateAzureNodePoolRequest(
                    azure_node_pool=azure_node_pool,
                )

                # Make the request
                operation = client.update_azure_node_pool(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.UpdateAzureNodePoolRequest, dict]):
                The request object. Request message for
                ``AzureClusters.UpdateAzureNodePool`` method.
            azure_node_pool (google.cloud.gke_multicloud_v1.types.AzureNodePool):
                Required. The
                [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool]
                resource to update.

                This corresponds to the ``azure_node_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Mask of fields to update. At least one path
                must be supplied in this field. The elements of the
                repeated paths field can only include these fields from
                [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool]:

                \*. ``annotations``.

                -  ``version``.
                -  ``autoscaling.min_node_count``.
                -  ``autoscaling.max_node_count``.
                -  ``config.ssh_config.authorized_key``.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.gke_multicloud_v1.types.AzureNodePool`
                An Anthos node pool running on Azure.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([azure_node_pool, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.UpdateAzureNodePoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.UpdateAzureNodePoolRequest):
            request = azure_service.UpdateAzureNodePoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if azure_node_pool is not None:
                request.azure_node_pool = azure_node_pool
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_azure_node_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("azure_node_pool.name", request.azure_node_pool.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            azure_resources.AzureNodePool,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_azure_node_pool(
        self,
        request: Optional[Union[azure_service.GetAzureNodePoolRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> azure_resources.AzureNodePool:
        r"""Describes a specific
        [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool]
        resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_get_azure_node_pool():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GetAzureNodePoolRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_azure_node_pool(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.GetAzureNodePoolRequest, dict]):
                The request object. Request message for ``AzureClusters.GetAzureNodePool``
                method.
            name (str):
                Required. The name of the
                [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool]
                resource to describe.

                ``AzureNodePool`` names are formatted as
                ``projects/<project-id>/locations/<region>/azureClusters/<cluster-id>/azureNodePools/<node-pool-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.AzureNodePool:
                An Anthos node pool running on Azure.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.GetAzureNodePoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.GetAzureNodePoolRequest):
            request = azure_service.GetAzureNodePoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_azure_node_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_azure_node_pools(
        self,
        request: Optional[Union[azure_service.ListAzureNodePoolsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAzureNodePoolsPager:
        r"""Lists all
        [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool]
        resources on a given
        [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_list_azure_node_pools():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.ListAzureNodePoolsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_azure_node_pools(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.ListAzureNodePoolsRequest, dict]):
                The request object. Request message for ``AzureClusters.ListAzureNodePools``
                method.
            parent (str):
                Required. The parent ``AzureCluster`` which owns this
                collection of
                [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool]
                resources.

                ``AzureCluster`` names are formatted as
                ``projects/<project-id>/locations/<region>/azureClusters/<cluster-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.services.azure_clusters.pagers.ListAzureNodePoolsPager:
                Response message for AzureClusters.ListAzureNodePools
                method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.ListAzureNodePoolsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.ListAzureNodePoolsRequest):
            request = azure_service.ListAzureNodePoolsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_azure_node_pools]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAzureNodePoolsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_azure_node_pool(
        self,
        request: Optional[Union[azure_service.DeleteAzureNodePoolRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a specific
        [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool]
        resource.

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_delete_azure_node_pool():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.DeleteAzureNodePoolRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_azure_node_pool(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.DeleteAzureNodePoolRequest, dict]):
                The request object. Delete message for ``AzureClusters.DeleteAzureNodePool``
                method.
            name (str):
                Required. The resource name the
                [AzureNodePool][google.cloud.gkemulticloud.v1.AzureNodePool]
                to delete.

                ``AzureNodePool`` names are formatted as
                ``projects/<project-id>/locations/<region>/azureClusters/<cluster-id>/azureNodePools/<node-pool-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.DeleteAzureNodePoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.DeleteAzureNodePoolRequest):
            request = azure_service.DeleteAzureNodePoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_azure_node_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_azure_server_config(
        self,
        request: Optional[
            Union[azure_service.GetAzureServerConfigRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> azure_resources.AzureServerConfig:
        r"""Returns information, such as supported Azure regions
        and Kubernetes versions, on a given Google Cloud
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            def sample_get_azure_server_config():
                # Create a client
                client = gke_multicloud_v1.AzureClustersClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GetAzureServerConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_azure_server_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_multicloud_v1.types.GetAzureServerConfigRequest, dict]):
                The request object. GetAzureServerConfigRequest gets the
                server config of GKE cluster on Azure.
            name (str):
                Required. The name of the
                [AzureServerConfig][google.cloud.gkemulticloud.v1.AzureServerConfig]
                resource to describe.

                ``AzureServerConfig`` names are formatted as
                ``projects/<project-id>/locations/<region>/azureServerConfig``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.AzureServerConfig:
                AzureServerConfig contains
                information about a Google Cloud
                location, such as supported Azure
                regions and Kubernetes versions.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a azure_service.GetAzureServerConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, azure_service.GetAzureServerConfigRequest):
            request = azure_service.GetAzureServerConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_azure_server_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "AzureClustersClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_operations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_operation(
        self,
        request: Optional[operations_pb2.DeleteOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a long-running operation.

        This method indicates that the client is no longer interested
        in the operation result. It does not cancel the operation.
        If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.DeleteOperationRequest`):
                The request object. Request message for
                `DeleteOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.DeleteOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def cancel_operation(
        self,
        request: Optional[operations_pb2.CancelOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.cancel_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("AzureClustersClient",)
