from typing import Any, Callable, List

import click
import typer.models
from typer.main import get_click_param, lenient_issubclass
from typer.utils import get_params_from_function
from typing_extensions import TypeGuard


def get_arg_names_that_can_be_processed_by_typer(
    callback: Callable[..., Any]
) -> List[str]:
    can_process: List[str] = []
    parameters = get_params_from_function(callback)
    for param_name, param in parameters.items():
        if lenient_issubclass(param.annotation, click.Context):
            continue
        try:
            _, _ = get_click_param(param)
        except RuntimeError as e:
            if "Type not yet supported" in str(e):
                continue
            raise e
        else:
            can_process.append(param_name)
    return can_process


def is_typer_parameter_info(argument: Any) -> TypeGuard[typer.models.ParameterInfo]:
    return all(
        [
            hasattr(argument, "default"),
            hasattr(argument, "help"),
            hasattr(argument, "metavar"),
            hasattr(argument, "is_eager"),
        ]
    )


# def is_typer_option_info(argument: Any) -> TypeGuard[typer.models.OptionInfo]:
#     if not _is_typer_parameter_info(argument):
#         return False
#     return all([
#         hasattr(argument, "prompt"),
#         hasattr(argument, "confirmation_prompt"),
#         hasattr(argument, "hide_input"),
#         hasattr(argument, "is_flag"),
#     ])
#
# def is_typer_argument_info(argument: Any) -> TypeGuard[typer.models.ArgumentInfo]:
#     if not _is_typer_parameter_info(argument):
#         return False
#     if is_typer_option_info(argument):
#         return False
#     return True
