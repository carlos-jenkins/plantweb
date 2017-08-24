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
Test suite for module plantweb.directive.

See http://pythontesting.net/framework/pytest/pytest-introduction/#fixtures
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from os import listdir
from os.path import join, basename


def identify_content(content):
    if content.startswith('@startuml'):
        return 'uml'
    if content.startswith('@startdot'):
        return 'graph'
    if content.startswith('@startditaa'):
        return 'diagram'
    return None


def images_in(path):
    return [
        f for f in listdir(path)
        if f.endswith('.png') or f.endswith('.svg')
    ]


DIRECTIVE_CONTENT_TPL = """
.. {}::

    {}
"""


def test_directive_content(sources, sphinx):

    directives = []

    # Read source files and format directives
    for src in sources:
        with open(src, 'rb') as fd:
            content = fd.read().decode('utf-8')

            directive_name = identify_content(content)
            directive = DIRECTIVE_CONTENT_TPL.format(
                directive_name,
                '\n    '.join(
                    content.split('\n')[1:-2]
                )
            )
            directives.append(directive)

    # Execute sphinx build
    sphinx('\n'.join(directives))

    # Assert images creation
    cached_images = images_in(sphinx.cachedir)
    copied_images = images_in(join(sphinx.outdir, '_images'))
    assert len(sources) == len(cached_images)
    assert sorted(cached_images) == sorted(copied_images)


DIRECTIVE_ARGUMENT_TPL = """
.. {}:: {}

"""


def test_directive_argument(sources, sphinx):
    directives = []

    # Read sources and create argument files
    for src in sources:
        with open(src, 'rb') as fdin:
            content = fdin.read().decode('utf-8')

            # Write destination file
            srcfile = basename(src)

            with open(join(sphinx.srcdir, srcfile), 'w') as fdout:
                fdout.write('\n'.join(content.split('\n')[1:-2]))

            # Format and add directive
            directive_name = identify_content(content)
            directive = DIRECTIVE_ARGUMENT_TPL.format(
                directive_name, srcfile
            )
            directives.append(directive)

    # Execute sphinx build
    sphinx('\n'.join(directives))

    # Assert sources and images creation
    source_files = listdir(sphinx.srcdir)
    for src in sources:
        assert basename(src) in source_files

    cached_images = images_in(sphinx.cachedir)
    copied_images = images_in(join(sphinx.outdir, '_images'))
    assert len(sources) == len(cached_images)
    assert sorted(cached_images) == sorted(copied_images)
