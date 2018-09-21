from .log import log

import toml


def run(hypervisor_uri, config_file):
    
    try:
        config = toml.load(config_file)
    except Exception as e:
        raise e

    log.debug('Loaded config: \n{}'.format(config))

def open_config(config_file):
    pass
