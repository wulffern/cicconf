#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
import git
import cicconf
import os
import yaml
import re

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table


@dataclass
class RepoStatus:
    name: str
    revision: str = ""
    current: str = ""
    status: str = ""
    state: str = "ok"
    details: list = field(default_factory=list)


@dataclass
class RepoAction:
    name: str
    revision: str = ""
    result: str = ""
    detail: str = ""
    state: str = "ok"


class Repo(cicconf.Command):

    def __init__(self,name,obj,verbose=False):
        super().__init__(verbose)
        self.name = name
        self.remote = None
        self.revision = None
        self.on_clone = None

        if("revision" in obj):
            self.revision = obj["revision"]

        if("remote" in obj):
            self.remote = obj["remote"]

        if("on_clone" in obj):
            self.on_clone = obj["on_clone"]

    def exists(self):
        if(os.path.exists(self.name)):
            return True
        return False

    def _open_repo(self):
        return git.Repo(self.name)

    def clone_action(self,useHttp=False,doOnClone=True):
        row = RepoAction(name=self.name,revision=self.revision or "")

        if(self.exists()):
            row.result = "skipped"
            row.detail = "already exists"
            row.state = "warning"
            return row

        if(not self.remote):
            row.result = "failed"
            row.detail = "no remote configured"
            row.state = "error"
            return row

        src = self.remote
        if(useHttp and "git@" in src):
            src = src.replace(":","/")
            src = src.replace("git@","https://")

        try:
            repo = git.Repo.clone_from(src, self.name)
            if(self.revision):
                repo.git.checkout(self.revision)
            if(self.on_clone and doOnClone):
                self.doCmd(f"cd {self.name};{self.on_clone}")
            row.result = "cloned"
            row.detail = src
        except Exception as e:
            row.result = "failed"
            row.detail = str(e)
            row.state = "error"

        return row

    def _parse_status_porcelain(self, text):
        info = {
            "head": "",
            "upstream": "",
            "ahead": 0,
            "behind": 0,
            "modified": 0,
            "untracked": [],
            "changes": [],
        }

        for line in text.splitlines():
            if(line.startswith("# branch.head ")):
                info["head"] = line.removeprefix("# branch.head ").strip()
            elif(line.startswith("# branch.upstream ")):
                info["upstream"] = line.removeprefix("# branch.upstream ").strip()
            elif(line.startswith("# branch.ab ")):
                m = re.search(r"\+(\d+) -(\d+)",line)
                if(m):
                    info["ahead"] = int(m.group(1))
                    info["behind"] = int(m.group(2))
            elif(line.startswith("? ")):
                path = line[2:].strip()
                info["untracked"].append(path)
            elif(line.startswith("1 ") or line.startswith("2 ") or line.startswith("u ")):
                info["modified"] += 1
                parts = line.split()
                if(parts):
                    path = parts[-1]
                    info["changes"].append(path)
        return info

    def collect_status(self,fast=True):
        row = RepoStatus(name=self.name,revision=self.revision or "")

        if(not self.exists()):
            row.state = "uncloned"
            row.status = "uncloned"
            return row

        try:
            repo = self._open_repo()
        except Exception:
            row.state = "error"
            row.status = "invalid git repo"
            return row

        try:
            args = ["--porcelain=2", "--branch"]
            if(fast):
                args.append("--untracked-files=no")
            text = repo.git.status(*args)
        except Exception as e:
            row.state = "error"
            row.status = str(e)
            return row

        info = self._parse_status_porcelain(text)

        branch = info["head"]
        if(branch == "(detached)"):
            try:
                sha = repo.head.commit.hexsha
                branch = "unknown"
                for t in repo.tags:
                    if(t.object.hexsha == sha):
                        branch = t.name
                        break
            except Exception:
                branch = "unknown"

        row.current = branch

        status = []
        if(self.revision and branch != self.revision):
            status.append(f"rev:{branch}")

        if(not fast):
            if(info["behind"] > 0):
                status.append(f"O-{info['behind']}")
            if(info["ahead"] > 0):
                status.append(f"O+{info['ahead']}")

        if(info["modified"] > 0):
            status.append(f"M+{info['modified']}")

        if(not fast and len(info["untracked"]) > 0):
            status.append(f"U+{len(info['untracked'])}")

        row.status = " ".join(status)
        if(row.status == ""):
            row.status = "clean"

        if(self.verbose):
            row.details.extend([self.name + "/" + p + " M" for p in info["changes"]])
            row.details.extend([self.name + "/" + p + " ?" for p in info["untracked"]])

        if(row.status != "clean"):
            row.state = "warning"

        return row

    def update_action(self):
        row = RepoAction(name=self.name,revision=self.revision or "")

        if(not self.exists()):
            return self.clone_action()

        try:
            repo = self._open_repo()
        except Exception as e:
            row.result = "failed"
            row.detail = str(e)
            row.state = "error"
            return row

        try:
            before = repo.head.commit.hexsha
            repo.git.fetch("--prune", "--quiet")
            if(self.revision):
                repo.git.checkout(self.revision)
            if(repo.head.is_detached):
                row.result = "skipped"
                row.detail = f"detached at {self.revision or repo.head.commit.hexsha[:8]}"
                row.state = "warning"
                return row

            tracking = repo.active_branch.tracking_branch()
            if(tracking is None):
                row.result = "skipped"
                row.detail = "no upstream"
                row.state = "warning"
                return row

            repo.git.fetch(tracking.remote_name, tracking.remote_head, "--quiet")
            repo.git.merge("--ff-only", tracking.name)
            after = repo.head.commit.hexsha
            if(before == after):
                row.result = "up-to-date"
                row.detail = str(repo.active_branch)
            else:
                row.result = "updated"
                row.detail = f"{before[:8]} -> {after[:8]}"
        except Exception as e:
            row.result = "failed"
            row.detail = str(e)
            row.state = "error"

        return row

    def pull_action(self):
        row = RepoAction(name=self.name,revision=self.revision or "")

        if(not self.exists()):
            return self.clone_action()

        try:
            repo = self._open_repo()
        except Exception as e:
            row.result = "failed"
            row.detail = str(e)
            row.state = "error"
            return row

        try:
            if(repo.head.is_detached):
                row.result = "skipped"
                row.detail = "detached HEAD"
                row.state = "warning"
                return row

            tracking = repo.active_branch.tracking_branch()
            if(tracking is None):
                row.result = "skipped"
                row.detail = "no upstream"
                row.state = "warning"
                return row

            before = repo.head.commit.hexsha
            repo.git.fetch(tracking.remote_name, tracking.remote_head, "--quiet")
            repo.git.merge("--ff-only", tracking.name)
            after = repo.head.commit.hexsha
            if(before == after):
                row.result = "up-to-date"
                row.detail = str(repo.active_branch)
            else:
                row.result = "pulled"
                row.detail = f"{before[:8]} -> {after[:8]}"
        except Exception as e:
            row.result = "failed"
            row.detail = str(e)
            row.state = "error"

        return row


