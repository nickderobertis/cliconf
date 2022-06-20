from typing import Any, Dict, Sequence, Type

import click
from click import Context, Parameter
from pyappconf import BaseConfig, ConfigFormats

from cliconf.settings import DEFAULT_SETTINGS


def create_generate_config_option(
    supported_formats: Sequence[ConfigFormats],
    default_format: ConfigFormats,
    model_cls: Type[BaseConfig],
    option_name: str = DEFAULT_SETTINGS.generate_config_option_name,
) -> click.Option:
    def gen_config(ctx: Context, param: Parameter, value: str) -> None:
        if len(supported_formats) == 1:
            use_format = default_format
        else:
            use_format = value

        if value and not ctx.resilient_parsing:
            if use_format != default_format:
                new_settings = model_cls._settings.copy(default_format=use_format)
                model_obj = model_cls(settings=new_settings)
            else:
                model_obj = model_cls()
            click.echo(f"Saving config to {model_obj.settings.config_location}")
            model_obj.save()
            ctx.exit()

    opt_flag = [f"--{option_name}"]
    common_kwargs: Dict[str, Any] = dict(
        help="Generate a config file from the command line arguments.",
        callback=gen_config,
    )

    if len(supported_formats) == 1:
        return click.Option(
            opt_flag,
            is_flag=True,
            **common_kwargs,
        )

    return click.Option(
        opt_flag,
        type=click.Choice(supported_formats),
        default=default_format,
        prompt="What format would you like to generate the config file in?",
        prompt_required=False,
        **common_kwargs,
    )
