from pathlib import Path
from typing import Optional, Type

from pyappconf import AppConfig, BaseConfig


def create_cli_base_config_class(
    base_cls: Type[BaseConfig], settings: Optional[AppConfig] = None
) -> Type[BaseConfig]:
    settings = settings or base_cls._settings
    prefix = _create_default_env_prefix(settings)

    class CLIBaseConfig(base_cls):  # type: ignore
        class Config:
            env_prefix = prefix

    return CLIBaseConfig


class CLIAppConfig(AppConfig):
    """
    Overrides some of the default settings for pyappconf to be more reasonable
    for what users would typically want to use in a CLI application.

    - Updates default folder to be the current directory
    - Outputs stub file for Python config format
    """

    def __init__(self, **kwargs):
        if "custom_config_folder" not in kwargs:
            kwargs["custom_config_folder"] = Path(".")
        if "py_config_generate_model_class_in_stub" not in kwargs:
            kwargs["py_config_generate_model_class_in_stub"] = True
        super().__init__(**kwargs)


def _create_default_env_prefix(settings: AppConfig) -> str:
    return settings.app_name.replace("-", "_").replace(" ", "_").upper() + "_"
