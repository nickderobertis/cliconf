from tests.fixtures.cliconfs import my_cli_func

DynamicConfig = my_cli_func.model_cls


def custom_d_func(c: float) -> str:
    return f"custom {c}"


# TODO: should allow putting ... for required arguments, as they will never be used anyway
config = DynamicConfig(a="", b=1, c=123.4, d=custom_d_func)
