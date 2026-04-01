parser grammar pascalParser;

options { tokenVocab=pascalLexer; }

// ------------------------------------------------------------
// Object Pascal / Delphi parser seed for ANTLR4 (Python target)
// ------------------------------------------------------------

program
    : module EOF
    ;

module
    : programModule
    | unitModule
    | libraryModule
    | packageModule
    ;

programModule
    : PROGRAM identifier (LPAREN identifierList RPAREN)? SEMI usesClause? block DOT
    ;

libraryModule
    : LIBRARY identifier SEMI usesClause? block DOT
    ;

packageModule
    : PACKAGE identifier SEMI packageRequiresClause? packageContainsClause? END DOT
    ;

packageRequiresClause
    : REQUIRES qualifiedIdentifier (COMMA qualifiedIdentifier)* SEMI
    ;

packageContainsClause
    : CONTAINS qualifiedIdentifier (COMMA qualifiedIdentifier)* SEMI
    ;

unitModule
    : UNIT qualifiedIdentifier SEMI
      interfaceSection
      implementationSection
      initializationSection?
      finalizationSection?
      END DOT
    ;

interfaceSection
    : INTERFACE usesClause? declarationPart?
    ;

implementationSection
    : IMPLEMENTATION usesClause? declarationPart? statementBlock?
    ;

initializationSection
    : INITIALIZATION statementList
    ;

finalizationSection
    : FINALIZATION statementList
    ;

usesClause
    : USES qualifiedIdentifier (COMMA qualifiedIdentifier)* SEMI
    ;

block
    : declarationPart? statementBlock
    ;

declarationPart
    : declaration*
    ;

declaration
    : labelSection
    | constSection
    | typeSection
    | varSection
    | resourceStringSection
    | routineDeclaration
    | routineImplementation
    ;

labelSection
    : LABEL labelIdentifierList SEMI
    ;

labelIdentifierList
    : labelIdentifier (COMMA labelIdentifier)*
    ;

labelIdentifier
    : INTEGER_NUMBER
    | identifier
    ;

constSection
    : CONST constDeclaration+
    ;

constDeclaration
    : identifier EQ constantExpression SEMI
    ;

resourceStringSection
    : RESOURCESTRING constDeclaration+
    ;

typeSection
    : TYPE typeDeclaration+
    ;

typeDeclaration
    : identifier EQ typeSpec SEMI
    ;

varSection
    : (VAR | THREADVAR) variableDeclaration+
    ;

variableDeclaration
    : identifierList COLON typeRef SEMI
    ;

routineDeclaration
    : routineHeading SEMI routineDirectiveList? SEMI
    ;

routineImplementation
    : routineHeading SEMI declarationPart? statementBlock SEMI
    ;

routineHeading
    : procedureHeading
    | functionHeading
    | constructorHeading
    | destructorHeading
    ;

procedureHeading
    : PROCEDURE qualifiedIdentifier formalParameters?
    ;

functionHeading
    : FUNCTION qualifiedIdentifier formalParameters? COLON typeRef
    ;

constructorHeading
    : CONSTRUCTOR qualifiedIdentifier formalParameters?
    ;

destructorHeading
    : DESTRUCTOR qualifiedIdentifier formalParameters?
    ;

formalParameters
    : LPAREN formalParameterSection (SEMI formalParameterSection)* RPAREN
    ;

formalParameterSection
    : parameterModifier? identifierList COLON typeRef
    ;

parameterModifier
    : VAR
    | CONST
    | OUT
    ;

routineDirectiveList
    : routineDirective (SEMI routineDirective)*
    ;

routineDirective
    : FORWARD
    | OVERLOAD
    | OVERRIDE
    | REINTRODUCE
    | VIRTUAL
    | ABSTRACT
    | STATIC
    | INLINE
    ;

typeSpec
    : simpleType
    | subrangeType
    | enumeratedType
    | arrayType
    | setType
    | fileType
    | pointerType
    | classType
    | recordType
    | procedureType
    | typeRef
    ;

simpleType
    : typeRef
    ;

subrangeType
    : constantExpression DOTDOT constantExpression
    ;

enumeratedType
    : LPAREN identifierList RPAREN
    ;

arrayType
    : ARRAY (LBRACK typeList RBRACK)? OF typeSpec
    ;

typeList
    : typeRef (COMMA typeRef)*
    ;

setType
    : SET OF typeSpec
    ;

fileType
    : FILE (OF typeSpec)?
    ;

pointerType
    : CARET typeSpec
    ;

procedureType
    : PROCEDURE formalParameters?
    | FUNCTION formalParameters? COLON typeRef
    ;

classType
    : CLASS classHeritage? classBody END
    ;

