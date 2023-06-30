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
Sphinx directives for rendering PlantUML, Graphviz and Ditaa using Plantweb.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from logging import getLogger
from traceback import format_exc
from os import makedirs
from abc import ABCMeta, abstractmethod
from os.path import join, relpath, dirname, isfile, isabs, realpath

from six import add_metaclass
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Image

from . import defaults
from .render import render


log = getLogger(__name__)


@add_metaclass(ABCMeta)
class Plantweb(Image):
    """
    FIXME: Document.
    """

    required_arguments = 0
    optional_arguments = 1
    option_spec = {
        'alt': directives.unchanged,
        'align': lambda arg: directives.choice(
            arg, ('left', 'center', 'right')
        ),
        'target': directives.unchanged_required,
    }
    has_content = True

    def _directive_checks(self):

        # Check if file insertion is enabled
        if not self.state.document.settings.file_insertion_enabled:
            msg = (
                'File and URL access deactivated. '
                'Ignoring directive "{}".'.format(self._get_directive_name())
            )
            warning = nodes.warning(
                '', self.state_machine.reporter.warning(
                    '', nodes.literal_block('', msg),
                    line=self.lineno
                )
            )
            return [warning]

        # Check that no content and argument are used at the same time
        if self.arguments and self.content:
            warning = self.state_machine.reporter.warning(
                '{} directive cannot have both content and a filename '
                'argument.'.format(self._get_directive_name()),
                line=self.lineno
            )
            return [warning]

        # Check that at least one was provided
        if not (self.arguments or self.content):
            warning = self.state_machine.reporter.warning(
                '{} directive must have content or a filename '
                'argument.'.format(self._get_directive_name()),
                line=self.lineno
            )
            return [warning]

        return None

    def run(self):

        # Execute sanity checks
        warnings = self._directive_checks()
        if warnings:
            return warnings

        # Fetch builder and environment objects
        env = self.state_machine.document.settings.env
        builder = env.app.builder

        # Determine document directory
        document_dir = realpath(dirname(env.doc2path(env.docname)))

        # Load content to render
        if not self.arguments:
            content = '\n'.join(self.content)
        else:
            # Source file should be relative to document, or absolute to
            # configuration directory.
            srcfile = self.arguments[0]

            if isabs(srcfile):
                srcpath = join(env.app.confdir, relpath(srcfile, start='/'))
            else:
                srcpath = join(document_dir, srcfile)

            if not isfile(srcpath):
                warning = self.state_machine.reporter.warning(
                    '{} directive cannot find file {}'.format(
                        self._get_directive_name(),
                        srcfile
                    ),
                    line=self.lineno
                )
                return [warning]

            with open(srcpath, 'rb') as fd:
                content = fd.read().decode('utf-8')

        # Execute plantweb call
        try:
            output, frmt, engine, sha = render(
                content,
                engine=self._get_engine_name()
            )
        except Exception:
            msg = format_exc()
            error = nodes.error(
                '', self.state_machine.reporter.error(
                    '', nodes.literal_block('', msg),
                    line=self.lineno
                )
            )
            return [error]

        # Determine filename
        filename = '{}.{}'.format(sha, frmt)
        imgpath = join(builder.outdir, builder.imagedir, 'plantweb')

        # Create images output folder
        log.debug('imgpath set to {}'.format(imgpath))
        makedirs(imgpath, exist_ok=True)

        # Write content
        filepath = join(imgpath, filename)

        with open(filepath, 'wb') as fd:
            fd.write(output)

        log.debug('Wrote image file {}'.format(filepath))

        # Default to align center
        if 'align' not in self.options:
            self.options['align'] = 'center'

        # Determine relative path to image from source document directory
        filepath_relative = relpath(filepath, document_dir)

        # Windows compatibility:
        # Sphinx Image directive expects paths in POSIX, Python's form.
        # Replace backslash with slash, otherwise they are removed.
        filepath_relative = filepath_relative.replace('\\', '/')

        log.debug('Image relative path {}'.format(filepath_relative))

        # Run Image directive
        self.arguments = [filepath_relative]
        return Image.run(self)

    @abstractmethod
    def _get_engine_name(self):
        """
        Returns the name of the engine that should be used to render the
        content.
        """

    @abstractmethod
    def _get_directive_name(self):
        """
        The name of this directive.
        """


class UmlDirective(Plantweb):
    """
    Specialized ``uml`` directive for Plantweb ``Plantweb`` engine.

    See :class:`Plantweb`.
    """
    def _get_engine_name(self):
        return 'plantuml'

    def _get_directive_name(self):
        return 'uml'


class GraphDirective(Plantweb):
    """
    Specialized ``graph`` directive for Plantweb ``graphviz`` engine.

    See :class:`Plantweb`.
    """
    def _get_engine_name(self):
        return 'graphviz'

    def _get_directive_name(self):
        return 'graph'


class DiagramDirective(Plantweb):
    """
    Specialized ``diagram`` directive for Plantweb ``ditaa`` engine.

    See :class:`Plantweb`.
    """
    def _get_engine_name(self):
        return 'ditaa'

    def _get_directive_name(self):
        return 'diagram'


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

    # Force defaults reload
    from .defaults import read_defaults
    if hasattr(read_defaults, 'cache'):
        del read_defaults.cache


def setup(app):
    """
    Setup function that makes this module a Sphinx extension.

    See http://www.sphinx-doc.org/en/stable/extdev/appapi.html#sphinx.application.Sphinx.add_config_value
    """  # noqa
    # Wee want to override the directives:
    # - 'graph' from sphinx.ext.graphviz extension.
    # - 'uml' from sphinxcontrib.plantuml
    # But Sphinx warns of the override, causing failure if warnings are set
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
    # Note: The str() is because:
    #       - In Python 2.7, Sphinx expects a str, not unicode.
    #       - In Python 3.4, Sphinx expects a str, not bytes.
    app.connect(str('builder-inited'), builder_inited_handler)


__all__ = [
    'Plantweb', 'UmlDirective', 'GraphDirective', 'DiagramDirective',
    'setup', 'builder_inited_handler', 'defaults_provider'
]
