import typer

from cliconf.command import configure
from cliconf.main import CLIConf
from tests.fixtures.app_settings import SETTINGS_ONE

single_command_cliconf = CLIConf(name="single_command")


@single_command_cliconf.command()
@configure(settings=SETTINGS_ONE)
def my_cli_func(
    a: str,
    b: int = typer.Argument(..., help="b help"),
    c: float = typer.Option(3.2, help="c help"),
):
    print(a, b, c)


if __name__ == "__main__":
    single_command_cliconf()
