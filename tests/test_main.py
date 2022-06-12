import shlex
from typing import Sequence

from click.testing import Result

from pycliconf.main import CLIConf
from pycliconf.testing import CLIRunner
from tests import ext_click
from tests.fixtures.typers import single_command_typer

runner = CLIRunner()


class CLIRunnerException(Exception):
    pass


def run(instance: CLIConf, args: Sequence[str]) -> Result:
    result = runner.invoke(instance, args)
    if result.exit_code != 0:
        output = ext_click.result_to_message(result)
        command = shlex.join([instance.info.name, *args])
        raise CLIRunnerException(
            f"{command} with exited with code {result.exit_code}.\n{output}"
        )
    return result


def test_single_command_typer_reads_from_config():
    result = run(single_command_typer, ["a", "2"])
    assert result.stdout == "a 2 45.6\n"
