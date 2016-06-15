.. toctree::
   :hidden:

================
Examples Gallery
================

This gallery shows many examples of figures that can be rendered using
Plantweb. All these examples were taken from the website of each project.

For the original source of this examples or for more information and examples
please visit the website of each project as shown in each section.

This section can be seen as a display of capabilities of the individual
projects, but it is mostly a medium to test Plantweb Sphinx_ directives.

.. _Sphinx: http://www.sphinx-doc.org/

.. contents::
   :local:


PlantUML
========

   PlantUML is a component that allows to quickly write many UML diagrams using
   a simple and intuitive language.

For more examples and information visit the official website:

   http://plantuml.com/


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

   Graphviz is open source graph visualization software. Graph visualization is
   a way of representing structural information as diagrams of abstract graphs
   and networks.

   It has important applications in networking, bioinformatics, software
   engineering, database and web design, machine learning, and in visual
   interfaces for other technical domains.

For more examples and information visit the official website:

    http://www.graphviz.org/Gallery.php


Cluster
-------

   This small example illustrates dot's feature to draw nodes and edges in
   clusters or separate rectangular layout regions. Clusters are encoded as
   subgraphs whose names have the prefix 'cluster'. The color attribute of a
   cluster is interpreted as its outline color or its background color if its
   style is 'filled'. Mdiamond and Msquare are modified symbols for data flow
   diagrams.

   - http://www.graphviz.org/content/cluster

.. graph::

   digraph G {

      subgraph cluster_0 {
         style=filled;
         color=lightgrey;
         node [style=filled,color=white];
         a0 -> a1 -> a2 -> a3;
         label = "process #1";
      }

      subgraph cluster_1 {
         node [style=filled];
         b0 -> b1 -> b2 -> b3;
         label = "process #2";
         color=blue
      }
      start -> a0;
      start -> b0;
      a1 -> b3;
      b2 -> a3;
      a3 -> a0;
      a3 -> end;
      b3 -> end;

      start [shape=Mdiamond];
      end [shape=Msquare];
   }


Data Structures
---------------

   The graph file was generated automatically from a session with the LDBX
   graphical interface to the standard DBX debugger.

   Nodes are drawn with the ``'record'`` shape. Labels of this shape are
   interpreted specially as nested horizontal and vertical box lists formatted
   as tables. In a record label, curly braces ``{ }`` enclose lists, vertical
   bar ``|`` separates list items, and creates a port identifier for attaching
   edges. Edges are also labeled with ``'id'`` attributes. Though not
   demonstrated in this particular file, these attributes allow referencing
   multiple (parallel) edges between the same node pair.

   - http://www.graphviz.org/content/datastruct

.. graph::

   digraph g {
      graph [
         rankdir = "LR"
      ];
      node [
         fontsize = "16"
         shape = "ellipse"
      ];
      edge [];
      "node0" [
         label = "<f0> 0x10ba8| <f1>"
         shape = "record"
      ];
      "node1" [
         label = "<f0> 0xf7fc4380| <f1> | <f2> |-1"
         shape = "record"
      ];
      "node2" [
         label = "<f0> 0xf7fc44b8| | |2"
         shape = "record"
      ];
      "node3" [
         label = "<f0> 3.43322790286038071e-06|44.79998779296875|0"
         shape = "record"
      ];
      "node4" [
         label = "<f0> 0xf7fc4380| <f1> | <f2> |2"
         shape = "record"
      ];
      "node5" [
         label = "<f0> (nil)| | |-1"
         shape = "record"
      ];
      "node6" [
         label = "<f0> 0xf7fc4380| <f1> | <f2> |1"
         shape = "record"
      ];
      "node7" [
         label = "<f0> 0xf7fc4380| <f1> | <f2> |2"
         shape = "record"
      ];
      "node8" [
         label = "<f0> (nil)| | |-1"
         shape = "record"
      ];
      "node9" [
         label = "<f0> (nil)| | |-1"
         shape = "record"
      ];
      "node10" [
         label = "<f0> (nil)| <f1> | <f2> |-1"
         shape = "record"
      ];
      "node11" [
         label = "<f0> (nil)| <f1> | <f2> |-1"
         shape = "record"
      ];
      "node12" [
         label = "<f0> 0xf7fc43e0| | |1"
         shape = "record"
      ];
      "node0":f0 -> "node1":f0 [id = 0];
      "node0":f1 -> "node2":f0 [id = 1];
      "node1":f0 -> "node3":f0 [id = 2];
      "node1":f1 -> "node4":f0 [id = 3];
      "node1":f2 -> "node5":f0 [id = 4];
      "node4":f0 -> "node3":f0 [id = 5];
      "node4":f1 -> "node6":f0 [id = 6];
      "node4":f2 -> "node10":f0 [id = 7];
      "node6":f0 -> "node3":f0 [id = 8];
      "node6":f1 -> "node7":f0 [id = 9];
      "node6":f2 -> "node9":f0 [id = 10];
      "node7":f0 -> "node3":f0 [id = 11];
      "node7":f1 -> "node1":f0 [id = 12];
      "node7":f2 -> "node8":f0 [id = 13];
      "node10":f1 -> "node11":f0 [id = 14];
      "node10":f2 -> "node12":f0 [id = 15];
      "node11":f2 -> "node1":f0 [id = 16];
   }


Finite Automaton
----------------

   This is a drawing of a finite automaton. The rankdir and orientation request
   a left-to-right drawing in landscape mode. Note the use of text labels on
   edges.

   - http://www.graphviz.org/content/fsm

.. graph::

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


Ditaa
=====

For more examples visit the official website:

    http://ditaa.sourceforge.net/

