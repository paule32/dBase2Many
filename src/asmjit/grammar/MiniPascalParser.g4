parser grammar MiniPascalParser;

options {
    tokenVocab = MiniPascalLexer;
}

programFile
    : PROGRAM IDENT SEMI varSection? procedureDeclaration* block DOT
    ;

procedureDeclaration
    : PROCEDURE IDENT formalParamList? SEMI block SEMI?
    ;

formalParamList
    : LPAREN formalParam (SEMI formalParam)* RPAREN
    ;

formalParam
    : identList COLON typeName
    ;

procedureCallStatement
    : IDENT actualParamList? SEMI?
    ;

actualParamList
    : LPAREN actualParam (COMMA actualParam)* RPAREN
    ;

actualParam
    : STRING
    | expr
    ;

varSection
    : VAR varDeclaration+
    ;

varDeclaration
    : identList COLON typeName SEMI
    ;

identList
    : IDENT (COMMA IDENT)*
    ;

typeName
    : DOUBLE
    | INTEGER
    | IDENT
    ;

block
    : BEGIN_ statementList END
    ;

statementList
    : (statement SEMI?)* 
    ;

statement
    : assignment
    | writeLnStatement
    | ifStatement
    | whileStatement
    | repeatStatement
    | forStatement
    | procedureCallStatement
    | compoundStatement
    ;

forStatement
    : FOR IDENT ASSIGN expr (TO | DOWNTO) expr DO statement
    ;

repeatStatement
    : REPEAT statementList UNTIL condition SEMI?
    ;

argumentList
    : expr (COMMA expr)*
    ;

whileStatement
    : WHILE condition DO statement
    ;

ifStatement
    : IF condition THEN statement (ELSE statement)?
    ;

condition
    : expr compareOp expr
    ;

compareOp
    : EQ_OP
    | NE_OP
    | LT_OP
    | LE_OP
    | GT_OP
    | GE_OP
    ;

compoundStatement
    : BEGIN_ statementList END
    ;

assignment
    : IDENT ASSIGN expr SEMI?
    ;

expr
    : term ((PLUS | MINUS) term)*
    ;

term
    : factor ((STAR | SLASH) factor)*
    ;

factor
    : NUMBER
    | FLOATNUMBER
    | HEXNUMBER
    | IDENT
    | LPAREN expr RPAREN
    ;

writeLnStatement
    : WRITELN LPAREN writeArgList? RPAREN SEMI?
    ;

writeArgList
    : writeArg (COMMA writeArg)*
    ;

writeArg
    : STRING
    | expr
    ;
