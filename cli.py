import asyncio

import asyncclick as click

from app import config
from app.tasks import render, update
from create import prepare_database

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
async def main():
    """Click entrypoint with help provided by default."""


@main.command(help="Display a dashboard")
async def dashboard():
    """ Dashboard command. """

    click.echo("loading dashboard")

    if config.ENABLE_PERSISTED_DATA:
        prepare_database()

    # TODO: move github polling to another thread
    await asyncio.gather(
        # asyncio.to_thread(update),
        asyncio.to_thread(render),
    )


if __name__ == "__main__":
    asyncio.run(main())
