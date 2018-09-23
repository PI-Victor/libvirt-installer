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

