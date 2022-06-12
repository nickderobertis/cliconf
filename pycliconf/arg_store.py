from typing import Any, Dict, List

from pydantic import BaseModel, Field


class CommandArgs(BaseModel):
    prog_name: str
    passed_args: List[Any]
    params: Dict[str, Any]

    @property
    def passed_as_kwargs(self) -> Dict[str, Any]:
        # TODO: Need a more resilient way to get the kwargs
        #  This will fail when multiple arguments have the same value,
        #  or when any passed value matches a kwarg default
        return {k: v for k, v in self.params.items() if str(v) in self.passed_args}


class ArgumentStore(BaseModel):
    """
    This class is used to store the arguments that are passed to the CLI.
    """

    commands: Dict[str, CommandArgs] = Field(default_factory=dict)

    def add_command(self, prog_name: str, args: List[str], params: Dict[str, Any]):
        self.commands[prog_name] = CommandArgs(
            prog_name=prog_name, passed_args=args, params=params
        )

    def remove_command(self, prog_name: str):
        del self.commands[prog_name]

    def __getitem__(self, item):
        return self.commands[item]


ARGS_STORE = ArgumentStore()
