from typing import Callable

import typer

from cliconf import configure
from cliconf.main import CLIConf
from tests.fixtures.app_settings import SETTINGS_ONE_YAML, SETTINGS_TWO_PY

single_command_yaml_cliconf = CLIConf(name="single_command_yaml")


@single_command_yaml_cliconf.command()
@configure(settings=SETTINGS_ONE_YAML)
def my_cli_func(
    a: str,
    b: int = typer.Argument(..., help="b help"),
    c: float = typer.Option(3.2, help="c help"),
):
    print(a, b, c)


single_command_py_cliconf = CLIConf(name="single_command_py")


def default_func_for_single_command_py(c: float):
    print(f"default {c}")


@single_command_py_cliconf.command()
@configure(settings=SETTINGS_TWO_PY)
def my_cli_func(
    a: str,
    b: int = typer.Argument(..., help="b help"),
    c: float = typer.Option(3.2, help="c help"),
    d: Callable[[float], None] = default_func_for_single_command_py,
):
    print(a, b, c, d(c))


if __name__ == "__main__":
    single_command_py_cliconf()
