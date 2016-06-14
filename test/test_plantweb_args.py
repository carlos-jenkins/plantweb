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
Test suite for module plantweb.args.

See http://pythontesting.net/framework/pytest/pytest-introduction/#fixtures
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from os import listdir
from os.path import join, abspath, dirname, normpath

from plantweb import args


def test_args():

    examples_dir = normpath(join(abspath(dirname(__file__)), '../examples/'))
    sources = [
        join(examples_dir, src)
        for src in listdir(examples_dir)
        if src.endswith('.uml')
    ]

    parsed = args.parse_args(sources + ['-vvvv'])

    assert parsed.verbose == 4
    assert parsed.sources == sources

    assert parsed.engine is None
    assert parsed.format is None
    assert parsed.server == 'http://plantuml.com/plantuml/'

    assert not parsed.no_cache
    assert parsed.cache_dir == '~/.cache/plantweb'
