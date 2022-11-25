#!/usr/bin/env python3

import git
import cicconf
import os
import yaml

class Repo(cicconf.Command):

    def __init__(self,name,obj):
        super().__init__()
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

    def clone(self,useHttp=False):
        if(self.exists()):
            self.comment(f"{self.name} already exists")
            return

        if(not self.remote):
            self.error(f"No remote found for {self.name}")
            return

        src = self.remote
        if(useHttp and "git@" in src):
            src = src.replace(":","/")
            src = src.replace("git@","https://")


        self.comment(f"%-25s: Cloning {src}" % (self.name))
        r = git.Repo.clone_from(src, self.name)

        if(self.revision):
            self.comment(f"%-25s: Checkout {self.revision}" % (self.name))
            r.git.checkout(self.revision)

        if(self.on_clone):
            self.doCmd(f"cd {self.name};{self.on_clone}")

    def status(self):

        if(not self.exists()):
            self.warning(f"%-25s%-15s%-15s" % (self.name,"","uncloned"))
            return


        repo = git.Repo(self.name)

        status = ""

        #- Check branch
        if(repo.head.is_detached):
            branch = ""
            sha = repo.head.commit.hexsha
            for t in repo.tags:
                if(t.object.hexsha == sha):
                    branch = t.name

            if(branch == ""):
                branch = "unknown"
        else:
            try:
                branch = repo.active_branch
            except Exception as e:
                self.error(" Could not find branch name of {self.name}")
                return


        if(str(branch) != self.revision):
            status += f"{branch} "


        #- Check ahead/behind
        commits_behind = repo.iter_commits(f"{branch}..origin/{branch}")
        commits_ahead = repo.iter_commits(f"origin/{branch}..{branch}")
        behind = sum(1 for c in commits_behind)
        ahead = sum(1 for c in commits_ahead)
        if(behind > 0):
            status += f"O-{behind} "
        if(ahead > 0):
            status += f"O+{ahead} "


        #- Check files
        diff = repo.index.diff(None)
        N = sum(1 for c in diff)
        if(N > 0):
            status += f"M+{N}"

        untracked =repo.untracked_files
        UN = sum(1 for c in untracked)
        if(UN > 0):
            status += f"U+{UN}"


        self.comment(f"%-25s%-15s%-15s" % (self.name,self.revision,status))


        if(self.verbose):
            self.indent +=1
            for d in untracked:
                self.warning(self.name + os.path.sep + d)
            for d in diff:
                self.warning(self.name + os.path.sep + d.a_path + " "  + d.change_type)
            self.indent -=1

        #if(not isClean):
        #    print(status)

    def update(self):

        if(not self.exists()):
            self.warning(f"%-25s%-15s%-15s" % (self.name,"","uncloned"))
            self.clone()
            return

        self.warning(f"%-25s%-15s%-15s" % (self.name,"","updating"))
        repo = git.Repo(self.name)
        repo.git.checkout(self.revision)
        repo.git.pull()


class Config(cicconf.Command):
    def __init__(self,filename):
        super().__init__()
        self.filename = filename
        self.children = dict()
        self.options = dict()

    def read(self):

        if(not os.path.exists(self.filename)):
            self.error(f"Could not find {self.filename}")
            return False

        with open(self.filename) as fi:
            self.config = yaml.safe_load(fi)

        for k in self.config:
            if(k == "options"):
                self.options = self.config[k]
            else:
                self.children[k] = Repo(k,self.config[k])

        return True

    def clone(self,useHttps):
        for name,c in self.children.items():
            c.clone(useHttp=useHttps)

    def newIp(self,name):
        #- Check for errors
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
        if(not error and "ip" not in self.options["template"]["ip"]):
            self.error(f"no 'ip' option defined for options->template in {self.filename}")
            error = True
        if(error):
            return

        #- Run template
        ip = self.options["project"] + "_" + name + "_" + self.options["technology"]
        iptemplate = self.options["template"]["ip"]
        cmd = cicconf.CmdIp(ip.upper(),iptemplate)
        cmd.run()

    def status(self):
        self.comment("%-25s%-15s%-15s" %("Name","Revision","Status"))
        self.comment("-"*55)
        for name,c in self.children.items():
            c.status()

    def update(self):

        for name,c in self.children.items():
            c.update()
