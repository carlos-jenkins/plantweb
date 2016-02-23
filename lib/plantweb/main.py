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
Application entry point module.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

import logging
from os.path import basename, splitext

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


def main(args):
    """
    Application main function.

    :param args: An arguments namespace.
    :type args: :py:class:`argparse.Namespace`
    :return: Exit code.
    :rtype: int
    """
    for src in args.sources:

        # Read source file
        with open(src, 'rb') as fd:
            content = fd.read().decode('utf-8')

        # Determine file extension
        extension = args.format
        if extension == 'auto':
            extension = 'svg' if args.engine != 'ditaa' else 'png'

        # Wrap content if required
        engine_found = determine_engine(content)
        engine = args.engine

        if engine_found is None:
            # Case 1: Unable to determine engine
            if engine == 'auto':
                log.warn(
                    'Unable to determine the engine for {}. '
                    'Assuming \'plantuml\'...'.format(src)
                )
                engine = 'plantuml'
            # Case 2: Forced engine, we need to wrap the content
            else:
                wrap = WRAP_STR[engine]
                content = '@start{0}\n{1}\n@end{0}'.format(wrap, content)
        # Case 3: Forced engine mismatch with found
        elif engine_found != engine:
            log.warn(
                'Engine mismatch: {0} != {1}. '
                'Assuming {0} ...'.format(engine, engine_found)
            )

        # Define destionation file
        destination = '{}.{}'.format(
            splitext(basename(src))[0],
            extension
        )

        # Write output
        output = plantuml(args.server, extension, content)
        print('Writing output for {} to {}'.format(src, destination))
        with open(destination, 'wb') as fd:
            fd.write(output)

    return 0


__all__ = ['WRAP_STR', 'determine_engine', 'main']
