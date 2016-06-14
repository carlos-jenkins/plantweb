.. toctree::
   :hidden:
   :maxdepth: 1

   developer
   plantweb/plantweb

========
Plantweb
========

.. container:: float-right

   .. image:: _static/images/logo.png

Plantweb is a project that provides a command line interface, Sphinx directives
and an API that allows to render powerful plain text UML diagrams, ASCII
diagrams and complex graphs.

It is a Python client for the PlantUML_ server and thus it can render
PlantUML_, Graphviz_ and Ditaa_ diagrams without the need to install them.

Plantweb features a local cache that prevents requesting the server for
previously rendered diagrams, speeding up building documentation with lots of
diagrams.

Finally, being pure Python, non-local rendering, Plantweb is an excellent way
to display and render PlantUML_, Graphviz_ and Ditaa_ diagrams in ReadTheDocs_
published documentation.

.. _PlantUML: http://plantuml.com/
.. _Graphviz: http://www.graphviz.org/
.. _Ditaa: http://ditaa.sourceforge.net/
.. _ReadTheDocs: http://readthedocs.org/

.. contents::
   :local:


Installation
============

    sudo pip3 install plantweb


Usage
=====

Command Line Interface
----------------------

If the content of your file is wrapped by ``@startxxx``, ``@endxxx`` then
Plantweb is capable of determining the engine to use.

Options are:

===============  =============  ========
    Opening         Closure      Engine
===============  =============  ========
``@startuml``    ``@enduml``    plantuml
``@startdot``    ``@enddot``    graphviz
``@startditaa``  ``@endditaa``  ditaa
===============  =============  ========

For example, the following Graphviz file ``mydotfile.dot``:

::

   @startdot
   digraph one_node_graph {
      node1 -> node2 -> node3
   }
   @enddot

Can be rendered with:

::

   user@host:~$ plantweb mydotfile.dot

.. note::

   File extensions are irrelevant for Plantweb.

If for some reason your files lack the ``@startxxx/@endxxx`` wrapper you can
still render the file by specifying the engine:

::

   user@host:~$ plantweb --engine=graphviz unwrappeddotfile.dot

Complete options:

::

   user@host:~$ plantweb --help
   usage: plantweb [-h] [-v] [--version]
                   [--engine {auto,plantuml,graphviz,ditaa}]
                   [--format {auto,svg,png}] [--server SERVER] [--no-cache]
                   [--cache-dir CACHE_DIR]
                   sources [sources ...]

   Python client for the PlantUML server

   positional arguments:
     sources               source files to render

   optional arguments:
     -h, --help            show this help message and exit
     -v, --verbose         increase verbosity level
     --version             show program's version number and exit
     --engine {auto,plantuml,graphviz,ditaa}
                           engine to use to render diagram
     --format {auto,svg,png}
                           diagram export format
     --server SERVER       server to use for rendering
     --no-cache            do not use cache
     --cache-dir CACHE_DIR
                           directory to store cached renders


Sphinx Directives
-----------------

TODO


Python API
----------

.. currentmodule:: plantweb.render

There are 2 main functions, both Python 2.7 and 3.4 compatible:

#. :func:`render` allows to render content directly.

   .. code-block:: python

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

#. :func:`render_file` allows to render files.

   .. code-block:: python

      from plantweb.render import render_file


      CONTENT = """
      digraph finite_state_machine {
          rankdir=LR;
          size="8,5"
          node [shape = doublecircle]; LR_0 LR_3 LR_4 LR_8;
          node [shape = circle];
          LR_0 -> LR_2 [ label = "SS(B)" ];
          LR_0 -> LR_1 [ label = "SS(S)" ];
          LR_1 -> LR_3 [ label = "S($end)" ];
          LR_2 -> LR_6 [ label = "SS(b)" ];
          LR_2 -> LR_5 [ label = "SS(a)" ];
          LR_2 -> LR_4 [ label = "S(A)" ];
          LR_5 -> LR_7 [ label = "S(b)" ];
          LR_5 -> LR_5 [ label = "S(a)" ];
          LR_6 -> LR_6 [ label = "S(b)" ];
          LR_6 -> LR_5 [ label = "S(a)" ];
          LR_7 -> LR_8 [ label = "S(b)" ];
          LR_7 -> LR_5 [ label = "S(a)" ];
          LR_8 -> LR_6 [ label = "S(b)" ];
          LR_8 -> LR_5 [ label = "S(a)" ];
      }
      """


      if __name__ == '__main__':

          infile = 'mygraph.dot'
          with open(infile, 'wb') as fd:
              fd.write(CONTENT.encode('utf-8'))

          print('==> INPUT FILE:')
          print(infile)

          outfile = render_file(
              infile,
              renderopts={
                  'engine': 'graphviz',
                  'format': 'png'
              },
              cacheopts={
                  'use_cache': False
              }
          )

          print('==> OUTPUT FILE:')
          print(outfile)


Overriding Defaults
===================

.. currentmodule:: plantweb.defaults

.. versionadded:: 0.3.0

The defaults defined in :data:`DEFAULT_CONFIG` will be used unless overridden
by the user.

To set a different default configuration create a JSON file ``.plantwebrc``
in your git repository root or in your home, as defined in
:data:`DEFAULTS_PROVIDERS`.

For example:

.. code-block:: json

   {
       "server": "http://mydomain.com/plantuml/"
   }

.. seealso::

   :ref:`server`.


.. _server:

PlantUML Server
===============

If you require:

- Guaranteed uptime.
- To render confidential diagrams.
- To speed up rendering in your intranet.
- Or you simply want to be nice and unload the public server.

Please consider installing a PlantUML server in your local network or private
server:

    http://plantuml.com/server.html

The `public PlantUML server <http://plantuml.com/plantuml/>`_ is run by a group
of volunteers for pure love.

Please consider `donating <http://plantuml.com/>`_ to the project through
Paypal, Patreon or Flattr.


Development
===========

- :doc:`Developer Guide. <developer>`
- :doc:`Internal Documentation Reference. <plantweb/plantweb>`
- `Project repository. <https://github.com/carlos-jenkins/plantweb>`_


TODO
====

- Given the fact that we can render Graphviz we could monkey patch the
  ``sphinx.ext.graphviz`` to call Plantweb API instead of executing ``dot``.
  Same for ``sphinx.ext.inheritance_diagram`` that also uses Graphviz.


License
=======

::

   Copyright (C) 2016 Carlos Jenkins

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.

Logo derived from work by VisciousSpeed_ under Public Domain.

.. _VisciousSpeed: https://openclipart.org/detail/126331/plant-and-vase-planter
