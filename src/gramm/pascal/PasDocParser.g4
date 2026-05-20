parser grammar PasDocParser;

options {
    tokenVocab = PasDocLexer;
}

unitFile
    : unitHeader? unitSection* EOF
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
    | typeSection
    | classDeclaration
    | otherToken
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
    | otherToken
    ;

classDeclaration
    : IDENT EQ classType SEMI?
    ;

recordDeclaration
    : IDENT EQ recordType SEMI?
    ;

classType
    : CLASS classInheritance? classBody
    ;

recordType
    : RECORD classBody
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
    | LPAREN
    | RPAREN
    | LBRACK
    | RBRACK
    | SEMI
    | COLON
    | COMMA
    | DOT
    | EQ
    | CARET
    | END
    | OTHER
    ;
