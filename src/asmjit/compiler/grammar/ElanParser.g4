parser grammar ElanParser;

options {
    tokenVocab = ElanLexer;
}

// -----------------------------------------------------------------------------
// Compilation unit
// -----------------------------------------------------------------------------
sourceFile
    : topLevelElement* EOF
    ;

topLevelElement
    : refinement
    | procedureDeclaration
    | typeDeclaration
    | letDeclaration
    | packetDeclaration
    | statement SEMI?
    ;

// -----------------------------------------------------------------------------
// ELAN refinements
//
// Example:
// program:
//     INT VAR x;
//     x := 10;
//     put(x).
// -----------------------------------------------------------------------------
refinement
    : refinementName COLON paragraph DOT
    ;

refinementName
    : IDENTIFIER
    ;

// -----------------------------------------------------------------------------
// Procedures
//
// PROC hello (TEXT CONST name):
//     put(name)
// ENDPROC
//
// INT PROC square (INT CONST value):
//     value * value
// ENDPROC
// -----------------------------------------------------------------------------
procedureDeclaration
    : resultType? PROC IDENTIFIER formalParameterList?
      COLON? procedureBody
      procedureEnd IDENTIFIER? SEMI?
    ;

procedureEnd
    : ENDPROC
    | END PROC
    ;

procedureBody
    : declarationOrStatement*
    ;

formalParameterList
    : LPAREN formalParameterGroup (COMMA formalParameterGroup)* RPAREN
    ;

formalParameterGroup
    : typeName parameterAccess? identifierList
    ;

parameterAccess
    : VAR
    | CONST
    ;

resultType
    : typeName
    ;

// -----------------------------------------------------------------------------
// Packets - simplified module form
// -----------------------------------------------------------------------------
packetDeclaration
    : PACKET IDENTIFIER COLON?
      topLevelElement*
      packetEnd IDENTIFIER? SEMI?
    ;

packetEnd
    : ENDPACKET
    | END PACKET
    ;

// -----------------------------------------------------------------------------
// Type declarations
// -----------------------------------------------------------------------------
typeDeclaration
    : TYPE IDENTIFIER EQ typeSpec SEMI
    ;

typeSpec
    : primitiveType
    | structType
    | rowType
    | IDENTIFIER
    ;

primitiveType
    : INT
    | REAL
    | TEXT
    | BOOL
    | CHAR
    | VOID
    ;

structType
    : STRUCT LPAREN structField (COMMA structField)* RPAREN
    ;

structField
    : typeName identifierList
    ;

rowType
    : ROW rowBounds? typeName
    | ROW rowBounds? OF typeName
    ;

rowBounds
    : LBRACK expression (COLON expression)? RBRACK
    ;

typeName
    : primitiveType
    | IDENTIFIER
    ;

// -----------------------------------------------------------------------------
// Object declarations
//
// INT VAR x;
// INT VAR x := 1;
// INT VAR x, y, z;
// INT VAR x := 1, y := 2, z;
//
// INT CONST limit := 100;
// LET answer = 42;
// -----------------------------------------------------------------------------
letDeclaration
    : LET IDENTIFIER EQ expression SEMI
    ;

objectDeclaration
    : typeName objectAccess objectDeclarator (COMMA objectDeclarator)* SEMI
    ;

objectDeclarator
    : IDENTIFIER (ASSIGN expression)?
    ;

objectAccess
    : VAR
    | CONST
    ;

identifierInitList
    : identifierInitializer (COMMA identifierInitializer)*
    ;

identifierInitializer
    : IDENTIFIER (ASSIGN expression)?
    ;

identifierList
    : IDENTIFIER (COMMA IDENTIFIER)*
    ;

declarationOrStatement
    : objectDeclaration
    | typeDeclaration
    | letDeclaration
    | procedureDeclaration
    | statement SEMI?
    ;

// -----------------------------------------------------------------------------
// Paragraphs and statements
// -----------------------------------------------------------------------------
paragraph
    : declarationOrStatement*
    ;

statement
    : assignmentStatement
    | procedureCallStatement
    | ifStatement
    | whileStatement
    | repeatUntilStatement
    | loopStatement
    | forStatement
    | leaveStatement
    | expressionStatement
    ;

assignmentStatement
    : assignable ASSIGN expression
    ;

procedureCallStatement
    : qualifiedName actualParameterList?
    ;

expressionStatement
    : expression
    ;

ifStatement
    : IF expression THEN paragraph
      elifPart*
      elsePart?
      ifEnd
    ;

elifPart
    : ELIF expression THEN paragraph
    ;

elsePart
    : ELSE paragraph
    ;

ifEnd
    : FI
    | ENDIF
    | END IF
    ;

whileStatement
    : WHILE expression repeatKeyword paragraph repeatEnd
    ;

repeatUntilStatement
    : repeatKeyword paragraph UNTIL expression repeatEnd
    ;

loopStatement
    : repeatKeyword paragraph repeatEnd
    ;

forStatement
    : FOR IDENTIFIER FROM expression forDirection expression
      repeatKeyword paragraph repeatEnd
    | forDirection expression repeatKeyword paragraph repeatEnd
    ;

forDirection
    : UPTO
    | DOWNTO
    ;

repeatKeyword
    : REP
    | REPEAT
    ;

repeatEnd
    : ENDREP
    | ENDREPEAT
    | END REP
    ;

leaveStatement
    : LEAVE refinementName (WITH expression)?
    ;

// -----------------------------------------------------------------------------
// Expressions
// -----------------------------------------------------------------------------
expression
    : logicalOrExpression
    ;

logicalOrExpression
    : logicalXorExpression ((OR) logicalXorExpression)*
    ;

logicalXorExpression
    : logicalAndExpression ((XOR) logicalAndExpression)*
    ;

logicalAndExpression
    : equalityExpression ((AND) equalityExpression)*
    ;

equalityExpression
    : relationalExpression ((EQ | NE) relationalExpression)*
    ;

relationalExpression
    : additiveExpression ((LT | LE | GT | GE) additiveExpression)*
    ;

additiveExpression
    : multiplicativeExpression ((PLUS | MINUS) multiplicativeExpression)*
    ;

multiplicativeExpression
    : unaryExpression ((STAR | SLASH | DIV | MOD) unaryExpression)*
    ;

unaryExpression
    : (PLUS | MINUS | NOT) unaryExpression
    | postfixExpression
    ;

postfixExpression
    : primaryExpression postfixPart*
    ;

postfixPart
    : actualParameterList
    | LBRACK expressionList RBRACK
    | DOT IDENTIFIER
    ;

primaryExpression
    : literal
    | qualifiedName
    | LPAREN expression RPAREN
    | ifExpression
    ;

ifExpression
    : IF expression THEN expression
      (ELIF expression THEN expression)*
      ELSE expression
      ifEnd
    ;

actualParameterList
    : LPAREN expressionList? RPAREN
    ;

expressionList
    : expression (COMMA expression)*
    ;

assignable
    : qualifiedName
      (LBRACK expressionList RBRACK | DOT IDENTIFIER)*
    ;

qualifiedName
    : IDENTIFIER (DOT IDENTIFIER)*
    ;

literal
    : INTEGER_LITERAL
    | REAL_LITERAL
    | STRING_LITERAL
    | CHAR_LITERAL
    | TRUE
    | FALSE
    | NIL
    ;
