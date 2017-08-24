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
Plantuml encoding module.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

import logging
from zlib import compress
from posixpath import join

from requests import get
from six.moves import range
from six import indexbytes, unichr

log = logging.getLogger(__name__)


def compress_and_encode(content):
    """
    Compress the plantuml text and encode it for the plantuml server.

    :param str content: Content to compress and encode.
    :return: The compressed and encoded content.
    :rtype: str
    """
    zlibbed_str = compress(content.strip().encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return encode(compressed_string)


def encode(data):
    """
    Encode given data into PlantUML server encoding.

    This algorithm is similar to the base64 but custom for the plantuml server.

    :param bytes data: Data to encode.
    :return: The encoded data as printable ASCII.
    :rtype: str
    """
    res = ''
    for i in range(0, len(data), 3):
        if i + 2 == len(data):
            res += _encode3bytes(
                indexbytes(data, i),
                indexbytes(data, i + 1),
                0
            )
        elif i + 1 == len(data):
            res += _encode3bytes(
                indexbytes(data, i),
                0, 0
            )
        else:
            res += _encode3bytes(
                indexbytes(data, i),
                indexbytes(data, i + 1),
                indexbytes(data, i + 2)
            )
    return res


def _encode3bytes(b1, b2, b3):
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    res = ''
    res += _encode6bit(c1 & 0x3F)
    res += _encode6bit(c2 & 0x3F)
    res += _encode6bit(c3 & 0x3F)
    res += _encode6bit(c4 & 0x3F)
    return res


def _encode6bit(b):
    if b < 10:
        return unichr(48 + b)
    b -= 10
    if b < 26:
        return unichr(65 + b)
    b -= 26
    if b < 26:
        return unichr(97 + b)
    b -= 26
    if b == 0:
        return '-'
    if b == 1:
        return '_'


def plantuml(server, extension, content):
    """
    Call the PlantUML server.

    :param str server: Base URL for the server.
    :param str extension: File format / extension to use for the request.
    :param str content: Content to render.
    :return: Response of the request.
    :rtype: str
    """
    encoded = compress_and_encode(content)
    url = join(server, extension, encoded)
    log.debug('Calling URL:\n{}'.format(url))
    response = get(url)
    response.raise_for_status()
    return response.content


__all__ = ['plantuml']
