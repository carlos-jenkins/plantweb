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
Sphinx directives for rendering PlantUML, Graphviz and Ditaa using Plantweb.
"""

from logging import getLogger
from traceback import format_exc
from os.path import join, relpath
from distutils.dir_util import mkpath
from abc import ABCMeta, abstractmethod

from six import add_metaclass
from docutils import nodes
from docutils.parsers.rst.directives.images import Image

from . import defaults
from .render import render


log = getLogger(__name__)


@add_metaclass(ABCMeta)
class Plantweb(Image):

    required_arguments = 0
    optional_arguments = 0  # Was 1 - Fixme to support loading external content
    option_spec = Image.option_spec.copy()
    has_content = True

    def run(self):
        # Check if file insertion is enabled
        if not self.state.document.settings.file_insertion_enabled:
            msg = (
                'File and URL access deactivated. '
                'Ignoring directive "{}".'.format(self.name)
            )
            warning = nodes.warning(
                '', self.state_machine.reporter.warning(
                    '', nodes.literal_block('', msg),
                    line=self.lineno
                )
            )
            return [warning]

        # Execute plantweb call
        try:
            output, frmt, engine, sha = render(
                '\n'.join(self.content),
                engine=self._get_engine_name()
            )
        except:
            msg = format_exc()
            error = nodes.error(
                '', self.state_machine.reporter.error(
                    '', nodes.literal_block('', msg),
                    line=self.lineno
                )
            )
            return [error]

        # Fetch builder
        builder = self.state_machine.document.settings.env.app.builder

        # Determine filename
        filename = '{}.{}'.format(sha, frmt)
        imgpath = join(builder.outdir, builder.imagedir, 'plantweb')

        # Create images output folder
        log.debug('imgpath set to {}'.format(imgpath))
        mkpath(imgpath)

        # Write content
        filepath = join(imgpath, filename)

        with open(filepath, 'wb') as fd:
            fd.write(output)

        log.debug('Wrote image file {}'.format(filepath))

        # Default to align center
        if 'align' not in self.options:
            self.options['align'] = 'center'

        # Determine relative path to image from src directory
        filepath_relative = relpath(filepath, builder.srcdir)

        # Run Image directive
        self.arguments = [filepath_relative]
        return Image.run(self)

    @abstractmethod
    def _get_engine_name(self):
        pass


class UmlDirective(Plantweb):
    def _get_engine_name(self):
        return 'plantuml'


class GraphDirective(Plantweb):
    def _get_engine_name(self):
        return 'graphviz'


class DiagramDirective(Plantweb):
    def _get_engine_name(self):
        return 'ditaa'


def defaults_provider():
    """
    Defaults provider that allows to register Sphinx user defaults.

    This dummy defaults provider just returns it's attribute ``overrides`` if
    it exists.

    :return: The dictionary of the form :data:`DEFAULT_CONFIG`.
    :rtype: dict
    """
    return getattr(defaults_provider, 'overrides', {})


def builder_inited_handler(app):
    """
    We use this event handler to grab user defaults for Plantweb and use them
    in Plantweb rendering.

    See https://plantweb.readthedocs.io/index.html#overriding-defaults

    This is the handler of the 'builder-inited' event emitted by Sphinx.

        Emitted when the builder object has been created.
        It is available as app.builder.

    See http://www.sphinx-doc.org/en/stable/extdev/appapi.html#event-builder-inited
    """  # noqa
    log.debug('Sphinx overridden Plantweb defaults:')
    log.debug(app.config.plantweb_defaults)

    # Set overrides in provider
    defaults_provider.overrides = app.config.plantweb_defaults

    # Register provider with the highest priority
    provider = 'python://plantweb.directive.defaults_provider'
    if provider not in defaults.DEFAULTS_PROVIDERS:
        defaults.DEFAULTS_PROVIDERS.append(provider)


def setup(app):
    """
    Setup function that makes this module a Sphinx extension.

    See http://www.sphinx-doc.org/en/stable/extdev/appapi.html#sphinx.application.Sphinx.add_config_value
    """  # noqa
    # Wee want to override the directives:
    # - 'graph' from sphinx.ext.graphviz extension.
    # - 'uml' from sphinxcontrib.plantuml
    # But Sphinx warns of the override, causing failure is warnings are set
    # to fail documentation build. So, we go down and use docutils registering
    # directly instead.

    # app.add_directive('uml', UmlDirective)
    # app.add_directive('graph', GraphDirective)
    # app.add_directive('diagram', DiagramDirective)

    from docutils.parsers.rst import directives
    directives.register_directive('uml', UmlDirective)
    directives.register_directive('graph', GraphDirective)
    directives.register_directive('diagram', DiagramDirective)

    # Register the config value to allow to set plantweb defaults in conf.py
    app.add_config_value('plantweb_defaults', {}, 'env')

    # Register Plantweb defaults setter
    app.connect('builder-inited', builder_inited_handler)


__all__ = ['setup', 'builder_inited_handler', 'defaults_provider']
