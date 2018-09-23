# Copyright (C) 2018 Victor Palade <victor@cloudflavor.io>.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC


class BaseResource(ABC):
    pass


class Network(BaseResource):
    """Network represents a libvirt network resource
    """
    
    dhcp_reserverd = {}
    network_type = ""
    cidr_block = ""
    bridge_source = ""
    
    def init(self, mac_address_map, network_type, cidr_block, bridge_source):
        self.dhcp_reserved = mac_address_map
        self.network_type = network_type


class StoragePool(BaseResource):
    """StoragePool represents a libvirt storage pool
    """

    pool_type = ""
    pool_directory_path = ""

    def init(self, pool_type, pool_directory_path):
        pass


class Node():
    """Node represents a KVM/Qemu node
    """

    def init(self):
        pass

