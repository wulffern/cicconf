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


if __name__ == "__main__":
    cli()
