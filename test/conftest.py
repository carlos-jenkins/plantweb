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
Pytest fixtures for Plantweb testing.

See https://pytest.org/latest/fixture.html
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from os import listdir
from shutil import rmtree
from tempfile import mkdtemp
from distutils.dir_util import mkpath
from os.path import join, abspath, dirname, normpath

from pytest import fixture
from sphinx.application import Sphinx


@fixture(scope='session')
def sources():
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


class SphinxTest(object):
    """
    Run a Sphinx build for testing.
    """
    def __init__(self):
        # Create workspace for this test
        self.workspace = mkdtemp(prefix='platwebtest')

        # Define sphinx folder
        self.srcdir = join(self.workspace, '__source')
        self.confdir = join(dirname(__file__), 'sphinxconf')
        self.outdir = join(self.workspace, '_build')
        self.doctreedir = join(self.workspace, '_doctrees')

        mkpath(self.srcdir)

        # Specify plantweb overrides
        self.cachedir = join(self.workspace, '_cache')
        self.confoverrides = {
            'plantweb_defaults': {
                'server': 'http://plantuml.com/plantuml/',
                'use_cache': True,
                'cache_dir': self.cachedir
            }
        }

    def execute(self, content, buildername='html'):
        # Create source index.rst
        with open(join(self.srcdir, 'index.rst'), 'wb') as fd:
            fd.write(content.encode('utf-8'))

        sphinx = Sphinx(
            self.srcdir,
            self.confdir,
            self.outdir,
            self.doctreedir,
            buildername,
            confoverrides=self.confoverrides,
            warningiserror=True
        )
        sphinx.build()

    def __call__(self, *args, **kwargs):
        return self.execute(*args, **kwargs)

    def clean(self):
        # Destroy build whole Sphinx directory
        rmtree(self.workspace)


@fixture(scope='function')
def sphinx(request):
    sphinxtest = SphinxTest()
    request.addfinalizer(sphinxtest.clean)
    return sphinxtest
