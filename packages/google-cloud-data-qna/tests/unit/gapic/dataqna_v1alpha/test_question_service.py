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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import Iterable
import json
import math

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.dataqna_v1alpha.services.question_service import (
    QuestionServiceAsyncClient,
    QuestionServiceClient,
    transports,
)
from google.cloud.dataqna_v1alpha.types import user_feedback as gcd_user_feedback
from google.cloud.dataqna_v1alpha.types import annotated_string
from google.cloud.dataqna_v1alpha.types import question
from google.cloud.dataqna_v1alpha.types import question as gcd_question
from google.cloud.dataqna_v1alpha.types import question_service
from google.cloud.dataqna_v1alpha.types import user_feedback


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert QuestionServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        QuestionServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        QuestionServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        QuestionServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        QuestionServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        QuestionServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (QuestionServiceClient, "grpc"),
        (QuestionServiceAsyncClient, "grpc_asyncio"),
        (QuestionServiceClient, "rest"),
    ],
)
def test_question_service_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "dataqna.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://dataqna.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.QuestionServiceGrpcTransport, "grpc"),
        (transports.QuestionServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.QuestionServiceRestTransport, "rest"),
    ],
)
def test_question_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (QuestionServiceClient, "grpc"),
        (QuestionServiceAsyncClient, "grpc_asyncio"),
        (QuestionServiceClient, "rest"),
    ],
)
def test_question_service_client_from_service_account_file(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "dataqna.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://dataqna.googleapis.com"
        )


def test_question_service_client_get_transport_class():
    transport = QuestionServiceClient.get_transport_class()
    available_transports = [
        transports.QuestionServiceGrpcTransport,
        transports.QuestionServiceRestTransport,
    ]
    assert transport in available_transports

    transport = QuestionServiceClient.get_transport_class("grpc")
    assert transport == transports.QuestionServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (QuestionServiceClient, transports.QuestionServiceGrpcTransport, "grpc"),
        (
            QuestionServiceAsyncClient,
            transports.QuestionServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (QuestionServiceClient, transports.QuestionServiceRestTransport, "rest"),
    ],
)
@mock.patch.object(
    QuestionServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(QuestionServiceClient),
)
@mock.patch.object(
    QuestionServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(QuestionServiceAsyncClient),
)
def test_question_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(QuestionServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(QuestionServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            QuestionServiceClient,
            transports.QuestionServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            QuestionServiceAsyncClient,
            transports.QuestionServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            QuestionServiceClient,
            transports.QuestionServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            QuestionServiceAsyncClient,
            transports.QuestionServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            QuestionServiceClient,
            transports.QuestionServiceRestTransport,
            "rest",
            "true",
        ),
        (
            QuestionServiceClient,
            transports.QuestionServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    QuestionServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(QuestionServiceClient),
)
@mock.patch.object(
    QuestionServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(QuestionServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_question_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [QuestionServiceClient, QuestionServiceAsyncClient]
)
@mock.patch.object(
    QuestionServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(QuestionServiceClient),
)
@mock.patch.object(
    QuestionServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(QuestionServiceAsyncClient),
)
def test_question_service_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (QuestionServiceClient, transports.QuestionServiceGrpcTransport, "grpc"),
        (
            QuestionServiceAsyncClient,
            transports.QuestionServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (QuestionServiceClient, transports.QuestionServiceRestTransport, "rest"),
    ],
)
def test_question_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            QuestionServiceClient,
            transports.QuestionServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            QuestionServiceAsyncClient,
            transports.QuestionServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (QuestionServiceClient, transports.QuestionServiceRestTransport, "rest", None),
    ],
)
def test_question_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_question_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dataqna_v1alpha.services.question_service.transports.QuestionServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = QuestionServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            QuestionServiceClient,
            transports.QuestionServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            QuestionServiceAsyncClient,
            transports.QuestionServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_question_service_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "dataqna.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="dataqna.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        question_service.GetQuestionRequest,
        dict,
    ],
)
def test_get_question(request_type, transport: str = "grpc"):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = question.Question(
            name="name_value",
            scopes=["scopes_value"],
            query="query_value",
            data_source_annotations=["data_source_annotations_value"],
            user_email="user_email_value",
        )
        response = client.get_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.GetQuestionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, question.Question)
    assert response.name == "name_value"
    assert response.scopes == ["scopes_value"]
    assert response.query == "query_value"
    assert response.data_source_annotations == ["data_source_annotations_value"]
    assert response.user_email == "user_email_value"


