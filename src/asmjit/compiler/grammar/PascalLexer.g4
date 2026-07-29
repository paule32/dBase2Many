lexer grammar PascalLexer;

PROGRAM             : [Pp][Rr][Oo][Gg][Rr][Aa][Mm] ;
BEGIN_              : [Bb][Ee][Gg][Ii][Nn] ;
END                 : [Ee][Nn][Dd] ;

LIBRARY             : [Ll][Ii][Bb][Rr][Aa][Rr][Yy] ;
UNIT                : [Uu][Nn][Ii][Tt] ;
INTERFACE           : [Ii][Nn][Tt][Ee][Rr][Ff][Aa][Cc][Ee] ;
IMPLEMENTATION      : [Ii][Mm][Pp][Ll][Ee][Mm][Ee][Nn][Tt][Aa][Tt][Ii][Oo][Nn] ;
USES                : [Uu][Ss][Ee][Ss] ;

EXPORTS             : [eE][xX][pP][oO][rR][tT][sS] ;
ORDINAL             : [Oo][Rr][Dd][Ii][Nn][Aa][Ll] ;

CONST               : [Cc][Oo][Nn][Ss][Tt] ;
VAR                 : [Vv][Aa][Rr] ;
TYPE                : [Tt][Yy][Pp][Ee] ;
PACKED              : [Pp][Aa][Cc][Kk][Ee][Dd] ;
RECORD              : [Rr][Ee][Cc][Oo][Rr][Dd] ;
ARRAY               : [Aa][Rr][Rr][Aa][Yy] ;
OF                  : [Oo][Ff] ;
NIL                 : [nN][iI][lL] ;

DOUBLE              : [Dd][Oo][Uu][Bb][Ll][Ee] ;
INTEGER             : [Ii][Nn][Tt][Ee][Gg][Ee][Rr] ;

CASE                : [Cc][Aa][Ss][Ee] ;
IF                  : [iI][fF] ;
THEN                : [tT][hH][eE][nN] ;
ELSE                : [eE][lL][sS][eE] ;

BREAK               : [Bb][Rr][Ee][Aa][Kk] ;
CONTINUE            : [Cc][Oo][Nn][Tt][Ii][Nn][Uu][Ee] ;

NOT                 : [nN][oO][tT] ;
AND                 : [Aa][Nn][Dd] ;
OR                  : [Oo][Rr] ;
XOR                 : [Xx][Oo][Rr] ;
SHL                 : [Ss][Hh][Ll] ;
SHR                 : [Ss][Hh][Rr] ;

WHILE               : [wW][hH][iI][lL][eE] ;
DO                  : [dD][oO] ;

REPEAT              : [Rr][Ee][Pp][Ee][Aa][Tt] ;
UNTIL               : [Uu][Nn][Tt][Ii][Ll] ;

FOR                 : [Ff][Oo][Rr] ;
TO                  : [Tt][Oo] ;
DOWNTO              : [Dd][Oo][Ww][Nn][Tt][Oo] ;

INC                 : [Ii][Nn][Cc] ;
DEC                 : [Dd][Ee][Cc] ;

LOW                 : [Ll][Oo][Ww] ;
HIGH                : [Hh][Ii][Gg][Hh] ;

POS                 : [Pp][Oo][Ss] ;
COPY                : [Cc][Oo][Pp][Yy] ;
LENGTH              : [Ll][Ee][Nn][Gg][Tt][Hh] ;
ASSIGNED            : [Aa][Ss][Ss][Ii][Gg][Nn][Ee][Dd] ;

PROCEDURE           : [Pp][Rr][Oo][Cc][Ee][Dd][Uu][Rr][Ee] ;
FUNCTION            : [Ff][Uu][Nn][Cc][Tt][Ii][Oo][Nn] ;
RESULT              : [Rr][Ee][Ss][Uu][Ll][Tt] ;
EXIT                : [eE][xX][iI][tT] ;

TRY                 : [Tt][Rr][Yy];
FINALLY             : [Ff][Ii][Nn][Aa][Ll][Ll][Yy];
EXCEPT              : [Ee][Xx][Cc][Ee][Pp][Tt];
RAISE               : [Rr][Aa][Ii][Ss][Ee];

