from tests.fixtures.cliconfs import (
    default_func_for_single_command_py,
    my_cli_func_two_py,
)

my_cli_func_two_py_Config = my_cli_func_two_py.model_cls
from typing import Callable, Optional

from pydantic import BaseModel

from tests.generate import custom_d_func

class my_cli_func_two_py_Config(BaseModel):
    a: Optional[str] = None
    b: Optional[int] = None
    c: Optional[float] = 123.4
    d: Optional[Callable[[float], str]] = custom_d_func

config: my_cli_func_two_py_Config
