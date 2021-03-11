from dexi import config
from enum import Enum, unique

from os import path

@unique
class Sound(Enum):
    SUCCESS = path.join(config.DATA_PATH, "audio/success.wav")
    FAILURE = path.join(config.DATA_PATH, "audio/failure.wav")

@unique
class Language(Enum):
    PYTHON = path.join(config.DATA_PATH, "icon/python_icon.png")
    RUBY = path.join(config.DATA_PATH, "icon/ruby_icon.png")
    GO = path.join(config.DATA_PATH, "icon/go_icon.png")
    JAVASCRIPT = path.join(config.DATA_PATH, "icon/javascript_icon.png")
    TERRAFORM = path.join(config.DATA_PATH, "icon/terraform_icon.png")
