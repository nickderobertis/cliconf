from pyappconf import AppConfig, ConfigFormats

from tests.config import CONFIGS_DIR

SETTINGS_ONE_YAML = AppConfig(
    app_name="MyApp",
    config_name="one",
    custom_config_folder=CONFIGS_DIR,
    default_format=ConfigFormats.YAML,
)


SETTINGS_TWO_PY = AppConfig(
    app_name="MyApp",
    config_name="two",
    custom_config_folder=CONFIGS_DIR,
    default_format=ConfigFormats.PY,
    py_config_imports=[
        "from tests.fixtures.cliconfs import my_cli_func",
        "DynamicConfig = my_cli_func.model_cls",
    ],
)
