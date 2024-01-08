from typing import List

from antlr4 import (
    CommonTokenStream,
    FileStream,
    InputStream,
)
from pylasu.model import Node
from pylasu.validation import Issue, IssueType, Result

from slang.parser.antlr.SlangLexer import SlangLexer as AntlrSlangLexer
from slang.parser.antlr.SlangParser import SlangParser as AntlrSlangParser
from slang.parser.pylasu.errors import SlangErrorListener
from slang.parser.pylasu.transformations import slang_parse_tree_to_ast


def parse_string(code: str) -> Result:
    """
    Parses slang code from a string and returns back the corresponding
    abstract syntax tree (AST) with a list of possible issues encountered in the process.

    :param code: the string containing the slang code to parse
    :type code: str
    :return: the corresponding AST root and a list of possible issues encountered while parsing
    :rtype: Result
    """
    return parse_input_stream(InputStream(code))


def parse_file(filename: str) -> Result:
    """
    Parses slang code from a file and returns back the corresponding
    abstract syntax tree (AST) with a list of possible issues encountered in the process.

    :param filename: the name of the file containing the slang code to parse
    :type filename: str
    :return: the corresponding AST root and a list of possible issues encountered while parsing
    :rtype: Result
    """
    return parse_input_stream(FileStream(filename))


def parse_input_stream(input_stream: InputStream):
    """
    Parses slang code from an input stream and returns back the corresponding
    abstract syntax tree (AST) with a list of possible issues encountered in the process.

    :param input_stream: the input stream containing the slang code to parse
    :type input_stream: InputStream
    :return: the corresponding AST root and a list of possible issues encountered while parsing
    :rtype: Result
    """
    issues: List[Issue] = []
    parse_tree = _build_slang_parse_tree(input_stream, issues)
    abstract_syntax_tree = _build_slang_abstract_syntax_tree(parse_tree, issues)
    return _build_pylasu_parse_result(abstract_syntax_tree, issues)


def _build_slang_parse_tree(input_stream: InputStream, issues: List[Issue]):
    return _slang_antlr_parser(input_stream, issues).workspace()


def _build_slang_abstract_syntax_tree(
    parse_tree: AntlrSlangParser.WorkspaceContext, issues: List[Issue]
):
    return slang_parse_tree_to_ast(parse_tree, issues)


def _slang_antlr_parser(input_stream: InputStream, issues: List[Issue]):
    lexer = _slang_antlr_lexer(input_stream, issues)
    parser = AntlrSlangParser(CommonTokenStream(lexer))
    parser.removeErrorListeners()
    parser.addErrorListener(SlangErrorListener(issue_type=IssueType.SYNTACTIC, issues=issues))
    return parser


def _slang_antlr_lexer(input_stream: InputStream, issues: List[Issue]):
    lexer = AntlrSlangLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(SlangErrorListener(issue_type=IssueType.LEXICAL, issues=issues))
    return lexer


def _build_pylasu_parse_result(root: Node, issues: List[Issue]):
    result = Result(root=root)
    result.issues = issues
    return result
