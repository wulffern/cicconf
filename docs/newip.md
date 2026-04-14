---
layout: page
title: newip
---

* TOC
{:toc }

## Command

```bash
cicconf newip --help
```

```bash
Usage: cicconf newip [OPTIONS] NAME

  Create a new IP with name <project>_<name>_<technology> The <project> and
  <technology> is fetched from the config file.

  The name should be short and must be unique (for example, bias, aic01 or
  similar).

Options:
  --project TEXT     Override project name in config file
  --technology TEXT  Override technology name in config file
  --ip TEXT          Override ip template name in config file
  --help             Show this message and exit.
```

## Description

`newip` creates a new IP directory from a template YAML file.

It uses the `options` section in `config.yaml`:

```yaml
options:
  template:
    ip: tech_sky130B/cicconf/ip_template.yaml
  project: rply
  technology: sky130nm
```

The generated IP name is:

```text
<project>_<name>_<technology>
```

The template runner converts that to uppercase for variable substitution and
creates the output directory in lowercase.

## Template format

The IP template file can contain:

```yaml
dirs:
  - work
  - sim

copy:
  - Makefile

create:
  README.md: |
    # ${IP}

do:
  - git init

echo: "Created ${IP}"
```

| Section | Meaning |
|:--------|:--------|
| `dirs` | List of directories to create |
| `copy` | Files to copy from a source IP if used |
| `create` | Files created from inline content |
| `do` | Shell commands to run after creation |
| `echo` | Text to print |

## Variable substitution

Before parsing the template YAML, `cicconf` replaces:

1. `${CELL}` and `${cell}`
2. `${IP}` and `${ip}`
3. matching environment variables such as `${USER}`

## Examples

Create a new IP using config defaults:

```bash
cicconf newip bias
```

Override project and technology:

```bash
cicconf newip bias --project sun --technology sky130nm
```

Override the template file:

```bash
cicconf newip bias --ip tech_sky130B/cicconf/ip_template.yaml
```