def test_get_question_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        client.get_question()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.GetQuestionRequest()


@pytest.mark.asyncio
async def test_get_question_async(
    transport: str = "grpc_asyncio", request_type=question_service.GetQuestionRequest
):
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            question.Question(
                name="name_value",
                scopes=["scopes_value"],
                query="query_value",
                data_source_annotations=["data_source_annotations_value"],
                user_email="user_email_value",
            )
        )
        response = await client.get_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.GetQuestionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, question.Question)
    assert response.name == "name_value"
    assert response.scopes == ["scopes_value"]
    assert response.query == "query_value"
    assert response.data_source_annotations == ["data_source_annotations_value"]
    assert response.user_email == "user_email_value"


@pytest.mark.asyncio
async def test_get_question_async_from_dict():
    await test_get_question_async(request_type=dict)


def test_get_question_field_headers():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.GetQuestionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        call.return_value = question.Question()
        client.get_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_question_field_headers_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.GetQuestionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(question.Question())
        await client.get_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_question_flattened():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = question.Question()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_question(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_question_flattened_error():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_question(
            question_service.GetQuestionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_question_flattened_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = question.Question()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(question.Question())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_question(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_question_flattened_error_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_question(
            question_service.GetQuestionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        question_service.CreateQuestionRequest,
        dict,
    ],
)
def test_create_question(request_type, transport: str = "grpc"):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_question.Question(
            name="name_value",
            scopes=["scopes_value"],
            query="query_value",
            data_source_annotations=["data_source_annotations_value"],
            user_email="user_email_value",
        )
        response = client.create_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.CreateQuestionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_question.Question)
    assert response.name == "name_value"
    assert response.scopes == ["scopes_value"]
    assert response.query == "query_value"
    assert response.data_source_annotations == ["data_source_annotations_value"]
    assert response.user_email == "user_email_value"


def test_create_question_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        client.create_question()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.CreateQuestionRequest()


@pytest.mark.asyncio
async def test_create_question_async(
    transport: str = "grpc_asyncio", request_type=question_service.CreateQuestionRequest
):
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_question.Question(
                name="name_value",
                scopes=["scopes_value"],
                query="query_value",
                data_source_annotations=["data_source_annotations_value"],
                user_email="user_email_value",
            )
        )
        response = await client.create_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.CreateQuestionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_question.Question)
    assert response.name == "name_value"
    assert response.scopes == ["scopes_value"]
    assert response.query == "query_value"
    assert response.data_source_annotations == ["data_source_annotations_value"]
    assert response.user_email == "user_email_value"


@pytest.mark.asyncio
async def test_create_question_async_from_dict():
    await test_create_question_async(request_type=dict)


