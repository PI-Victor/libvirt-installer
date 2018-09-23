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

from .log import log
from .utils import Error


def connection_wrapper(func):
    """Wraps a function, representing an action, with the libvirt connection 
    handler.
    param func: Any function that needs to perform actions against libvirt
    """
    def _wrap_connection(**kwargs):
        conn = libvirt.openReadOnly(kwargs.get('hypervisor_uri'))
        if conn == None:
            raise Error
        else:
            func(**kwargs, conn=conn)
    
    return _wrap_connection

@connection_wrapper
def create_domains(hypervisor_uri, config_file, conn=None):
    """Create new domains 
    :param config_file: toml format configuration file that describes the 
    domains.
    """
    config = load_config(config_file)
    log.debug('Loaded config: \n{}'.format(config))

@connection_wrapper
def delete_domains(hypervisor_uri, *domains, active):
    """Deletes domains 
    """
    
    pass

@connection_wrapper
def list_domains(hypervisor_uri, active=False):
    """List all available domains
    """
    
    pass

def load_config(config_file):
    """Loads the configuration 
    param config: TOML spec configuration used for creating new resources.
    """
    
    try:
        config = toml.load(config_file)
    except Exception as e:
        raise e

    return config
