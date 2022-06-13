import functools
import inspect
from types import FunctionType
from typing import Callable, Optional, Type

from pyappconf import AppConfig, BaseConfig

from cliconf.dynamic_config import create_and_load_dynamic_config
from cliconf.ext_typer import get_arg_names_that_can_be_processed_by_typer


def configure(
    settings: AppConfig, base_cls: Optional[Type[BaseConfig]] = None
) -> Callable:
    def actual_decorator(func: FunctionType):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Load the config, overriding with any user passed args
            config = create_and_load_dynamic_config(
                func, args, kwargs, settings, base_cls
            )
            return func(**config.dict(exclude={"settings"}))

        # Override call signature to exclude any variables that cannot be processed by typer
        typer_args = get_arg_names_that_can_be_processed_by_typer(func)
        sig = inspect.signature(func)
        typer_sig = sig.replace(
            parameters=tuple(
                val for name, val in sig.parameters.items() if name in typer_args
            )
        )
        wrapper.__signature__ = typer_sig

        return wrapper

    return actual_decorator
