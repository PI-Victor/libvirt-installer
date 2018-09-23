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

from installer.core import (create_domains, delete_domains, list_domains)


_global_options = [
    click.option(
        '--hypervisor_uri',
        default='qemu:///system',
        help='The URI of the connection',
    ),
]

def add_options(options):
    """Wrap common parameters that all commands should 
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
@add_options(_global_options)
@click.argument(
    'config-file',
    default='config.toml',
    type=click.File('r'),
)
def create(hypervisor_uri, config_file):
    create_domains(hypervisor_uri=hypervisor_uri, config_file=config_file)

@cli.command()
@add_options(_global_options)
@click.argument(
    '--list',
    default=False,
    type=bool,
)
def list(hypervisor_uri):
    list_domains(hypervisor_uri=hypervisor_uri)

@cli.command()
@click.argument('')
@add_options(_global_options)
def delete(hypervisor_uri, domain_list):
    delete_domains(hypervisor_uri=hypervisor_uri, domain_list=domain_list)

if __name__ == '__main__':
    cli()
