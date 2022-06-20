from tests.fixtures.cliconfs import (
    default_func_for_single_command_py,
    my_cli_func_two_py,
)
from tests.generate import custom_d_func

MyCliFuncTwoPyConfig = my_cli_func_two_py.model_cls

config = MyCliFuncTwoPyConfig(
    a=None,
    b=None,
    c=123.4,
    d=custom_d_func,
)
