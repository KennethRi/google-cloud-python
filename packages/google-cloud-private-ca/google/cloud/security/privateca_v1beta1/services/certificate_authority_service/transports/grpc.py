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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers, operations_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore

from google.cloud.security.privateca_v1beta1.types import resources, service

from .base import DEFAULT_CLIENT_INFO, CertificateAuthorityServiceTransport


class CertificateAuthorityServiceGrpcTransport(CertificateAuthorityServiceTransport):
    """gRPC backend transport for CertificateAuthorityService.

    [Certificate Authority
    Service][google.cloud.security.privateca.v1beta1.CertificateAuthorityService]
    manages private certificate authorities and issued certificates.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "privateca.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[grpc.Channel] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
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
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "privateca.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(self.grpc_channel)

        # Return the client from cache.
        return self._operations_client

    @property
    def create_certificate(
        self,
    ) -> Callable[[service.CreateCertificateRequest], resources.Certificate]:
        r"""Return a callable for the create certificate method over gRPC.

        Create a new
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
        in a given Project, Location from a particular
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Returns:
            Callable[[~.CreateCertificateRequest],
                    ~.Certificate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_certificate" not in self._stubs:
            self._stubs["create_certificate"] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/CreateCertificate",
                request_serializer=service.CreateCertificateRequest.serialize,
                response_deserializer=resources.Certificate.deserialize,
            )
        return self._stubs["create_certificate"]

    @property
    def get_certificate(
        self,
    ) -> Callable[[service.GetCertificateRequest], resources.Certificate]:
        r"""Return a callable for the get certificate method over gRPC.

        Returns a
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate].

        Returns:
            Callable[[~.GetCertificateRequest],
                    ~.Certificate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_certificate" not in self._stubs:
            self._stubs["get_certificate"] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/GetCertificate",
                request_serializer=service.GetCertificateRequest.serialize,
                response_deserializer=resources.Certificate.deserialize,
            )
        return self._stubs["get_certificate"]

    @property
    def list_certificates(
        self,
    ) -> Callable[[service.ListCertificatesRequest], service.ListCertificatesResponse]:
        r"""Return a callable for the list certificates method over gRPC.

        Lists
        [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

        Returns:
            Callable[[~.ListCertificatesRequest],
                    ~.ListCertificatesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_certificates" not in self._stubs:
            self._stubs["list_certificates"] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/ListCertificates",
                request_serializer=service.ListCertificatesRequest.serialize,
                response_deserializer=service.ListCertificatesResponse.deserialize,
            )
        return self._stubs["list_certificates"]

    @property
    def revoke_certificate(
        self,
    ) -> Callable[[service.RevokeCertificateRequest], resources.Certificate]:
        r"""Return a callable for the revoke certificate method over gRPC.

        Revoke a
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate].

        Returns:
            Callable[[~.RevokeCertificateRequest],
                    ~.Certificate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "revoke_certificate" not in self._stubs:
            self._stubs["revoke_certificate"] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/RevokeCertificate",
                request_serializer=service.RevokeCertificateRequest.serialize,
                response_deserializer=resources.Certificate.deserialize,
            )
        return self._stubs["revoke_certificate"]

    @property
    def update_certificate(
        self,
    ) -> Callable[[service.UpdateCertificateRequest], resources.Certificate]:
        r"""Return a callable for the update certificate method over gRPC.

        Update a
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate].
        Currently, the only field you can update is the
        [labels][google.cloud.security.privateca.v1beta1.Certificate.labels]
        field.

        Returns:
            Callable[[~.UpdateCertificateRequest],
                    ~.Certificate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_certificate" not in self._stubs:
            self._stubs["update_certificate"] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/UpdateCertificate",
                request_serializer=service.UpdateCertificateRequest.serialize,
                response_deserializer=resources.Certificate.deserialize,
            )
        return self._stubs["update_certificate"]

    @property
    def activate_certificate_authority(
        self,
    ) -> Callable[
        [service.ActivateCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the activate certificate authority method over gRPC.

        Activate a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        that is in state
        [PENDING_ACTIVATION][google.cloud.security.privateca.v1beta1.CertificateAuthority.State.PENDING_ACTIVATION]
        and is of type
        [SUBORDINATE][google.cloud.security.privateca.v1beta1.CertificateAuthority.Type.SUBORDINATE].
        After the parent Certificate Authority signs a certificate
        signing request from
        [FetchCertificateAuthorityCsr][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.FetchCertificateAuthorityCsr],
        this method can complete the activation process.

        Returns:
            Callable[[~.ActivateCertificateAuthorityRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "activate_certificate_authority" not in self._stubs:
            self._stubs[
                "activate_certificate_authority"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/ActivateCertificateAuthority",
                request_serializer=service.ActivateCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["activate_certificate_authority"]

    @property
    def create_certificate_authority(
        self,
    ) -> Callable[
        [service.CreateCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the create certificate authority method over gRPC.

        Create a new
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        in a given Project and Location.

        Returns:
            Callable[[~.CreateCertificateAuthorityRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_certificate_authority" not in self._stubs:
            self._stubs["create_certificate_authority"] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/CreateCertificateAuthority",
                request_serializer=service.CreateCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_certificate_authority"]

    @property
    def disable_certificate_authority(
        self,
    ) -> Callable[
        [service.DisableCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the disable certificate authority method over gRPC.

        Disable a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Returns:
            Callable[[~.DisableCertificateAuthorityRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "disable_certificate_authority" not in self._stubs:
            self._stubs[
                "disable_certificate_authority"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/DisableCertificateAuthority",
                request_serializer=service.DisableCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["disable_certificate_authority"]

    @property
    def enable_certificate_authority(
        self,
    ) -> Callable[
        [service.EnableCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the enable certificate authority method over gRPC.

        Enable a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Returns:
            Callable[[~.EnableCertificateAuthorityRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "enable_certificate_authority" not in self._stubs:
            self._stubs["enable_certificate_authority"] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/EnableCertificateAuthority",
                request_serializer=service.EnableCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["enable_certificate_authority"]

    @property
    def fetch_certificate_authority_csr(
        self,
    ) -> Callable[
        [service.FetchCertificateAuthorityCsrRequest],
        service.FetchCertificateAuthorityCsrResponse,
    ]:
        r"""Return a callable for the fetch certificate authority
        csr method over gRPC.

        Fetch a certificate signing request (CSR) from a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        that is in state
        [PENDING_ACTIVATION][google.cloud.security.privateca.v1beta1.CertificateAuthority.State.PENDING_ACTIVATION]
        and is of type
        [SUBORDINATE][google.cloud.security.privateca.v1beta1.CertificateAuthority.Type.SUBORDINATE].
        The CSR must then be signed by the desired parent Certificate
        Authority, which could be another
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        resource, or could be an on-prem certificate authority. See also
        [ActivateCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ActivateCertificateAuthority].

        Returns:
            Callable[[~.FetchCertificateAuthorityCsrRequest],
                    ~.FetchCertificateAuthorityCsrResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_certificate_authority_csr" not in self._stubs:
            self._stubs[
                "fetch_certificate_authority_csr"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/FetchCertificateAuthorityCsr",
                request_serializer=service.FetchCertificateAuthorityCsrRequest.serialize,
                response_deserializer=service.FetchCertificateAuthorityCsrResponse.deserialize,
            )
        return self._stubs["fetch_certificate_authority_csr"]

    @property
    def get_certificate_authority(
        self,
    ) -> Callable[
        [service.GetCertificateAuthorityRequest], resources.CertificateAuthority
    ]:
        r"""Return a callable for the get certificate authority method over gRPC.

        Returns a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Returns:
            Callable[[~.GetCertificateAuthorityRequest],
                    ~.CertificateAuthority]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_certificate_authority" not in self._stubs:
            self._stubs["get_certificate_authority"] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/GetCertificateAuthority",
                request_serializer=service.GetCertificateAuthorityRequest.serialize,
                response_deserializer=resources.CertificateAuthority.deserialize,
            )
        return self._stubs["get_certificate_authority"]

    @property
    def list_certificate_authorities(
        self,
    ) -> Callable[
        [service.ListCertificateAuthoritiesRequest],
        service.ListCertificateAuthoritiesResponse,
    ]:
        r"""Return a callable for the list certificate authorities method over gRPC.

        Lists
        [CertificateAuthorities][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Returns:
            Callable[[~.ListCertificateAuthoritiesRequest],
                    ~.ListCertificateAuthoritiesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_certificate_authorities" not in self._stubs:
            self._stubs["list_certificate_authorities"] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/ListCertificateAuthorities",
                request_serializer=service.ListCertificateAuthoritiesRequest.serialize,
                response_deserializer=service.ListCertificateAuthoritiesResponse.deserialize,
            )
        return self._stubs["list_certificate_authorities"]

    @property
    def restore_certificate_authority(
        self,
    ) -> Callable[
        [service.RestoreCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the restore certificate authority method over gRPC.

        Restore a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        that is scheduled for deletion.

        Returns:
            Callable[[~.RestoreCertificateAuthorityRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restore_certificate_authority" not in self._stubs:
            self._stubs[
                "restore_certificate_authority"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/RestoreCertificateAuthority",
                request_serializer=service.RestoreCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restore_certificate_authority"]

    @property
    def schedule_delete_certificate_authority(
        self,
    ) -> Callable[
        [service.ScheduleDeleteCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the schedule delete certificate
        authority method over gRPC.

        Schedule a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        for deletion.

        Returns:
            Callable[[~.ScheduleDeleteCertificateAuthorityRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "schedule_delete_certificate_authority" not in self._stubs:
            self._stubs[
                "schedule_delete_certificate_authority"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/ScheduleDeleteCertificateAuthority",
                request_serializer=service.ScheduleDeleteCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["schedule_delete_certificate_authority"]

    @property
    def update_certificate_authority(
        self,
    ) -> Callable[
        [service.UpdateCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the update certificate authority method over gRPC.

        Update a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Returns:
            Callable[[~.UpdateCertificateAuthorityRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_certificate_authority" not in self._stubs:
            self._stubs["update_certificate_authority"] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/UpdateCertificateAuthority",
                request_serializer=service.UpdateCertificateAuthorityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_certificate_authority"]

    @property
    def get_certificate_revocation_list(
        self,
    ) -> Callable[
        [service.GetCertificateRevocationListRequest],
        resources.CertificateRevocationList,
    ]:
        r"""Return a callable for the get certificate revocation
        list method over gRPC.

        Returns a
        [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList].

        Returns:
            Callable[[~.GetCertificateRevocationListRequest],
                    ~.CertificateRevocationList]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_certificate_revocation_list" not in self._stubs:
            self._stubs[
                "get_certificate_revocation_list"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/GetCertificateRevocationList",
                request_serializer=service.GetCertificateRevocationListRequest.serialize,
                response_deserializer=resources.CertificateRevocationList.deserialize,
            )
        return self._stubs["get_certificate_revocation_list"]

    @property
    def list_certificate_revocation_lists(
        self,
    ) -> Callable[
        [service.ListCertificateRevocationListsRequest],
        service.ListCertificateRevocationListsResponse,
    ]:
        r"""Return a callable for the list certificate revocation
        lists method over gRPC.

        Lists
        [CertificateRevocationLists][google.cloud.security.privateca.v1beta1.CertificateRevocationList].

        Returns:
            Callable[[~.ListCertificateRevocationListsRequest],
                    ~.ListCertificateRevocationListsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_certificate_revocation_lists" not in self._stubs:
            self._stubs[
                "list_certificate_revocation_lists"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/ListCertificateRevocationLists",
                request_serializer=service.ListCertificateRevocationListsRequest.serialize,
                response_deserializer=service.ListCertificateRevocationListsResponse.deserialize,
            )
        return self._stubs["list_certificate_revocation_lists"]

    @property
    def update_certificate_revocation_list(
        self,
    ) -> Callable[
        [service.UpdateCertificateRevocationListRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the update certificate revocation
        list method over gRPC.

        Update a
        [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList].

        Returns:
            Callable[[~.UpdateCertificateRevocationListRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_certificate_revocation_list" not in self._stubs:
            self._stubs[
                "update_certificate_revocation_list"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/UpdateCertificateRevocationList",
                request_serializer=service.UpdateCertificateRevocationListRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_certificate_revocation_list"]

    @property
    def get_reusable_config(
        self,
    ) -> Callable[[service.GetReusableConfigRequest], resources.ReusableConfig]:
        r"""Return a callable for the get reusable config method over gRPC.

        Returns a
        [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig].

        Returns:
            Callable[[~.GetReusableConfigRequest],
                    ~.ReusableConfig]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_reusable_config" not in self._stubs:
            self._stubs["get_reusable_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/GetReusableConfig",
                request_serializer=service.GetReusableConfigRequest.serialize,
                response_deserializer=resources.ReusableConfig.deserialize,
            )
        return self._stubs["get_reusable_config"]

    @property
    def list_reusable_configs(
        self,
    ) -> Callable[
        [service.ListReusableConfigsRequest], service.ListReusableConfigsResponse
    ]:
        r"""Return a callable for the list reusable configs method over gRPC.

        Lists
        [ReusableConfigs][google.cloud.security.privateca.v1beta1.ReusableConfig].

        Returns:
            Callable[[~.ListReusableConfigsRequest],
                    ~.ListReusableConfigsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_reusable_configs" not in self._stubs:
            self._stubs["list_reusable_configs"] = self.grpc_channel.unary_unary(
                "/google.cloud.security.privateca.v1beta1.CertificateAuthorityService/ListReusableConfigs",
                request_serializer=service.ListReusableConfigsRequest.serialize,
                response_deserializer=service.ListReusableConfigsResponse.deserialize,
            )
        return self._stubs["list_reusable_configs"]

    def close(self):
        self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("CertificateAuthorityServiceGrpcTransport",)
