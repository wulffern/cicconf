---
layout: home
---

[https://github.com/wulffern/cicconf](https://github.com/wulffern/cicconf)

`cicconf` is a small helper tool for IC projects built from many git
repositories.

It keeps the project dependency list in a single `config.yaml` file and helps
you clone, inspect, update, and template new IP blocks.

## Commands

```bash
cicconf --help
```

```bash
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
```

## Install stable version

```bash
python3 -m pip install cicconf
```

## Install latest development version

```bash
git clone https://github.com/wulffern/cicconf
cd cicconf
python3 -m pip install --user -e .
```

## Get started

Create a `config.yaml`:

```yaml
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
```

Clone the dependencies:

```bash
cicconf clone
```

Inspect status:

```bash
cicconf status
cicconf status --no-fast
```

Create a new IP from the configured template:

```bash
cicconf newip bias
```

## Documentation

- [Configuration file](config)
- [clone](clone)
- [newip](newip)
- [status](status)
- [update](update)
- [pull](pull)
