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
from google.cloud.vmwareengine import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.vmwareengine_v1.services.vmware_engine.async_client import (
    VmwareEngineAsyncClient,
)
from google.cloud.vmwareengine_v1.services.vmware_engine.client import (
    VmwareEngineClient,
)
from google.cloud.vmwareengine_v1.types.vmwareengine import (
    CreateClusterRequest,
    CreateHcxActivationKeyRequest,
    CreateNetworkPolicyRequest,
    CreatePrivateCloudRequest,
    CreatePrivateConnectionRequest,
    CreateVmwareEngineNetworkRequest,
    DeleteClusterRequest,
    DeleteNetworkPolicyRequest,
    DeletePrivateCloudRequest,
    DeletePrivateConnectionRequest,
    DeleteVmwareEngineNetworkRequest,
    GetClusterRequest,
    GetHcxActivationKeyRequest,
    GetNetworkPolicyRequest,
    GetNodeTypeRequest,
    GetPrivateCloudRequest,
    GetPrivateConnectionRequest,
    GetSubnetRequest,
    GetVmwareEngineNetworkRequest,
    ListClustersRequest,
    ListClustersResponse,
    ListHcxActivationKeysRequest,
    ListHcxActivationKeysResponse,
    ListNetworkPoliciesRequest,
    ListNetworkPoliciesResponse,
    ListNodeTypesRequest,
    ListNodeTypesResponse,
    ListPrivateCloudsRequest,
    ListPrivateCloudsResponse,
    ListPrivateConnectionPeeringRoutesRequest,
    ListPrivateConnectionPeeringRoutesResponse,
    ListPrivateConnectionsRequest,
    ListPrivateConnectionsResponse,
    ListSubnetsRequest,
    ListSubnetsResponse,
    ListVmwareEngineNetworksRequest,
    ListVmwareEngineNetworksResponse,
    OperationMetadata,
    ResetNsxCredentialsRequest,
    ResetVcenterCredentialsRequest,
    ShowNsxCredentialsRequest,
    ShowVcenterCredentialsRequest,
    UndeletePrivateCloudRequest,
    UpdateClusterRequest,
    UpdateNetworkPolicyRequest,
    UpdatePrivateCloudRequest,
    UpdatePrivateConnectionRequest,
    UpdateSubnetRequest,
    UpdateVmwareEngineNetworkRequest,
)
from google.cloud.vmwareengine_v1.types.vmwareengine_resources import (
    Cluster,
    Credentials,
    Hcx,
    HcxActivationKey,
    NetworkConfig,
    NetworkPolicy,
    NodeType,
    NodeTypeConfig,
    Nsx,
    PeeringRoute,
    PrivateCloud,
    PrivateConnection,
    Subnet,
    Vcenter,
    VmwareEngineNetwork,
)

__all__ = (
    "VmwareEngineClient",
    "VmwareEngineAsyncClient",
    "CreateClusterRequest",
    "CreateHcxActivationKeyRequest",
    "CreateNetworkPolicyRequest",
    "CreatePrivateCloudRequest",
    "CreatePrivateConnectionRequest",
    "CreateVmwareEngineNetworkRequest",
    "DeleteClusterRequest",
    "DeleteNetworkPolicyRequest",
    "DeletePrivateCloudRequest",
    "DeletePrivateConnectionRequest",
    "DeleteVmwareEngineNetworkRequest",
    "GetClusterRequest",
    "GetHcxActivationKeyRequest",
    "GetNetworkPolicyRequest",
    "GetNodeTypeRequest",
    "GetPrivateCloudRequest",
    "GetPrivateConnectionRequest",
    "GetSubnetRequest",
    "GetVmwareEngineNetworkRequest",
    "ListClustersRequest",
    "ListClustersResponse",
    "ListHcxActivationKeysRequest",
    "ListHcxActivationKeysResponse",
    "ListNetworkPoliciesRequest",
    "ListNetworkPoliciesResponse",
    "ListNodeTypesRequest",
    "ListNodeTypesResponse",
    "ListPrivateCloudsRequest",
    "ListPrivateCloudsResponse",
    "ListPrivateConnectionPeeringRoutesRequest",
    "ListPrivateConnectionPeeringRoutesResponse",
    "ListPrivateConnectionsRequest",
    "ListPrivateConnectionsResponse",
    "ListSubnetsRequest",
    "ListSubnetsResponse",
    "ListVmwareEngineNetworksRequest",
    "ListVmwareEngineNetworksResponse",
    "OperationMetadata",
    "ResetNsxCredentialsRequest",
    "ResetVcenterCredentialsRequest",
    "ShowNsxCredentialsRequest",
    "ShowVcenterCredentialsRequest",
    "UndeletePrivateCloudRequest",
    "UpdateClusterRequest",
    "UpdateNetworkPolicyRequest",
    "UpdatePrivateCloudRequest",
    "UpdatePrivateConnectionRequest",
    "UpdateSubnetRequest",
    "UpdateVmwareEngineNetworkRequest",
    "Cluster",
    "Credentials",
    "Hcx",
    "HcxActivationKey",
    "NetworkConfig",
    "NetworkPolicy",
    "NodeType",
    "NodeTypeConfig",
    "Nsx",
    "PeeringRoute",
    "PrivateCloud",
    "PrivateConnection",
    "Subnet",
    "Vcenter",
    "VmwareEngineNetwork",
)