classHeritage
    : LPAREN typeRefList RPAREN
    ;

typeRefList
    : typeRef (COMMA typeRef)*
    ;

classBody
    : classMember*
    ;

classMember
    : visibilitySection
    | classField
    | classMethod
    | propertyDeclaration
    ;

visibilitySection
    : (STRICT? PRIVATE
      | STRICT? PROTECTED
      | PUBLIC
      | PUBLISHED
      | AUTOMATED)
    ;

classField
    : identifierList COLON typeRef SEMI
    ;

classMethod
    : routineHeading SEMI routineDirectiveList? SEMI
    ;

propertyDeclaration
    : PROPERTY identifier propertySpec* SEMI
    ;

propertySpec
    : LBRACK expressionList RBRACK
    | COLON typeRef
    | READ identifier
    | WRITE identifier
    | DEFAULT
    | INDEX constantExpression
    | DISPID constantExpression
    | STORED identifier
    | IMPLEMENTS typeRef
    ;

recordType
    : RECORD recordField* END
    ;

recordField
    : identifierList COLON typeRef SEMI
    ;

typeRef
    : qualifiedIdentifier
    ;

statementBlock
    : BEGIN statementList? END
    ;

statementList
    : statement (SEMI statement)* SEMI?
    ;

statement
    : compoundStatement
    | assignmentStatement
    | procedureCallStatement
    | ifStatement
    | caseStatement
    | whileStatement
    | repeatStatement
    | forStatement
    | withStatement
    | tryStatement
    | raiseStatement
    | gotoStatement
    | breakStatement
    | continueStatement
    | exitStatement
    | emptyStatement
    ;

compoundStatement
    : statementBlock
    ;

assignmentStatement
    : variable ASSIGN expression
    ;

procedureCallStatement
    : designator actualParameterList?
    ;

ifStatement
    : IF expression THEN statement (ELSE statement)?
    ;

caseStatement
    : CASE expression OF caseBranch+ (ELSE statementList)? END
    ;

caseBranch
    : caseLabelList COLON statement
    ;

caseLabelList
    : constantExpression (COMMA constantExpression)*
    ;

whileStatement
    : WHILE expression DO statement
    ;

repeatStatement
    : REPEAT statementList UNTIL expression
    ;

forStatement
    : FOR identifier ASSIGN expression (TO | DOWNTO) expression DO statement
    ;

withStatement
    : WITH variableList DO statement
    ;

variableList
    : variable (COMMA variable)*
    ;

tryStatement
    : TRY statementList (EXCEPT exceptionHandlerList? | FINALLY statementList) END
    ;

exceptionHandlerList
    : exceptionHandler (SEMI exceptionHandler)* SEMI?
    ;

exceptionHandler
    : ON identifier COLON typeRef DO statement
    | statement
    ;

raiseStatement
    : RAISE expression?
    ;

gotoStatement
    : GOTO labelIdentifier
    ;

breakStatement
    : BREAK
    ;

continueStatement
    : CONTINUE
    ;

exitStatement
    : EXIT (LPAREN expression RPAREN)?
    ;

emptyStatement
    :
    ;

actualParameterList
    : LPAREN expressionList? RPAREN
    ;

expressionList
    : expression (COMMA expression)*
    ;

expression
    : relationalExpression
    ;

relationalExpression
    : additiveExpression ((EQ | NE | LT | LE | GT | GE | IN | IS | AS) additiveExpression)*
    ;

additiveExpression
    : multiplicativeExpression ((PLUS | MINUS | OR | XOR) multiplicativeExpression)*
    ;

multiplicativeExpression
    : unaryExpression ((STAR | SLASH | DIV | MOD | AND | SHL | SHR) unaryExpression)*
    ;

unaryExpression
    : (PLUS | MINUS | NOT | AT | CARET) unaryExpression
    | primaryExpression
    ;

primaryExpression
    : literal
    | designator
    | LPAREN expression RPAREN
    | setConstructor
    ;

setConstructor
    : LBRACK expressionList? RBRACK
    ;

variable
    : designator
    ;

designator
    : qualifiedIdentifier designatorSuffix*
    ;

designatorSuffix
    : DOT identifier
    | LBRACK expressionList RBRACK
    | CARET
    | actualParameterList
    ;

constantExpression
    : expression
    ;

literal
    : NIL
    | TRUE
    | FALSE
    | STRING_LITERAL
    | INTEGER_NUMBER
    | REAL_NUMBER
    | HEX_NUMBER
    ;

identifierList
    : identifier (COMMA identifier)*
    ;

qualifiedIdentifier
    : identifier (DOT identifier)*
    ;

identifier
    : IDENT
    ;
