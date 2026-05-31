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
    : assignment SEMI
    | writeLnStatement SEMI
    ;

assignment
    : IDENT ASSIGN expr
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
    : WRITELN LPAREN writeArgList? RPAREN
    ;

writeArgList
    : writeArg (COMMA writeArg)*
    ;

writeArg
    : STRING
    | expr
    ;
