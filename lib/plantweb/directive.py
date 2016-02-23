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
Migrate to
https://github.com/carlos-jenkins/arenal/blob/master/lib/arenal/directives/uml.py
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

import logging


log = logging.getLogger(__name__)


def generate_name(self, node, fileformat):
    key = hashlib.sha1(node['uml'].encode('utf-8')).hexdigest()
    fname = 'plantuml-%s.%s' % (key, fileformat)
    imgpath = getattr(self.builder, 'imgpath', None)
    if imgpath:
        return ('/'.join((self.builder.imgpath, fname)),
                os.path.join(self.builder.outdir, '_images', fname))
    else:
        return fname, os.path.join(self.builder.outdir, fname)


def align(argument):
    align_values = ('left', 'center', 'right')
    return directives.choice(argument, align_values)

class UmlDirective(Directive):
    """Directive to insert PlantUML markup

    Example::

        .. uml::
           :alt: Alice and Bob

           Alice -> Bob: Hello
           Alice <- Bob: Hi
    """
    has_content = True
    option_spec = {'alt': directives.unchanged,
                   'caption': directives.unchanged,
                   'height': directives.length_or_unitless,
                   'width': directives.length_or_percentage_or_unitless,
                   'scale': directives.percentage,
                   'align': align,
                   }

    def run(self):
        node = plantuml(self.block_text, **self.options)
        node['uml'] = '\n'.join(self.content)

        # XXX maybe this should be moved to _visit_plantuml functions. it
        # seems wrong to insert "figure" node by "plantuml" directive.
        if 'caption' in self.options or 'align' in self.options:
            node = nodes.figure('', node)
            if 'align' in self.options:
                node['align'] = self.options['align']
        if 'caption' in self.options:
            import docutils.statemachine
            cnode = nodes.Element()  # anonymous container for parsing
            sl = docutils.statemachine.StringList([self.options['caption']],
                                                  source='')
            self.state.nested_parse(sl, self.content_offset, cnode)
            caption = nodes.caption(self.options['caption'], '', *cnode)
            node += caption

        return [node]




def setup(app):
    app.add_directive('uml', UmlDirective)
    app.add_directive('graph', GraphDirective)
    app.add_directive('diagram', DiagramDirective)
    app.add_config_value('plantweb_server', None, 'html')


__all__ = ['UmlDirective', 'GraphDirective', 'DiagramDirective']
