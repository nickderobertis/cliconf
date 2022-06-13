from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import click
from typer.main import get_click_param, lenient_issubclass
from typer.utils import get_params_from_function


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