CLASS               : [Cc][Ll][Aa][Ss][Ss] ;
CONSTRUCTOR         : [Cc][Oo][Nn][Ss][Tt][Rr][Uu][Cc][Tt][Oo][Rr] ;
DESTRUCTOR          : [Dd][Ee][Ss][Tt][Rr][Uu][Cc][Tt][Oo][Rr] ;

PRIVATE             : [pP][rR][iI][vV][aA][tT][eE] ;
PROTECTED           : [pP][rR][oO][tT][eE][cC][tT][eE][dD] ;
PUBLIC              : [pP][uU][bB][lL][iI][cC] ;
PUBLISHED           : [Pp][Uu][Bb][Ll][Ii][Ss][Hh][Ee][Dd] ;
PROPERTY            : [Pp][Rr][Oo][Pp][Ee][Rr][Tt][Yy] ;

VIRTUAL             : [Vv][Ii][Rr][Tt][Uu][Aa][Ll] ;
OVERRIDE            : [Oo][Vv][Ee][Rr][Rr][Ii][Dd][Ee] ;

READ                : [rR][eE][aA][dD] ;
WRITE               : [wW][rR][iI][tT][eE] ;

INHERITED           : [iI][nN][hH][eE][rR][iI][tT][eE][dD] ;

WRITELN             : [Ww][Rr][Ii][Tt][Ee][Ll][Nn] ;

BOOLEAN             : [Bb][Oo][Oo][Ll][Ee][Aa][Nn] ;
TRUE                : [Tt][Rr][Uu][Ee] ;
FALSE               : [Ff][Aa][Ll][Ss][Ee] ;

DISKFREE            : [dD][iI][sS][kK][fF][rR][eE][eE] ;
DISKTOTAL           : [dD][iI][sS][kK][tT][oO][tT][aA][lL] ;
DISKLABEL           : [dD][iI][sS][kK][lL][aA][bB][eE][lL] ;
DISKSERIAL          : [dD][iI][sS][kK][sS][eE][rR][iI][aA][lL] ;
DISKFILESYSTEM      : [dD][iI][sS][kK][fF][iI][lL][eE][sS][yY][sS][tT][eE][mM] ;
DISKTYPE            : [dD][iI][sS][kK][tT][yY][pP][eE] ;
DISKSHARE           : [dD][iI][sS][kK][sS][hH][aA][rR][eE] ;

CDECL               : [cC][dD][eE][cC][lL] ;
STDCALL             : [sS][tT][dD][cC][aA][lL][lL] ;
PASCAL              : [pP][aA][sS][cC][aA][lL] ;
EXTERNAL            : [Ee][Xx][Tt][Ee][Rr][Nn][Aa][Ll] ;
NAME                : [nN][aA][mM][eE] ;

COMPILER_DIRECTIVE  : '{$' .*? '}' ;
    
DOTDOT              : '..';
DOT                 : '.'   ;

ASSIGN              : ':='  ;
COLON               : ':'   ;
SEMI                : ';'   ;
COMMA               : ','   ;
PLUS                : '+'   ;
MINUS               : '-'   ;
STAR                : '*'   ;
SLASH               : '/'   ;
LBRACK              : '['   ;
LPAREN              : '('   ;
RPAREN              : ')'   ;
RBRACK              : ']'   ;

CARET               : '^'   ;
AT                  : '@'   ;

EQ_OP               : '='   ;
LE_OP               : '<='  ;
NE_OP               : '<>'  ;
LT_OP               : '<'   ;
GE_OP               : '>='  ;
GT_OP               : '>'   ;

STRING              : '\'' ( ~['\\] | '\\' . )* '\'' ;
CHARCODE            : '#'  ( '$' [0-9A-Fa-f]+ | [0-9]+ ) ;

FLOATNUMBER         : [0-9]+ '.' [0-9]+ ;
HEXNUMBER           : '$' [0-9a-fA-F]+  ;
NUMBER              : [0-9]+ ;

IDENT               : [a-zA-Z_][a-zA-Z0-9_]* ;

WS                  : [ \t\r\n]+    -> skip ;
COMMENT1            : '//' ~[\r\n]* -> skip ;
COMMENT2            : '{' .*? '}'   -> skip ;
COMMENT3            : '(*' .*? '*)' -> skip ;
