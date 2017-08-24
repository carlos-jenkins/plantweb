# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 Carlos Jenkins
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
Test suite for module plantweb.defaults.

See http://pythontesting.net/framework/pytest/pytest-introduction/#fixtures
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from json import dumps
from copy import deepcopy
from os import chdir, getcwd
from os.path import abspath, join
from subprocess import check_call
from shlex import split as shsplit
from distutils.spawn import find_executable

from pytest import mark

from plantweb import defaults


@mark.skipif(
    find_executable('git') is None,
    reason='git executable is missing'
)
def test_defaults(tmpdir, monkeypatch):

    cwd = getcwd()

    # Create work folders
    home = abspath(str(tmpdir.mkdir('home')))
    repo_root = abspath(str(tmpdir.mkdir('gitrepo')))

    basefile = '.plantwebrc'
    homefile = join(home, basefile)

    # Monkey path providers to use this directories
    providers_patch = deepcopy(defaults.DEFAULTS_PROVIDERS)
    providers_patch[1] = 'file://{}'.format(homefile)
    monkeypatch.setattr(defaults, 'DEFAULTS_PROVIDERS', providers_patch)

    # Test errort path
    try:
        chdir(home)
        user_defaults = defaults._read_defaults_git(basefile)
        assert not user_defaults
    finally:
        chdir(cwd)

    user_defaults = defaults._read_defaults_file(homefile)
    assert not user_defaults

    user_defaults = defaults._read_defaults_python(
        'thismodule.doesntexists.MYVAR'
    )
    assert not user_defaults

    user_defaults = defaults._read_defaults_python(
        'plantweb.defaults.THISVARDOESNTEXISTS'
    )
    assert not user_defaults

    try:
        # Create git repository
        chdir(repo_root)
        check_call(shsplit('git init'))

        # Write overrides
        common_filename = '.plantwebrc'

        with open(join(repo_root, common_filename), 'w') as fd:
            defaults1 = {'format': 'png', 'engine': 'graphviz'}
            fd.write(dumps(defaults1))

        with open(join(home, common_filename), 'w') as fd:
            defaults2 = {'use_cache': False, 'engine': 'ditaa'}
            fd.write(dumps(defaults2))

        # Check multilayer defaults
        user_defaults = defaults.read_defaults(cached=False)
        assert user_defaults['server'] == \
            defaults.DEFAULT_CONFIG['server']
        assert user_defaults['cache_dir'] == \
            defaults.DEFAULT_CONFIG['cache_dir']
        assert user_defaults['format'] == 'png'
        assert user_defaults['engine'] == 'graphviz'
        assert user_defaults['use_cache'] is False

        # Check cache
        with open(join(repo_root, common_filename), 'w') as fd:
            defaults3 = {'engine': 'ditaa'}
            fd.write(dumps(defaults3))

        user_defaults = defaults.read_defaults(cached=True)
        assert user_defaults['engine'] == 'graphviz'

        user_defaults = defaults.read_defaults(cached=False)
        assert user_defaults['engine'] == 'ditaa'

    finally:
        chdir(cwd)
