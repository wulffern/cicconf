#!/usr/bin/env python3

import click
import cicconf

@click.group()
def cli():
    pass

@cli.command()
@click.option("--config",default="config.yaml",help="Configuration file")
@click.option("--https",is_flag=True,default=False,help="Use https for clone (override for git@)")
def clone(config,https):
    """Clone repositories in config file"""

    c = cicconf.Config(config)
    if(c.read()):
        c.clone(useHttps=https)
        pass

@cli.command()
@click.option("--config",default="config.yaml",help="Configuration file")
@click.argument("name")
def newip(config,name):
    """Create a new IP with name <project>_<name>_<technology>
    The <project> and <technology> is fetched from the config file.

    The name should be short and must be unique (for example, bias, aic01 or similar).
    """

    c = cicconf.Config(config)
    if(c.read()):
        c.newIp(name)


@cli.command()
@click.option("--config",default="config.yaml",help="Configuration file")
def status(config):
    """
    Report the status of each of the configured IPs
    """
    c = cicconf.Config(config)
    if(c.read()):
        c.status()

@cli.command()
@click.option("--config",default="config.yaml",help="Configuration file")
def update(config):
    """
    Update all ips to correct branch according to config file
    """
    c = cicconf.Config(config)
    if(c.read()):
        c.update()

if __name__ == "__main__":
    cli()
