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
    | interfaceDeclaration
    | recordDeclaration
    | arrayDeclaration
    | setDeclaration
    | enumDeclaration
    | otherToken
    ;

varSection
    : VAR varDeclaration*
    ;

varDeclaration
    : docComment
    | fieldDeclaration
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
    | interfaceDeclaration
    | arrayDeclaration
    | setDeclaration
    | enumDeclaration
    | unknownTypeDeclaration
    ;

unknownTypeDeclaration
    : IDENT EQ unknownTypeToken* SEMI
    ;

unknownTypeToken
    : IDENT
    | STRING
    | NUMBER
    | LPAREN
    | RPAREN
    | LBRACK
    | RBRACK
    | COLON
    | COMMA
    | DOTDOT
    | LT
    | GT
    | DOT
    | CARET
    ;

classDeclaration
    : IDENT genericParams? EQ classType SEMI?
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
    : IDENT genericParams? EQ recordType SEMI?
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
    : IDENT EQ arrayType SEMI docComment?
    ;

arrayType
    : ARRAY LBRACK arrayIndex RBRACK OF typeName
    ;

arrayIndex
    : constValue DOTDOT constValue
    | typeName
    ;

setDeclaration
    : IDENT EQ setType SEMI docComment?
    ;

setType
    : SET OF typeName
    ;

enumDeclaration
    : IDENT EQ enumType SEMI docComment?
    ;

enumType
    : LPAREN enumItem enumItemTail* RPAREN
    ;

enumItemTail
    : COMMA docComment? enumItem
    ;

enumItem
    : IDENT docComment?
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
    : PROPERTY IDENT COLON typeName docComment? propertyAccessor* SEMI
    ;

propertyAccessor
    : READ  IDENT docComment?
    | WRITE IDENT docComment?
    ;

fieldDeclaration
    : IDENT (COMMA IDENT)* COLON typeName SEMI docComment?
    ;

interfaceDeclaration
    : IDENT genericParams? EQ INTERFACE interfaceBaseList? docComment?
      interfaceBody
      END SEMI
    ;

interfaceBaseList
    : LPAREN typeName (COMMA typeName)* RPAREN
    ;

interfaceBody
    : interfaceMember*
    ;

interfaceMember
    : methodDeclaration
    | propertyDeclaration
    | docComment
    ;

genericParams
    : LT IDENT (COMMA IDENT)* GT
    ;

typeName
    : CARET? IDENT genericTypeArgs? (DOT IDENT genericTypeArgs?)*
    ;

genericTypeArgs
    : LT typeName (COMMA typeName)* GT
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
