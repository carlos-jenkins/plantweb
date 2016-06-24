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

- http://plantuml.com/

.. contents::
   :local:

Sequence
--------

   A Sequence diagram is an interaction diagram that shows how objects operate
   with one another and in what order.

   - *Wikipedia, "Sequence Diagram".*

For detailed explanation see:

- http://plantuml.com/sequence.html


.. uml::

   Alice -> Bob: Authentication Request
   Bob --> Alice: Authentication Response

   Alice -> Bob: Another authentication Request
   Alice <-- Bob: another authentication Response

-------------------------

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

-------------------------

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

   A use case diagram at its simplest is a representation of a user's
   interaction with the system that shows the relationship between the user and
   the different use cases in which the user is involved.

   - *Wikipedia, "Use Case Diagram".*

For detailed explanation see:

- http://plantuml.com/usecase.html


.. uml::

   :Main Admin: as Admin
   (Use the application) as (Use)

   User <|-- Admin
   (Start) <|-- (Use)

-------------------------

.. uml::

   left to right direction
   skinparam packageStyle rect
   actor customer
   actor clerk
   rectangle checkout {
     customer -- (checkout)
     (checkout) .> (payment) : include
     (help) .> (checkout) : extends
     (checkout) -- clerk
   }


Class
-----

   A class diagram is a type of static structure diagram that describes the
   structure of a system by showing the system's classes, their attributes,
   operations (or methods), and the relationships among objects.

   - *Wikipedia, "Use Class Diagram".*

For detailed explanation see:

- http://plantuml.com/classes.html


.. uml::

   class Foo1 {
     You can use
     several lines
     ..
     as you want
     and group
     ==
     things together.
     __
     You can have as many groups
     as you want
     --
     End of class
   }

   class User {
     .. Simple Getter ..
     + getName()
     + getAddress()
     .. Some setter ..
     + setName()
     __ private data __
     int age
     -- encrypted --
     String password
   }

-------------------------

.. uml::

   package "Classic Collections" #DDDDDD {
     Object <|-- ArrayList
   }

   package net.sourceforge.plantuml {
     Object <|-- Demo1
     Demo1 *- Demo2
   }

   package foo6 <<Database>> {
     class Class6
   }


Activity
--------

   Activity diagrams are graphical representations of workflows of stepwise
   activities and actions with support for choice, iteration and concurrency. In
   the Unified Modeling Language, activity diagrams are intended to model both
   computational and organizational processes (i.e. workflows). Activity
   diagrams show the overall flow of control.

   - *Wikipedia, "Use Activity Diagram".*

For detailed explanation see:

- http://plantuml.com/activity2.html


.. uml::

   start
   :Hello world;
   :This is on defined on
   several **lines**;
   stop

-------------------------

.. uml::

   start
   if (condition A) then (yes)
     :Text 1;
   elseif (condition B) then (yes)
     :Text 2;
     stop
   elseif (condition C) then (yes)
     :Text 3;
   elseif (condition D) then (yes)
     :Text 4;
   else (nothing)
     :Text else;
   endif

-------------------------

.. uml::

   start

   if (multiprocessor?) then (yes)
     fork
       :Treatment 1;
     fork again
       :Treatment 2;
     end fork
   else (monoproc)
      partition Partition {
         :Process 1;
         :Process 2;
      }
     :Treatment 1;
     :Treatment 2;
   endif


Component
---------

   A component diagram depicts how components are wired together to form larger
   components and or software systems. They are used to illustrate the
   structure of arbitrarily complex systems.

   - *Wikipedia, "Component Diagram".*

For detailed explanation see:

- http://plantuml.com/component.html


.. uml::

   DataAccess - [First Component]
   [First Component] ..> HTTP : use

-------------------------

.. uml::

   package "Some Group" {
     HTTP - [First Component]
     [Another Component]
   }

   node "Other Groups" {
     FTP - [Second Component]
     [First Component] --> FTP
   }

   cloud {
     [Example 1]
   }


   database "MySql" {
     folder "This is my folder" {
       [Folder 3]
     }
     frame "Foo" {
       [Frame 4]
     }
   }


   [Another Component] --> [Example 1]
   [Example 1] --> [Folder 3]
   [Folder 3] --> [Frame 4]


