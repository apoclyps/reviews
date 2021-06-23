from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

import humanize


@dataclass
class Label:
    """Labels on a Pull Request."""

    name: str


@dataclass
class PullRequest:
    """Models a Pull Request"""

    number: int
    title: str
    draft: bool
    repository_url: str
    link: str
    created_at: datetime
    updated_at: datetime
    approved: str
    approved_by_others: bool
    additions: int = 0
    deletions: int = 0
    labels: List[Label] = field(default_factory=list)

    def render_approved(self) -> str:
        """Renders the approved status as a colourised string"""
        status = ""

        if self.approved == "AUTHOR":
            status = "[grey]Author[/]"
        elif self.approved == "APPROVED":
            status = "[green]Approved[/]"
        elif self.approved == "CHANGES_REQUESTED":
            status = "[red]Changes Requested[/]"

        return status

    def render_approved_by_others(self) -> str:
        """Renders approved_by_others flag as a colourised string"""
        return "[green]Ready[/]" if self.approved_by_others else ""

    def render_labels(self, colour_map: Dict[str, str]) -> str:
        """Renders the labels as a joined colourised string"""
        return ", ".join([f"{colour_map.get(label.name.lower(), '[white]')}{label.name}[/]" for label in self.labels])

    def render_title(self) -> str:
        """Renders the title as a colourised string"""
        colour = ""
        title = self.title

        if title.startswith("[Security]"):
            title = title.removeprefix("[Security]")
            colour = "[bold red][Security][/]"

        if self.draft:
            colour += "[bold grey][Draft][/] "

        return f"{colour}[white][link={self.link}]{title}[/link][/]"

    def render_updated_at(self, since: Optional[datetime] = None) -> str:
        """Renders the updated_at as a human-readable and colourised string"""
        colour = ""
        suffix = ""

        now = since or datetime.now(timezone.utc)
        days = (now - self.updated_at).days

        if days >= 7:
            colour = "[red]"
        elif days >= 1:
            colour = "[yellow]"

        if colour:
            suffix = "[/]"

        return f"{colour}{humanize.naturaltime(self.updated_at, when=now)}{suffix}"

    def render_diff(self) -> str:
        """Renders the additions and deletions using the Github convention of +/-"""
        return f"[green]+{self.additions}[/green] [red]-{self.deletions}[/red]"
