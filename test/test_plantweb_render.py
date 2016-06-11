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
Test suite for module plantweb.render.

See http://pythontesting.net/framework/pytest/pytest-introduction/#fixtures
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from os import listdir, getcwd
from os.path import join, abspath, dirname, normpath, isfile

import pytest  # noqa

from plantweb import render_file, render


def setup_module(module):
    print('setup_module({})'.format(module.__name__))


def teardown_module(module):
    print('teardown_module({})'.format(module.__name__))


def find_sources():

    examples_dir = normpath(join(abspath(dirname(__file__)), '../examples/'))
    sources = [
        join(examples_dir, src)
        for src in listdir(examples_dir)
        if src.endswith('.uml')
    ]

    if not sources:
        raise Exception(
            'No sources found in {}: {}'.format(examples_dir, sources)
        )

    return sources


def test_render(tmpdir):

    cache_dir = str(tmpdir.mkdir('cache'))
    print('Cache directory at: {}'.format(cache_dir))

    for src in find_sources():

        print('Rendering {} ...'.format(src))

        # Render content directly
        with open(src, 'rb') as fd:
            output, format, engine, sha = render(
                fd.read().decode('utf-8'),
                cacheopts={
                    'use_cache': True,
                    'cache_dir': cache_dir
                }
            )

        # Assert cache exists
        assert isfile(join(cache_dir, '{}.{}'.format(sha, format)))


def test_render_file(tmpdir):

    cache_dir = str(tmpdir.mkdir('cache'))
    print('Cache directory at: {}'.format(cache_dir))

    for src in find_sources():

        print('Rendering {} ...'.format(src))

        outfile = render_file(
            src,
            cacheopts={
                'use_cache': True,
                'cache_dir': cache_dir
            }
        )

        # Make sure output is at cwd
        outfile = join(getcwd(), outfile)

        assert isfile(outfile)
        print('Output file at {}'.format(outfile))


def test_render_cache(tmpdir):

    cache_dir = str(tmpdir.mkdir('cache'))
    print('Cache directory at: {}'.format(cache_dir))

    sources = find_sources()

    for src in sources:

        print('Rendering without cache {} ...'.format(src))

        outfile = render_file(
            src,
            cacheopts={
                'use_cache': False,
                'cache_dir': cache_dir
            }
        )

        # Make sure output is at cwd
        outfile = join(getcwd(), outfile)

        assert isfile(outfile)
        print('Output file at {}'.format(outfile))

    assert not listdir(cache_dir)

    for src in sources:

        print('Rendering {} ...'.format(src))

        # Render content directly
        with open(src, 'rb') as fd:
            output, format, engine, sha = render(
                fd.read().decode('utf-8'),
                cacheopts={
                    'use_cache': True,
                    'cache_dir': cache_dir
                }
            )

        # Assert cache exists
        assert isfile(join(cache_dir, '{}.{}'.format(sha, format)))


def test_render_defaultsrc(tmpdir):
    # FIXME: Test .plantwebrc changes by mocking DEFAULT_CONFIG
    pass
