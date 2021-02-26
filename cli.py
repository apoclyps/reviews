import click

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """Click entrypoint with help provided by default."""


@main.command(help="Display a dashboard")
def dashboard():
    """ Dashboard command. """

    click.echo("start dashboard")

    from time import sleep

    from rich.live import Live

    from dexi.fullscreen import job_progress, layout, overall_progress, overall_task

    with Live(layout, refresh_per_second=10, screen=True):
        while not overall_progress.finished:
            sleep(0.1)
            for job in job_progress.tasks:
                if not job.finished:
                    job_progress.advance(job.id)

            completed = sum(task.completed for task in job_progress.tasks)
            overall_progress.update(overall_task, completed=completed)


if __name__ == "__main__":
    main()