class Config(cicconf.Command):
    def __init__(self,filename,verbose=False,rundir="./"):
        super().__init__(verbose)
        self.children = dict()
        self.options = dict()
        self.rundir = rundir
        self.cwd = os.getcwd()
        self.console = Console()

        if(filename.startswith("/")):
            pass
        else:
            filename = self.cwd + os.path.sep + filename

        self.filename = filename

        os.chdir(self.rundir)

    def read(self):

        if(not os.path.exists(self.filename)):
            self.error(f"Could not find {self.filename}")
            return False

        with open(self.filename) as fi:
            self.config = yaml.safe_load(fi)

        self.children = dict()
        self.options = dict()
        for k in self.config:
            if(k == "options"):
                self.options = self.config[k]
            else:
                self.children[k] = Repo(k,self.config[k],self.verbose)

        return True

    def _selected_children(self,regex):
        matcher = re.compile(regex)
        return [(name, child) for name, child in self.children.items() if matcher.search(name)]

    def _run_parallel(self, items, fn, jobs, progress_label=None):
        if(not items):
            return []
        max_workers = min(max(1, jobs), len(items))
        rows = []
        with Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
            console=self.console,
        ) as progress:
            task_id = progress.add_task(progress_label or "Working", total=len(items))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_name = {executor.submit(fn, item[1]): item[0] for item in items}
                for future in as_completed(future_to_name):
                    row = future.result()
                    rows.append(row)
                    progress_value = getattr(row, "result", getattr(row, "status", "done"))
                    progress.update(
                        task_id,
                        advance=1,
                        description=f"{progress_label or 'Working'}: {row.name} {progress_value}",
                    )
        rows.sort(key=lambda row: row.name)
        return rows

    def _render_action_table(self,title,rows):
        table = Table(title=title)
        table.add_column("Name",style="cyan",no_wrap=True)
        table.add_column("Revision",style="magenta")
        table.add_column("Result",style="green")
        table.add_column("Detail",style="blue")

        for row in rows:
            result_style = "green"
            if(row.state == "warning"):
                result_style = "yellow"
            elif(row.state == "error"):
                result_style = "bold red"

            table.add_row(
                row.name,
                row.revision,
                f"[{result_style}]{row.result}[/{result_style}]",
                row.detail,
            )

        self.console.print(table)

    def clone(self,useHttps,doOnClone=True,jobs=4):
        rows = self._run_parallel(
            list(self.children.items()),
            lambda repo: repo.clone_action(useHttp=useHttps, doOnClone=doOnClone),
            jobs,
            progress_label="Cloning repositories",
        )
        self._render_action_table("cicconf clone", rows)

    def newIp(self,name):
        error = False
        if("project" not in self.options):
            self.error(f"project option not defined in {self.filename}")
            error = True
        if("technology" not in self.options):
            self.error(f"technology option not defined in {self.filename}")
            error = True

        if("template" not in self.options):
            self.error(f"template option not defined in {self.filename}")
            error = True
        if(not error and "ip" not in self.options["template"]):
            self.error(f"no 'ip' option defined for options->template in {self.filename}")
            error = True
        if(error):
            return

        ip = self.options["project"] + "_" + name + "_" + self.options["technology"]
        iptemplate = self.options["template"]["ip"]
        cmd = cicconf.CmdIp(ip.upper(),iptemplate)
        cmd.run()

    def status(self,fast=True):
        table = Table(title="cicconf status")
        table.add_column("Name",style="cyan",no_wrap=True)
        table.add_column("Revision",style="magenta")
        table.add_column("Current",style="blue")
        table.add_column("Status",style="green")

        rows = self._run_parallel(
            list(self.children.items()),
            lambda repo: repo.collect_status(fast=fast),
            8,
            progress_label="Collecting status",
        )

        for row in rows:
            status_style = "green"
            if(row.state == "warning"):
                status_style = "yellow"
            elif(row.state == "uncloned"):
                status_style = "red"
            elif(row.state == "error"):
                status_style = "bold red"

            table.add_row(
                row.name,
                row.revision,
                row.current,
                f"[{status_style}]{row.status}[/{status_style}]",
            )

        self.console.print(table)

        if(fast):
            self.console.print("[dim]Fast mode skips ahead/behind counts. Use --no-fast for full git status.[/dim]")
        else:
            self.console.print("[dim]O = Commits behind/ahead branch, M = Modified files, U = Untracked files[/dim]")

        if(self.verbose):
            for row in rows:
                for detail in row.details:
                    self.console.print(f"  [yellow]{detail}[/yellow]")

    def update(self,regex,jobs=4):
        rows = self._run_parallel(
            self._selected_children(regex),
            lambda repo: repo.update_action(),
            jobs,
            progress_label="Updating repositories",
        )
        self._render_action_table("cicconf update", rows)

    def pull(self,regex,jobs=4):
        rows = self._run_parallel(
            self._selected_children(regex),
            lambda repo: repo.pull_action(),
            jobs,
            progress_label="Pulling repositories",
        )
        self._render_action_table("cicconf pull", rows)
