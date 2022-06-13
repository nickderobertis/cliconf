import inspect
from types import FunctionType
from typing import Any, Dict, Optional, Sequence, Tuple, Type

from pyappconf import AppConfig, BaseConfig
from pydantic import create_model

from cliconf.arg_store import ARGS_STORE
from cliconf.command_name import get_command_name
from cliconf.ext_pyappconf import create_cli_base_config_class
from cliconf.ext_typer import is_typer_parameter_info


def create_dynamic_config_class_from_function(
    func: FunctionType,
    settings: AppConfig,
    base_cls: Optional[Type[BaseConfig]] = None,
) -> Type[BaseConfig]:
    """
    Create a BaseConfig class from a function.
    """
    base_cls = base_cls or create_cli_base_config_class(BaseConfig, settings)
    (
        args,
        _,
        varkw,
        defaults,
        kwonlyargs,
        kwonlydefaults,
        annotations,
    ) = inspect.getfullargspec(func)
    defaults = defaults or []
    args = args or []

    non_default_args = len(args) - len(defaults)
    defaults = (...,) * non_default_args + defaults

    keyword_only_params = {
        param: kwonlydefaults.get(param, Any) for param in kwonlyargs
    }
    params = {
        param: (annotations.get(param, Any), _extract_default(default))
        for param, default in zip(args, defaults)
    }

    return create_model(
        f"{func.__name__}_Config",
        __base__=base_cls,
        **params,
        **keyword_only_params,
        settings=settings,
        _settings=settings,
    )


def filter_func_args_and_kwargs_to_get_user_passed_data(
    func: FunctionType,
    func_args: Sequence[Any],
    func_kwargs: Dict[str, Any],
) -> Dict[str, Any]:
    args_kwargs = dict(zip(func.__code__.co_varnames[1:], func_args))
    args_kwargs.update(func_kwargs)
    # Get user passed args from command line via args store
    args_store = ARGS_STORE[get_command_name(func.__name__)]
    user_kwargs = args_store.params
    return user_kwargs


def create_and_load_dynamic_config(
    func: FunctionType,
    func_args: Sequence[Any],
    func_kwargs: Dict[str, Any],
    settings: AppConfig,
    base_cls: Optional[Type[BaseConfig]] = None,
) -> Tuple[BaseConfig, Type[BaseConfig]]:
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
    return DynamicConfig.load_or_create(model_kwargs=user_kwargs), DynamicConfig


def _extract_default(value: Any) -> Any:
    if is_typer_parameter_info(value):
        return value.default
    return value
