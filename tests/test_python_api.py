from tests.fixtures.cliconfs import my_cli_func_one_yaml


def test_cliconf_decorated_executes_as_a_normal_python_function():
    result = my_cli_func_one_yaml("a", 2)
    assert result == ("a", 2, 3.2)
