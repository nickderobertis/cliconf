from typing import Optional, Type

from pyappconf import AppConfig, BaseConfig
from pydantic import BaseConfig as PydanticBaseConfig
from pydantic import create_model


def create_cli_base_config_class(
    base_cls: Type[BaseConfig], settings: Optional[AppConfig] = None
) -> Type[BaseConfig]:
    settings = settings or base_cls._settings
    prefix = _create_default_env_prefix(settings)

    class CLIBaseConfig(base_cls):
        class Config:
            env_prefix = prefix

    return CLIBaseConfig


def _create_default_env_prefix(settings: AppConfig) -> str:
    return settings.app_name.replace("-", "_").replace(" ", "_").upper() + "_"
