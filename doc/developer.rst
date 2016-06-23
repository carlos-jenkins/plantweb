.. toctree::

===============
Developer Guide
===============


Setup Development Environment
=============================

#. Install ``pip3`` and ``tox``:

   .. code-block:: sh

      wget https://bootstrap.pypa.io/get-pip.py
      sudo python3 get-pip.py
      sudo pip3 install tox

#. Configure git pre-commit hook:

   .. code-block:: sh

      sudo pip3 install flake8 pep8-naming
      flake8 --install-hook
      git config flake8.strict true


Building Documentation
======================

.. code-block:: sh

   tox -e doc

Output will be available at ``.tox/doc/tmp/html``. It is recommended to install
the ``webdev`` package:

.. code-block:: sh

   sudo pip3 install webdev

So a development web server can serve any location like this:

.. code-block:: sh

   $ webdev .tox/doc/tmp/html


Running Test Suite
==================

.. code-block:: sh

   tox -e py27,py34


Running Coverage
================

.. code-block:: sh

   tox -e coverage
