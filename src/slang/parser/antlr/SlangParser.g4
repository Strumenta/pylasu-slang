parser grammar SlangParser;

options { tokenVocab=SlangLexer; }

workspace:
    functions+=function*
    statements+=statement*
;

function:
    FUNCTION name=NAME
    LPAREN (parameters+=NAME (COMMA parameters+=NAME)*)? RPAREN
    LBRACE statements+=statement* RBRACE
;

statement
    : RETURN value=expression COLON                                                         #returnStatement
    | PRINT argument=expression COLON                                                       #printStatement
    | IF LPAREN condition=expression RPAREN                     
        (LBRACE positive_branch+=statement* RBRACE | positive_branch+=statement)
        (ELSE (LBRACE negative_branch+=statement* RBRACE | negative_branch+=statement))?    #conditionalStatement
    | name=NAME BND value=expression COLON                                                  #bindingStatement
    | expression COLON                                                                      #expressionStatement
    ;

expression
    : LPAREN expression RPAREN                                                              #groupingExpression
    | operator=(NOT|ADD|SUB) operand=expression                                             #unaryOperationExpression
    | left=expression operator=(MUL|DIV) right=expression                                   #binaryOperationExpression
    | left=expression operator=(ADD|SUB) right=expression                                   #binaryOperationExpression
    | left=expression operator=(LT|GT|GTQ|LTQ) right=expression                             #binaryOperationExpression
    | left=expression operator=(EQ|NQ) right=expression                                     #binaryOperationExpression
    | target=NAME LPAREN (arguments+=expression (COMMA arguments+=expression)*)? RPAREN     #invocationExpression
    | target=NAME                                                                           #referenceExpression
    | value=NUMBER                                                                          #literalExpression
    ;