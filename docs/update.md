---
layout: page
title: update
---

* TOC
{:toc }

## Command

```bash
cicconf update --help
```

```bash
Usage: cicconf update [OPTIONS]

  Update IPs to correct branch according to config file

Options:
  --regex TEXT    Regex pattern for folders to update
  --jobs INTEGER  Number of repositories to process in parallel
  --help          Show this message and exit.
```

## Description

`update` iterates over the configured repositories, filters them by regex, runs
`git fetch`, checks out the configured `revision`, and then runs
`git pull --ff-only`.

If a configured repository has not been cloned yet, `update` will attempt to
clone it first. The command renders a rich summary table and can process
repositories in parallel.

## Examples

Update all repositories:

```bash
cicconf update
```

Update only technology repositories:

```bash
cicconf update --regex "tech_.*"
```

Update a specific dependency:

```bash
cicconf update --regex "^cpdk$"
```

Update multiple repositories in parallel:

```bash
cicconf update --regex "tech_.*" --jobs 8
```
