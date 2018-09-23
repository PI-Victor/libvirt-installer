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

import toml
import libvirt
import sys

from libvirt import (
    VIR_CONNECT_LIST_DOMAINS_ACTIVE,
)

from .log import log
from .utils import Error


def connection_wrapper(func):
    """Wraps a function, representing an action, with the libvirt connection 
    handler.

    param func: Any function that needs to perform actions against libvirt
    """
    def _wrap_connection(*args, **kwargs):
        conn = libvirt.open(kwargs.get('hypervisor_uri'))
        if conn == None:
            raise Error
        else:
            func(conn, *args, **kwargs)
    
    return _wrap_connection

@connection_wrapper
def create_domains(conn=None, config_file=None, hypervisor_uri=''):
    """Create new domains based on the passed configuration file.

    :param config_file: TOML format configuration file that describes the 
    domains.
    """
    config = load_config(config_file)
    log.debug('Loaded config: {}'.format(config))

@connection_wrapper
def delete_domains(conn=None, *domain_ids, hypervisor_uri=''):
    """Deletes one or more domain 

    :param domains: A comma separated list of domain IDs to delete.
    """

    try:
        log.info()
    except Exception as e:
        raise e

@connection_wrapper
def list_domains(conn=None, active=True, describe=False, hypervisor_uri=''):
    """List all available domains

    :param active: Set to false to include inactive domains.
    :param describe: Set to true to describe each specified domain.
    """
    for domain in conn.listAllDomains(0):
        if active and domain.isActive() == 0:
            continue
        
        if domain.ID() == -1:
            print('Name:{} UUID:{}'.format(domain.name(), domain.UUIDString()))
            continue
            
        print('Name:{} ID:{}'.format(domain.name(), domain.ID()))

@connection_wrapper
def halt_domains(conn=None, *domain_ids, restart=False, hypervisor_uri):
    """Shuts down one or more domains.
    
    :param domain_ids: Comma separated domain IDs to shutdown/restart.
    :param restart: If set to true will restart the specified domains instead
    of shutting them down.
    """
    
    pass

@connection_wrapper
def start_domains(conn=None, *domain_ids, hypervisor_uri=''):
    """Starts one or more domains.
    If the domain is already active, it will warn the user and skip it.
    
    :param domain_ids: Comma separated domain IDs to start.
    """
    
    domains = conn.listAllDomains(VIR_CONNECT_LIST_DOMAINS_ACTIVE)
    available_domains = any(domain in domain_ids for domain in domains)
    

def load_config(config_file):
    """Loads the configuration 

    param config: TOML spec configuration used for creating new resources.
    """
    
    try:
        config = toml.load(config_file)
    except Exception as e:
        raise e

    return config
