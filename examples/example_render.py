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
plantweb example 1.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from plantweb.render import render


CONTENT = """
actor Foo1
boundary Foo2
control Foo3
entity Foo4
database Foo5
Foo1 -> Foo2 : To boundary
Foo1 -> Foo3 : To control
Foo1 -> Foo4 : To entity
Foo1 -> Foo5 : To database
"""


if __name__ == '__main__':

    print('==> INPUT:')
    print(CONTENT)

    output = render(
        CONTENT,
        engine='plantuml',
        format='svg',
        cacheopts={
            'use_cache': False
        }
    )

    print('==> OUTPUT:')
    print(output)
