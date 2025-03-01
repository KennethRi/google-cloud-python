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
from google.cloud.gke_multicloud import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.gke_multicloud_v1.services.attached_clusters.async_client import (
    AttachedClustersAsyncClient,
)
from google.cloud.gke_multicloud_v1.services.attached_clusters.client import (
    AttachedClustersClient,
)
from google.cloud.gke_multicloud_v1.services.aws_clusters.async_client import (
    AwsClustersAsyncClient,
)
from google.cloud.gke_multicloud_v1.services.aws_clusters.client import (
    AwsClustersClient,
)
from google.cloud.gke_multicloud_v1.services.azure_clusters.async_client import (
    AzureClustersAsyncClient,
)
from google.cloud.gke_multicloud_v1.services.azure_clusters.client import (
    AzureClustersClient,
)
from google.cloud.gke_multicloud_v1.types.attached_resources import (
    AttachedCluster,
    AttachedClusterError,
    AttachedClustersAuthorization,
    AttachedClusterUser,
    AttachedOidcConfig,
    AttachedPlatformVersionInfo,
    AttachedServerConfig,
)
from google.cloud.gke_multicloud_v1.types.attached_service import (
    CreateAttachedClusterRequest,
    DeleteAttachedClusterRequest,
    GenerateAttachedClusterInstallManifestRequest,
    GenerateAttachedClusterInstallManifestResponse,
    GetAttachedClusterRequest,
    GetAttachedServerConfigRequest,
    ImportAttachedClusterRequest,
    ListAttachedClustersRequest,
    ListAttachedClustersResponse,
    UpdateAttachedClusterRequest,
)
from google.cloud.gke_multicloud_v1.types.aws_resources import (
    AwsAuthorization,
    AwsAutoscalingGroupMetricsCollection,
    AwsCluster,
    AwsClusterError,
    AwsClusterNetworking,
    AwsClusterUser,
    AwsConfigEncryption,
    AwsControlPlane,
    AwsDatabaseEncryption,
    AwsInstancePlacement,
    AwsK8sVersionInfo,
    AwsNodeConfig,
    AwsNodePool,
    AwsNodePoolAutoscaling,
    AwsNodePoolError,
    AwsProxyConfig,
    AwsServerConfig,
    AwsServicesAuthentication,
    AwsSshConfig,
    AwsVolumeTemplate,
)
from google.cloud.gke_multicloud_v1.types.aws_service import (
    CreateAwsClusterRequest,
    CreateAwsNodePoolRequest,
    DeleteAwsClusterRequest,
    DeleteAwsNodePoolRequest,
    GenerateAwsAccessTokenRequest,
    GenerateAwsAccessTokenResponse,
    GetAwsClusterRequest,
    GetAwsNodePoolRequest,
    GetAwsServerConfigRequest,
    ListAwsClustersRequest,
    ListAwsClustersResponse,
    ListAwsNodePoolsRequest,
    ListAwsNodePoolsResponse,
    UpdateAwsClusterRequest,
    UpdateAwsNodePoolRequest,
)
from google.cloud.gke_multicloud_v1.types.azure_resources import (
    AzureAuthorization,
    AzureClient,
    AzureCluster,
    AzureClusterError,
    AzureClusterNetworking,
    AzureClusterResources,
    AzureClusterUser,
    AzureConfigEncryption,
    AzureControlPlane,
    AzureDatabaseEncryption,
    AzureDiskTemplate,
    AzureK8sVersionInfo,
    AzureNodeConfig,
    AzureNodePool,
    AzureNodePoolAutoscaling,
    AzureNodePoolError,
    AzureProxyConfig,
    AzureServerConfig,
    AzureServicesAuthentication,
    AzureSshConfig,
    ReplicaPlacement,
)
from google.cloud.gke_multicloud_v1.types.azure_service import (
    CreateAzureClientRequest,
    CreateAzureClusterRequest,
    CreateAzureNodePoolRequest,
    DeleteAzureClientRequest,
    DeleteAzureClusterRequest,
    DeleteAzureNodePoolRequest,
    GenerateAzureAccessTokenRequest,
    GenerateAzureAccessTokenResponse,
    GetAzureClientRequest,
    GetAzureClusterRequest,
    GetAzureNodePoolRequest,
    GetAzureServerConfigRequest,
    ListAzureClientsRequest,
    ListAzureClientsResponse,
    ListAzureClustersRequest,
    ListAzureClustersResponse,
    ListAzureNodePoolsRequest,
    ListAzureNodePoolsResponse,
    UpdateAzureClusterRequest,
    UpdateAzureNodePoolRequest,
)
from google.cloud.gke_multicloud_v1.types.common_resources import (
    Fleet,
    LoggingComponentConfig,
    LoggingConfig,
    ManagedPrometheusConfig,
    MaxPodsConstraint,
    MonitoringConfig,
    NodeTaint,
    OperationMetadata,
    WorkloadIdentityConfig,
)

