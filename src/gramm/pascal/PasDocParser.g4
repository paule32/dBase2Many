parser grammar PasDocParser;

options {
    tokenVocab = PasDocLexer;
}

unitFile
    : programHeader? unitHeader? unitSection* EOF
    ;

programHeader
    : PROGRAM IDENT SEMI
    ;

unitHeader
    : UNIT IDENT SEMI
    ;

unitSection
    : INTERFACE declaration*
    | IMPLEMENTATION declaration*
    | declaration
    ;

declaration
    : docComment
    | constSection
    | varSection
    | typeSection
    | classDeclaration
    | recordDeclaration
    | arrayDeclaration
    | setDeclaration
    | otherToken
    ;

varSection
    : VAR fieldDeclaration*
    ;

constSection
    : CONST constDeclaration+
    ;

constDeclaration
    : constItem SEMI docComment?
    ;

constItem
    : IDENT EQ constValue
    ;

constValue
    : sign? NUMBER
    | STRING
    | IDENT
    ;

sign
    : PLUS
    | MINUS
    ;

docComment
    : DOC_COMMENT
    ;

typeSection
    : TYPE typeDeclaration*
    ;

typeDeclaration
    : classDeclaration
    | recordDeclaration
    | arrayDeclaration
    | setDeclaration
    | unknownTypeDeclaration
    ;

unknownTypeDeclaration
    : IDENT EQ .*? SEMI
    ;

classDeclaration
    : IDENT EQ classType SEMI?
    ;

classType
    : CLASS classInheritance? classBody
    ;

classInheritance
    : LPAREN typeName (COMMA typeName)* RPAREN
    ;

classBody
    : classMember* END
    ;

classMember
    : docComment
    | visibilitySection
    | methodDeclaration
    | propertyDeclaration
    | fieldDeclaration
    | otherToken
    ;

recordDeclaration
    : IDENT EQ recordType SEMI?
    ;

recordType
    : RECORD recordBody END
    ;

recordBody
    : recordMember*
    ;

recordMember
    : docComment
    | fieldDeclaration
    | otherToken
    ;

arrayDeclaration
    : IDENT EQ arrayType SEMI?
    ;

arrayType
    : ARRAY LBRACK arrayIndex RBRACK OF typeName
    ;

arrayIndex
    : constValue DOTDOT constValue
    | typeName
    ;

setDeclaration
    : IDENT EQ setType SEMI?
    ;

setType
    : SET OF typeName
    ;

visibilitySection
    : visibility
    ;

visibility
    : PUBLIC
    | PRIVATE
    | PROTECTED
    | PUBLISHED
    ;

methodDeclaration
    : methodKind IDENT parameterList? returnType? methodDirectiveList? SEMI
    ;

methodDirectiveList
    : SEMI methodDirective+
    ;

methodKind
    : PROCEDURE
    | FUNCTION
    | CONSTRUCTOR
    | DESTRUCTOR
    ;

parameterList
    : LPAREN parameterDecl? RPAREN
    ;

parameterDecl
    : parameterItem (SEMI parameterItem)*
    ;

parameterItem
    : parameterModifier? IDENT (COMMA IDENT)* COLON typeName
    ;

parameterModifier
    : CONST
    ;

returnType
    : COLON typeName
    ;

methodDirective
    : VIRTUAL
    | OVERRIDE
    | ABSTRACT
    | STATIC
    | OVERLOAD
    | REINTRODUCE
    ;

propertyDeclaration
    : PROPERTY IDENT propertyType? propertyAccessor* SEMI
    ;

propertyType
    : COLON typeName
    ;

propertyAccessor
    : READ IDENT
    | WRITE IDENT
    ;

fieldDeclaration
    : IDENT (COMMA IDENT)* COLON typeName SEMI
    ;

typeName
    : CARET? IDENT (DOT IDENT)*
    ;

otherToken
    : IDENT
    | STRING
    | NUMBER
    | PROGRAM
    | VAR
    | BEGIN
    | LPAREN
    | RPAREN
    | LBRACK
    | RBRACK
    | SEMI
    | COLON
    | COMMA
    | DOTDOT
    | DOT
    | EQ
    | CARET
    | ARRAY
    | SET
    | OF
    | RECORD
    | END
    | OTHER
    ;
