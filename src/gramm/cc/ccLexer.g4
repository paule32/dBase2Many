lexer grammar ccLexer;

PP_DIRECTIVE : '#' ~[\r\n]* ;

NAMESPACE    : 'namespace' ;
USING        : 'using' ;
TYPEDEF      : 'typedef' ;
CLASS        : 'class' ;
STRUCT       : 'struct' ;
ENUM         : 'enum' ;
UNION        : 'union' ;
PUBLIC       : 'public' ;
PRIVATE      : 'private' ;
PROTECTED    : 'protected' ;
VIRTUAL      : 'virtual' ;
OVERRIDE     : 'override' ;
FINAL        : 'final' ;
TEMPLATE     : 'template' ;
TYPENAME     : 'typename' ;
FRIEND       : 'friend' ;
INLINE       : 'inline' ;
EXPLICIT     : 'explicit' ;
EXTERN       : 'extern' ;
STATIC       : 'static' ;
MUTABLE      : 'mutable' ;
CONSTEXPR    : 'constexpr' ;
CONST        : 'const' ;
VOLATILE     : 'volatile' ;
AUTO         : 'auto' ;
VOID         : 'void' ;
BOOL         : 'bool' ;
CHAR         : 'char' ;
SHORT        : 'short' ;
INT          : 'int' ;
LONG         : 'long' ;
FLOAT        : 'float' ;
DOUBLE       : 'double' ;
SIGNED       : 'signed' ;
UNSIGNED     : 'unsigned' ;
IF           : 'if' ;
ELSE         : 'else' ;
SWITCH       : 'switch' ;
CASE         : 'case' ;
DEFAULT      : 'default' ;
FOR          : 'for' ;
WHILE        : 'while' ;
DO           : 'do' ;
BREAK        : 'break' ;
CONTINUE     : 'continue' ;
RETURN       : 'return' ;
GOTO         : 'goto' ;
TRY          : 'try' ;
CATCH        : 'catch' ;
THROW        : 'throw' ;
NEW          : 'new' ;
DELETE       : 'delete' ;
THIS         : 'this' ;
NULLPTR      : 'nullptr' ;
TRUE         : 'true' ;
FALSE        : 'false' ;
NOEXCEPT     : 'noexcept' ;
OPERATOR     : 'operator' ;
SIZEOF       : 'sizeof' ;

ELLIPSIS     : '...' ;
SCOPE        : '::' ;
ARROW        : '->' ;
ARROWSTAR    : '->*' ;
PLUSPLUS     : '++' ;
MINUSMINUS   : '--' ;
ANDAND       : '&&' ;
OROR         : '||' ;
LE           : '<=' ;
GE           : '>=' ;
EQ           : '==' ;
NE           : '!=' ;
PLUSEQ       : '+=' ;
MINUSEQ      : '-=' ;
STAREQ       : '*=' ;
DIVEQ        : '/=' ;
MODEQ        : '%=' ;
ANDEQ        : '&=' ;
OREQ         : '|=' ;
XOREQ        : '^=' ;
LSHIFTEQ     : '<<=' ;
RSHIFTEQ     : '>>=' ;
LSHIFT       : '<<' ;
RSHIFT       : '>>' ;

LPAREN       : '(' ;
RPAREN       : ')' ;
LBRACE       : '{' ;
RBRACE       : '}' ;
LBRACK       : '[' ;
RBRACK       : ']' ;
SEMI         : ';' ;
COMMA        : ',' ;
DOT          : '.' ;
COLON        : ':' ;
QUESTION     : '?' ;
ASSIGN       : '=' ;
PLUS         : '+' ;
MINUS        : '-' ;
STAR         : '*' ;
DIV          : '/' ;
MOD          : '%' ;
AMP          : '&' ;
PIPE         : '|' ;
CARET        : '^' ;
BANG         : '!' ;
TILDE        : '~' ;
LT           : '<' ;
GT           : '>' ;

IntegerLiteral
    : '0' [xX] [0-9a-fA-F]+ [uU]? [lL]{0,2}
    | '0' [bB] [01]+ [uU]? [lL]{0,2}
    | [0-9]+ [uU]? [lL]{0,2}
    ;

FloatingLiteral
    : [0-9]+ '.' [0-9]* ExponentPart? FloatSuffix?
    | '.' [0-9]+ ExponentPart? FloatSuffix?
    | [0-9]+ ExponentPart FloatSuffix?
    | [0-9]+ FloatSuffix
    ;

CharacterLiteral
    : '\'' ( EscapeSequence | ~['\\\r\n] ) '\''
    ;

StringLiteral
    : '"' ( EscapeSequence | ~["\\\r\n] )* '"'
    ;

Identifier
    : [a-zA-Z_] [a-zA-Z_0-9]*
    ;

fragment ExponentPart : [eE] [+-]? [0-9]+ ;
fragment FloatSuffix  : [fFlL] ;
fragment EscapeSequence
    : '\\' [btnfr"'\\]
    | '\\' [0-7]{1,3}
    | '\\' 'x' [0-9a-fA-F]+
    ;

LineComment  : '//' ~[\r\n]* -> skip ;
BlockComment : '/*' .*? '*/' -> skip ;
WS           : [ \t\r\n\f]+ -> skip ;
