lexer grammar lispLexer;

fragment A : [aA] ;
fragment B : [bB] ;
fragment C : [cC] ;
fragment D : [dD] ;
fragment E : [eE] ;
fragment F : [fF] ;
fragment G : [gG] ;
fragment H : [hH] ;
fragment I : [iI] ;
fragment J : [jJ] ;
fragment K : [kK] ;
fragment L : [lL] ;
fragment M : [mM] ;
fragment N : [nN] ;
fragment O : [oO] ;
fragment P : [pP] ;
fragment Q : [qQ] ;
fragment R : [rR] ;
fragment S : [sS] ;
fragment T : [tT] ;
fragment U : [uU] ;
fragment V : [vV] ;
fragment W : [wW] ;
fragment X : [xX] ;
fragment Y : [yY] ;
fragment Z : [zZ] ;

LPAREN       : '(' ;
RPAREN       : ')' ;
QUOTE        : '\'' ;
BACKQUOTE    : '`' ;
COMMA_AT     : ',@' ;
COMMA        : ',' ;
DOT          : '.' ;
VECTOR_START : '#(' ;

AMP_OPTIONAL : '&optional' ;
AMP_REST     : '&rest' ;
AMP_KEY      : '&key' ;
AMP_AUX      : '&aux' ;

DEFUN        : D E F U N ;
LAMBDA       : L A M B D A ;
LETSTAR      : L E T '*' ;
LET          : L E T ;
IF           : I F ;
COND         : C O N D ;
PROGN        : P R O G N ;
SETQ         : S E T Q ;
DEFVAR       : D E F V A R ;
DEFPARAMETER : D E F P A R A M E T E R ;
DEFCONSTANT  : D E F C O N S T A N T ;
QUOTE_KW     : Q U O T E ;
FUNCTION_KW  : F U N C T I O N ;
NIL          : N I L ;
TRUE         : T ;
BOOLEAN      : '#t' | '#f' ;

CharacterLiteral
    : '#\\' ( 'Space' | 'Newline' | . )
    ;

Number
    : [+-]? [0-9]+ ('.' [0-9]+)? ([eE] [+-]? [0-9]+)?
    ;

StringLiteral
    : '"' ( EscapeSequence | ~["\\\r\n] )* '"'
    ;

SYMBOL
    : SymbolInitial SymbolSubsequent*
    ;

fragment SymbolInitial
    : [a-zA-Z_*/+\-<>=!?$%&~^:]
    ;

fragment SymbolSubsequent
    : SymbolInitial
    | [0-9.]
    ;

fragment EscapeSequence
    : '\\' [btnfr"\\]
    ;

LineComment  : ';' ~[\r\n]* -> skip ;
BlockComment : '#|' .*? '|#' -> skip ;
WS           : [ \t\r\n\f]+ -> skip ;
