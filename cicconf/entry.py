#!/usr/bin/env python3

import click
import cicconf

@click.group()
@click.option("--config",default="config.yaml",help="Configuration file")
@click.option("--verbose/--no-verbose",default=False,help="Turn on extra output")
@click.option("--rundir",default="./",help="Where to run cicconf")
@click.pass_context
def cli(ctx,config,verbose,rundir):
    ctx.ensure_object(dict)
    c = cicconf.Config(config,verbose,rundir)
    ctx.obj["c"] = c
    pass

@cli.command()
@click.option("--https",is_flag=True,default=False,help="Use https for clone (override for git@)")
@click.option("--onclone/--no-onclone",is_flag=True,default=True,help="Don't run on_clone event")
@click.pass_context
def clone(ctx,https,onclone):
    """Clone repositories in config file"""
    c = ctx.obj["c"]

    if(c.read()):
        c.clone(useHttps=https,doOnClone=onclone)
        pass

@cli.command()
@click.argument("name")
@click.option("--project",default=None,help="Override project name in config file")
@click.option("--technology",default=None,help="Override technology name in config file")
@click.option("--ip",default=None,help="Override ip template name in config file")
@click.pass_context
def newip(ctx,name,project,technology,ip):
    """Create a new IP with name <project>_<name>_<technology>
    The <project> and <technology> is fetched from the config file.

    The name should be short and must be unique (for example, bias, aic01 or similar).
    """

    c = ctx.obj["c"]
    if(c.read()):
        if(project is not None):
            c.options["project"] = project
        if(technology is not None):
            c.options["technology"] = technology
        if(ip is not None):
            c.options["template"]["ip"] = ip
        c.newIp(name)


@cli.command()
@click.pass_context
def status(ctx):
    """
    Report the status of each of the configured IPs
    """
    c = ctx.obj["c"]
    if(c.read()):
        c.status()

@cli.command()
@click.pass_context
@click.option("--regex",default=".*",help="Regex pattern for folders to update")
def update(ctx,regex):
    """
    Update IPs to correct branch according to config file
    """
    c = ctx.obj["c"]
    if(c.read()):
        c.update(regex)

if __name__ == "__main__":
    cli(obj={})
