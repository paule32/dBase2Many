lexer grammar PasDocLexer;

UNIT            : [uU][nN][iI][tT];
INTERFACE       : [iI][nN][tT][eE][rR][fF][aA][cC][eE];
IMPLEMENTATION  : [iI][mM][pP][lL][eE][mM][eE][nN][tT][aA][tT][iI][oO][nN];
TYPE            : [tT][yY][pP][eE];
CLASS           : [cC][lL][aA][sS][sS];
RECORD          : [rR][eE][cC][oO][rR][dD];
END             : [eE][nN][dD];

PUBLIC          : [pP][uU][bB][lL][iI][cC];
PRIVATE         : [pP][rR][iI][vV][aA][tT][eE];
PROTECTED       : [pP][rR][oO][tT][eE][cC][tT][eE][dD];
PUBLISHED       : [pP][uU][bB][lL][iI][sS][hH][eE][dD];

PROCEDURE       : [pP][rR][oO][cC][eE][dD][uU][rR][eE];
FUNCTION        : [fF][uU][nN][cC][tT][iI][oO][nN];
CONSTRUCTOR     : [cC][oO][nN][sS][tT][rR][uU][cC][tT][oO][rR];
DESTRUCTOR      : [dD][eE][sS][tT][rR][uU][cC][tT][oO][rR];

PROPERTY        : [pP][rR][oO][pP][eE][rR][tT][yY];
VIRTUAL         : [vV][iI][rR][tT][uU][aA][lL];
OVERRIDE        : [oO][vV][eE][rR][rR][iI][dD][eE];
ABSTRACT        : [aA][bB][sS][tT][rR][aA][cC][tT];
STATIC          : [sS][tT][aA][tT][iI][cC];
OVERLOAD        : [oO][vV][eE][rR][lL][oO][aA][dD];
REINTRODUCE     : [rR][eE][iI][nN][tT][rR][oO][dD][uU][cC][eE];

READ            : [rR][eE][aA][dD];
WRITE           : [wW][rR][iI][tT][eE];

CONST           : [cC][oO][nN][sS][tT];

IDENT           : [a-zA-Z_][a-zA-Z0-9_]*;
STRING          : '\'' (~['\r\n] | '\'\'')* '\'';

NUMBER          : '$' [0-9a-fA-F]+
                | [0-9]+ ('.' [0-9]+)?
                ;

DOC_COMMENT     : '(**!' .*? '*)'
                | '{**!' .*? '*}'
                ;

LINE_COMMENT    : '//' ~[\r\n]* -> channel(HIDDEN);
BRACE_COMMENT   : '{' .*? '}' -> channel(HIDDEN);
PAREN_COMMENT   : '(*' .*? '*)' -> channel(HIDDEN);

WS              : [ \t\r\n]+ -> channel(HIDDEN);

MINUS           : '-';
PLUS            : '+';

LPAREN          : '(';
RPAREN          : ')';
LBRACK          : '[';
RBRACK          : ']';
SEMI            : ';';
COLON           : ':';
COMMA           : ',';
DOT             : '.';
EQ              : '=';
CARET           : '^';

OTHER           : .;
