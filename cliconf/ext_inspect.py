import inspect
from types import FunctionType
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeGuard,
    Union,
    get_args,
    get_origin,
    no_type_check,
)

from cliconf.ext_typer import is_typer_parameter_info


@no_type_check
def get_function_params(
    func: FunctionType,
    make_optional: bool = True,
) -> Dict[str, Tuple[Type, Any]]:
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
        param: (
            _extract_type(annotations.get(param), make_optional),
            _extract_default(kwonlydefaults.get(param), make_optional),
        )
        for param in kwonlyargs
    }
    params = {
        param: (
            _extract_type(annotations.get(param), make_optional),
            _extract_default(default, make_optional),
        )
        for param, default in zip(args, defaults)
    }
    return {
        **params,
        **keyword_only_params,
    }


def get_function_args(func: FunctionType) -> List[str]:
    (
        args,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = inspect.getfullargspec(func)
    return args or []


@no_type_check
def _extract_type(typ: Optional[type], make_optional: bool) -> type:
    if typ is None:
        return Any

    if not make_optional:
        return typ

    if _is_optional(typ):
        return typ

    # Wrap type in Optional if it is not already
    return Optional[typ]


def _extract_from_typer_parameter_info_if_necessary(value: Any) -> Any:
    if is_typer_parameter_info(value):
        return value.default
    return value


def _extract_default(value: Any, make_optional: bool) -> Any:
    underlying_value = _extract_from_typer_parameter_info_if_necessary(value)
    if not make_optional:
        return underlying_value
    return underlying_value if underlying_value is not ... else None


def _is_optional(typ: type) -> TypeGuard[Type[Optional[Any]]]:
    return get_origin(typ) is Union and type(None) in get_args(typ)
