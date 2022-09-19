.. webezyio documentation master file, created by
   sphinx-quickstart on Mon Sep 19 10:19:24 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to webezyio's documentation!
====================================

Overview
********
webezyio is free and open-source project that aims to be a complete framework for developing micro-services projects.
The underlying communication protocol is `HTTP2` and for serialization and deserialization is protobuf.
It utulize those communication protocol, message serialization / deserialization and code generator with `gRPC` opensource project by google. 

Get full explanation and many more details on usage at `webezy.io`_.

Installation
************

Download package from pip

.. code-block:: bash

    pip install webezyio

Download package from git

.. code-block:: bash

    pip install git+https://github.com/webezy-io/webezyio.git#egg=webezyio


Usage
******
Write webezy.io projects with Package API or with CLI.

====
CLI
====

Start a new project
-------------------
Start your webezyio project structure now and run this command:

.. code-block:: bash
    :caption: Replace content in <> with your cool project name

    wz new <project-name>

The `wz new` command will generate all your project directories and files under the current path.
If you want to start your project in other location run it with the `--path` argument

Add resources
-------------
Continue developing your project packages and services:

.. code-block:: bash

    wz generate --package

====
API
====

Init a Architect
----------------

Init a Builder
--------------


.. _webezy.io: https://www.webezy.io/


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
