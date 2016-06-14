# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Carlos Jenkins
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Plantweb main rendering module.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

import logging
from json import loads
from copy import deepcopy
from inspect import isfunction
from traceback import format_exc
from shlex import split as shsplit
from importlib import import_module
from os.path import isfile, expanduser, join
from subprocess import check_output, CalledProcessError


log = logging.getLogger(__name__)


DEFAULT_CONFIG = {
    'engine': 'plantuml',
    'format': 'svg',
    'server': 'http://plantuml.com/plantuml/',
    'use_cache': True,
    'cache_dir': '~/.cache/plantweb'
}
"""
Default configuration for plantweb.

.. note::

   The default engine will be used only when the engine was unset and it was
   unable to be auto-determined.

To set a different default configuration create a JSON file ``.plantwebrc``
in your git repository root or in your home, as defined in
:data:`DEFAULTS_PROVIDERS`.
"""


DEFAULTS_PROVIDERS = [
    'python://plantweb.defaults.DEFAULT_CONFIG',
    'file://~.plantwebrc',
    'git://.plantwebrc'
]
"""
List of defaults providers ordered by read priority.

Last items will be processed last and thus will override previous values.

Available providers are:

``git://``
   Will fetch the repository root from current working directory using git's
   ``git rev-parse --show-toplevel`` and then read the specified file from
   that path.

``file://``
   Will read the file specified. User expansion ``~`` is supported.

``python://``
   Will import the given path to a variable or function:

   - If function, it will be executed without arguments and its result will be
     returned.
   - If variable, it must be dictionary similar to :data:`DEFAULT_CONFIG`.
"""


def _read_defaults_git(path):
    """
    Read defaults from given path in current git repository.

    See :data:`DEFAULTS_PROVIDERS` for inner workings.
    """
    # Determine repository root
    try:
        cmd_git = 'git rev-parse --show-toplevel'

        repo_root = check_output(
            shsplit(cmd_git)
        ).decode('utf-8').strip()

    except CalledProcessError:
        log.warning('ERROR: Unable to determine git root directory')
        return {}

    return _read_defaults_file(
        join(repo_root, path)
    )


def _read_defaults_file(path):
    """
    Read defaults from given path.

    See :data:`DEFAULTS_PROVIDERS` for inner workings.
    """

    rcfile = expanduser(path)
    if isfile(rcfile):
        with open(rcfile, 'r') as fd:
            return loads(fd.read())

    log.warning('Defaults file {} doesn\'t exists'.format(path))
    return {}


def _read_defaults_python(location):
    """
    Import and read defaults from given Python entity.

    See :data:`DEFAULTS_PROVIDERS` for inner workings.
    """
    try:
        module_path, variable_name = location.rsplit('.', 1)
        module = import_module(module_path)

        if not hasattr(module, variable_name):
            log.warning('Unknown entity {}'.format(location))
            return {}

        entity = getattr(module, variable_name)

        if isfunction(entity):
            return entity()

        return entity

    except:
        log.debug(format_exc())
        log.warning('Unable to load entity {}'.format(location))

    return {}


SCHEMES = {
    'git://': _read_defaults_git,
    'file://': _read_defaults_file,
    'python://': _read_defaults_python
}


def read_defaults(cached=True):
    """
    Get the defaults values.

    :param bool cached: Read cached default values or determine them from
     the list of providers. See :data:`DEFAULTS_PROVIDERS`.

    :return: A dictionary like :data:`DEFAULT_CONFIG` with the user defaults.
    :rtype: dict
    """
    if cached and hasattr(read_defaults, 'cache'):
        return read_defaults.cache

    defaults = {}

    for provider in DEFAULTS_PROVIDERS:
        for scheme, func in SCHEMES.items():
            if provider.startswith(scheme):
                overrides = func(
                    provider.replace(scheme, '', 1)
                )
                defaults.update(deepcopy(overrides))

                break
        else:
            raise Exception('Unknown provider URI {}'.format(provider))

    read_defaults.cache = defaults
    return defaults


__all__ = ['DEFAULT_CONFIG', 'DEFAULTS_PROVIDERS', 'read_defaults']