def test_create_question_field_headers():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.CreateQuestionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        call.return_value = gcd_question.Question()
        client.create_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_question_field_headers_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.CreateQuestionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_question.Question()
        )
        await client.create_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_question_flattened():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_question.Question()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_question(
            parent="parent_value",
            question=gcd_question.Question(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].question
        mock_val = gcd_question.Question(name="name_value")
        assert arg == mock_val


def test_create_question_flattened_error():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_question(
            question_service.CreateQuestionRequest(),
            parent="parent_value",
            question=gcd_question.Question(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_question_flattened_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_question.Question()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_question.Question()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_question(
            parent="parent_value",
            question=gcd_question.Question(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].question
        mock_val = gcd_question.Question(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_question_flattened_error_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_question(
            question_service.CreateQuestionRequest(),
            parent="parent_value",
            question=gcd_question.Question(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        question_service.ExecuteQuestionRequest,
        dict,
    ],
)
def test_execute_question(request_type, transport: str = "grpc"):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = question.Question(
            name="name_value",
            scopes=["scopes_value"],
            query="query_value",
            data_source_annotations=["data_source_annotations_value"],
            user_email="user_email_value",
        )
        response = client.execute_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.ExecuteQuestionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, question.Question)
    assert response.name == "name_value"
    assert response.scopes == ["scopes_value"]
    assert response.query == "query_value"
    assert response.data_source_annotations == ["data_source_annotations_value"]
    assert response.user_email == "user_email_value"


def test_execute_question_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        client.execute_question()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.ExecuteQuestionRequest()


@pytest.mark.asyncio
async def test_execute_question_async(
    transport: str = "grpc_asyncio",
    request_type=question_service.ExecuteQuestionRequest,
):
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            question.Question(
                name="name_value",
                scopes=["scopes_value"],
                query="query_value",
                data_source_annotations=["data_source_annotations_value"],
                user_email="user_email_value",
            )
        )
        response = await client.execute_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.ExecuteQuestionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, question.Question)
    assert response.name == "name_value"
    assert response.scopes == ["scopes_value"]
    assert response.query == "query_value"
    assert response.data_source_annotations == ["data_source_annotations_value"]
    assert response.user_email == "user_email_value"


@pytest.mark.asyncio
async def test_execute_question_async_from_dict():
    await test_execute_question_async(request_type=dict)


def test_execute_question_field_headers():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.ExecuteQuestionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        call.return_value = question.Question()
        client.execute_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_execute_question_field_headers_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.ExecuteQuestionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(question.Question())
        await client.execute_question(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_execute_question_flattened():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = question.Question()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.execute_question(
            name="name_value",
            interpretation_index=2159,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].interpretation_index
        mock_val = 2159
        assert arg == mock_val


def test_execute_question_flattened_error():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.execute_question(
            question_service.ExecuteQuestionRequest(),
            name="name_value",
            interpretation_index=2159,
        )


@pytest.mark.asyncio
async def test_execute_question_flattened_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.execute_question), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = question.Question()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(question.Question())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.execute_question(
            name="name_value",
            interpretation_index=2159,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].interpretation_index
        mock_val = 2159
        assert arg == mock_val


@pytest.mark.asyncio
async def test_execute_question_flattened_error_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.execute_question(
            question_service.ExecuteQuestionRequest(),
            name="name_value",
            interpretation_index=2159,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        question_service.GetUserFeedbackRequest,
        dict,
    ],
)
def test_get_user_feedback(request_type, transport: str = "grpc"):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = user_feedback.UserFeedback(
            name="name_value",
            free_form_feedback="free_form_feedback_value",
            rating=user_feedback.UserFeedback.UserFeedbackRating.POSITIVE,
        )
        response = client.get_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.GetUserFeedbackRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, user_feedback.UserFeedback)
    assert response.name == "name_value"
    assert response.free_form_feedback == "free_form_feedback_value"
    assert response.rating == user_feedback.UserFeedback.UserFeedbackRating.POSITIVE


def test_get_user_feedback_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        client.get_user_feedback()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.GetUserFeedbackRequest()


@pytest.mark.asyncio
async def test_get_user_feedback_async(
    transport: str = "grpc_asyncio",
    request_type=question_service.GetUserFeedbackRequest,
):
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            user_feedback.UserFeedback(
                name="name_value",
                free_form_feedback="free_form_feedback_value",
                rating=user_feedback.UserFeedback.UserFeedbackRating.POSITIVE,
            )
        )
        response = await client.get_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.GetUserFeedbackRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, user_feedback.UserFeedback)
    assert response.name == "name_value"
    assert response.free_form_feedback == "free_form_feedback_value"
    assert response.rating == user_feedback.UserFeedback.UserFeedbackRating.POSITIVE


@pytest.mark.asyncio
async def test_get_user_feedback_async_from_dict():
    await test_get_user_feedback_async(request_type=dict)


def test_get_user_feedback_field_headers():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.GetUserFeedbackRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        call.return_value = user_feedback.UserFeedback()
        client.get_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_user_feedback_field_headers_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.GetUserFeedbackRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            user_feedback.UserFeedback()
        )
        await client.get_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_user_feedback_flattened():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = user_feedback.UserFeedback()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_user_feedback(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_user_feedback_flattened_error():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_user_feedback(
            question_service.GetUserFeedbackRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_user_feedback_flattened_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = user_feedback.UserFeedback()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            user_feedback.UserFeedback()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_user_feedback(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_user_feedback_flattened_error_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_user_feedback(
            question_service.GetUserFeedbackRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        question_service.UpdateUserFeedbackRequest,
        dict,
    ],
)
def test_update_user_feedback(request_type, transport: str = "grpc"):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_user_feedback.UserFeedback(
            name="name_value",
            free_form_feedback="free_form_feedback_value",
            rating=gcd_user_feedback.UserFeedback.UserFeedbackRating.POSITIVE,
        )
        response = client.update_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.UpdateUserFeedbackRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_user_feedback.UserFeedback)
    assert response.name == "name_value"
    assert response.free_form_feedback == "free_form_feedback_value"
    assert response.rating == gcd_user_feedback.UserFeedback.UserFeedbackRating.POSITIVE


def test_update_user_feedback_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        client.update_user_feedback()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.UpdateUserFeedbackRequest()


@pytest.mark.asyncio
async def test_update_user_feedback_async(
    transport: str = "grpc_asyncio",
    request_type=question_service.UpdateUserFeedbackRequest,
):
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_user_feedback.UserFeedback(
                name="name_value",
                free_form_feedback="free_form_feedback_value",
                rating=gcd_user_feedback.UserFeedback.UserFeedbackRating.POSITIVE,
            )
        )
        response = await client.update_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == question_service.UpdateUserFeedbackRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_user_feedback.UserFeedback)
    assert response.name == "name_value"
    assert response.free_form_feedback == "free_form_feedback_value"
    assert response.rating == gcd_user_feedback.UserFeedback.UserFeedbackRating.POSITIVE


