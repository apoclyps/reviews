import click

from ..commands import render, render_config, single_render
from ..version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, "-v", "--version", message="version %(version)s")
def cli() -> None:
    """Reviews - A terminal UI Dashboard for monitoring code review requests.\n

    For feature requests or bug reports: https://github.com/apoclyps/reviews/issues
    """


@cli.command(help="Show the current configuration used by Reviews")
@click.option("-show", "--show/--hide", default=False, is_flag=True)
def config(show: bool) -> None:
    """
    Command:\n
        reviews config

    Usage:\n
        reviews config --show \n
        reviews config --hide \n
    """
    render_config(show=show)


@cli.command(help="Visualize code review requests as a Dashboard")
@click.option("-r", "--reload/--no-reload", default=True, is_flag=True)
def dashboard(reload: bool) -> None:
    """
    Command:\n
        reviews dashboard

    Usage:\n
        reviews dashboard --reload \n
        reviews dashboard --no-reload \n
    """

    click.echo("loading dashboard")

    if reload:
        render()
    else:
        single_render()


def main() -> None:
    """Entry point to CLI"""
    cli()
