parser grammar MiniPascalParser;

options {
    tokenVocab = MiniPascalLexer;
}

programFile
    : PROGRAM IDENT SEMI varSection? block DOT EOF
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
    : statement*
    ;

statement
    : assignment
    | writeLnStatement
    | ifStatement
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
