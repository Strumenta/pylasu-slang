from typing import Callable, List, Optional, cast

from pylasu.mapping.parse_tree_to_ast_transformer import (
    ParseTreeToASTTransformer as ParseTreeToAstTransformer,
)
from pylasu.model.processing import assign_parents
from pylasu.parsing.parse_tree import to_position
from pylasu.transformation.transformation import PropertyRef
from pylasu.validation import Issue, IssueSeverity, IssueType

from slang.ast.nodes import (
    Addition,
    BinaryOperation,
    Binding,
    Conditional,
    Division,
    Equals,
    Function,
    GreaterThan,
    GreaterThanEquals,
    Invocation,
    LessThan,
    LessThanEquals,
    Literal,
    Minus,
    Multiplication,
    Not,
    NotEquals,
    Plus,
    Print,
    Reference,
    Return,
    Subtraction,
    UnaryOperation,
    Workspace,
    WhileLoop,
    ForLoop
)
from slang.parser.antlr.SlangParser import SlangParser as _


def slang_parse_tree_to_ast(parse_tree: _.WorkspaceContext, issues: Optional[List[Issue]] = None):
    transformer = create_slang_parse_tree_to_ast_transformer(issues)
    abstract_syntax_tree = transformer.transform(parse_tree)
    assign_parents(abstract_syntax_tree)
    return cast(Optional[Workspace], abstract_syntax_tree)


