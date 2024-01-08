from pathlib import Path

import pytest
from pylasu.model import Node
from slang.ast.nodes import (
    Addition,
    Conditional,
    Function,
    Invocation,
    LessThanEquals,
    Literal,
    Reference,
    Return,
    Subtraction,
    Workspace,
)
from slang.ast.serializers import serialize_node
from slang.parser import parse_file, parse_string


@pytest.fixture()
def check_ast_from_string():
    def _(filename: str, expected: Node):
        code = (Path(__file__).parent / "data" / f"{filename}.slang").read_text()
        result = parse_string(code)
        assert len(result.issues) == 0
        assert serialize_node(
            result.root,
            with_position=False,
        ) == serialize_node(
            expected,
            with_position=False,
        )

    return _


@pytest.fixture()
def check_ast_from_file():
    def _(filename: str, expected: Node):
        filepath = str((Path(__file__).parent / "data" / f"{filename}.slang").absolute())
        result = parse_file(filepath)
        assert len(result.issues) == 0
        assert serialize_node(
            result.root,
            with_position=False,
        ) == serialize_node(
            expected,
            with_position=False,
        )

    return _


def test_slang_parse_string(check_ast_from_string):
    check_ast_from_string("fibonacci", FIBONACCI_WORKSPACE)


def test_slang_parse_file(check_ast_from_file):
    check_ast_from_file("fibonacci", FIBONACCI_WORKSPACE)


FIBONACCI_WORKSPACE = Workspace(
    functions=[
        Function(
            name="fibonacci",
            parameters=["n"],
            statements=[
                Conditional(
                    condition=LessThanEquals(
                        left=Reference(target="n"),
                        right=Literal(value="1"),
                    ),
                    positive_branch=[
                        Return(
                            value=Reference(target="n"),
                        ),
                    ],
                    negative_branch=[
                        Return(
                            Addition(
                                left=Invocation(
                                    target="fibonacci",
                                    arguments=[
                                        Subtraction(
                                            left=Reference(target="n"),
                                            right=Literal(value="1"),
                                        )
                                    ],
                                ),
                                right=Invocation(
                                    target="fibonacci",
                                    arguments=[
                                        Subtraction(
                                            left=Reference(target="n"),
                                            right=Literal(value="2"),
                                        )
                                    ],
                                ),
                            )
                        )
                    ],
                )
            ],
        )
    ]
)
