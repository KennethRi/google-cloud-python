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
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
)

from google.cloud.beyondcorp_appconnections_v1.types import app_connections_service


class ListAppConnectionsPager:
    """A pager for iterating through ``list_app_connections`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.beyondcorp_appconnections_v1.types.ListAppConnectionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``app_connections`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListAppConnections`` requests and continue to iterate
    through the ``app_connections`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.beyondcorp_appconnections_v1.types.ListAppConnectionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., app_connections_service.ListAppConnectionsResponse],
        request: app_connections_service.ListAppConnectionsRequest,
        response: app_connections_service.ListAppConnectionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.beyondcorp_appconnections_v1.types.ListAppConnectionsRequest):
                The initial request object.
            response (google.cloud.beyondcorp_appconnections_v1.types.ListAppConnectionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = app_connections_service.ListAppConnectionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[app_connections_service.ListAppConnectionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[app_connections_service.AppConnection]:
        for page in self.pages:
            yield from page.app_connections

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListAppConnectionsAsyncPager:
    """A pager for iterating through ``list_app_connections`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.beyondcorp_appconnections_v1.types.ListAppConnectionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``app_connections`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListAppConnections`` requests and continue to iterate
    through the ``app_connections`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.beyondcorp_appconnections_v1.types.ListAppConnectionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[app_connections_service.ListAppConnectionsResponse]
        ],
        request: app_connections_service.ListAppConnectionsRequest,
        response: app_connections_service.ListAppConnectionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.beyondcorp_appconnections_v1.types.ListAppConnectionsRequest):
                The initial request object.
            response (google.cloud.beyondcorp_appconnections_v1.types.ListAppConnectionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = app_connections_service.ListAppConnectionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[app_connections_service.ListAppConnectionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[app_connections_service.AppConnection]:
        async def async_generator():
            async for page in self.pages:
                for response in page.app_connections:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ResolveAppConnectionsPager:
    """A pager for iterating through ``resolve_app_connections`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.beyondcorp_appconnections_v1.types.ResolveAppConnectionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``app_connection_details`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ResolveAppConnections`` requests and continue to iterate
    through the ``app_connection_details`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.beyondcorp_appconnections_v1.types.ResolveAppConnectionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., app_connections_service.ResolveAppConnectionsResponse],
        request: app_connections_service.ResolveAppConnectionsRequest,
        response: app_connections_service.ResolveAppConnectionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.beyondcorp_appconnections_v1.types.ResolveAppConnectionsRequest):
                The initial request object.
            response (google.cloud.beyondcorp_appconnections_v1.types.ResolveAppConnectionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = app_connections_service.ResolveAppConnectionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[app_connections_service.ResolveAppConnectionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(
        self,
    ) -> Iterator[
        app_connections_service.ResolveAppConnectionsResponse.AppConnectionDetails
    ]:
        for page in self.pages:
            yield from page.app_connection_details

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ResolveAppConnectionsAsyncPager:
    """A pager for iterating through ``resolve_app_connections`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.beyondcorp_appconnections_v1.types.ResolveAppConnectionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``app_connection_details`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ResolveAppConnections`` requests and continue to iterate
    through the ``app_connection_details`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.beyondcorp_appconnections_v1.types.ResolveAppConnectionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[app_connections_service.ResolveAppConnectionsResponse]
        ],
        request: app_connections_service.ResolveAppConnectionsRequest,
        response: app_connections_service.ResolveAppConnectionsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.beyondcorp_appconnections_v1.types.ResolveAppConnectionsRequest):
                The initial request object.
            response (google.cloud.beyondcorp_appconnections_v1.types.ResolveAppConnectionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = app_connections_service.ResolveAppConnectionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterator[app_connections_service.ResolveAppConnectionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(
        self,
    ) -> AsyncIterator[
        app_connections_service.ResolveAppConnectionsResponse.AppConnectionDetails
    ]:
        async def async_generator():
            async for page in self.pages:
                for response in page.app_connection_details:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
