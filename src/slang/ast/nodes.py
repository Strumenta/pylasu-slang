from dataclasses import dataclass, field
from typing import List, Optional

from pylasu.model import Node


@dataclass
class Workspace(Node):
    functions: List["Function"] = field(default_factory=list)
    statements: List["Statement"] = field(default_factory=list)


@dataclass
class Function(Node):
    name: str = field(default_factory=str)
    parameters: List[str] = field(default_factory=list)
    statements: List["Statement"] = field(default_factory=list)


@dataclass
class Statement(Node):
    pass


@dataclass
class Return(Statement):
    value: Optional["Expression"] = field(default=None)


@dataclass
class Print(Statement):
    argument: Optional["Expression"] = field(default=None)


@dataclass
class Conditional(Statement):
    condition: Optional["Expression"] = field(default=None)
    positive_branch: List["Statement"] = field(default_factory=list)
    negative_branch: List["Statement"] = field(default_factory=list)


@dataclass
class Binding(Statement):
    name: str = field(default_factory=str)
    value: Optional["Expression"] = field(default=None)


@dataclass
class Expression(Statement):
    pass


@dataclass
class UnaryOperation(Expression):
    operand: Optional["Expression"] = field(default=None)


@dataclass
class Not(UnaryOperation):
    pass


@dataclass
class Plus(UnaryOperation):
    pass


@dataclass
class Minus(UnaryOperation):
    pass


@dataclass
class BinaryOperation(Expression):
    left: Optional[Expression] = field(default=None)
    right: Optional[Expression] = field(default=None)


@dataclass
class Multiplication(BinaryOperation):
    pass


@dataclass
class Division(BinaryOperation):
    pass


@dataclass
class Addition(BinaryOperation):
    pass


@dataclass
class Subtraction(BinaryOperation):
    pass


@dataclass
class LessThan(BinaryOperation):
    pass


@dataclass
class GreaterThan(BinaryOperation):
    pass


@dataclass
class LessThanEquals(BinaryOperation):
    pass


@dataclass
class GreaterThanEquals(BinaryOperation):
    pass


@dataclass
class Equals(BinaryOperation):
    pass


@dataclass
class NotEquals(BinaryOperation):
    pass


@dataclass
class Invocation(Expression):
    target: str = field(default_factory=str)
    arguments: List["Expression"] = field(default_factory=list)


@dataclass
class Reference(Expression):
    target: str = field(default_factory=str)


@dataclass
class Literal(Expression):
    value: str = field(default_factory=str)


@dataclass
class WhileLoop(Statement):
    condition: Optional["Expression"] = field(default=None)
    statements: List["Statement"] = field(default_factory=list)

@dataclass
class ForLoop(Statement):
    variable: str = field(default_factory=str)
    start: Optional["Expression"] = field(default=None)
    end: Optional["Expression"] = field(default=None)
    interval: Optional["Expression"] = field(default=None)
    statements: List["Statement"] = field(default_factory=list)