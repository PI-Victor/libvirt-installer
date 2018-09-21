import click

from installer.core import run


@click.group()
def cli():
    pass

@cli.command()
@click.option(
    '--hypervisor-uri',
    default='qemu:///system',
    help='Hypervisor URI to connecto to',
)

@click.option(
    '--config-file',
    default='config.toml',
    help='Path to TOML application config',
    type=click.Path(),
)
def start(hypervisor_uri, config_file):
    run(hypervisor_uri, config_file)
    
if __name__ == '__main__':
    cli()
