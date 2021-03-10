from enum import Enum, unique


@unique
class Tasks(Enum):
    PULL_REQUESTS = 0
    ORG_SCAN = 1
