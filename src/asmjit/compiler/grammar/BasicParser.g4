parser grammar BasicParser;

options {
    tokenVocab = BasicLexer;
}

// ---------------------------------------------------------------------------
// Program
// ---------------------------------------------------------------------------

program
    : separators*
      topLevelItem?
      (separators+ topLevelItem)*
      separators*
      EOF
    ;

topLevelItem
    : subDeclaration
    | functionDeclaration
    | statement
    ;

separators
    : separator+
    ;

separator
    : NEWLINE
    | COLON
    ;

// ---------------------------------------------------------------------------
// Procedures and functions
// ---------------------------------------------------------------------------

subDeclaration
    : SUB IDENT parameterList?
      separators
      statementBlock
      END SUB
    ;

functionDeclaration
    : FUNCTION IDENT parameterList?
      (AS typeName)?
      separators
      statementBlock
      END FUNCTION
    ;

parameterList
    : LPAREN parameterDeclList? RPAREN
    ;

parameterDeclList
    : parameterDecl (COMMA parameterDecl)*
    ;

parameterDecl
    : (BYVAL | BYREF)?
      IDENT
      (AS typeName)?
    ;

// ---------------------------------------------------------------------------
// Statements
// ---------------------------------------------------------------------------

statement
    : lineNumber? statementCore
    ;

lineNumber
    : INTEGER_LITERAL
    ;

statementCore
    : assignmentStatement
    | constStatement
    | printStatement
    | inputStatement
    | dimStatement
    | ifStatement
    | forStatement
    | whileStatement
    | doLoopStatement
    | gotoStatement
    | gosubStatement
    | returnStatement
    | callStatement
    | exitStatement
    | labelStatement
    | stopStatement
    ;

statementBlock
    : (statement separators+)*
    ;

// Statements permitted after THEN on the same line.

inlineStatement
    : assignmentStatement
    | constStatement
    | printStatement
    | inputStatement
    | dimStatement
    | gotoStatement
    | gosubStatement
    | returnStatement
    | callStatement
    | exitStatement
    | stopStatement
    ;

// ---------------------------------------------------------------------------
// Variables and constants
// ---------------------------------------------------------------------------

assignmentStatement
    : LET? lvalue EQ expression
    ;

constStatement
    : CONST IDENT
      (AS typeName)?
      EQ expression
    ;

dimStatement
    : DIM variableDecl (COMMA variableDecl)*
    ;

variableDecl
    : IDENT
      arrayBounds?
      (AS typeName)?
      (EQ expression)?
    ;

arrayBounds
    : LPAREN expression (COMMA expression)* RPAREN
    ;

lvalue
    : IDENT
      (LPAREN argumentList RPAREN)?
    ;

// ---------------------------------------------------------------------------
// Input and output
// ---------------------------------------------------------------------------

printStatement
    : PRINT printList?
    ;

printList
    : expression
      ((COMMA | SEMI) expression)*
      (COMMA | SEMI)?
    ;

inputStatement
    : INPUT
      (STRING_LITERAL COMMA)?
      lvalue
      (COMMA lvalue)*
    ;

// ---------------------------------------------------------------------------
// IF
// ---------------------------------------------------------------------------

ifStatement
    : IF expression THEN
      inlineStatement
      (ELSE inlineStatement)?
      # inlineIf

    | IF expression THEN
      separators
      statementBlock

      (
          ELSEIF expression THEN
          separators
          statementBlock
      )*

      (
          ELSE
          separators
          statementBlock
      )?

      END IF
      # blockIf
    ;

// ---------------------------------------------------------------------------
// FOR
// ---------------------------------------------------------------------------

forStatement
    : FOR lvalue EQ expression
      (TO | DOWNTO)
      expression
      (STEP expression)?
      separators
      statementBlock
      NEXT IDENT?
    ;

// ---------------------------------------------------------------------------
// WHILE
// ---------------------------------------------------------------------------

whileStatement
    : WHILE expression
      separators
      statementBlock
      (
          WEND
        | END WHILE
      )
    ;

// ---------------------------------------------------------------------------
// DO / LOOP
// ---------------------------------------------------------------------------

doLoopStatement
    : DO WHILE expression
      separators
      statementBlock
      LOOP
      # doWhilePre

    | DO UNTIL expression
      separators
      statementBlock
      LOOP
      # doUntilPre

    | DO
      separators
      statementBlock
      LOOP WHILE expression
      # doWhilePost

    | DO
      separators
      statementBlock
      LOOP UNTIL expression
      # doUntilPost

    | DO
      separators
      statementBlock
      LOOP
      # doForever
    ;

// ---------------------------------------------------------------------------
// Flow control
// ---------------------------------------------------------------------------

gotoStatement
    : GOTO jumpTarget
    ;

gosubStatement
    : GOSUB jumpTarget
    ;

jumpTarget
    : INTEGER_LITERAL
    | IDENT
    ;

returnStatement
    : RETURN expression?
    ;

callStatement
    : CALL IDENT
      (LPAREN argumentList? RPAREN)?
    ;

exitStatement
    : EXIT
      (
          FOR
        | DO
        | WHILE
        | SUB
        | FUNCTION
      )?
    ;

labelStatement
    : LABEL IDENT
    ;

stopStatement
    : STOP
    ;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

typeName
    : BOOLEAN
    | INTEGER_KW
    | LONG
    | SINGLE
    | DOUBLE
    | STRING_KW
    | IDENT
    ;

// ---------------------------------------------------------------------------
// Expressions
// ---------------------------------------------------------------------------

expression
    : orExpression
    ;

orExpression
    : xorExpression (OR xorExpression)*
    ;

xorExpression
    : andExpression (XOR andExpression)*
    ;

andExpression
    : notExpression (AND notExpression)*
    ;

notExpression
    : NOT notExpression
    | comparisonExpression
    ;

comparisonExpression
    : additiveExpression
      (
          (EQ | NE | LT | LE | GT | GE)
          additiveExpression
      )?
    ;

additiveExpression
    : multiplicativeExpression
      (
          (PLUS | MINUS | AMP)
          multiplicativeExpression
      )*
    ;

multiplicativeExpression
    : powerExpression
      (
          (STAR | SLASH | INTDIV | MOD)
          powerExpression
      )*
    ;

powerExpression
    : unaryExpression
      (CARET powerExpression)?
    ;

unaryExpression
    : (PLUS | MINUS) unaryExpression
    | primaryExpression
    ;

primaryExpression
    : literal
    | IDENT LPAREN argumentList? RPAREN
    | IDENT
    | LPAREN expression RPAREN
    ;

argumentList
    : expression (COMMA expression)*
    ;

literal
    : INTEGER_LITERAL
    | FLOAT_LITERAL
    | HEX_LITERAL
    | BINARY_LITERAL
    | STRING_LITERAL
    | TRUE
    | FALSE
    ;
