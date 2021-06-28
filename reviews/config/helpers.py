from typing import List, Tuple

from decouple import Csv


def get_configuration(config: Csv) -> List[Tuple[str, str]]:
    """converts a comma separated list of organizations/repositories into a list
    of tuples.
    """

    def _to_tuple(values: List[str]) -> Tuple[str, str]:
        return (values[0], values[1])

    def split(configuration: str) -> List[str]:
        if ":" in configuration:
            return configuration.split(sep=":", maxsplit=1)

        return configuration.split(sep="/", maxsplit=1)

    return [_to_tuple(values=split(configuration=configuration)) for configuration in config]
