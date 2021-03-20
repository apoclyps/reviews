import asyncio

import asyncclick as click

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

    prepare_database()

    await asyncio.gather(
        asyncio.to_thread(update),
        asyncio.to_thread(render),
    )


if __name__ == "__main__":
    asyncio.run(main())
