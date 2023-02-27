#!/usr/bin/env python
"""
Python Project Template Entrypoint Script
"""

import logging
import os
from typing import Any, List

import click

try:
    from gdc_tosvc_tools import __version__
except Exception:
    __version__ = "0.0.0"

log = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s:%(lineno)s %(levelname)s | %(message)s",
)

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "cli"))


class CLI(click.MultiCommand):
    def list_commands(self, _: click.Context) -> List[str]:
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and not filename == "__init__.py":
                rv.append(filename.strip(".py"))
        rv.sort()
        return rv

    def get_command(self, _: click.Context, name: str) -> Any:
        try:
            mod = __import__(f"gdc_tosvc_tools.cli.{name}", None, None, ["main"])
        except ImportError:
            return
        return mod.main


@click.command(cls=CLI)
def cli() -> None:
    click.echo()


if __name__ == "__main__":
    cli()


# __END__
