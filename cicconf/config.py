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

        if("revision" in obj):
            self.revision = obj["revision"]

        if("remote" in obj):
            self.remote = obj["remote"]

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
