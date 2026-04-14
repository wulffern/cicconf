======================================
Custom IC Creator Configuration Tool
======================================

``cicconf`` is a small command-line tool for managing an IC project that is
assembled from multiple git repositories.

It is built for the workflow where:

- each IP lives in its own repository
- the top-level IC needs specific branches, tags, or commits of those IPs
- tool repositories should also be pinned with the design
- new IPs should be generated from a shared template

Why
===

An integrated circuit is usually made from multiple IP blocks maintained by
different designers. Each IP should keep its own version history, but the
top-level IC must still be able to lock each dependency to a known revision at
milestones such as tapeout.

``cicconf`` keeps that dependency list in a single ``config.yaml`` file and
provides commands to:

- clone all configured repositories
- report the current revision status of each dependency
- update or pull selected repositories
- create a new IP directory from a template

Install
=======

Latest development version:

.. code-block:: bash

   git clone https://github.com/wulffern/cicconf
   cd cicconf
   python3 -m pip install --user -e .

Published version:

.. code-block:: bash

   python3 -m pip install cicconf

Quick Start
===========

Create a ``config.yaml`` in the project directory:

.. code-block:: yaml

   options:
     template:
       ip: tech_sky130B/cicconf/ip_template.yaml
     project: rply
     technology: sky130nm

   cpdk:
     remote: git@github.com:wulffern/cpdk.git
     revision: main

   tech_sky130B:
     remote: git@github.com:wulffern/tech_sky130B.git
     revision: main

Then clone the configured repositories:

.. code-block:: bash

   cicconf clone

To inspect the current state of the working tree:

.. code-block:: bash

   cicconf status

Configuration File
==================

``cicconf`` reads a YAML configuration file. By default it looks for
``config.yaml``.

The ``options`` section is used by ``newip``:

.. code-block:: yaml

   options:
     template:
       ip: tech_sky130B/cicconf/ip_template.yaml
     project: rply
     technology: sky130nm

Repository entries follow this pattern:

.. code-block:: yaml

   <folder>:
     remote: <git url>
     revision: <git branch|tag|hash>
     on_clone: <optional shell command>

Fields:

- ``remote``: repository URL to clone
- ``revision``: branch, tag, or commit to check out after clone
- ``on_clone``: optional shell command run inside the cloned repository

Template-based IP creation uses ``options.template.ip``. A template file can
define:

- ``dirs``: directories to create
- ``copy``: files copied from a source IP when used
- ``create``: files written from inline text
- ``do``: shell commands executed after setup
- ``echo``: text printed during generation

Commands
========

Top-level help:

.. code-block:: bash

   cicconf --help

Current command set:

.. code-block:: text

   Usage: cicconf [OPTIONS] COMMAND [ARGS]...

   Options:
     --config TEXT             Configuration file
     --verbose / --no-verbose  Turn on extra output
     --rundir TEXT             Where to run cicconf
     --help                    Show this message and exit.

   Commands:
     clone   Clone repositories in config file
     newip   Create a new IP with name <project>_<name>_<technology> ...
     pull    Pull latest data
     status  Report the status of each of the configured IPs
     update  Update IPs to correct branch according to config file

Examples:

.. code-block:: bash

   cicconf clone
   cicconf clone --https
   cicconf clone --jobs 8
   cicconf status
   cicconf status --no-fast
   cicconf update --regex "tech_.*" --jobs 8
   cicconf pull --regex "cpdk|tech_.*" --jobs 8
   cicconf newip bias
   cicconf newip bias --project sun --technology sky130nm

Documentation
=============

Following the same documentation model as ``cicsim``, the repo now has focused
pages under ``docs/``:

- ``docs/index.md``: overview and install
- ``docs/config.md``: configuration file format
- ``docs/clone.md``: clone command
- ``docs/newip.md``: newip command and template behavior
- ``docs/status.md``: status output
- ``docs/update.md``: update command
- ``docs/pull.md``: pull command

The ``docs/`` directory is set up for Jekyll in the same style as ``cicsim``.
To serve it locally:

.. code-block:: bash

   cd docs
   bundle install
   bundle exec jekyll serve

Then open the local URL printed by Jekyll.

Notes
=====

- If you combine ``--rundir`` with ``--config``, prefer an absolute path for
  ``--config``.
- ``clone``, ``pull`` and ``update`` now use rich summary tables and can run
  repositories in parallel with ``--jobs``.
- ``status`` now renders a rich table. Fast mode is the default and skips
  ahead/behind counting for speed. Use ``cicconf status --no-fast`` for the
  fuller git summary.
- ``update`` checks out the configured revision before pulling.
