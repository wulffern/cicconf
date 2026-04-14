---
layout: page
title: pull
---

* TOC
{:toc }

## Command

```bash
cicconf pull --help
```

```bash
Usage: cicconf pull [OPTIONS]

  Pull latest data

Options:
  --regex TEXT    Regex pattern for folders to update
  --jobs INTEGER  Number of repositories to process in parallel
  --help          Show this message and exit.
```

## Description

`pull` runs `git pull --ff-only` for repositories selected by regex.

Unlike `update`, it does not first check out the configured revision. Use it
when you want to pull the current branch of selected dependencies.

If a configured repository has not been cloned yet, `pull` will attempt to
clone it first. The command renders a rich summary table and can process
repositories in parallel.

## Examples

Pull all repositories:

```bash
cicconf pull
```

Pull only selected repositories:

```bash
cicconf pull --regex "cpdk|tech_.*"
```

Pull in parallel:

```bash
cicconf pull --regex "cpdk|tech_.*" --jobs 8
```