__all__ = (
    "AttachedClustersClient",
    "AttachedClustersAsyncClient",
    "AwsClustersClient",
    "AwsClustersAsyncClient",
    "AzureClustersClient",
    "AzureClustersAsyncClient",
    "AttachedCluster",
    "AttachedClusterError",
    "AttachedClustersAuthorization",
    "AttachedClusterUser",
    "AttachedOidcConfig",
    "AttachedPlatformVersionInfo",
    "AttachedServerConfig",
    "CreateAttachedClusterRequest",
    "DeleteAttachedClusterRequest",
    "GenerateAttachedClusterInstallManifestRequest",
    "GenerateAttachedClusterInstallManifestResponse",
    "GetAttachedClusterRequest",
    "GetAttachedServerConfigRequest",
    "ImportAttachedClusterRequest",
    "ListAttachedClustersRequest",
    "ListAttachedClustersResponse",
    "UpdateAttachedClusterRequest",
    "AwsAuthorization",
    "AwsAutoscalingGroupMetricsCollection",
    "AwsCluster",
    "AwsClusterError",
    "AwsClusterNetworking",
    "AwsClusterUser",
    "AwsConfigEncryption",
    "AwsControlPlane",
    "AwsDatabaseEncryption",
    "AwsInstancePlacement",
    "AwsK8sVersionInfo",
    "AwsNodeConfig",
    "AwsNodePool",
    "AwsNodePoolAutoscaling",
    "AwsNodePoolError",
    "AwsProxyConfig",
    "AwsServerConfig",
    "AwsServicesAuthentication",
    "AwsSshConfig",
    "AwsVolumeTemplate",
    "CreateAwsClusterRequest",
    "CreateAwsNodePoolRequest",
    "DeleteAwsClusterRequest",
    "DeleteAwsNodePoolRequest",
    "GenerateAwsAccessTokenRequest",
    "GenerateAwsAccessTokenResponse",
    "GetAwsClusterRequest",
    "GetAwsNodePoolRequest",
    "GetAwsServerConfigRequest",
    "ListAwsClustersRequest",
    "ListAwsClustersResponse",
    "ListAwsNodePoolsRequest",
    "ListAwsNodePoolsResponse",
    "UpdateAwsClusterRequest",
    "UpdateAwsNodePoolRequest",
    "AzureAuthorization",
    "AzureClient",
    "AzureCluster",
    "AzureClusterError",
    "AzureClusterNetworking",
    "AzureClusterResources",
    "AzureClusterUser",
    "AzureConfigEncryption",
    "AzureControlPlane",
    "AzureDatabaseEncryption",
    "AzureDiskTemplate",
    "AzureK8sVersionInfo",
    "AzureNodeConfig",
    "AzureNodePool",
    "AzureNodePoolAutoscaling",
    "AzureNodePoolError",
    "AzureProxyConfig",
    "AzureServerConfig",
    "AzureServicesAuthentication",
    "AzureSshConfig",
    "ReplicaPlacement",
    "CreateAzureClientRequest",
    "CreateAzureClusterRequest",
    "CreateAzureNodePoolRequest",
    "DeleteAzureClientRequest",
    "DeleteAzureClusterRequest",
    "DeleteAzureNodePoolRequest",
    "GenerateAzureAccessTokenRequest",
    "GenerateAzureAccessTokenResponse",
    "GetAzureClientRequest",
    "GetAzureClusterRequest",
    "GetAzureNodePoolRequest",
    "GetAzureServerConfigRequest",
    "ListAzureClientsRequest",
    "ListAzureClientsResponse",
    "ListAzureClustersRequest",
    "ListAzureClustersResponse",
    "ListAzureNodePoolsRequest",
    "ListAzureNodePoolsResponse",
    "UpdateAzureClusterRequest",
    "UpdateAzureNodePoolRequest",
    "Fleet",
    "LoggingComponentConfig",
    "LoggingConfig",
    "ManagedPrometheusConfig",
    "MaxPodsConstraint",
    "MonitoringConfig",
    "NodeTaint",
    "OperationMetadata",
    "WorkloadIdentityConfig",
)
