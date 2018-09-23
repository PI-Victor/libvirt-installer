import sys

import toml
import libvirt


from .log import log
from .utils import Error


def connection_wrapper(func):
    """Wraps a function with the libvirt connection handler
    param func: Any function that needs to perform actions against the 
    hypervisor.
    """
    def _wrap_connection(**kwargs):
        # NOTE: should we handle key validation as well?
        conn = libvirt.openReadOnly(kwargs.get('hypervisor_uri'))
        if conn == None:
            raise Error
        else:
            func(**kwargs, conn=conn)
    
    return _wrap_connection

@connection_wrapper
def create_domains(hypervisor_uri, config_file, conn=''):
    """Create new domains 
    :param config_file: toml format configuration file that describes the 
    domains.
    """
    try:
        config = toml.load(config_file)
    except Exception as e:
        raise e
    
    log.debug('Loaded config: \n{}'.format(config))

@connection_wrapper
def delete_domains(hypervisor_uri):
    """
    """
    
    pass

@connection_wrapper
def list_domains(hypervisor_uri):
    """List all available domains
    """
    
    pass

