lexer grammar BasicLexer;

// ---------------------------------------------------------------------------
// Comments
// ---------------------------------------------------------------------------
REM_COMMENT
    : R E M ([ \t]+ ~[\r\n]*)? -> skip
    ;

APOSTROPHE_COMMENT
    : '\'' ~[\r\n]* -> skip
    ;

// ---------------------------------------------------------------------------
// Keywords
// ---------------------------------------------------------------------------
AND         : A N D;
AS          : A S;
BOOLEAN     : B O O L E A N;
BYREF       : B Y R E F;
BYVAL       : B Y V A L;
CALL        : C A L L;
CONST       : C O N S T;
DIM         : D I M;
DO          : D O;
DOUBLE      : D O U B L E;
DOWNTO      : D O W N T O;
ELSE        : E L S E;
ELSEIF      : E L S E I F;
END         : E N D;
EXIT        : E X I T;
FALSE       : F A L S E;
FOR         : F O R;
FUNCTION    : F U N C T I O N;
GOSUB       : G O S U B;
GOTO        : G O T O;
IF          : I F;
INPUT       : I N P U T;
INTEGER_KW  : I N T E G E R;
LABEL       : L A B E L;
LET         : L E T;
LONG        : L O N G;
LOOP        : L O O P;
MOD         : M O D;
NEXT        : N E X T;
NOT         : N O T;
OR          : O R;
PRINT       : P R I N T;
RETURN      : R E T U R N;
SINGLE      : S I N G L E;
STEP        : S T E P;
STOP        : S T O P;
STRING_KW   : S T R I N G;
SUB         : S U B;
THEN        : T H E N;
TO          : T O;
TRUE        : T R U E;
UNTIL       : U N T I L;
WEND        : W E N D;
WHILE       : W H I L E;
XOR         : X O R;

// ---------------------------------------------------------------------------
// Literals
// ---------------------------------------------------------------------------
HEX_LITERAL
    : '&' [hH] [0-9a-fA-F]+
    ;

BINARY_LITERAL
    : '&' [bB] [01]+
    ;

FLOAT_LITERAL
    : DIGIT+ '.' DIGIT* EXPONENT?
    | '.' DIGIT+ EXPONENT?
    | DIGIT+ EXPONENT
    ;

INTEGER_LITERAL
    : DIGIT+
    ;

STRING_LITERAL
    : '"' ('""' | ~["\r\n])* '"'
    ;

// ---------------------------------------------------------------------------
// Operators
// ---------------------------------------------------------------------------

LE      : '<=';
GE      : '>=';
NE      : '<>' | '!=';
EQ      : '=';
LT      : '<';
GT      : '>';

PLUS    : '+';
MINUS   : '-';
STAR    : '*';
SLASH   : '/';
INTDIV  : '\\';
CARET   : '^';
AMP     : '&';

LPAREN  : '(';
RPAREN  : ')';
COMMA   : ',';
SEMI    : ';';
COLON   : ':';

// ---------------------------------------------------------------------------
// Identifiers
//
// Unterstützte BASIC-Typsuffixe:
//   Name$  String
//   Name%  Integer
//   Name!  Single
//   Name#  Double
// ---------------------------------------------------------------------------
IDENT
    : [a-zA-Z_] [a-zA-Z0-9_]* [$%#!]?
    ;

// ---------------------------------------------------------------------------
// Line handling
// ---------------------------------------------------------------------------
NEWLINE
    : '\r\n'
    | '\n'
    | '\r'
    ;

WS
    : [ \t\f]+ -> skip
    ;

// ---------------------------------------------------------------------------
// Fragments for case-insensitive keywords
// ---------------------------------------------------------------------------

fragment DIGIT    : [0-9];
fragment EXPONENT : [eE] [+\-]? DIGIT+;

fragment A : [aA];
fragment B : [bB];
fragment C : [cC];
fragment D : [dD];
fragment E : [eE];
fragment F : [fF];
fragment G : [gG];
fragment H : [hH];
fragment I : [iI];
fragment J : [jJ];
fragment K : [kK];
fragment L : [lL];
fragment M : [mM];
fragment N : [nN];
fragment O : [oO];
fragment P : [pP];
fragment Q : [qQ];
fragment R : [rR];
fragment S : [sS];
fragment T : [tT];
fragment U : [uU];
fragment V : [vV];
fragment W : [wW];
fragment X : [xX];
fragment Y : [yY];
fragment Z : [zZ];
