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
Test suite for module plantweb.main.

See http://pythontesting.net/framework/pytest/pytest-introduction/#fixtures
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from os import listdir, getcwd
from os.path import splitext, basename

from plantweb.main import main
from plantweb.args import parse_args


def test_main(tmpdir, sources):

    cache_dir = str(tmpdir.mkdir('cache'))
    print('Cache directory at: {}'.format(cache_dir))

    parsed = parse_args(
        sources + ['-vvvv', '--cache-dir', cache_dir]
    )

    assert parsed.verbose == 4
    assert parsed.sources == sources

    rcode = main(parsed)
    assert rcode == 0

    src_names = [
        splitext(basename(src))[0]
        for src in sources
    ]
    out_names = [
        name
        for name, ext in [splitext(out) for out in listdir(getcwd())]
        if ext in ['.png', '.svg']
    ]

    assert set(src_names) == set(out_names)
