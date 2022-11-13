#!/usr/bin/env python3

import click
import cicconf









@click.group()
def cli():
    pass

@cli.command()
@click.option("--config",default="config.yaml",help="Configuration file")
def clone(config):
    """Clone repositories in config file"""

    c = cicconf.Config(config)
    if(c.read()):
        c.clone()
        pass


if __name__ == "__main__":
    cli()
