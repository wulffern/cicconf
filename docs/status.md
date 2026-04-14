---
layout: page
title: status
---

* TOC
{:toc }

## Command

```bash
cicconf status --help
```

```bash
Usage: cicconf status [OPTIONS]

  Report the status of each of the configured IPs

Options:
  --fast / --no-fast  Skip ahead/behind commit counting for faster status
  --help  Show this message and exit.
```

## Description

`status` prints a rich table with one row per configured repository.

The output includes:

- the configured repository name
- the configured revision
- a status string with branch mismatch, ahead/behind count, and modified files

By default, `status` runs in fast mode. In fast mode it skips ahead/behind
counting and untracked-file counting to reduce git work on large dependency
trees.

Use full mode when you want the more detailed summary:

```bash
cicconf status --no-fast
```

In full mode the legend is:

- `O = Commits behind/ahead branch`
- `M = Modified files`
- `U = Untracked files`

Detailed file paths are still only listed when `--verbose` is enabled on the
top-level command.

## Example

```bash
cicconf --verbose status
```

Typical workflow:

```bash
cicconf status
cicconf update --regex "tech_.*"
cicconf status
```
