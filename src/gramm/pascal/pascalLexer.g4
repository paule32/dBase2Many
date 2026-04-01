lexer grammar pascalLexer;

// ------------------------------------------------------------
// Object Pascal / Delphi lexer seed for ANTLR4 (Python target)
// ------------------------------------------------------------

PROGRAM        : P R O G R A M ;
UNIT           : U N I T ;
LIBRARY        : L I B R A R Y ;
PACKAGE        : P A C K A G E ;
INTERFACE      : I N T E R F A C E ;
IMPLEMENTATION : I M P L E M E N T A T I O N ;
USES           : U S E S ;
CONST          : C O N S T ;
TYPE           : T Y P E ;
VAR            : V A R ;
THREADVAR      : T H R E A D V A R ;
LABEL          : L A B E L ;
RESOURCESTRING : R E S O U R C E S T R I N G ;
BEGIN          : B E G I N ;
END            : E N D ;
INITIALIZATION : I N I T I A L I Z A T I O N ;
FINALIZATION   : F I N A L I Z A T I O N ;
PROCEDURE      : P R O C E D U R E ;
FUNCTION       : F U N C T I O N ;
CONSTRUCTOR    : C O N S T R U C T O R ;
DESTRUCTOR     : D E S T R U C T O R ;
CLASS          : C L A S S ;
RECORD         : R E C O R D ;
OBJECT         : O B J E C T ;
ARRAY          : A R R A Y ;
SET            : S E T ;
FILE           : F I L E ;
OF             : O F ;
PROPERTY       : P R O P E R T Y ;
READ           : R E A D ;
WRITE          : W R I T E ;
DEFAULT        : D E F A U L T ;
INDEX          : I N D E X ;
DISPID         : D I S P I D ;
STORED         : S T O R E D ;
IMPLEMENTS     : I M P L E M E N T S ;
PRIVATE        : P R I V A T E ;
PROTECTED      : P R O T E C T E D ;
PUBLIC         : P U B L I C ;
PUBLISHED      : P U B L I S H E D ;
AUTOMATED      : A U T O M A T E D ;
STRICT         : S T R I C T ;
FORWARD        : F O R W A R D ;
OVERLOAD       : O V E R L O A D ;
OVERRIDE       : O V E R R I D E ;
REINTRODUCE    : R E I N T R O D U C E ;
VIRTUAL        : V I R T U A L ;
ABSTRACT       : A B S T R A C T ;
STATIC         : S T A T I C ;
INLINE         : I N L I N E ;
OPERATOR       : O P E R A T O R ;
OUT            : O U T ;
IN             : I N ;
NIL            : N I L ;
TRUE           : T R U E ;
FALSE          : F A L S E ;
IF             : I F ;
THEN           : T H E N ;
ELSE           : E L S E ;
CASE           : C A S E ;
WHILE          : W H I L E ;
DO             : D O ;
REPEAT         : R E P E A T ;
UNTIL          : U N T I L ;
FOR            : F O R ;
TO             : T O ;
DOWNTO         : D O W N T O ;
WITH           : W I T H ;
TRY            : T R Y ;
EXCEPT         : E X C E P T ;
FINALLY        : F I N A L L Y ;
RAISE          : R A I S E ;
ON             : O N ;
AS             : A S ;
IS             : I S ;
NOT            : N O T ;
AND            : A N D ;
OR             : O R ;
XOR            : X O R ;
DIV            : D I V ;
MOD            : M O D ;
SHL            : S H L ;
SHR            : S H R ;
BREAK          : B R E A K ;
CONTINUE       : C O N T I N U E ;
EXIT           : E X I T ;
GOTO           : G O T O ;
REQUIRES       : R E Q U I R E S ;
CONTAINS       : C O N T A I N S ;

ASSIGN         : ':=' ;
LE             : '<=' ;
GE             : '>=' ;
NE             : '<>' ;
DOTDOT         : '..' ;
LPAREN         : '(' ;
RPAREN         : ')' ;
LBRACK         : '[' ;
RBRACK         : ']' ;
COMMA          : ',' ;
SEMI           : ';' ;
COLON          : ':' ;
DOT            : '.' ;
PLUS           : '+' ;
MINUS          : '-' ;
STAR           : '*' ;
SLASH          : '/' ;
EQ             : '=' ;
LT             : '<' ;
GT             : '>' ;
AT             : '@' ;
CARET          : '^' ;

STRING_LITERAL
    : '\'' ( '\'\'' | ~'\'' )* '\''
    ;

HEX_NUMBER
    : '$' [0-9A-Fa-f]+
    ;

REAL_NUMBER
    : [0-9]+ '.' [0-9]+ ([eE] [+-]? [0-9]+)?
    | [0-9]+ [eE] [+-]? [0-9]+
    ;

INTEGER_NUMBER
    : [0-9]+
    ;

IDENT
    : [A-Za-z_] [A-Za-z_0-9]*
    ;

LINE_COMMENT
    : '//' ~[\r\n]* -> skip
    ;

BRACE_COMMENT
    : '{' .*? '}' -> skip
    ;

PAREN_COMMENT
    : '(*' .*? '*)' -> skip
    ;

WS
    : [ \t\r\n\f]+ -> skip
    ;

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
