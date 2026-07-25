lexer grammar ResourceLexer;

BEGIN       : B E G I N;
END         : E N D;
LANGUAGE    : L A N G U A G E;
CHARACTERISTICS : C H A R A C T E R I S T I C S;
VERSION     : V E R S I O N;

STRINGTABLE : S T R I N G T A B L E;
VERSIONINFO : V E R S I O N I N F O;
FILEVERSION : F I L E V E R S I O N;
PRODUCTVERSION : P R O D U C T V E R S I O N;
FILEFLAGSMASK : F I L E F L A G S M A S K;
FILEFLAGS   : F I L E F L A G S;
FILEOS      : F I L E O S;
FILETYPE    : F I L E T Y P E;
FILESUBTYPE : F I L E S U B T Y P E;
BLOCK       : B L O C K;
VALUE       : V A L U E;

MENU        : M E N U;
MENUEX      : M E N U E X;
MENUITEM    : M E N U I T E M;
POPUP       : P O P U P;
SEPARATOR   : S E P A R A T O R;
CHECKED     : C H E C K E D;
GRAYED      : G R A Y E D;
HELP        : H E L P;
INACTIVE    : I N A C T I V E;
MENUBARBREAK: M E N U B A R B R E A K;
MENUBREAK   : M E N U B R E A K;

ACCELERATORS: A C C E L E R A T O R S;
VIRTKEY     : V I R T K E Y;
ASCII       : A S C I I;
NOINVERT    : N O I N V E R T;
SHIFT       : S H I F T;
CONTROL     : C O N T R O L;
ALT         : A L T;

DIALOG      : D I A L O G;
DIALOGEX    : D I A L O G E X;
STYLE       : S T Y L E;
EXSTYLE     : E X S T Y L E;
CAPTION     : C A P T I O N;
CLASS       : C L A S S;
FONT        : F O N T;

AUTO3STATE  : A U T O '3' S T A T E;
AUTOCHECKBOX: A U T O C H E C K B O X;
AUTORADIOBUTTON: A U T O R A D I O B U T T O N;
CHECKBOX    : C H E C K B O X;
COMBOBOX    : C O M B O B O X;
CTEXT       : C T E X T;
DEFPUSHBUTTON: D E F P U S H B U T T O N;
EDITTEXT    : E D I T T E X T;
GROUPBOX    : G R O U P B O X;
ICONCONTROL : I C O N;
LISTBOX     : L I S T B O X;
LTEXT       : L T E X T;
PUSHBOX     : P U S H B O X;
PUSHBUTTON  : P U S H B U T T O N;
RADIOBUTTON : R A D I O B U T T O N;
RTEXT       : R T E X T;
SCROLLBAR   : S C R O L L B A R;
STATE3      : S T A T E '3';
USERBUTTON  : U S E R B U T T O N;

BITMAP      : B I T M A P;
CURSOR      : C U R S O R;
RCDATA      : R C D A T A;
HTML        : H T M L;
MANIFEST    : M A N I F E S T;
MESSAGETABLE: M E S S A G E T A B L E;
DLGINIT     : D L G I N I T;
AVI         : A V I;
TYPELIB     : T Y P E L I B;

MOVEABLE    : M O V E A B L E;
FIXED       : F I X E D;
PURE        : P U R E;
IMPURE      : I M P U R E;
PRELOAD     : P R E L O A D;
LOADONCALL  : L O A D O N C A L L;
DISCARDABLE : D I S C A R D A B L E;

LBRACE      : '{';
RBRACE      : '}';
LPAREN      : '(';
RPAREN      : ')';
COMMA       : ',';
PIPE        : '|';
AMP         : '&';
CARET       : '^';
TILDE       : '~';
PLUS        : '+';
MINUS       : '-';
STAR        : '*';
SLASH       : '/';
PERCENT     : '%';
LSHIFT      : '<<';
RSHIFT      : '>>';

WIDE_STRING : [lL] '"' (ESCAPE_SEQUENCE | ~["\\\r\n])* '"';
STRING      : '"' (ESCAPE_SEQUENCE | ~["\\\r\n])* '"';

INTEGER
    : '0' [xX] HEX_DIGIT+ [uUlL]*
    | '0' [oO] [0-7]+ [uUlL]*
    | [0-9]+ [uUlL]*
    ;

IDENTIFIER  : [A-Za-z_$@?] [A-Za-z0-9_$@?.]*;
NL          : '\r'? '\n';
WS          : [ \t\f]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;

fragment ESCAPE_SEQUENCE
    : '\\' (['"?\\abfnrtv] | [0-7] [0-7]? [0-7]? | [xX] HEX_DIGIT+)
    ;
fragment HEX_DIGIT : [0-9A-Fa-f];
fragment A:[aA]; fragment B:[bB]; fragment C:[cC]; fragment D:[dD];
fragment E:[eE]; fragment F:[fF]; fragment G:[gG]; fragment H:[hH];
fragment I:[iI]; fragment J:[jJ]; fragment K:[kK]; fragment L:[lL];
fragment M:[mM]; fragment N:[nN]; fragment O:[oO]; fragment P:[pP];
fragment Q:[qQ]; fragment R:[rR]; fragment S:[sS]; fragment T:[tT];
fragment U:[uU]; fragment V:[vV]; fragment W:[wW]; fragment X:[xX];
fragment Y:[yY]; fragment Z:[zZ];
