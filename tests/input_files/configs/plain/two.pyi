from tests.fixtures.cliconfs import (
    default_func_for_single_command_py,
    my_cli_func_two_py,
)

MyCliFuncTwoPyConfig = my_cli_func_two_py.model_cls
from typing import Callable, Optional

from pydantic import BaseModel

class MyCliFuncTwoPyConfig(BaseModel):
    a: Optional[str] = None
    b: Optional[int] = None
    c: Optional[float] = 3.2
    d: Optional[Callable[[float], str]] = default_func_for_single_command_py

config: MyCliFuncTwoPyConfig
