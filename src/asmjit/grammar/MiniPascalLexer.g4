lexer grammar MiniPascalLexer;

PROGRAM         : [Pp][Rr][Oo][Gg][Rr][Aa][Mm] ;
BEGIN_          : [Bb][Ee][Gg][Ii][Nn] ;
END             : [Ee][Nn][Dd] ;

LIBRARY         : [Ll][Ii][Bb][Rr][Aa][Rr][Yy] ;
UNIT            : [Uu][Nn][Ii][Tt] ;
INTERFACE       : [Ii][Nn][Tt][Ee][Rr][Ff][Aa][Cc][Ee] ;
IMPLEMENTATION  : [Ii][Mm][Pp][Ll][Ee][Mm][Ee][Nn][Tt][Aa][Tt][Ii][Oo][Nn] ;
USES            : [Uu][Ss][Ee][Ss] ;

CONST           : [Cc][Oo][Nn][Ss][Tt] ;
VAR             : [Vv][Aa][Rr] ;
TYPE            : [Tt][Yy][Pp][Ee] ;
RECORD          : [Rr][Ee][Cc][Oo][Rr][Dd] ;
ARRAY           : [Aa][Rr][Rr][Aa][Yy] ;
OF              : [Oo][Ff] ;
NIL             : [nN][iI][lL] ;

DOUBLE          : [Dd][Oo][Uu][Bb][Ll][Ee] ;
INTEGER         : [Ii][Nn][Tt][Ee][Gg][Ee][Rr] ;

CASE            : [Cc][Aa][Ss][Ee] ;
IF              : [iI][fF] ;
THEN            : [tT][hH][eE][nN] ;
ELSE            : [eE][lL][sS][eE] ;

BREAK           : [Bb][Rr][Ee][Aa][Kk] ;
CONTINUE        : [Cc][Oo][Nn][Tt][Ii][Nn][Uu][Ee] ;

NOT             : [nN][oO][tT] ;
AND             : [aA][nN][dD] ;
OR              : [oO][rR] ;
XOR             : [xX][oO][rR] ;

WHILE           : [wW][hH][iI][lL][eE] ;
DO              : [dD][oO] ;

REPEAT          : [Rr][Ee][Pp][Ee][Aa][Tt] ;
UNTIL           : [Uu][Nn][Tt][Ii][Ll] ;

FOR             : [Ff][Oo][Rr] ;
TO              : [Tt][Oo] ;
DOWNTO          : [Dd][Oo][Ww][Nn][Tt][Oo] ;

PROCEDURE       : [Pp][Rr][Oo][Cc][Ee][Dd][Uu][Rr][Ee] ;
FUNCTION        : [Ff][Uu][Nn][Cc][Tt][Ii][Oo][Nn] ;
RESULT          : [Rr][Ee][Ss][Uu][Ll][Tt] ;
EXIT            : [eE][xX][iI][tT] ;

TRY             : [Tt][Rr][Yy];
FINALLY         : [Ff][Ii][Nn][Aa][Ll][Ll][Yy];
EXCEPT          : [Ee][Xx][Cc][Ee][Pp][Tt];

CLASS           : [Cc][Ll][Aa][Ss][Ss] ;
CONSTRUCTOR     : [Cc][Oo][Nn][Ss][Tt][Rr][Uu][Cc][Tt][Oo][Rr] ;
DESTRUCTOR      : [Dd][Ee][Ss][Tt][Rr][Uu][Cc][Tt][Oo][Rr] ;

INHERITED       : [iI][nN][hH][eE][rR][iI][tT][eE][dD] ;

WRITELN         : [Ww][Rr][Ii][Tt][Ee][Ll][Nn] ;

DOTDOT          : '..'  ;
DOT             : '.'   ;

ASSIGN          : ':='  ;
COLON           : ':'   ;
SEMI            : ';'   ;
COMMA           : ','   ;
PLUS            : '+'   ;
MINUS           : '-'   ;
STAR            : '*'   ;
SLASH           : '/'   ;
LBRACK          : '['   ;
LPAREN          : '('   ;
RPAREN          : ')'   ;
RBRACK          : ']'   ;

CARET           : '^'   ;
AT              : '@'   ;

EQ_OP           : '='   ;
LE_OP           : '<='  ;
NE_OP           : '<>'  ;
LT_OP           : '<'   ;
GE_OP           : '>='  ;
GT_OP           : '>'   ;

STRING          : '\'' ( ~['\\] | '\\' . )* '\'' ;
    
IDENT           : [a-zA-Z_][a-zA-Z0-9_]* ;

HEXNUMBER       : '$' [0-9a-fA-F]+  ;
FLOATNUMBER     : [0-9]+ '.' [0-9]+ ;
NUMBER          : [0-9]+ ;

WS              : [ \t\r\n]+    -> skip ;
COMMENT1        : '//' ~[\r\n]* -> skip ;
COMMENT2        : '{' .*? '}'   -> skip ;
COMMENT3        : '(*' .*? '*)' -> skip ;
