========
Plantweb
========

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


Documentation
=============

    https://plantweb.readthedocs.io/


Changelog
=========

1.3.0 (Sep 17, 2024)
--------------------

**Fixes**

- Fix #25 removes dependency on deprecated module distutils.

1.2.1 (Sep 18, 2019)
--------------------

**Fixes**

- Fix #15 so that directive works on Windows.
- Fix #16 so that the executable is available on Windows.

1.2.0 (Sep 18, 2019)
--------------------

.. warning::

   Bad release. Do not use it. Ups.

1.1.0 (Jul 11, 2017)
--------------------

**New**

- Added documentation on how to run a PlantUML docker container to simplify
  deployment.

**Fixes**

- Fix #9 passing source files to the Sphinx directive as an absolute path.
- Fix #7 source files passed as argument to the Sphinx directive failed to
  render correctly.
- Fixed test suite to be compatible with newer versions of Sphinx.
- Fixed several PEP8 violations.

**Changes**

- Improved algorithm to gather configuration for a git repository root.
- Test suite now test Python 3 with Python 3.5 instead of Python 3.4.

1.0.1 (Mar 20, 2017)
--------------------

**Fixes**

- Fix #1 that caused diagrams rendering to fail with a 404 in Windows OSes.

1.0.0 (Jun 27, 2016)
--------------------

**New**

- Sphinx directives now support passing a source file as argument.

0.4.0 (Jun 23, 2016)
--------------------

**New**

- Added a set of Sphinx directives ``uml``, ``graph`` and ``diagram``.

0.3.0 (Jun 22, 2016)
--------------------

**New**

- Default options can now be overriden with a ``.plantwebrc`` file in the user
  home or in the git repository root.

0.2.0 (Jun 22, 2016)
--------------------

**Fixes**

- Fixed bug when calling ``render_cache`` that returned a non-tuple.

**Changes**

- Documentation was greatly improved.

0.1.0 (Jun 9, 2016)
-------------------

**New**

- Initial public release.


License
=======

::

   Copyright (C) 2016-2017 Carlos Jenkins

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
