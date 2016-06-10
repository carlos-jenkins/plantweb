=========================
PlantUML Client in Python
=========================

Python client for the PlantUML server.

A command line interface is provided that allows to render PlantUML, Graphviz
and Ditaa diagrams without the need to install them.

A Python 2.7 and 3.4 API (``render`` and ``render_file``) and a Sphinx
directive ``uml ::`` is also provided.

Plantweb features a local cache that allows to avoid requesting the server for
already rendered diagrams, speeding up CI of documentation with lots of
diagrams.

Finally, being pure Python, non-local rendering, Plantweb is the only way to
display and render PlantUML, Graphviz and Ditaa diagrams in ReadTheDocs
published documentation.


Documentation
=============

    https://plantweb.readthedocs.org/


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
