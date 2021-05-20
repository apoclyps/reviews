import asyncio

import asyncclick as click

from ..tasks import render, single_render
from ..version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, "-v", "--version", message="version %(version)s")
async def cli() -> None:
    """Reviews - A terminal UI Dashboard for monitoring code review requests.\n

    For feature requests or bug reports: https://github.com/apoclyps/reviews/issues
    """


@cli.command(help="Visualize code review requests as a Dashboard")
@click.option("-r", "--reload/--no-reload", default=True, is_flag=True)
async def dashboard(reload: bool) -> None:
    """
    Command:\n
        reviews dashboard

    Usage:\n
        reviews dashboard --reload \n
        reviews dashboard --no-reload \n
    """

    click.echo("loading dashboard")

    if reload:
        await asyncio.gather(
            # asyncio.to_thread(update),
            asyncio.to_thread(render),
        )
    else:
        single_render()


def main() -> None:
    """Entry point to CLI"""
    asyncio.run(cli())
