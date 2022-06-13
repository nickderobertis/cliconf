from typing import Callable

import typer

from cliconf import CLIConf, configure
from tests.fixtures.app_settings import SETTINGS_TWO_PY
from tests.fixtures.cliconfs import default_func_for_single_command_py


def test_configure_creates_dynamic_model():
    @configure(SETTINGS_TWO_PY)
    def my_cli_func(a: int, b: str = "b"):
        pass

    model_cls = my_cli_func.model_cls
    model = model_cls(a=10)
    assert model.a == 10
    assert model.b == "b"


def test_configure_creates_dynamic_model_with_typer():
    cliconf_instance = CLIConf(name="dynamic_model_with_typer")

    @cliconf_instance.command()
    @configure(settings=SETTINGS_TWO_PY)
    def my_cli_func(
        a: str,
        b: int = typer.Argument(..., help="b help"),
        c: float = typer.Option(3.2, help="c help"),
        d: Callable[[float], None] = default_func_for_single_command_py,
    ):
        print(a, b, c, d(c))

    model_cls = my_cli_func.model_cls
    model = model_cls(a="a", b=1000)
    assert model.a == "a"
    assert model.b == 1000
    assert model.c == 3.2
    assert model.d == default_func_for_single_command_py
