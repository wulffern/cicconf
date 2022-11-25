======================================
Custom IC Creator Configuration tool
======================================

When you make an IC it will be a combination of multiple IPs. Each IP usually have
different analog designer, but often the IPs depend on each other.

For each IP one must have version control, which is handled nicely by git as
long as the files are not too large (or binary)

For the IC, though, one must have the ability to lock the version of an IP, but
allow the IP development to continue. As such, it's not feasible to have
everything in one repo. 

We need a configuration tool, one that can pick the IPs, and get the right
versions from git. 


*Disclamer:* I have not spent much time searching whether there is a tool that
fits my purpose, but it was quick to write, so I get something that matches
exactly what I want


Getting Started
===============

Clone the repository, and do
::
   cd cicconf
   python3 -m pip install --user -e .

Idea
=====

cicconf will search the current directory for a `ciconf.yaml` file. An example

cicconf.yaml::
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
named. The ip_template contains the instructions for creating an IP, for example see
[ip_template.yaml](https://github.com/wulffern/tech_sky130B/blob/main/cicconf/ip_template.yaml)

The rest follows a simple pattern
::
   <folder>:
    remote: <git url>
    revision: <git branch|tag|hash>

Running
=======
Construct a cicconf.yaml of your desire (see
[config.yaml](https://github.com/wulffern/aicex/blob/main/ip/config.yaml) for a
more extensive example)

Then run::
  cicconf clone


Usage
=====
For latest command, check `cicconf --help`

::
   Usage: cicconf [OPTIONS] COMMAND [ARGS]...

   Options:
    --help  Show this message and exit.

   Commands:
    clone   Clone repositories in config file
    newip   Create a new IP with name <project>_<name>_<technology> The...
    status  Report the status of each of the configured IPs
    update  Update all ips to correct branch according to config file
