lexer grammar ElanLexer;

PROC        : [Pp][Rr][Oo][Cc];
ENDPROC     : [Ee][Nn][Dd][Pp][Rr][Oo][Cc];
END         : [Ee][Nn][Dd];
OP          : [Oo][Pf];
ENDOP       : [Ee][Nn][Dd][Oo][Pp];

TYPE        : [Tt][Yy][Pp][Ee];
STRUCT      : [Ss][Tt][Rr][Uu][Cc][Tt];
ROW         : [Rr][Oo][Ww];
OF          : [Oo][Ff];

INT         : [Ii][Nn][Tt];
REAL        : [Rr][Ee][Aa][Ll];
TEXT        : [Tt][Ee][Xx][Tt];
BOOL        : [Bb][Oo][Oo][Ll];
CHAR        : [Cc][Hh][Aa][Rr];
VOID        : [Vv][Oo][Ii][Dd];

VAR         : [Vv][Aa][Rr];
CONST       : [Cc][Oo][Nn][Ss][Tt];
LET         : [Ll][Ee][Tt];

IF          : [Ii][Ff];
THEN        : [Tt][Hh][Ee][Nn];
ELIF        : [Ee][Ll][Ii][Ff];
ELSE        : [Ee][Ll][Ss][Ee];
FI          : [Ff][Ii];
ENDIF       : [Ee][Nn][Dd][Ii][Ff];

WHILE       : [Ww][Hh][Ii][Ll][Ee];
UNTIL       : [Uu][Nn][Tt][Ii][Ll];
FOR         : [Ff][Oo][Rr];
FROM        : [Ff][Rr][Oo][Mm];
UPTO        : [Uu][Pp][Tt][Oo];
DOWNTO      : [Dd][Oo][Ww][Nn][Tt][Oo];
REP         : [Rr][Ee][Pp];
REPEAT      : [Rr][Ee][Pp][Ee][Aa][Tt];
ENDREP      : [Ee][Nn][Dd][Rr][Ee][Pp];
ENDREPEAT   : [Ee][Nn][Dd][Rr][Ee][Pp][Ee][Aa][Tt];

LEAVE       : [Ll][Ee][Aa][Vv][Ee];
WITH        : [Ww][Ii][Tt][Hh];

TRUE        : [Tt][Rr][Uu][Ee];
FALSE       : [Ff][Aa][Ll][Ss][Ee];
NIL         : [Nn][Ii][Ll];

AND         : [Aa][Nn][Dd];
OR          : [Oo][Rr];
XOR         : [Xx][Oo][Rr];
NOT         : [Nn][Oo][Tt];
DIV         : [Dd][Ii][Vv];
MOD         : [Mm][Oo][Dd];

PACKET      : [Pp][Aa][Cc][Kk][Ee][Tt];
ENDPACKET   : [Ee][Nn][Dd][Pp][Aa][Cc][Kk][Ee][Tt];
USE         : [Uu][Ss][Ee];

LINE        : [Ll][Ii][Nn][Ee];
NEWLINE     : [Nn][Ee][Ww][Ll][Ii][Nn][Ee];
    
ASSIGN      : ':=';
LE          : '<=';
GE          : '>=';
NE          : '<>';
EQ          : '=';
LT          : '<';
GT          : '>';

PLUS        : '+';
MINUS       : '-';
STAR        : '*';
SLASH       : '/';

LPAREN      : '(';
RPAREN      : ')';
LBRACK      : '[';
RBRACK      : ']';
COMMA       : ',';
SEMI        : ';';
COLON       : ':';
DOT         : '.';

REAL_LITERAL
    : DIGIT+ '.' DIGIT+ EXPONENT?
    | DIGIT+ EXPONENT
    ;

INTEGER_LITERAL
    : DIGIT+
    ;

STRING_LITERAL
    : '"' ('""' | ~["\r\n])* '"'
    ;

CHAR_LITERAL
    : '\'' ('\'\'' | ~['\r\n]) '\''
    ;

IDENTIFIER
    : LETTER (LETTER | DIGIT | '_')*
    ;

COMMENT_PAREN : '(*' .*? '*)' -> skip ;
COMMENT_BRACE : '{' .*? '}'   -> skip ;

LINE_COMMENT  : '//' ~[\r\n]* -> skip ;

WS            : [ \t\r\n\f]+  -> skip ;

EXPONENT : [eE] [+-]? DIGIT+;
DIGIT    : [0-9];
LETTER   : [A-Za-z_];
