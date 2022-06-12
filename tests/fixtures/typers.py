import typer

single_command_typer = typer.Typer()


@single_command_typer.command()
def my_cli_func(
    a: str,
    b: int = typer.Argument(..., help="b help"),
    c: float = typer.Option(3.2, help="c help"),
):
    print(a, b, c)


if __name__ == "__main__":
    single_command_typer()
