parser grammar ResourceParser;

options { tokenVocab=ResourceLexer; }

resourceScript
    : eol* resourceStatement* EOF
    ;

resourceStatement
    : languageStatement eol+
    | characteristicsStatement eol+
    | versionStatement eol+
    | stringTableResource eol*
    | versionInfoResource eol*
    | menuResource eol*
    | acceleratorsResource eol*
    | dialogResource eol*
    | fileResource eol+
    | rawResource eol*
    | eol+
    ;

languageStatement
    : LANGUAGE expression COMMA expression
    ;

characteristicsStatement
    : CHARACTERISTICS expression
    ;

versionStatement
    : VERSION expression
    ;

resourceId
    : INTEGER
    | IDENTIFIER
    | STRING
    ;

resourceType
    : INTEGER
    | IDENTIFIER
    | STRING
    ;

resourceOptions
    : (MOVEABLE | FIXED | PURE | IMPURE | PRELOAD | LOADONCALL | DISCARDABLE
      | LANGUAGE expression COMMA expression
      | CHARACTERISTICS expression
      | VERSION expression
      )*
    ;

fileResource
    : resourceId fileResourceKind resourceOptions stringLiteral
    ;

fileResourceKind
    : fileResourceType
    | resourceType
    ;

fileResourceType
    : BITMAP
    | ICONCONTROL
    | CURSOR
    | RCDATA
    | HTML
    | MANIFEST
    | MESSAGETABLE
    | FONT
    | DLGINIT
    | AVI
    | TYPELIB
    ;

rawResource
    : resourceId rawResourceType resourceOptions rawDataBlock
    ;

rawResourceType
    : resourceType
    | RCDATA
    | DLGINIT
    | HTML
    | MANIFEST
    ;

rawDataBlock
    : blockStart eol* rawDataItemList? eol* blockEnd
    ;

rawDataItemList
    : rawDataItem (separator rawDataItem)* separator?
    ;

rawDataItem
    : expression
    | stringLiteral
    ;

stringTableResource
    : STRINGTABLE resourceOptions eol* blockStart eol* stringEntry* blockEnd
    ;

stringEntry
    : expression stringLiteral eol+
    ;

versionInfoResource
    : resourceId VERSIONINFO resourceOptions eol*
      fixedVersionLine*
      blockStart eol* versionElement* blockEnd
    ;

fixedVersionLine
    : FILEVERSION quadExpression eol+
    | PRODUCTVERSION quadExpression eol+
    | FILEFLAGSMASK expression eol+
    | FILEFLAGS expression eol+
    | FILEOS expression eol+
    | FILETYPE expression eol+
    | FILESUBTYPE expression eol+
    ;

quadExpression
    : expression COMMA expression COMMA expression COMMA expression
    ;

versionElement
    : versionBlock
    | versionValue
    | eol+
    ;

versionBlock
    : BLOCK stringLiteral eol* blockStart eol* versionElement* blockEnd eol*
    ;

versionValue
    : VALUE stringLiteral COMMA versionValueItem (COMMA versionValueItem)* eol+
    ;

versionValueItem
    : expression
    | stringLiteral
    ;

menuResource
    : resourceId (MENU | MENUEX) resourceOptions eol*
      blockStart eol* menuItem* blockEnd
    ;

menuItem
    : MENUITEM SEPARATOR menuFlags? eol+
    | MENUITEM stringLiteral COMMA expression menuFlags? eol+
    | POPUP stringLiteral menuFlags? eol*
      blockStart eol* menuItem* blockEnd eol*
    ;

menuFlags
    : (COMMA? (CHECKED | GRAYED | HELP | INACTIVE | MENUBARBREAK | MENUBREAK | expression))+
    ;

acceleratorsResource
    : resourceId ACCELERATORS resourceOptions eol*
      blockStart eol* acceleratorEntry* blockEnd
    ;

acceleratorEntry
    : acceleratorKey COMMA expression acceleratorFlags? eol+
    ;

acceleratorKey
    : stringLiteral
    | expression
    ;

acceleratorFlags
    : (COMMA? (VIRTKEY | ASCII | NOINVERT | SHIFT | CONTROL | ALT))+
    ;

dialogResource
    : resourceId dialogKind resourceOptions
      expression COMMA expression COMMA expression COMMA expression eol+
      dialogHeaderLine*
      blockStart eol* dialogControl* blockEnd
    ;

dialogKind
    : DIALOG
    | DIALOGEX
    ;

dialogHeaderLine
    : STYLE expression eol+
    | EXSTYLE expression eol+
    | CAPTION stringLiteral eol+
    | CLASS resourceId eol+
    | MENU resourceId eol+
    | FONT expression COMMA stringLiteral
      (COMMA expression COMMA expression COMMA expression)? eol+
    | LANGUAGE expression COMMA expression eol+
    | CHARACTERISTICS expression eol+
    | VERSION expression eol+
    ;

dialogControl
    : CONTROL stringLiteral COMMA expression COMMA resourceId COMMA expression COMMA
      expression COMMA expression COMMA expression COMMA expression
      (COMMA expression)? eol+
    | controlWithText stringLiteral COMMA expression COMMA
      expression COMMA expression COMMA expression COMMA expression
      (COMMA expression (COMMA expression)?)? eol+
    | controlWithoutText expression COMMA
      expression COMMA expression COMMA expression COMMA expression
      (COMMA expression (COMMA expression)?)? eol+
    | ICONCONTROL resourceId COMMA expression COMMA
      expression COMMA expression COMMA expression COMMA expression
      (COMMA expression (COMMA expression)?)? eol+
    ;

controlWithText
    : AUTO3STATE
    | AUTOCHECKBOX
    | AUTORADIOBUTTON
    | CHECKBOX
    | CTEXT
    | DEFPUSHBUTTON
    | GROUPBOX
    | LTEXT
    | PUSHBOX
    | PUSHBUTTON
    | RADIOBUTTON
    | RTEXT
    | STATE3
    | USERBUTTON
    ;

controlWithoutText
    : COMBOBOX
    | EDITTEXT
    | LISTBOX
    | SCROLLBAR
    ;

stringLiteral
    : STRING
    | WIDE_STRING
    ;

separator
    : COMMA eol*
    | eol+
    ;

blockStart
    : BEGIN
    | LBRACE
    ;

blockEnd
    : END
    | RBRACE
    ;

eol
    : NL
    ;

expression
    : bitOrExpression
    ;

bitOrExpression
    : bitXorExpression (PIPE bitXorExpression)*
    ;

bitXorExpression
    : bitAndExpression (CARET bitAndExpression)*
    ;

bitAndExpression
    : shiftExpression (AMP shiftExpression)*
    ;

shiftExpression
    : additiveExpression ((LSHIFT | RSHIFT) additiveExpression)*
    ;

additiveExpression
    : multiplicativeExpression ((PLUS | MINUS) multiplicativeExpression)*
    ;

multiplicativeExpression
    : unaryExpression ((STAR | SLASH | PERCENT) unaryExpression)*
    ;

unaryExpression
    : (PLUS | MINUS | TILDE) unaryExpression
    | primaryExpression
    ;

primaryExpression
    : INTEGER
    | IDENTIFIER
    | LPAREN expression RPAREN
    ;
