lexer grammar MiniPascalLexer;

PROGRAM : [Pp][Rr][Oo][Gg][Rr][Aa][Mm] ;
BEGIN_  : [Bb][Ee][Gg][Ii][Nn] ;
END     : [Ee][Nn][Dd] ;

VAR     : [Vv][Aa][Rr] ;
DOUBLE  : [Dd][Oo][Uu][Bb][Ll][Ee] ;
INTEGER : [Ii][Nn][Tt][Ee][Gg][Ee][Rr] ;

WRITELN : [Ww][Rr][Ii][Tt][Ee][Ll][Nn] ;

ASSIGN  : ':=' ;
COLON   : ':' ;
SEMI    : ';' ;
DOT     : '.' ;
COMMA   : ',' ;
PLUS    : '+' ;
MINUS   : '-' ;
STAR    : '*' ;
SLASH   : '/' ;
LPAREN  : '(' ;
RPAREN  : ')' ;

STRING  : '\'' ( ~['\\] | '\\' . )* '\'' ;
    
IDENT   : [a-zA-Z_] [a-zA-Z_0-9]* ;

HEXNUMBER   : '$' [0-9a-fA-F]+  ;
FLOATNUMBER : [0-9]+ '.' [0-9]+ ;
NUMBER      : [0-9]+ ;

WS      : [ \t\r\n]+    -> skip ;
COMMENT1: '//' ~[\r\n]* -> skip ;
COMMENT2: '{' .*? '}'   -> skip ;
COMMENT3: '(*' .*? '*)' -> skip ;
