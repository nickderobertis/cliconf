from typing import Any

import typer

from pycliconf.command import get_command


class CLIConf(typer.Typer):
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Overrides Typer's __call__ method to use pycliconf's get_command function.
        """
        return get_command(self)(*args, **kwargs)
