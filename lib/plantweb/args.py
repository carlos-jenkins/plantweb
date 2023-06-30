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
Argument management module.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

import logging
from os import makedirs
from os.path import isfile, abspath, expanduser

from . import __version__


log = logging.getLogger(__name__)


FORMAT = '%(asctime)s:::%(levelname)s:::%(message)s'
V_LEVELS = {
    0: logging.ERROR,
    1: logging.WARNING,
    2: logging.INFO,
    3: logging.DEBUG,
}


class InvalidArguments(Exception):
    """
    Typed exception that allows to fail in argument parsing and verification
    without quiting the process.
    """
    pass


def validate_args(args):
    """
    Validate that arguments are valid.

    :param args: An arguments namespace.
    :type args: :py:class:`argparse.Namespace`
    :return: The validated namespace.
    :rtype: :py:class:`argparse.Namespace`
    """
    level = V_LEVELS.get(args.verbose, logging.DEBUG)
    logging.basicConfig(format=FORMAT, level=level)

    log.debug('Raw arguments:\n{}'.format(args))

    # Verify source file exists
    sources = []
    for src in args.sources:
        if not isfile(src):
            raise InvalidArguments(
                'No such file {}'.format(src)
            )
        sources.append(abspath(src))
    args.sources = sources

    # Check that format and engine compatibility
    if args.format == 'svg' and args.engine == 'ditaa':
        raise InvalidArguments(
            'The ditaa engine doens\'t support the svg format'
        )

    # Prepare default datatypes
    if args.engine == 'auto':
        args.engine = None
    if args.format == 'auto':
        args.format = None

    # Ensure cache dir
    if not args.no_cache:
        makedirs(expanduser(args.cache_dir), exist_ok=True)

    return args


def parse_args(argv=None):
    """
    Argument parsing routine.

    :param argv: A list of argument strings.
    :rtype argv: list
    :return: A parsed and verified arguments namespace.
    :rtype: :py:class:`argparse.Namespace`
    """
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='Python client for the PlantUML server'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='increase verbosity level',
        default=0,
        action='count'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='Plantweb {}'.format(__version__)
    )

    parser.add_argument(
        '--engine',
        default='auto',
        help='engine to use to render diagram',
        choices=['auto', 'plantuml', 'graphviz', 'ditaa']
    )
    parser.add_argument(
        '--format',
        default='auto',
        help='diagram export format',
        choices=['auto', 'svg', 'png']
    )

    parser.add_argument(
        '--server',
        default='http://plantuml.com/plantuml/',
        help='server to use for rendering'
    )

    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='do not use cache'
    )
    parser.add_argument(
        '--cache-dir',
        default='~/.cache/plantweb',
        help='directory to store cached renders'
    )

    parser.add_argument(
        'sources',
        nargs='+',
        help='source files to render'
    )

    args = parser.parse_args(argv)
    try:
        args = validate_args(args)
    except InvalidArguments as e:
        log.critical(e)
        raise e

    return args


__all__ = ['parse_args']
