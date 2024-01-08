lexer grammar SlangLexer;

// comments (ignored)
COMMENT: '#' ~[\r\n]* -> skip;

// keywords
ELSE: 'else';
FUNCTION: 'function';
IF: 'if';
PRINT: 'print';
RETURN: 'return';

// operators
GTQ: '>=';
LTQ: '<=';
EQ: '==';
NQ: '!=';
GT: '>';
LT: '<';
NOT: '!';
ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
BND: '=';

// groupings
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';

// delimiters
COMMA: ',';
COLON: ';';

// identifiers
NAME: [a-z][a-zA-Z]*;

// literals
NUMBER: '0'|[1-9][0-9]*;

// whitespaces (ignored)
WHITESPACE: [\t\n\r ] -> skip;