from pycliconf.testing import CLIRunner
from tests.fixtures.typers import single_command_typer

runner = CLIRunner()


def test_single_command_typer_reads_from_config():
    result = runner.invoke(single_command_typer, ["a", "2"])
    assert result.stdout == "a 2 45.6\n"
