import asyncio

import asyncclick as click

from create import prepare_database
from reviews import config
from reviews.tasks import render, single_render
from reviews.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, "-v", "--version", message="version %(version)s")
async def main():
    """Click entrypoint with help provided by default."""


@main.command(help="Display a dashboard")
@click.option("-r", "--reload/--no-reload", default=True, is_flag=True)
async def dashboard(reload):
    """Dashboard command."""

    click.echo("loading dashboard")

    if config.ENABLE_PERSISTED_DATA:
        prepare_database()

    if reload:
        # TODO: move github polling to another thread
        await asyncio.gather(
            # asyncio.to_thread(update),
            asyncio.to_thread(render),
        )
    else:
        single_render()


if __name__ == "__main__":
    asyncio.run(main())
