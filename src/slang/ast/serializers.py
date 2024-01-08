import typing

import pylasu.model
from pylasu.astruntime import Result
from pylasu.model import Node
from pylasu.validation import Issue


def serialize_result(result: Result, with_position: bool = True):
    return {
        "issues": serialize_value(result.issues, with_position),
        "root": serialize_value(result.root, with_position),
    }


def serialize_value(value: object, with_position: bool = True):
    if isinstance(value, Result):
        return serialize_result(value, with_position)
    elif isinstance(value, Issue):
        return serialize_issue(value)
    if isinstance(value, Node):
        return serialize_node(value, with_position)
    elif isinstance(value, typing.Iterable) and not isinstance(value, str):
        return serialize_iterable(value, with_position)
    else:
        return value


def serialize_iterable(iterable: typing.Iterable, with_position: bool = True):
    return [serialize_value(item, with_position) for item in iterable]


def serialize_issue(issue: Issue):
    return {
        "type": issue.type.name if issue.type else None,
        "severity": issue.severity.name if issue.severity else None,
        "message": issue.message,
    }


def serialize_node(node: Node, with_position: bool = True):
    return {
        "#type": node.node_type.__name__,  # node.__class__.__name__,
        **dict([(p.name, serialize_value(p.value, with_position)) for p in node.properties]),
        "#position": serialize_position(node.position)
        if with_position and node.position
        else None,
    }


def serialize_position(position: pylasu.model.Position):
    return {"start": serialize_point(position.start), "end": serialize_point(position.end)}


def serialize_point(point: pylasu.model.Point):
    return {"line": point.line, "column": point.column}
