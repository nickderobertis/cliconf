from tests.fixtures.cliconfs import (
    default_func_for_single_command_py,
    my_cli_func_two_py,
)

my_cli_func_two_py_Config = my_cli_func_two_py.model_cls
from tests.generate import custom_d_func

config = my_cli_func_two_py_Config(
    a=None,
    b=None,
    c=123.4,
    d=custom_d_func,
)
