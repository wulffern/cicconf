---
layout: page
title: clone
---

* TOC
{:toc }

## Command

```bash
cicconf clone --help
```

```bash
Usage: cicconf clone [OPTIONS]

  Clone repositories in config file

Options:
  --https                   Use https for clone (override for git@)
  --onclone / --no-onclone  Don't run on_clone event
  --jobs INTEGER            Number of repositories to process in parallel
  --help                    Show this message and exit.
```

## Description

`clone` reads the configured repositories and clones each missing dependency
into the current project directory. The command renders a rich summary table
and can process repositories in parallel.

If `revision` is configured, `cicconf` checks out that revision after cloning.

If `on_clone` is configured, it can also run a shell command inside the cloned
repository.

## Examples

Clone everything from `config.yaml`:

```bash
cicconf clone
```

Force `https://` URLs when the config uses `git@...` remotes:

```bash
cicconf clone --https
```

Clone with a larger worker pool:

```bash
cicconf clone --jobs 8
```

Skip post-clone hooks:

```bash
cicconf clone --no-onclone
```
