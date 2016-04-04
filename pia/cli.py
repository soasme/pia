# -*- coding: utf-8 -*-
"""
pia.cli
~~~~~~~~~~~~~

A simple command line application for pia.
"""

import click

@click.group()
def cli():
    """
    Pia cli group
    """
    pass

@cli.command()
def run():
    """
    Run remote pia program.
    """
    pass

@cli.command()
def dev():
    """
    Develop a pia program locally.
    """

def main():
    """ Pia main function """
    cli()

if __name__ == '__main__':
    main()
