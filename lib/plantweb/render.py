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
from hashlib import sha256
from os.path import basename, splitext, isfile, expanduser, join

from .plantuml import plantuml


log = logging.getLogger(__name__)


WRAP_STR = {
    'plantuml': 'uml',
    'ditaa': 'ditaa',
    'graphviz': 'dot'
}
"""
Map between the name of the engine and the wrap string used in the
``@startXXX`` directive.
"""


def determine_engine(content):
    """
    Determine the engine used in the given content.

    The engine is determined by the ``@startXXX`` used at the beginning of the
    file. Possible values are:

    ::

        @startuml --> plantuml
        @startdot --> graphviz
        @startditaa --> ditaa

    :param str content: Content to analyze.
    :return: The name of the engine found, or None.
    :rtype: str
    """
    if content.startswith('@startuml'):
        return 'plantuml'
    if content.startswith('@startdot'):
        return 'graphviz'
    if content.startswith('@startditaa'):
        return 'ditaa'
    return None


def render_cached(
        content, format,
        server='http://plantuml.com/plantuml/',
        use_cache=True, cache_dir='~/.cache/plantweb'):

    if not use_cache:
        return plantuml(server, format, content)

    sha = sha256(content.encode('utf-8')).hexdigest()

    cache_file = join(
        expanduser(cache_dir),
        '{}.{}'.format(sha, format)
    )

    # Use cache if available
    if isfile(cache_file):
        with open(cache_file, 'rb') as fd:
            return fd.read()

    # Normal render and save cache
    output = plantuml(server, format, content)

    with open(cache_file, 'wb') as fd:
        fd.write(output)

    return output


def render(content, engine=None, format=None, server=None, cacheopts=None):

    # Determine engine
    engine_found = determine_engine(content)

    # Case 1: forced engine
    if engine is not None:

        if engine_found is None:
            wrap = WRAP_STR[engine]
            content = '@start{0}\n{1}\n@end{0}'.format(wrap, content)

        elif engine_found != engine:
            log.warn(
                'Engine mismatch. Set: {0} != Found: {1}. '
                'Assuming {1} ...'.format(engine, engine_found)
            )
            engine = engine_found

    # Case 2: Use engine found
    elif engine_found is not None:
        engine = engine_found

    # Case 3: Use a default engine
    else:
        log.warn(
            'Unable to determine the engine. Assuming \'plantuml\'...'
        )
        engine = 'plantuml'

    # Determine output file format
    if format is None:
        format = 'svg' if engine != 'ditaa' else 'png'

    # Render cached
    if cacheopts is None:
        cacheopts = {}

    output = render_cached(content, format, server=server, **cacheopts)

    return (output, format)


def render_file(infile, outfile=None, renderopts=None, cacheopts=None):

    # Read source file
    with open(infile, 'rb') as fd:
        content = fd.read().decode('utf-8')

    # Render output
    if renderopts is None:
        renderopts = {}

    output, format = render(content, cacheopts=cacheopts, **renderopts)

    # Determine destination file
    if outfile is None:
        outfile = '{}.{}'.format(
            splitext(basename(infile))[0],
            format
        )

    # Write output
    with open(outfile, 'wb') as fd:
        fd.write(output)

    return outfile


__all__ = ['render_file', 'render']
