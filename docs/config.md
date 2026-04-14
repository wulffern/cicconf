---
layout: page
title: config
---

* TOC
{:toc }

## Description

`cicconf` uses a YAML file, by default `config.yaml`, to describe the project
dependencies and the defaults used by `newip`.

## Basic structure

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

## `options`

The `options` section is used by `cicconf newip`.

| Key | Meaning |
|:----|:--------|
| `project` | Prefix used when generating the new IP name |
| `technology` | Suffix used when generating the new IP name |
| `template.ip` | Path to the IP template YAML file |

The generated IP name is:

```text
<project>_<name>_<technology>
```

## Repository entries

Each top-level key other than `options` is interpreted as a repository folder.

```yaml
<folder>:
  remote: <git url>
  revision: <git branch|tag|hash>
  on_clone: <optional shell command>
```

| Key | Meaning |
|:----|:--------|
| `remote` | Repository URL |
| `revision` | Branch, tag, or commit to check out |
| `on_clone` | Optional shell command executed after clone |

## Path handling

`--config` selects the configuration file and `--rundir` selects where
`cicconf` runs its repo operations.

If you combine `--rundir` with `--config`, use an absolute path for
`--config`.
