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
Plantweb main rendering module.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

import logging
from hashlib import sha256
from os import makedirs
from os.path import basename, splitext, isfile, expanduser, join

from .plantuml import plantuml
from .defaults import read_defaults


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
        server, format, content,
        use_cache=None, cache_dir=None):
    """
    Render given content in the PlantUML server or fetch it from cache.

    :param str server: URL to PlantUML server.
    :param str format: File format to render the content. One of the supported
     by the PlantUML server (``svg`` or ``png``).
    :param str content: Content to render with mandatory ``@startxxx`` tags.
    :param bool use_cache: Use local cache to avoid requesting the server for
     already rendered diagrams. If ``None``, the default value will be used.
    :param str cache_dir: Directory to store the cached diagrams. If ``None``
     the default value will be used.

    :return: A tuple of ``(content, sha)`` with the bytes of the rendered
     content and a sha256 hash string identifying the content.
    :rtype: tuple
    """
    sha = sha256(content.encode('utf-8')).hexdigest()

    if use_cache is None:
        use_cache = read_defaults()['use_cache']

    if not use_cache:
        return (
            plantuml(server, format, content),
            sha
        )

    if cache_dir is None:
        cache_dir = read_defaults()['cache_dir']
    cache_dir = expanduser(cache_dir)

    cache_file = join(
        cache_dir, '{}.{}'.format(sha, format)
    )

    # Use cache if available
    log.debug('Trying to load cache file {} ...'.format(cache_file))
    if isfile(cache_file):
        with open(cache_file, 'rb') as fd:
            return (fd.read(), sha)

    # No cache, make sure the directory is available
    makedirs(cache_dir, exist_ok=True)

    # Normal render and save cache
    output = plantuml(server, format, content)

    with open(cache_file, 'wb') as fd:
        fd.write(output)
    log.debug('Wrote cache file {} ...'.format(cache_file))

    return (output, sha)


def render(
        content,
        engine=None,
        format=None,
        server=None,
        cacheopts=None):
    """
    Render given PlantUML, Graphviz or DITAA content.

    :param str content: Content to render.
    :param str engine: Engine to use to render the content. One of
     ``'plantuml'``, ``'graphviz'`` or ``'ditaa'``. If ``None``, the engine
     will be auto-determined by looking into the content for the ``@startxxxx``
     tags, and if unable to be auto-determined the default engine will be used.
    :param str format: Format of the rendered content. Raster ``png`` or vector
     ``svg``. Please note that engine ``ditaa`` can only render to ``png``. If
     ``None``, the default formatwill always be selected unless the engine
     doesn't supports it.
    :param str server: URL to PlantUML server. This will passed as is to
     :func:`render_cached`. If ``None`` the default server URL will be used.

    :return: A tuple of ``(output, format, engine, sha)`` with the bytes of the
     rendered output, a string with the name of the output format, a string
     with the name of the engine used or detected and a string of the sha256
     for identifying the cache file.
    :rtype: tuple
    """

    # Determine engine
    engine_found = determine_engine(content)

    # Case 1: forced engine
    if engine is not None:

        if engine_found is None:
            wrap = WRAP_STR[engine]
            content = '@start{0}\n{1}\n@end{0}'.format(wrap, content)

        elif engine_found != engine:
            log.warning(
                'Engine mismatch. Set: {0} != Found: {1}. '
                'Assuming {1} ...'.format(engine, engine_found)
            )
            engine = engine_found

    # Case 2: Use engine found
    elif engine_found is not None:
        engine = engine_found

    # Case 3: Use a default engine
    else:
        engine = read_defaults()['engine']
        log.warning(
            'Unable to determine the engine. Assuming \'{}\'...'.format(engine)
        )

    # Determine output file format
    if format is None:
        format = read_defaults()['format'] if engine != 'ditaa' else 'png'

    # Determine server
    if server is None:
        server = read_defaults()['server']

    # Render cached
    if cacheopts is None:
        cacheopts = {}

    output, sha = render_cached(server, format, content, **cacheopts)

    return (output, format, engine, sha)


def render_file(infile, outfile=None, renderopts=None, cacheopts=None):
    """
    Render given PlantUML, Graphviz or DITAA file.

    :param str infile: Path to source file to render.
    :param str outfile: Path to output file. If ``None``, the filename will be
     auto-determined and saved to the current working directory.
    :param dict renderopts: Rendering options (``engine``, ``format`` and
     ``server``) as in :func:`render`.
    :param dict cacheopts: Caching options (``use_cache`` and ``cache_dir``) as
     in :func:`render`.

    :return: Path to output file.
    :rtype: str
    """

    # Read source file
    with open(infile, 'rb') as fd:
        content = fd.read().decode('utf-8')

    # Render output
    if renderopts is None:
        renderopts = {}

    output, format, engine, sha = render(
        content, cacheopts=cacheopts, **renderopts
    )

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


__all__ = [
    'render_file',
    'render',
    'render_cached',
    'determine_engine',
    'WRAP_STR'
]