@pytest.mark.asyncio
async def test_update_user_feedback_async_from_dict():
    await test_update_user_feedback_async(request_type=dict)


def test_update_user_feedback_field_headers():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.UpdateUserFeedbackRequest()

    request.user_feedback.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        call.return_value = gcd_user_feedback.UserFeedback()
        client.update_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "user_feedback.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_user_feedback_field_headers_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = question_service.UpdateUserFeedbackRequest()

    request.user_feedback.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_user_feedback.UserFeedback()
        )
        await client.update_user_feedback(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "user_feedback.name=name_value",
    ) in kw["metadata"]


def test_update_user_feedback_flattened():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_user_feedback.UserFeedback()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_user_feedback(
            user_feedback=gcd_user_feedback.UserFeedback(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].user_feedback
        mock_val = gcd_user_feedback.UserFeedback(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_user_feedback_flattened_error():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_user_feedback(
            question_service.UpdateUserFeedbackRequest(),
            user_feedback=gcd_user_feedback.UserFeedback(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_user_feedback_flattened_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_user_feedback), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_user_feedback.UserFeedback()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_user_feedback.UserFeedback()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_user_feedback(
            user_feedback=gcd_user_feedback.UserFeedback(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].user_feedback
        mock_val = gcd_user_feedback.UserFeedback(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_user_feedback_flattened_error_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_user_feedback(
            question_service.UpdateUserFeedbackRequest(),
            user_feedback=gcd_user_feedback.UserFeedback(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        question_service.GetQuestionRequest,
        dict,
    ],
)
def test_get_question_rest(request_type):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/questions/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = question.Question(
            name="name_value",
            scopes=["scopes_value"],
            query="query_value",
            data_source_annotations=["data_source_annotations_value"],
            user_email="user_email_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = question.Question.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_question(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, question.Question)
    assert response.name == "name_value"
    assert response.scopes == ["scopes_value"]
    assert response.query == "query_value"
    assert response.data_source_annotations == ["data_source_annotations_value"]
    assert response.user_email == "user_email_value"


def test_get_question_rest_required_fields(
    request_type=question_service.GetQuestionRequest,
):
    transport_class = transports.QuestionServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_question._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_question._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("read_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = question.Question()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = question.Question.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_question(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_question_rest_unset_required_fields():
    transport = transports.QuestionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_question._get_unset_required_fields({})
    assert set(unset_fields) == (set(("readMask",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_question_rest_interceptors(null_interceptor):
    transport = transports.QuestionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.QuestionServiceRestInterceptor(),
    )
    client = QuestionServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.QuestionServiceRestInterceptor, "post_get_question"
    ) as post, mock.patch.object(
        transports.QuestionServiceRestInterceptor, "pre_get_question"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = question_service.GetQuestionRequest.pb(
            question_service.GetQuestionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = question.Question.to_json(question.Question())

        request = question_service.GetQuestionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = question.Question()

        client.get_question(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_question_rest_bad_request(
    transport: str = "rest", request_type=question_service.GetQuestionRequest
):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/questions/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_question(request)


def test_get_question_rest_flattened():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = question.Question()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/questions/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = question.Question.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_question(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=projects/*/locations/*/questions/*}"
            % client.transport._host,
            args[1],
        )


def test_get_question_rest_flattened_error(transport: str = "rest"):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_question(
            question_service.GetQuestionRequest(),
            name="name_value",
        )


def test_get_question_rest_error():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        question_service.CreateQuestionRequest,
        dict,
    ],
)
def test_create_question_rest(request_type):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["question"] = {
        "name": "name_value",
        "scopes": ["scopes_value1", "scopes_value2"],
        "query": "query_value",
        "data_source_annotations": [
            "data_source_annotations_value1",
            "data_source_annotations_value2",
        ],
        "interpret_error": {
            "message": "message_value",
            "code": 1,
            "details": {
                "unsupported_details": {
                    "operators": ["operators_value1", "operators_value2"],
                    "intent": ["intent_value1", "intent_value2"],
                },
                "incomplete_query_details": {"entities": [1]},
                "ambiguity_details": {},
            },
        },
        "interpretations": [
            {
                "data_sources": ["data_sources_value1", "data_sources_value2"],
                "confidence": 0.1038,
                "unused_phrases": ["unused_phrases_value1", "unused_phrases_value2"],
                "human_readable": {
                    "generated_interpretation": {
                        "text_formatted": "text_formatted_value",
                        "html_formatted": "html_formatted_value",
                        "markups": [
                            {"type_": 1, "start_char_index": 1698, "length": 642}
                        ],
                    },
                    "original_question": {},
                },
                "interpretation_structure": {
                    "visualization_types": [1],
                    "column_info": [
                        {
                            "output_alias": "output_alias_value",
                            "display_name": "display_name_value",
                        }
                    ],
                },
                "data_query": {"sql": "sql_value"},
                "execution_info": {
                    "job_creation_status": {
                        "code": 411,
                        "message": "message_value",
                        "details": [
                            {
                                "type_url": "type.googleapis.com/google.protobuf.Duration",
                                "value": b"\x08\x0c\x10\xdb\x07",
                            }
                        ],
                    },
                    "job_execution_state": 1,
                    "create_time": {"seconds": 751, "nanos": 543},
                    "bigquery_job": {
                        "job_id": "job_id_value",
                        "project_id": "project_id_value",
                        "location": "location_value",
                    },
                },
            }
        ],
        "create_time": {},
        "user_email": "user_email_value",
        "debug_flags": {
            "include_va_query": True,
            "include_nested_va_query": True,
            "include_human_interpretation": True,
            "include_aqua_debug_response": True,
            "time_override": 1390,
            "is_internal_google_user": True,
            "ignore_cache": True,
            "include_search_entities_rpc": True,
            "include_list_column_annotations_rpc": True,
            "include_virtual_analyst_entities": True,
            "include_table_list": True,
            "include_domain_list": True,
        },
        "debug_info": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcd_question.Question(
            name="name_value",
            scopes=["scopes_value"],
            query="query_value",
            data_source_annotations=["data_source_annotations_value"],
            user_email="user_email_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gcd_question.Question.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_question(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_question.Question)
    assert response.name == "name_value"
    assert response.scopes == ["scopes_value"]
    assert response.query == "query_value"
    assert response.data_source_annotations == ["data_source_annotations_value"]
    assert response.user_email == "user_email_value"


def test_create_question_rest_required_fields(
    request_type=question_service.CreateQuestionRequest,
):
    transport_class = transports.QuestionServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_question._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_question._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gcd_question.Question()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = gcd_question.Question.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_question(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_question_rest_unset_required_fields():
    transport = transports.QuestionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_question._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "question",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_question_rest_interceptors(null_interceptor):
    transport = transports.QuestionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.QuestionServiceRestInterceptor(),
    )
    client = QuestionServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.QuestionServiceRestInterceptor, "post_create_question"
    ) as post, mock.patch.object(
        transports.QuestionServiceRestInterceptor, "pre_create_question"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = question_service.CreateQuestionRequest.pb(
            question_service.CreateQuestionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gcd_question.Question.to_json(
            gcd_question.Question()
        )

        request = question_service.CreateQuestionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gcd_question.Question()

        client.create_question(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_question_rest_bad_request(
    transport: str = "rest", request_type=question_service.CreateQuestionRequest
):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["question"] = {
        "name": "name_value",
        "scopes": ["scopes_value1", "scopes_value2"],
        "query": "query_value",
        "data_source_annotations": [
            "data_source_annotations_value1",
            "data_source_annotations_value2",
        ],
        "interpret_error": {
            "message": "message_value",
            "code": 1,
            "details": {
                "unsupported_details": {
                    "operators": ["operators_value1", "operators_value2"],
                    "intent": ["intent_value1", "intent_value2"],
                },
                "incomplete_query_details": {"entities": [1]},
                "ambiguity_details": {},
            },
        },
        "interpretations": [
            {
                "data_sources": ["data_sources_value1", "data_sources_value2"],
                "confidence": 0.1038,
                "unused_phrases": ["unused_phrases_value1", "unused_phrases_value2"],
                "human_readable": {
                    "generated_interpretation": {
                        "text_formatted": "text_formatted_value",
                        "html_formatted": "html_formatted_value",
                        "markups": [
                            {"type_": 1, "start_char_index": 1698, "length": 642}
                        ],
                    },
                    "original_question": {},
                },
                "interpretation_structure": {
                    "visualization_types": [1],
                    "column_info": [
                        {
                            "output_alias": "output_alias_value",
                            "display_name": "display_name_value",
                        }
                    ],
                },
                "data_query": {"sql": "sql_value"},
                "execution_info": {
                    "job_creation_status": {
                        "code": 411,
                        "message": "message_value",
                        "details": [
                            {
                                "type_url": "type.googleapis.com/google.protobuf.Duration",
                                "value": b"\x08\x0c\x10\xdb\x07",
                            }
                        ],
                    },
                    "job_execution_state": 1,
                    "create_time": {"seconds": 751, "nanos": 543},
                    "bigquery_job": {
                        "job_id": "job_id_value",
                        "project_id": "project_id_value",
                        "location": "location_value",
                    },
                },
            }
        ],
        "create_time": {},
        "user_email": "user_email_value",
        "debug_flags": {
            "include_va_query": True,
            "include_nested_va_query": True,
            "include_human_interpretation": True,
            "include_aqua_debug_response": True,
            "time_override": 1390,
            "is_internal_google_user": True,
            "ignore_cache": True,
            "include_search_entities_rpc": True,
            "include_list_column_annotations_rpc": True,
            "include_virtual_analyst_entities": True,
            "include_table_list": True,
            "include_domain_list": True,
        },
        "debug_info": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_question(request)


def test_create_question_rest_flattened():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcd_question.Question()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            question=gcd_question.Question(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gcd_question.Question.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_question(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{parent=projects/*/locations/*}/questions"
            % client.transport._host,
            args[1],
        )


def test_create_question_rest_flattened_error(transport: str = "rest"):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_question(
            question_service.CreateQuestionRequest(),
            parent="parent_value",
            question=gcd_question.Question(name="name_value"),
        )


def test_create_question_rest_error():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        question_service.ExecuteQuestionRequest,
        dict,
    ],
)
def test_execute_question_rest(request_type):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/questions/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = question.Question(
            name="name_value",
            scopes=["scopes_value"],
            query="query_value",
            data_source_annotations=["data_source_annotations_value"],
            user_email="user_email_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = question.Question.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.execute_question(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, question.Question)
    assert response.name == "name_value"
    assert response.scopes == ["scopes_value"]
    assert response.query == "query_value"
    assert response.data_source_annotations == ["data_source_annotations_value"]
    assert response.user_email == "user_email_value"


def test_execute_question_rest_required_fields(
    request_type=question_service.ExecuteQuestionRequest,
):
    transport_class = transports.QuestionServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["interpretation_index"] = 0
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).execute_question._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["interpretationIndex"] = 2159

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).execute_question._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "interpretationIndex" in jsonified_request
    assert jsonified_request["interpretationIndex"] == 2159

    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = question.Question()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = question.Question.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.execute_question(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_execute_question_rest_unset_required_fields():
    transport = transports.QuestionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.execute_question._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "interpretationIndex",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_execute_question_rest_interceptors(null_interceptor):
    transport = transports.QuestionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.QuestionServiceRestInterceptor(),
    )
    client = QuestionServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.QuestionServiceRestInterceptor, "post_execute_question"
    ) as post, mock.patch.object(
        transports.QuestionServiceRestInterceptor, "pre_execute_question"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = question_service.ExecuteQuestionRequest.pb(
            question_service.ExecuteQuestionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = question.Question.to_json(question.Question())

        request = question_service.ExecuteQuestionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = question.Question()

        client.execute_question(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_execute_question_rest_bad_request(
    transport: str = "rest", request_type=question_service.ExecuteQuestionRequest
):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/questions/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.execute_question(request)


def test_execute_question_rest_flattened():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = question.Question()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/questions/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            interpretation_index=2159,
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = question.Question.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.execute_question(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=projects/*/locations/*/questions/*}:execute"
            % client.transport._host,
            args[1],
        )


def test_execute_question_rest_flattened_error(transport: str = "rest"):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.execute_question(
            question_service.ExecuteQuestionRequest(),
            name="name_value",
            interpretation_index=2159,
        )


def test_execute_question_rest_error():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        question_service.GetUserFeedbackRequest,
        dict,
    ],
)
def test_get_user_feedback_rest(request_type):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/questions/sample3/userFeedback"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = user_feedback.UserFeedback(
            name="name_value",
            free_form_feedback="free_form_feedback_value",
            rating=user_feedback.UserFeedback.UserFeedbackRating.POSITIVE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = user_feedback.UserFeedback.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_user_feedback(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, user_feedback.UserFeedback)
    assert response.name == "name_value"
    assert response.free_form_feedback == "free_form_feedback_value"
    assert response.rating == user_feedback.UserFeedback.UserFeedbackRating.POSITIVE


def test_get_user_feedback_rest_required_fields(
    request_type=question_service.GetUserFeedbackRequest,
):
    transport_class = transports.QuestionServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_user_feedback._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_user_feedback._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = user_feedback.UserFeedback()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = user_feedback.UserFeedback.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_user_feedback(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_user_feedback_rest_unset_required_fields():
    transport = transports.QuestionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_user_feedback._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_user_feedback_rest_interceptors(null_interceptor):
    transport = transports.QuestionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.QuestionServiceRestInterceptor(),
    )
    client = QuestionServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.QuestionServiceRestInterceptor, "post_get_user_feedback"
    ) as post, mock.patch.object(
        transports.QuestionServiceRestInterceptor, "pre_get_user_feedback"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = question_service.GetUserFeedbackRequest.pb(
            question_service.GetUserFeedbackRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = user_feedback.UserFeedback.to_json(
            user_feedback.UserFeedback()
        )

        request = question_service.GetUserFeedbackRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = user_feedback.UserFeedback()

        client.get_user_feedback(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_user_feedback_rest_bad_request(
    transport: str = "rest", request_type=question_service.GetUserFeedbackRequest
):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/questions/sample3/userFeedback"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_user_feedback(request)


def test_get_user_feedback_rest_flattened():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = user_feedback.UserFeedback()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/questions/sample3/userFeedback"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = user_feedback.UserFeedback.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_user_feedback(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=projects/*/locations/*/questions/*/userFeedback}"
            % client.transport._host,
            args[1],
        )


def test_get_user_feedback_rest_flattened_error(transport: str = "rest"):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_user_feedback(
            question_service.GetUserFeedbackRequest(),
            name="name_value",
        )


def test_get_user_feedback_rest_error():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        question_service.UpdateUserFeedbackRequest,
        dict,
    ],
)
def test_update_user_feedback_rest(request_type):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "user_feedback": {
            "name": "projects/sample1/locations/sample2/questions/sample3/userFeedback"
        }
    }
    request_init["user_feedback"] = {
        "name": "projects/sample1/locations/sample2/questions/sample3/userFeedback",
        "free_form_feedback": "free_form_feedback_value",
        "rating": 1,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcd_user_feedback.UserFeedback(
            name="name_value",
            free_form_feedback="free_form_feedback_value",
            rating=gcd_user_feedback.UserFeedback.UserFeedbackRating.POSITIVE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gcd_user_feedback.UserFeedback.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_user_feedback(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_user_feedback.UserFeedback)
    assert response.name == "name_value"
    assert response.free_form_feedback == "free_form_feedback_value"
    assert response.rating == gcd_user_feedback.UserFeedback.UserFeedbackRating.POSITIVE


def test_update_user_feedback_rest_required_fields(
    request_type=question_service.UpdateUserFeedbackRequest,
):
    transport_class = transports.QuestionServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_user_feedback._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_user_feedback._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gcd_user_feedback.UserFeedback()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = gcd_user_feedback.UserFeedback.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_user_feedback(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_user_feedback_rest_unset_required_fields():
    transport = transports.QuestionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_user_feedback._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("userFeedback",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_user_feedback_rest_interceptors(null_interceptor):
    transport = transports.QuestionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.QuestionServiceRestInterceptor(),
    )
    client = QuestionServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.QuestionServiceRestInterceptor, "post_update_user_feedback"
    ) as post, mock.patch.object(
        transports.QuestionServiceRestInterceptor, "pre_update_user_feedback"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = question_service.UpdateUserFeedbackRequest.pb(
            question_service.UpdateUserFeedbackRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gcd_user_feedback.UserFeedback.to_json(
            gcd_user_feedback.UserFeedback()
        )

        request = question_service.UpdateUserFeedbackRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gcd_user_feedback.UserFeedback()

        client.update_user_feedback(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_user_feedback_rest_bad_request(
    transport: str = "rest", request_type=question_service.UpdateUserFeedbackRequest
):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "user_feedback": {
            "name": "projects/sample1/locations/sample2/questions/sample3/userFeedback"
        }
    }
    request_init["user_feedback"] = {
        "name": "projects/sample1/locations/sample2/questions/sample3/userFeedback",
        "free_form_feedback": "free_form_feedback_value",
        "rating": 1,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_user_feedback(request)


def test_update_user_feedback_rest_flattened():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcd_user_feedback.UserFeedback()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "user_feedback": {
                "name": "projects/sample1/locations/sample2/questions/sample3/userFeedback"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            user_feedback=gcd_user_feedback.UserFeedback(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gcd_user_feedback.UserFeedback.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_user_feedback(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{user_feedback.name=projects/*/locations/*/questions/*/userFeedback}"
            % client.transport._host,
            args[1],
        )


def test_update_user_feedback_rest_flattened_error(transport: str = "rest"):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_user_feedback(
            question_service.UpdateUserFeedbackRequest(),
            user_feedback=gcd_user_feedback.UserFeedback(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_user_feedback_rest_error():
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.QuestionServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = QuestionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.QuestionServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = QuestionServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.QuestionServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = QuestionServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = QuestionServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.QuestionServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = QuestionServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.QuestionServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = QuestionServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.QuestionServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.QuestionServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.QuestionServiceGrpcTransport,
        transports.QuestionServiceGrpcAsyncIOTransport,
        transports.QuestionServiceRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = QuestionServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.QuestionServiceGrpcTransport,
    )


def test_question_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.QuestionServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_question_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dataqna_v1alpha.services.question_service.transports.QuestionServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.QuestionServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_question",
        "create_question",
        "execute_question",
        "get_user_feedback",
        "update_user_feedback",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_question_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dataqna_v1alpha.services.question_service.transports.QuestionServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.QuestionServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_question_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dataqna_v1alpha.services.question_service.transports.QuestionServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.QuestionServiceTransport()
        adc.assert_called_once()


def test_question_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        QuestionServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.QuestionServiceGrpcTransport,
        transports.QuestionServiceGrpcAsyncIOTransport,
    ],
)
def test_question_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.QuestionServiceGrpcTransport,
        transports.QuestionServiceGrpcAsyncIOTransport,
        transports.QuestionServiceRestTransport,
    ],
)
def test_question_service_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.QuestionServiceGrpcTransport, grpc_helpers),
        (transports.QuestionServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_question_service_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "dataqna.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="dataqna.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.QuestionServiceGrpcTransport,
        transports.QuestionServiceGrpcAsyncIOTransport,
    ],
)
def test_question_service_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_question_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.QuestionServiceRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_question_service_host_no_port(transport_name):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataqna.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "dataqna.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://dataqna.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_question_service_host_with_port(transport_name):
    client = QuestionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataqna.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "dataqna.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://dataqna.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_question_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = QuestionServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = QuestionServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.get_question._session
    session2 = client2.transport.get_question._session
    assert session1 != session2
    session1 = client1.transport.create_question._session
    session2 = client2.transport.create_question._session
    assert session1 != session2
    session1 = client1.transport.execute_question._session
    session2 = client2.transport.execute_question._session
    assert session1 != session2
    session1 = client1.transport.get_user_feedback._session
    session2 = client2.transport.get_user_feedback._session
    assert session1 != session2
    session1 = client1.transport.update_user_feedback._session
    session2 = client2.transport.update_user_feedback._session
    assert session1 != session2


def test_question_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.QuestionServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_question_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.QuestionServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.QuestionServiceGrpcTransport,
        transports.QuestionServiceGrpcAsyncIOTransport,
    ],
)
def test_question_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.QuestionServiceGrpcTransport,
        transports.QuestionServiceGrpcAsyncIOTransport,
    ],
)
def test_question_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_question_path():
    project = "squid"
    location = "clam"
    question = "whelk"
    expected = "projects/{project}/locations/{location}/questions/{question}".format(
        project=project,
        location=location,
        question=question,
    )
    actual = QuestionServiceClient.question_path(project, location, question)
    assert expected == actual


def test_parse_question_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "question": "nudibranch",
    }
    path = QuestionServiceClient.question_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_question_path(path)
    assert expected == actual


def test_user_feedback_path():
    project = "cuttlefish"
    location = "mussel"
    question = "winkle"
    expected = "projects/{project}/locations/{location}/questions/{question}/userFeedback".format(
        project=project,
        location=location,
        question=question,
    )
    actual = QuestionServiceClient.user_feedback_path(project, location, question)
    assert expected == actual


def test_parse_user_feedback_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "question": "abalone",
    }
    path = QuestionServiceClient.user_feedback_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_user_feedback_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = QuestionServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = QuestionServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = QuestionServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = QuestionServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = QuestionServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = QuestionServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = QuestionServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = QuestionServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = QuestionServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = QuestionServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = QuestionServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.QuestionServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = QuestionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.QuestionServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = QuestionServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = QuestionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = QuestionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = QuestionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (QuestionServiceClient, transports.QuestionServiceGrpcTransport),
        (QuestionServiceAsyncClient, transports.QuestionServiceGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
