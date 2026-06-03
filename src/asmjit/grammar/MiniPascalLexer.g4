lexer grammar MiniPascalLexer;

PROGRAM     : [Pp][Rr][Oo][Gg][Rr][Aa][Mm] ;
BEGIN_      : [Bb][Ee][Gg][Ii][Nn] ;
END         : [Ee][Nn][Dd] ;

VAR         : [Vv][Aa][Rr] ;
DOUBLE      : [Dd][Oo][Uu][Bb][Ll][Ee] ;
INTEGER     : [Ii][Nn][Tt][Ee][Gg][Ee][Rr] ;

IF          : [iI][fF];
THEN        : [tT][hH][eE][nN];
ELSE        : [eE][lL][sS][eE];

WHILE       : [wW][hH][iI][lL][eE];
DO          : [dD][oO];

REPEAT      : [Rr][Ee][Pp][Ee][Aa][Tt] ;
UNTIL       : [Uu][Nn][Tt][Ii][Ll] ;

FOR         : [Ff][Oo][Rr] ;
TO          : [Tt][Oo] ;
DOWNTO      : [Dd][Oo][Ww][Nn][Tt][Oo] ;

PROCEDURE   : [Pp][Rr][Oo][Cc][Ee][Dd][Uu][Rr][Ee] ;
FUNCTION    : [Ff][Uu][Nn][Cc][Tt][Ii][Oo][Nn] ;

WRITELN     : [Ww][Rr][Ii][Tt][Ee][Ll][Nn] ;

ASSIGN      : ':=' ;
COLON       : ':' ;
SEMI        : ';' ;
DOT         : '.' ;
COMMA       : ',' ;
PLUS        : '+' ;
MINUS       : '-' ;
STAR        : '*' ;
SLASH       : '/' ;
LPAREN      : '(' ;
RPAREN      : ')' ;

EQ_OP       : '='   ;
LE_OP       : '<='  ;
NE_OP       : '<>'  ;
LT_OP       : '<'   ;
GE_OP       : '>='  ;
GT_OP       : '>'   ;

STRING      : '\'' ( ~['\\] | '\\' . )* '\'' ;
    
IDENT       : [a-zA-Z_][a-zA-Z0-9_]* ;

HEXNUMBER   : '$' [0-9a-fA-F]+  ;
FLOATNUMBER : [0-9]+ '.' [0-9]+ ;
NUMBER      : [0-9]+ ;

WS          : [ \t\r\n]+    -> skip ;
COMMENT1    : '//' ~[\r\n]* -> skip ;
COMMENT2    : '{' .*? '}'   -> skip ;
COMMENT3    : '(*' .*? '*)' -> skip ;