def create_slang_parse_tree_to_ast_transformer(issues: Optional[List[Issue]]):
    transformer = ParseTreeToAstTransformer(allow_generic_node=False, issues=issues)

    # workspace (constructor-node-factory-with-child)
    (
        transformer.register_node_factory(_.WorkspaceContext, Workspace)
        .with_child(PropertyRef("functions"), PropertyRef("functions"))
        .with_child(PropertyRef("statements"), PropertyRef("statements"))
    )

    # function (def-node-factory)
    def function_node_factory(source: _.FunctionContext):
        function = Function()
        function.name = source.name.text
        function.parameters = [parameter.text for parameter in source.parameters]
        function.statements = [transformer.transform(statement) for statement in source.statements]
        return function

    transformer.register_node_factory(
        _.FunctionContext,
        function_node_factory,
    )

    # statement - return (constructor-node-factory-with-child)
    transformer.register_node_factory(
        _.ReturnStatementContext,
        Return,
    ).with_child(PropertyRef("value"), PropertyRef("value"))

    # statement - print (constructor-node-factory-with-child)
    transformer.register_node_factory(
        _.PrintStatementContext,
        Print,
    ).with_child(PropertyRef("argument"), PropertyRef("argument"))

    # statement - conditional (constructor-node-factory-with-child)
    (
        transformer.register_node_factory(_.ConditionalStatementContext, Conditional)
        .with_child(PropertyRef("condition"), PropertyRef("condition"))
        .with_child(PropertyRef("positive_branch"), PropertyRef("positive_branch"))
        .with_child(PropertyRef("negative_branch"), PropertyRef("negative_branch"))
    )

    # statement - binding (lambda-node-factory-with-child)
    transformer.register_node_factory(
        _.BindingStatementContext,
        lambda source: Binding(name=source.name.text),
    ).with_child(PropertyRef("value"), PropertyRef("value"))

    # statement - expression (lambda-node-factory)
    transformer.register_node_factory(
        _.ExpressionStatementContext,
        lambda source: transformer.transform(source.expression()),
    )

    # expression - grouping (lambda-node-factory)
    transformer.register_node_factory(
        _.GroupingExpressionContext,
        lambda source: transformer.transform(source.expression()),
    )

    # expression - unary_operation (def-node-factory)
    def unary_operation_node_factory(source: _.UnaryOperationExpressionContext):
        def build_unary_operation(unary_operation_constructor: Callable[[], UnaryOperation]):
            unary_operation = unary_operation_constructor()
            unary_operation.expression = transformer.transform(source.operand)
            return unary_operation

        if source.NOT():
            return build_unary_operation(Not)
        elif source.ADD():
            return build_unary_operation(Plus)
        elif source.SUB():
            return build_unary_operation(Minus)
        else:
            issues.append(
                Issue(
                    IssueType.SYNTACTIC,
                    f"Unsupported unary operation: {source.operator.text}",
                    IssueSeverity.ERROR,
                    to_position(source),
                )
            )
            return None

    transformer.register_node_factory(
        _.UnaryOperationExpressionContext,
        unary_operation_node_factory,
    )

    # expression - binary_operation (def-node-factory)
    def binary_operation_node_factory(source: _.BinaryOperationExpressionContext):
        def build_binary_operation(binary_operation_constructor: Callable[[], BinaryOperation]):
            binary_operation = binary_operation_constructor()
            binary_operation.left = transformer.transform(source.left)
            binary_operation.right = transformer.transform(source.right)
            return binary_operation

        if source.MUL():
            return build_binary_operation(Multiplication)
        elif source.DIV():
            return build_binary_operation(Division)
        elif source.ADD():
            return build_binary_operation(Addition)
        elif source.SUB():
            return build_binary_operation(Subtraction)
        elif source.LT():
            return build_binary_operation(LessThan)
        elif source.GT():
            return build_binary_operation(GreaterThan)
        elif source.LTQ():
            return build_binary_operation(LessThanEquals)
        elif source.GTQ():
            return build_binary_operation(GreaterThanEquals)
        elif source.EQ():
            return build_binary_operation(Equals)
        elif source.NQ():
            return build_binary_operation(NotEquals)
        else:
            issues.append(
                Issue(
                    IssueType.SYNTACTIC,
                    f"Unsupported binary operation: {source.operator.text}",
                    IssueSeverity.ERROR,
                    to_position(source),
                )
            )
            return None

    transformer.register_node_factory(
        _.BinaryOperationExpressionContext,
        binary_operation_node_factory,
    )

    # expression - invocation (declarative-lambda-getter)
    transformer.register_node_factory(
        _.InvocationExpressionContext,
        lambda source: Invocation(target=source.target.text),
    ).with_child(PropertyRef("arguments"), PropertyRef("arguments"))

    # expression - reference (declarative-lambda-getter)
    transformer.register_node_factory(
        _.ReferenceExpressionContext,
        lambda source: Reference(target=source.target.text),
    )

    # expression - literal (declarative-lambda-getter)
    transformer.register_node_factory(
        _.LiteralExpressionContext,
        lambda source: Literal(value=source.value.text),
    )

    #statement - while loop
    transformer.register_node_factory(
        _.WhileStatementContext,
        WhileLoop
    ).with_child(PropertyRef("condition"), PropertyRef("condition")
                 ).with_child(PropertyRef("statements"), PropertyRef("statements"))


    def for_loop_node_factory(source, transformer):
        for_loop = ForLoop(
            variable=source.variable.text,
            start=transformer.transform(source.start),
            end=transformer.transform(source.end),
            interval=transformer.transform(source.interval) if source.interval else 1,
            statements=[transformer.transform(stmt) for stmt in source.statements]
        )
        return for_loop

    # statement - for loop
    transformer.register_node_factory(
        _.ForStatementContext,
        for_loop_node_factory
    )

    return transformer


if __name__ == "__main__":
    from antlr4 import CommonTokenStream, InputStream

    from slang.parser.antlr.SlangLexer import SlangLexer as AntlrLexer
    from slang.parser.antlr.SlangParser import SlangParser as AntlrParser

    input_stream = InputStream(
        """
function test(n)
{
    if(n>0)
    {
    while (n<5)
    {
        for(i:0->n)
        {
            print(i);
            n=n+1;
        }
     }
    }  
}
    """
    )
    lexer = AntlrLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = AntlrParser(tokens)
    tree = parser.workspace()
    ast = cast(Workspace, slang_parse_tree_to_ast(tree))
    print(ast)
