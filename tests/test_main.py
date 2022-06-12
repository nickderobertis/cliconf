from typer.testing import CliRunner

from tests.fixtures.typers import single_command_typer

runner = CliRunner()


def test_single_command_typer_reads_from_config():
    result = runner.invoke(single_command_typer, ["a", "2"])
    assert result.stdout == "a 2 3.2\n"
