import click
from rich.console import Console

from ..commands import render, render_config, single_render
from ..config import GITHUB_TOKEN
from ..errors import InvalidGithubToken
from ..metrics import repository_metrics
from ..version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, "-v", "--version", message="version %(version)s")
def cli() -> None:
    """Reviews - A terminal UI Dashboard for monitoring code review requests.\n

    For feature requests or bug reports: https://github.com/apoclyps/reviews/issues
    """


@cli.command(help="Show the activity metrics per repository")
def metrics() -> None:
    """
    Command:\n
        reviews metrics
    """
    repository_metrics()


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
    console = Console()
    style = "bold"

    github_token_msg = (
        "> a valid GITHUB_TOKEN should be provided as an environmental "  # nosec
        "variable or a value within a settings.ini or .env file. Please see "
        "the project [link=https://github.com/apoclyps/reviews]"
        "README[/link] for more methods on providing configuration."
        "\n"
    )
    missing_github_token_msg = (
        "\n[red]GITHUB_TOKEN[/] is required and has not been provided as "
        "configuration needed to use Reviews. \n\n"
        f"{github_token_msg}"
    )
    invalid_github_token_msg = (
        "\n[red]GITHUB_TOKEN[/] is required configuration and an invalid "
        "token has been supplied to Reviews. \n\n"
        f"{github_token_msg}"
    )

    if not GITHUB_TOKEN:
        console.print(
            missing_github_token_msg,
            style=style,
        )
        return

    try:
        click.echo("loading dashboard")

        if reload:
            render()
        else:
            single_render()
    except InvalidGithubToken:
        console.print(
            invalid_github_token_msg,
            style=style,
        )

    return


def main() -> None:
    """Entry point to CLI"""
    cli()
