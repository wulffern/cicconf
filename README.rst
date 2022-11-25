======================================
Custom IC Creator Configuration tool
======================================


An integrated circuit (IC) will be a combination of multiple IPs. Each IP usually have
different analog designer, but often the IPs depend on each other.

For each IP one must have version control, and revision control (tags), which is handled nicely by git as
long as the files are not too large (or binary)

For the IC, though, one must have the ability to use a specific revision (tag) of an IP, but
allow the IP development to continue. As such, it's not feasible to have
everything in one repo.

In addition to IPs, it's common to have a toolset of
scripts, and those also need to be in the correct revision. In the beginning of
a development the tools and IPs might be to a *main* branch, but at tapeout,
it's important to lock the revision, so it's easy to go back to a old IC and run
new simulations.

I needed a configuration tool, one that can pick the IPs, and get the right
versions from git repositories.

*Disclamer: I have not spent much time searching whether there is a tool that
fits my purpose, but cicconf was quick to write, and I get something that matches
exactly what I want. One alternative is git submodules, but I find that more of a hassle.*


Getting Started
===============

Clone the repository, and do

.. code-block:: bash

   cd cicconf
   python3 -m pip install --user -e .


Idea
====

cicconf will search the current directory for a *ciconf.yaml* file. An example
cicconf.yaml

.. code-block:: yaml

   options:
    template:
        ip: tech_sky130B/cicconf/ip_template.yaml
    project: rply
    technology: sky130nm
  cpdk:
    remote: git@github.com:wulffern/cpdk.git
    revision: main
  tech_sky130A:
    remote: git@github.com:wulffern/tech_sky130A.git
    revision: main
  tech_sky130B:
    remote: git@github.com:wulffern/tech_sky130B.git
    revision: main


The option section has some custom fields to tell cicconf how new IPs should be
named. The ip_template contains the instructions for creating an IP, for example
`ip_template.yaml <https://github.com/wulffern/tech_sky130B/blob/main/cicconf/ip_template.yaml>`_

The rest follows a simple pattern

.. code-block:: yaml

   <folder>:
    remote: <git url>
    revision: <git branch|tag|hash>


Running
=======

Construct a cicconf.yaml of your desire (see
`config.yaml <https://github.com/wulffern/aicex/blob/main/ip/config.yaml>`_ for a
more extensive example). Then run

.. code-block:: bash

  cicconf clone



Usage
=====

For latest command, check `cicconf --help`

.. code-block::

   Usage: cicconf [OPTIONS] COMMAND [ARGS]...

   Options:
    --help  Show this message and exit.

   Commands:
    clone   Clone repositories in config file
    newip   Create a new IP with name <project>_<name>_<technology> The...
    status  Report the status of each of the configured IPs
    update  Update all ips to correct branch according to config file
