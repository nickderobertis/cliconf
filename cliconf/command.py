import functools
import types
from types import FunctionType
from typing import Any, Callable, Dict, Optional, Sequence, Type

import click
from pyappconf import AppConfig, BaseConfig
from pydantic import create_model
from typer import Typer
from typer.main import get_command as typer_get_command
from typer.main import get_command_name

from cliconf.arg_store import ARGS_STORE


def cli_conf_main(
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
    func_name = prog_name or _get_command_name(self.callback.__name__)  # type: ignore
    params = _create_passed_param_dict_from_command(self, func_name, use_args)
    # It seems typer always provides prog_name, but for safety calculate a fallback
    ARGS_STORE.add_command(func_name, use_args, params)
    return super(type(self), self).main(  # type: ignore
        args, func_name, complete_var, standalone_mode, windows_expand_args, **extra
    )


def get_command(typer_instance: Typer) -> click.Command:
    """
    Extends typer's get_command function to modify the created click.Command instance
    to inspect the passed arguments and load from config.
    """
    command = typer_get_command(typer_instance)
    # Override the main function to load config
    command.main = types.MethodType(cli_conf_main, command)
    return command


def configure(settings: AppConfig, base_cls: Type[BaseConfig] = BaseConfig) -> Callable:
    def actual_decorator(func: FunctionType):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get args and kwargs as a single dict
            args_kwargs = dict(zip(func.__code__.co_varnames[1:], args))
            args_kwargs.update(kwargs)
            # Get user passed args from command line via args store
            args_store = ARGS_STORE[_get_command_name(func.__name__)]
            user_kwargs = args_store.params
            # Create a BaseConfig instance based off the function kwargs
            DynamicConfig = create_model(
                f"{func.__name__}_Config",
                __base__=base_cls,
                **args_kwargs,
                settings=settings,
                _settings=settings,
            )
            # Load the config, overriding with any user passed args
            config = DynamicConfig.load(model_kwargs=user_kwargs)
            return func(**config.dict(exclude={"settings"}))

        return wrapper

    return actual_decorator


def _get_command_name(name: str) -> str:
    return get_command_name(name.strip())


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
