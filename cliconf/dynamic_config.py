from types import FunctionType
from typing import Any, Dict, Optional, Sequence, Type

from pyappconf import AppConfig, BaseConfig
from pydantic import BaseConfig as PydanticBaseConfig
from pydantic import create_model

from cliconf.arg_store import ARGS_STORE
from cliconf.command_name import get_command_name
from cliconf.ext_pyappconf import create_cli_base_config_class


def create_and_load_dynamic_config(
    func: FunctionType,
    func_args: Sequence[Any],
    func_kwargs: Dict[str, Any],
    settings: AppConfig,
    base_cls: Optional[Type[BaseConfig]] = None,
) -> BaseConfig:
    args_kwargs = dict(zip(func.__code__.co_varnames[1:], func_args))
    args_kwargs.update(func_kwargs)
    # Get user passed args from command line via args store
    args_store = ARGS_STORE[get_command_name(func.__name__)]
    user_kwargs = args_store.params
    base_cls = base_cls or create_cli_base_config_class(BaseConfig, settings)
    # Create a BaseConfig instance based off the function kwargs
    DynamicConfig = create_model(
        f"{func.__name__}_Config",
        __base__=base_cls,
        **args_kwargs,
        settings=settings,
        _settings=settings,
    )
    # Load the config, overriding with any user passed args
    return DynamicConfig.load(model_kwargs=user_kwargs)
