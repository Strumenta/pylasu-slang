from pathlib import Path

import pytest


@pytest.fixture()
def get_absolute_path():
    def _(file_path: str):
        return (Path(__file__).parent / file_path).absolute()

    return _


@pytest.fixture()
def get_file():
    def _(file_path: str):
        return (Path(__file__).parent / file_path).read_text()

    return _
