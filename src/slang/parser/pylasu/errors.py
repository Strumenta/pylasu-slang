from typing import List

from antlr4.error.ErrorListener import ErrorListener
from pylasu.validation.validation import Issue, IssueType


class SlangErrorListener(ErrorListener):
    issues: List[Issue] = []

    def __init__(self, issue_type: IssueType, issues: List[Issue]):
        self.issue_type = issue_type
        self.issues = issues

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.issues.append(Issue(type=self.issue_type, message=msg))
