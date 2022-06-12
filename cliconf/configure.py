import functools
from types import FunctionType
from typing import Callable, Optional, Type

from pyappconf import AppConfig, BaseConfig

from cliconf.dynamic_config import create_and_load_dynamic_config


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

        return wrapper

    return actual_decorator
