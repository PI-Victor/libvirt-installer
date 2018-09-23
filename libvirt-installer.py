import click

from installer.core import (
    create_domains,
    delete_domains,
    list_domains,
)


_global_options = [
    click.option(
        '--hypervisor_uri',
        default='qemu:///system',
        help='The URI of the connection',
    ),
]

def add_options(options):
    """Pre-wrap common parameters that all commands should 
    implement.
    """
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

@click.group()
def cli(**kwargs):
    pass

@cli.command()
@click.option(
    '--config-file',
    default='config.toml',
    help='Path to TOML application config',
    type=click.Path(exists=True),
)
@add_options(_global_options)
def create(hypervisor_uri, config_file):
    create_domains(
        hypervisor_uri=hypervisor_uri,
        config_file=config_file,
    )

@cli.command()
@click.option(
    '--list',
    default='',
    help='List all available domains',
)
@add_options(_global_options)
def list(hypervisor_uri):
    list_domains(hypervisor_uri=hypervisor_uri)

@cli.command()
@click.option(
    '--delete',
    default='',
    help='A single or comma separated values of available domains to delete',
)
@add_options(_global_options)
def delete(hypervisor_uri, domain_list):
    delete_domains(
        hypervisor_uri=hypervisor_uri,
        domain_list=hypervisory_uri,
    )

if __name__ == '__main__':
    cli()