State
-----

   A state diagram, also called a state machine diagram or statechart diagram,
   is an illustration of the states an object can attain as well as the
   transitions between those states.

   - *TechTarget, "State Diagram".*

For detailed explanation see:

- http://plantuml.com/state.html


.. uml::

   [*] --> State1
   State1 --> [*]
   State1 : this is a string
   State1 : this is another string

   State1 -> State2
   State2 --> [*]

-------------------------

.. uml::

   scale 350 width
   [*] --> NotShooting

   state NotShooting {
     [*] --> Idle
     Idle --> Configuring : EvConfig
     Configuring --> Idle : EvConfig
   }

   state Configuring {
     [*] --> NewValueSelection
     NewValueSelection --> NewValuePreview : EvNewValue
     NewValuePreview --> NewValueSelection : EvNewValueRejected
     NewValuePreview --> NewValueSelection : EvNewValueSaved

     state NewValuePreview {
        State1 -> State2
     }

   }


Object
------

   An object diagram is a graph of instances, including objects and data
   values. A static object diagram is an instance of a class diagram; it shows
   a snapshot of the detailed state of a system at a point in time. The use of
   object diagrams is fairly limited, namely to show examples of data
   structure.

   - *Object Management Group (2001), "UML specification 1.4".*

.. uml::

   object Object01
   Object01 : name = "Dummy"
   Object01 : id = 123

   object Object02
   object Object03
   object Object04
   object Object05
   object Object06
   object Object07
   object Object08

   Object01 <|-- Object02
   Object03 *-- Object04
   Object05 o-- "4" Object06
   Object07 .. Object08 : some labels


Graphviz
========

   Graphviz is open source graph visualization software. Graph visualization is
   a way of representing structural information as diagrams of abstract graphs
   and networks.

   It has important applications in networking, bioinformatics, software
   engineering, database and web design, machine learning, and in visual
   interfaces for other technical domains.

For more examples and information visit the official website:

- http://www.graphviz.org/Gallery.php

.. contents::
   :local:


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

- http://ditaa.sourceforge.net/

Ditaa rendering is particularly usefull when using ASCII drawing tools like:

- http://asciiflow.com/


.. diagram::

   +--------+   +-------+    +-------+
   |        +---+ ditaa +--> |       |
   |  Text  |   +-------+    |diagram|
   |Document|   |!magic!|    |       |
   |     {d}|   |       |    |       |
   +---+----+   +-------+    +-------+
       :                         ^
       |       Lots of work      |
       +-------------------------+

-------------------------

.. diagram::

   /--------\   +-------+
   |cAAA    +---+Version|
   |  Data  |   |   V3  |
   |  Base  |   |cRED{d}|
   |     {s}|   +-------+
   \---+----/

-------------------------

.. diagram::

   +---+-----+   +----------+
   | cBLU    |   | {io}     |
   | Ext-Foo |   |  S-ATA   |
   |   +-----+   |   cFEA   |
   |   |cPNK |   +----------+
   |   | Foo |
   +---+-----+

-------------------------

.. diagram::

   /-------------+-------------\
   |cRED RED     |cBLU BLU     |
   +-------------+-------------+
   |cGRE GRE     |cPNK PNK     |
   +-------------+-------------+
   |cAAA               AAA     |
   +-------------+-------------+
   |cCCC               CCC     |
   +-------------+-------------+
   |cBLK BLK     |cYEL YEL     |
   \-------------+-------------/

-------------------------

.. diagram::

   +---------------+                       +----------+
   | This was      |                       | And it is|
   | created with  +-----------+---------->+ great!   |
   | asciiflow.com |           |           |          |
   +---------------+           |           +----------+
                               |
                               |
       +-----------+           |
       |           |           |
       | Awesome!  +<----------+
       |           |
       +-----------+
