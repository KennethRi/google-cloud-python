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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.securitycenter.v1",
    manifest={
        "MitreAttack",
    },
)


class MitreAttack(proto.Message):
    r"""MITRE ATT&CK tactics and techniques related to this finding.
    See: https://attack.mitre.org

    Attributes:
        primary_tactic (google.cloud.securitycenter_v1.types.MitreAttack.Tactic):
            The MITRE ATT&CK tactic most closely
            represented by this finding, if any.
        primary_techniques (MutableSequence[google.cloud.securitycenter_v1.types.MitreAttack.Technique]):
            The MITRE ATT&CK technique most closely represented by this
            finding, if any. primary_techniques is a repeated field
            because there are multiple levels of MITRE ATT&CK
            techniques. If the technique most closely represented by
            this finding is a sub-technique (e.g.
            ``SCANNING_IP_BLOCKS``), both the sub-technique and its
            parent technique(s) will be listed (e.g.
            ``SCANNING_IP_BLOCKS``, ``ACTIVE_SCANNING``).
        additional_tactics (MutableSequence[google.cloud.securitycenter_v1.types.MitreAttack.Tactic]):
            Additional MITRE ATT&CK tactics related to
            this finding, if any.
        additional_techniques (MutableSequence[google.cloud.securitycenter_v1.types.MitreAttack.Technique]):
            Additional MITRE ATT&CK techniques related to
            this finding, if any, along with any of their
            respective parent techniques.
        version (str):
            The MITRE ATT&CK version referenced by the
            above fields. E.g. "8".
    """

    class Tactic(proto.Enum):
        r"""MITRE ATT&CK tactics that can be referenced by SCC findings.
        See: https://attack.mitre.org/tactics/enterprise/

        Values:
            TACTIC_UNSPECIFIED (0):
                Unspecified value.
            RECONNAISSANCE (1):
                TA0043
            RESOURCE_DEVELOPMENT (2):
                TA0042
            INITIAL_ACCESS (5):
                TA0001
            EXECUTION (3):
                TA0002
            PERSISTENCE (6):
                TA0003
            PRIVILEGE_ESCALATION (8):
                TA0004
            DEFENSE_EVASION (7):
                TA0005
            CREDENTIAL_ACCESS (9):
                TA0006
            DISCOVERY (10):
                TA0007
            LATERAL_MOVEMENT (11):
                TA0008
            COLLECTION (12):
                TA0009
            COMMAND_AND_CONTROL (4):
                TA0011
            EXFILTRATION (13):
                TA0010
            IMPACT (14):
                TA0040
        """
        TACTIC_UNSPECIFIED = 0
        RECONNAISSANCE = 1
        RESOURCE_DEVELOPMENT = 2
        INITIAL_ACCESS = 5
        EXECUTION = 3
        PERSISTENCE = 6
        PRIVILEGE_ESCALATION = 8
        DEFENSE_EVASION = 7
        CREDENTIAL_ACCESS = 9
        DISCOVERY = 10
        LATERAL_MOVEMENT = 11
        COLLECTION = 12
        COMMAND_AND_CONTROL = 4
        EXFILTRATION = 13
        IMPACT = 14

    class Technique(proto.Enum):
        r"""MITRE ATT&CK techniques that can be referenced by SCC
        findings. See: https://attack.mitre.org/techniques/enterprise/

        Values:
            TECHNIQUE_UNSPECIFIED (0):
                Unspecified value.
            ACTIVE_SCANNING (1):
                T1595
            SCANNING_IP_BLOCKS (2):
                T1595.001
            INGRESS_TOOL_TRANSFER (3):
                T1105
            NATIVE_API (4):
                T1106
            SHARED_MODULES (5):
                T1129
            COMMAND_AND_SCRIPTING_INTERPRETER (6):
                T1059
            UNIX_SHELL (7):
                T1059.004
            RESOURCE_HIJACKING (8):
                T1496
            PROXY (9):
                T1090
            EXTERNAL_PROXY (10):
                T1090.002
            MULTI_HOP_PROXY (11):
                T1090.003
            DYNAMIC_RESOLUTION (12):
                T1568
            UNSECURED_CREDENTIALS (13):
                T1552
            VALID_ACCOUNTS (14):
                T1078
            LOCAL_ACCOUNTS (15):
                T1078.003
            CLOUD_ACCOUNTS (16):
                T1078.004
            NETWORK_DENIAL_OF_SERVICE (17):
                T1498
            PERMISSION_GROUPS_DISCOVERY (18):
                T1069
            CLOUD_GROUPS (19):
                T1069.003
            EXFILTRATION_OVER_WEB_SERVICE (20):
                T1567
            EXFILTRATION_TO_CLOUD_STORAGE (21):
                T1567.002
            ACCOUNT_MANIPULATION (22):
                T1098
            SSH_AUTHORIZED_KEYS (23):
                T1098.004
            CREATE_OR_MODIFY_SYSTEM_PROCESS (24):
                T1543
            STEAL_WEB_SESSION_COOKIE (25):
                T1539
            MODIFY_CLOUD_COMPUTE_INFRASTRUCTURE (26):
                T1578
            EXPLOIT_PUBLIC_FACING_APPLICATION (27):
                T1190
            MODIFY_AUTHENTICATION_PROCESS (28):
                T1556
            DATA_DESTRUCTION (29):
                T1485
            DOMAIN_POLICY_MODIFICATION (30):
                T1484
            IMPAIR_DEFENSES (31):
                T1562
            NETWORK_SERVICE_DISCOVERY (32):
                T1046
            ACCESS_TOKEN_MANIPULATION (33):
                T1134
            ABUSE_ELEVATION_CONTROL_MECHANISM (34):
                T1548
            DEFAULT_ACCOUNTS (35):
                T1078.001
        """
        TECHNIQUE_UNSPECIFIED = 0
        ACTIVE_SCANNING = 1
        SCANNING_IP_BLOCKS = 2
        INGRESS_TOOL_TRANSFER = 3
        NATIVE_API = 4
        SHARED_MODULES = 5
        COMMAND_AND_SCRIPTING_INTERPRETER = 6
        UNIX_SHELL = 7
        RESOURCE_HIJACKING = 8
        PROXY = 9
        EXTERNAL_PROXY = 10
        MULTI_HOP_PROXY = 11
        DYNAMIC_RESOLUTION = 12
        UNSECURED_CREDENTIALS = 13
        VALID_ACCOUNTS = 14
        LOCAL_ACCOUNTS = 15
        CLOUD_ACCOUNTS = 16
        NETWORK_DENIAL_OF_SERVICE = 17
        PERMISSION_GROUPS_DISCOVERY = 18
        CLOUD_GROUPS = 19
        EXFILTRATION_OVER_WEB_SERVICE = 20
        EXFILTRATION_TO_CLOUD_STORAGE = 21
        ACCOUNT_MANIPULATION = 22
        SSH_AUTHORIZED_KEYS = 23
        CREATE_OR_MODIFY_SYSTEM_PROCESS = 24
        STEAL_WEB_SESSION_COOKIE = 25
        MODIFY_CLOUD_COMPUTE_INFRASTRUCTURE = 26
        EXPLOIT_PUBLIC_FACING_APPLICATION = 27
        MODIFY_AUTHENTICATION_PROCESS = 28
        DATA_DESTRUCTION = 29
        DOMAIN_POLICY_MODIFICATION = 30
        IMPAIR_DEFENSES = 31
        NETWORK_SERVICE_DISCOVERY = 32
        ACCESS_TOKEN_MANIPULATION = 33
        ABUSE_ELEVATION_CONTROL_MECHANISM = 34
        DEFAULT_ACCOUNTS = 35

    primary_tactic: Tactic = proto.Field(
        proto.ENUM,
        number=1,
        enum=Tactic,
    )
    primary_techniques: MutableSequence[Technique] = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum=Technique,
    )
    additional_tactics: MutableSequence[Tactic] = proto.RepeatedField(
        proto.ENUM,
        number=3,
        enum=Tactic,
    )
    additional_techniques: MutableSequence[Technique] = proto.RepeatedField(
        proto.ENUM,
        number=4,
        enum=Technique,
    )
    version: str = proto.Field(
        proto.STRING,
        number=5,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
