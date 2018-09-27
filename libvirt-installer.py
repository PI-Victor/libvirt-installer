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

import click

from installer.core import (
    create_domains,
    delete_domains,
    list_domains,
    halt_domains,
    start_domains,
)


_global_options = [
    click.option(
        '--hypervisor-uri',
        default='qemu:///system',
        help='The URI of the connection',
    ),
]

def add_options(options):
    """Wrap common parameters that all commands should implement."""
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

@click.group()
def cli():
    pass

@cli.command()
@add_options(_global_options)
@click.argument('config-file', default='config.toml', type=click.File('r'))
def create(hypervisor_uri, config_file):
    """Create a new cluster based on the config file."""
    create_domains(hypervisor_uri=hypervisor_uri, config_file=config_file)

@cli.command()
@add_options(_global_options)
@click.option(
    '--active',
    default=True,
    help='Set to false to list inactive domains',
    type=bool,
)
@click.option(
    '--describe',
    default=False,
    help='Set to True to view a more detailed domain description',
    type=bool,
)
def list(hypervisor_uri, active, describe):
    """Lists all domains."""
    list_domains(
        active=active,
        describe=describe,
        hypervisor_uri=hypervisor_uri
    )

@cli.command()
@add_options(_global_options)
@click.argument('UUIDs', nargs=-1)
def delete(hypervisor_uri, uuids):
    """A list of domain UUIDs to delete.

    Use the *list* command to list the corresponding domains UUIDs.
    This command will first try to destroy and then undefine the corresponding
    domain.
    """
    delete_domains(hypervisor_uri, uuids)

@cli.command()
@add_options(_global_options)
@click.option(
    '--restart',
    default=False,
    type=bool,
    help='Restart the machines instead of shutting them down',
)
@click.argument('UUIDs', nargs=-1)
def halt(hypervisor_uri, uuids, restart):
    """Shutdown one or more domains."""
    halt_domains(uuids, hypervisor_uri=hypervisor_uri, restart=restart)

@cli.command()
@add_options(_global_options)
@click.argument('UUIDs', nargs=-1)
def start(hypervisor_uri, uuids):
    """Start one or more domains."""
    start_domains(uuids, hypervisor_uri=hypervisor_uri)

if __name__ == '__main__':
    cli()
