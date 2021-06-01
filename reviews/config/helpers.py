from typing import Dict, List, Tuple

from rich.color import ANSI_COLOR_NAMES

from .settings import REVIEWS_LABEL_CONFIGURATION, REVIEWS_REPOSITORY_CONFIGURATION


def get_configuration() -> List[Tuple[str, str]]:
    """converts a comma seperated list of organizations/repositories into a list
    of tuples.
    """

    def _to_tuple(values: List[str]) -> Tuple[str, str]:
        return (values[0], values[1])

    return [
        _to_tuple(values=configuration.split(sep="/", maxsplit=1))
        for configuration in REVIEWS_REPOSITORY_CONFIGURATION
    ]


def get_label_colour_map() -> Dict[str, str]:
    """converts a comma seperated list of organizations/repositories into a list
    of tuples.
    """

    def _preproc(label_colour: str) -> List[str]:
        return label_colour.lower().split(sep="/")

    return {
        label: f"[{colour}]"
        for label, colour in map(_preproc, REVIEWS_LABEL_CONFIGURATION)
        if colour in ANSI_COLOR_NAMES
    }
