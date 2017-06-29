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
Application entry point module.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

import logging

from .render import render_file
from .defaults import read_defaults


log = logging.getLogger(__name__)


def main(args):
    """
    Application main function.

    :param args: An arguments namespace.
    :type args: :py:class:`argparse.Namespace`
    :return: Exit code.
    :rtype: int
    """

    config = {
        'engine': args.engine,
        'format': args.format,
        'server': args.server,
        'use_cache': args.use_cache,
        'cache_dir': args.cache_dir
    }

    # Set overridable arguments with configuration
    defaults = read_defaults()

    for key in config.keys():
        if config[key] is None:
            config[key] = defaults[key]

    for human, key in [
        ('Engine: ', 'engine'),
        ('Format: ', 'format'),
        ('Server: ', 'server'),
        ('Use Cache: ', 'use_cache'),
        ('Cache Dir: ', 'cache_dir'),
    ]:
        print('  {}: {}'.format(human, config[key]))

    for src in args.sources:

        destination = render_file(
            src,
            renderopts={
                key: config[key] for key in ['engine', 'format', 'server']
            },
            cacheopts={
                key: config[key] for key in ['use_cache', 'cache_dir']
            },
        )

        print('Writing output for {} to {}'.format(src, destination))

    return 0


__all__ = ['main']
