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
from tabulate import tabulate
from .log import log

def load_config(config_file):
    """Loads the configuration 

    param config: TOML spec configuration used for creating new resources.
    """
    
    try:
        config = toml.load(config_file)
    except Exception as e:
        raise e

    return config


def tabulate_data(data, headers):
    _table_type = 'fancy_grid'
    print(tabulate(data, headers, tablefmt=_table_type))
