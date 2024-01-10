from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from json import dumps
from pathlib import Path

from pylasu.astruntime import Result
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from typer import Argument, Typer
from typing_extensions import Annotated

from slang.ast.serializers import serialize_result
from slang.parser import parse_file, parse_string

app = Typer()
parser_app = Typer()
app.add_typer(parser_app, name="parse", help="Parse Slang code from strings or files.")


def track_progress(description: str):
    def track_progress_decorator(func):
        @wraps(func)
        def track_progress_handler(*args, **kwargs):
            console = Console()
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=None),
                TimeElapsedColumn(),
                console=console,
            ) as progress, ThreadPoolExecutor() as executor:
                task_progress = progress.add_task(f"[green]{description}", total=None)
                task_future = executor.submit(func, *args, **kwargs)
                while not task_future.done():
                    progress.update(task_progress, advance=1)
                    try:
                        task_future.result(timeout=0.2)
                    except (TimeoutError, Exception):
                        continue
                task_result = task_future.result()
            console.print(task_result)

        return track_progress_handler

    return track_progress_decorator


def build_report(parse_result: Result):
    return dumps(serialize_result(parse_result), sort_keys=False, indent=2)


@parser_app.command("string", help="Parse Slang code from a string.")
@track_progress(description="Parsing")
def from_string(code: Annotated[str, Argument(help="The string containing Slang code.")]):
    return build_report(parse_string(code))


@parser_app.command("file", help="Parse Slang code from a file.")
@track_progress(description="Parsing")
def from_file(path: Annotated[Path, Argument(help="The path of the file containing Slang code.")]):
    return build_report(parse_file(str(path.absolute())))
