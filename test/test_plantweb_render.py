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
from os.path import join, isfile

from plantweb import defaults
from plantweb.render import render_file, render

from pytest import raises


def test_render(tmpdir, sources):

    cache_dir = str(tmpdir.mkdir('cache'))
    print('Cache directory at: {}'.format(cache_dir))

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


def test_render_forced_and_defaults(monkeypatch):

    # Monkey path providers to use just known defaults
    monkeypatch.setattr(
        defaults,
        'DEFAULTS_PROVIDERS',
        [defaults.DEFAULTS_PROVIDERS[0]]
    )
    # Force reload of defaults
    defaults.read_defaults(cached=False)

    # Test forced render
    src = """\
digraph G {
    a1 -> a2;
    a2 -> a3;
}
    """
    output, frmt, engine, sha = render(src, engine='graphviz')
    assert b'<title>a1</title>' in output
    assert b'<title>a2</title>' in output
    assert b'<title>a3</title>' in output
    assert b'<title>a4</title>' not in output
    assert b'Syntax Error' not in output

    # Test default engine
    src = """\
Bob -> Alice : hello
"""
    output, frmt, engine, sha = render(src)
    assert b'Bob</text>' in output
    assert b'Alice</text>' in output
    assert b'hello</text>' in output

    # Test mismatched forced engine
    src = """\
@startuml
Bob -> Alice : hello
@enduml
"""
    output, frmt, engine, sha = render(src, engine='ditaa')
    assert b'Bob</text>' in output
    assert b'Alice</text>' in output
    assert b'hello</text>' in output


def test_render_file(tmpdir, sources):

    cache_dir = str(tmpdir.mkdir('cache'))
    print('Cache directory at: {}'.format(cache_dir))

    for src in sources:

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


def test_render_cache(tmpdir, monkeypatch, sources):

    cache_dir = str(tmpdir.mkdir('cache'))
    print('Cache directory at: {}'.format(cache_dir))
    assert not listdir(cache_dir)

    for src in sources:

        print('Rendering without cache {} ...'.format(src))

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

    assert listdir(cache_dir)

    # Re-render using cache
    from plantweb import render as rendermod

    def plantuml(server, format, content):
        raise Exception('You shouldn\'t have got here.')
    monkeypatch.setattr(rendermod, 'plantuml', plantuml)

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

    # Test server recall if not use_cache
    for src in sources:
        with open(src, 'rb') as fd:
            with raises(Exception) as e:
                render(
                    fd.read().decode('utf-8'),
                    cacheopts={
                        'use_cache': False
                    }
                )
            assert str(e.value) == 'You shouldn\'t have got here.'
