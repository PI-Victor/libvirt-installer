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

import libvirt

from .log import log
from .utils import load_config, tabulate_data



def connection_wrapper(func):
    """Validates the connection to libvirt before allowing any actions against
    it.

    param func: Any function that needs to perform actions against libvirt
    resources.
    """
    def _wrap_connection(*args, **kwargs):
        conn = libvirt.open(kwargs.get('hypervisor_uri'))
        if conn == None:
            raise Error
        else:
            func(*args, **kwargs, conn=conn)

    return _wrap_connection

@connection_wrapper
def create_domains(config_file=None, hypervisor_uri='', conn=None):
    """Create new domains based on the passed configuration file.

    :param config_file: TOML format configuration file that describes the 
    domains.
    """
    config = load_config(config_file)
    log.debug('Loaded config: {}'.format(config))

@connection_wrapper
def delete_domains(domain_uuids, hypervisor_uri='', conn=None):
    """Deletes one or more domain 

    :param domains: A list of domain UUIDs to delete.
    """
    validate_domains(domain_uuids, conn=conn)
    
@connection_wrapper
def list_domains(active=True, describe=False, hypervisor_uri='', conn=None):
    """List all available domains

    :param active: A filter for inactive domains.
    :param describe: A filter to describe domains.
    """
    # NOTE: implement describe
    
    _state_map = {
        libvirt.VIR_DOMAIN_RUNNING  : "running",
        libvirt.VIR_DOMAIN_BLOCKED  : "idle",
        libvirt.VIR_DOMAIN_PAUSED   : "paused",
        libvirt.VIR_DOMAIN_SHUTDOWN : "in shutdown",
        libvirt.VIR_DOMAIN_SHUTOFF  : "shut off",
        libvirt.VIR_DOMAIN_CRASHED  : "crashed",
        libvirt.VIR_DOMAIN_NOSTATE  : "no state",
    }

    _table_headers = [
        'Name',
        'ID',
        'State',
        'UUID',
    ]

    domains = list([
        d.name(),
        d.ID(),
        ', '.join(set(map(lambda s: _state_map[s], d.state()))), d.UUIDString()]
    for d in conn.listAllDomains(libvirt.VIR_DOMAIN_RUNNING if active else 0))
        
    tabulate_data(domains, _table_headers)

@connection_wrapper
def halt_domains(domain_uuids, hypervisor_uri='', restart=False, conn=None):
    """Shuts down or restarts one or more domains.
    
    :param domain_uuids: A list of domain UUIDs to shutdown/restart.
    :param restart: If set to true will restart the specified domains instead
    of shutting them down.
    """
    domains = validate_domains(
        domains=domain_uuids,
        state=libvirt.VIR_CONNECT_LIST_DOMAINS_RUNNING,
        conn=conn,
    )
    
    if not domains:
        log.error("No matching domains in running state found!")
        
    if restart:
        for domain in domains:
            log.info('Rebooting domain {}...'.format(domain.name()))
            domain.reboot()
        return

    for domain in domains:
        log.info('Shutting down domain {}...'.format(domain.name()))
        domain.shutdown()

@connection_wrapper
def start_domains(domain_uuids, hypervisor_uri='', conn=None):
    """Starts one or more domains.
    
    :param domain_uuids: A list of domain UUIDs to start.
    """
    domains = validate_domains(
        domains=domain_uuids,
        state=libvirt.VIR_CONNECT_LIST_DOMAINS_SHUTOFF,
        conn=conn,
    )

    if not domains:
        log.error("No matching domains in shutoff state found!")
        
    for domain in domains:
        log.info('Starting domain {}...'.format(domain.name()))
        domain.create()

def validate_domains(domains, state=0, conn=None):
    """Filters out domains based on the required state.

    :param domains: a list of UUIDs for the domains that the user wants to 
    operate on.
    :param state: A machine state filter.
    """
    doms = conn.listAllDomains(state)
    
    return [d for d in doms if d.UUIDString() in list(domains)]
