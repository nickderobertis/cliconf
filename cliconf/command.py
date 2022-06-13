import types
from typing import Any, Dict, Optional, Sequence

import click
from typer import Typer
from typer.main import get_command as typer_get_command

from cliconf.arg_store import ARGS_STORE
from cliconf.command_name import get_command_name
from cliconf.ext_typer import get_arg_names_that_can_be_processed_by_typer


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
    use_args = args or []
    func_name = prog_name or get_command_name(self.callback.__name__)  # type: ignore
    params = _create_passed_param_dict_from_command(self, func_name, use_args)
    # It seems typer always provides prog_name, but for safety calculate a fallback
    ARGS_STORE.add_command(func_name, use_args, params)
    return super(type(self), self).main(  # type: ignore
        args, func_name, complete_var, standalone_mode, windows_expand_args, **extra
    )


def _create_passed_param_dict_from_command(
    command: click.Command, prog_name: str, args: Sequence[str]
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
