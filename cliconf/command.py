import os
import sys
import types
from typing import Any, Dict, List, Optional, Sequence

import click
from click.utils import _expand_args
from typer import Typer
from typer.main import get_command as typer_get_command

from cliconf.arg_store import ARGS_STORE
from cliconf.command_name import get_command_name


def get_command(typer_instance: Typer) -> click.Command:
    """
    Extends typer's get_command function to modify the created click.Command instance
    to inspect the passed arguments and load from config.
    """
    command = typer_get_command(typer_instance)
    # Override the main function to load config
    command.main = types.MethodType(_cli_conf_main, command)
    return command


def _cli_conf_main(
    self: click.Command,
    args: Optional[Sequence[str]] = None,
    prog_name: Optional[str] = None,
    complete_var: Optional[str] = None,
    standalone_mode: bool = True,
    windows_expand_args: bool = True,
    **extra: Any,
) -> Any:
    """
    A modified version of click.Command's main function that records which arguments were passed
    """
    use_args = _get_arguments_from_passed_or_argv(args)
    func_name = prog_name or get_command_name(self.callback.__name__)  # type: ignore
    params = _create_passed_param_dict_from_command(self, func_name, use_args)
    # It seems typer always provides prog_name, but for safety calculate a fallback
    ARGS_STORE.add_command(func_name, use_args, params)
    return super(type(self), self).main(  # type: ignore
        args, func_name, complete_var, standalone_mode, windows_expand_args, **extra
    )


def _create_passed_param_dict_from_command(
    command: click.Command,
    prog_name: str,
    args: Sequence[str],
) -> Dict[str, Any]:
    context = command.make_context(prog_name, [*args])
    parser = command.make_parser(context)
    opts, _, param_order = parser.parse_args(args=[*args])
    # Reorder the opts dict to match the order of the command's params
    out_opts: Dict[str, Any] = {}
    for argument in param_order:
        if argument.name in opts:
            out_opts[argument.name] = opts[argument.name]
    return out_opts


def _get_arguments_from_passed_or_argv(
    args: Optional[Sequence[str]] = None,
) -> List[str]:
    """
    Returns the arguments passed to the command.

    Note: Mostly adapted from click.BaseCommand.main
    :param args:
    :return:
    """
    if args is not None:
        return list(args)

    args = sys.argv[1:]

    if os.name == "nt":
        # It's not ideal to be using a private method, but want to make sure
        # it works exactly the same for param extraction as how Click handles it
        return _expand_args(args)
    return args
