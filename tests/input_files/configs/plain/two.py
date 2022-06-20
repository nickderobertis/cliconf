from tests.fixtures.cliconfs import (
    default_func_for_single_command_py,
    my_cli_func_two_py,
)

my_cli_func_two_py_Config = my_cli_func_two_py.model_cls

config = my_cli_func_two_py_Config(
    a=None,
    b=None,
    c=3.2,
    d=default_func_for_single_command_py,
)
