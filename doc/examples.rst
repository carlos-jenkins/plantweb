.. toctree::
   :hidden:

================
Examples Gallery
================

.. contents::
   :local:


PlantUML
========

Sequence
--------

.. uml::

   Alice -> Bob: Authentication Request
   Bob --> Alice: Authentication Response

   Alice -> Bob: Another authentication Request
   Alice <-- Bob: another authentication Response

.. uml::

   actor Foo1
   boundary Foo2
   control Foo3
   entity Foo4
   database Foo5
   Foo1 -> Foo2 : To boundary
   Foo1 -> Foo3 : To control
   Foo1 -> Foo4 : To entity
   Foo1 -> Foo5 : To database

.. uml::

   autonumber 10 10 "<b>[000]"
   Bob -> Alice : Authentication Request
   Bob <- Alice : Authentication Response

   autonumber stop
   Bob -> Alice : dummy

   autonumber resume "<font color=red><b>Message 0  "
   Bob -> Alice : Yet another authentication Request
   Bob <- Alice : Yet another authentication Response

   autonumber stop
   Bob -> Alice : dummy

   autonumber resume 1 "<font color=blue><b>Message 0  "
   Bob -> Alice : Yet another authentication Request
   Bob <- Alice : Yet another authentication Response


Use Case
--------

Class
-----

Activity
--------

Component
---------

State
-----

Object
------

Graphviz
========

For more examples visit the official website:

    http://www.graphviz.org/Gallery.php


Ditaa
=====

For more examples visit the official website:

    http://ditaa.sourceforge.net/

