from typing import Callable

from pyappconf import BaseConfig

from tests.fixtures.app_settings import SETTINGS_ONE_YAML, SETTINGS_TWO_PY
from tests.fixtures.cliconfs import default_func_for_single_command_py


class ConfigOne(BaseConfig):
    a: str
    b: int
    c: float = 45.6

    _settings = SETTINGS_ONE_YAML


def generate_config_one():
    ConfigOne(a="a from config", b=1000).save()


if __name__ == "__main__":
    generate_config_one()
