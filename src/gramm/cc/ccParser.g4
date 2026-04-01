parser grammar ccParser;

options { tokenVocab=ccLexer; }

translationUnit
    : topLevelDeclaration* EOF
    ;

topLevelDeclaration
    : preprocessorDirective
    | namespaceDefinition
    | linkageSpecification
    | templateDeclaration
    | classDefinition
    | enumDefinition
    | usingDeclaration
    | typedefDeclaration
    | functionDefinition
    | declaration SEMI
    | SEMI
    ;

preprocessorDirective
    : PP_DIRECTIVE
    ;

templateDeclaration
    : TEMPLATE LT templateParameterList GT topLevelDeclaration
    ;

templateParameterList
    : templateParameter (COMMA templateParameter)*
    ;

templateParameter
    : (CLASS | TYPENAME) Identifier
    | declSpecifierSeq declarator?
    ;

namespaceDefinition
    : NAMESPACE Identifier? LBRACE topLevelDeclaration* RBRACE
    ;

linkageSpecification
    : EXTERN StringLiteral (LBRACE topLevelDeclaration* RBRACE | topLevelDeclaration)
    ;

classDefinition
    : classKey Identifier? baseClause? LBRACE classMemberDeclaration* RBRACE SEMI?
    ;

classKey
    : CLASS
    | STRUCT
    ;

baseClause
    : COLON baseSpecifier (COMMA baseSpecifier)*
    ;

baseSpecifier
    : accessSpecifier? VIRTUAL? qualifiedIdentifier
    ;

classMemberDeclaration
    : accessSpecifier COLON
    | functionDefinition
    | declaration SEMI
    | classDefinition
    | enumDefinition
    | usingDeclaration
    | typedefDeclaration
    | preprocessorDirective
    | SEMI
    ;

accessSpecifier
    : PUBLIC
    | PRIVATE
    | PROTECTED
    ;

enumDefinition
    : ENUM (CLASS | STRUCT)? Identifier? LBRACE enumeratorList? COMMA? RBRACE SEMI?
    ;

enumeratorList
    : enumerator (COMMA enumerator)*
    ;

enumerator
    : Identifier (ASSIGN expression)?
    ;

usingDeclaration
    : USING NAMESPACE qualifiedIdentifier SEMI?
    | USING Identifier ASSIGN typeReference SEMI?
    | USING qualifiedIdentifier SEMI?
    ;

typedefDeclaration
    : TYPEDEF typeReference declaratorList SEMI?
    ;

functionDefinition
    : declSpecifierSeq? functionDeclarator functionBody
    ;

functionDeclarator
    : ptrOperator* qualifiedIdentifier LPAREN parameterDeclarationList? RPAREN cvQualifier* refQualifier? noexceptSpecification? trailingReturnType?
    ;

functionBody
    : compoundStatement
    | ASSIGN DEFAULT SEMI
    | ASSIGN DELETE SEMI
    ;

declaration
    : declSpecifierSeq initDeclaratorList?
    ;

initDeclaratorList
    : initDeclarator (COMMA initDeclarator)*
    ;

initDeclarator
    : declarator (ASSIGN initializer)?
    ;

declaratorList
    : declarator (COMMA declarator)*
    ;

declarator
    : ptrOperator* qualifiedIdentifier (LPAREN parameterDeclarationList? RPAREN cvQualifier* refQualifier? noexceptSpecification? trailingReturnType?)? arraySuffix*
    ;

arraySuffix
    : LBRACK expression? RBRACK
    ;

ptrOperator
    : STAR cvQualifier*
    | AMP
    | ANDAND
    ;

refQualifier
    : AMP
    | ANDAND
    ;

noexceptSpecification
    : NOEXCEPT (LPAREN expression? RPAREN)?
    ;

trailingReturnType
    : ARROW typeReference
    ;

parameterDeclarationList
    : parameterDeclaration (COMMA parameterDeclaration)* (COMMA ELLIPSIS)?
    | ELLIPSIS
    ;

parameterDeclaration
    : declSpecifierSeq declarator? (ASSIGN initializer)?
    ;

declSpecifierSeq
    : declSpecifier+
    ;

declSpecifier
    : storageClassSpecifier
    | functionSpecifier
    | cvQualifier
    | simpleTypeSpecifier
    | qualifiedIdentifier
    ;

storageClassSpecifier
    : STATIC
    | EXTERN
    | MUTABLE
    ;

functionSpecifier
    : INLINE
    | VIRTUAL
    | EXPLICIT
    | FRIEND
    | CONSTEXPR
    | OVERRIDE
    | FINAL
    ;

cvQualifier
    : CONST
    | VOLATILE
    ;

simpleTypeSpecifier
    : VOID
    | BOOL
    | CHAR
    | SHORT
    | INT
    | LONG
    | FLOAT
    | DOUBLE
    | SIGNED
    | UNSIGNED
    | AUTO
    ;

typeReference
    : declSpecifierSeq
    ;

qualifiedIdentifier
    : (Identifier SCOPE)* unqualifiedIdentifier
    ;

unqualifiedIdentifier
    : Identifier
    | TILDE Identifier
    | OPERATOR operatorToken
    ;

operatorToken
    : PLUS
    | MINUS
    | STAR
    | DIV
    | MOD
    | EQ
    | NE
    | LT
    | GT
    | LE
    | GE
    | ASSIGN
    | PLUSPLUS
    | MINUSMINUS
    | ANDAND
    | OROR
    | LBRACK RBRACK
    | LPAREN RPAREN
    ;

initializer
    : braceInitializer
    | expression
    ;

braceInitializer
    : LBRACE (initializer (COMMA initializer)*)? COMMA? RBRACE
    ;

compoundStatement
    : LBRACE statement* RBRACE
    ;

statement
    : compoundStatement
    | declarationStatement
    | ifStatement
    | switchStatement
    | whileStatement
    | doWhileStatement
    | forStatement
    | returnStatement
    | breakStatement
    | continueStatement
    | tryStatement
    | labeledStatement
    | expressionStatement
    | SEMI
    ;

declarationStatement
    : declaration SEMI
    ;

ifStatement
    : IF LPAREN expression RPAREN statement (ELSE statement)?
    ;

switchStatement
    : SWITCH LPAREN expression RPAREN statement
    ;

whileStatement
    : WHILE LPAREN expression RPAREN statement
    ;

doWhileStatement
    : DO statement WHILE LPAREN expression RPAREN SEMI
    ;

forStatement
    : FOR LPAREN forInitStatement expression? SEMI expression? RPAREN statement
    ;

forInitStatement
    : declaration? SEMI
    | expression? SEMI
    ;

returnStatement
    : RETURN expression? SEMI
    ;

breakStatement
    : BREAK SEMI
    ;

continueStatement
    : CONTINUE SEMI
    ;

tryStatement
    : TRY compoundStatement handler+
    ;

handler
    : CATCH LPAREN exceptionDeclaration RPAREN compoundStatement
    ;

exceptionDeclaration
    : ELLIPSIS
    | declSpecifierSeq declarator?
    ;

labeledStatement
    : CASE constantExpression COLON statement
    | DEFAULT COLON statement
    | Identifier COLON statement
    ;

expressionStatement
    : expression? SEMI
    ;

constantExpression
    : conditionalExpression
    ;

expression
    : assignmentExpression (COMMA assignmentExpression)*
    ;

assignmentExpression
    : conditionalExpression
    | unaryExpression assignmentOperator assignmentExpression
    ;

assignmentOperator
    : ASSIGN
    | PLUSEQ
    | MINUSEQ
    | STAREQ
    | DIVEQ
    | MODEQ
    | ANDEQ
    | OREQ
    | XOREQ
    | LSHIFTEQ
    | RSHIFTEQ
    ;

conditionalExpression
    : logicalOrExpression (QUESTION expression COLON assignmentExpression)?
    ;

logicalOrExpression
    : logicalAndExpression (OROR logicalAndExpression)*
    ;

logicalAndExpression
    : inclusiveOrExpression (ANDAND inclusiveOrExpression)*
    ;

inclusiveOrExpression
    : exclusiveOrExpression (PIPE exclusiveOrExpression)*
    ;

exclusiveOrExpression
    : andExpression (CARET andExpression)*
    ;

andExpression
    : equalityExpression (AMP equalityExpression)*
    ;

equalityExpression
    : relationalExpression ((EQ | NE) relationalExpression)*
    ;

relationalExpression
    : shiftExpression ((LT | GT | LE | GE) shiftExpression)*
    ;

shiftExpression
    : additiveExpression ((LSHIFT | RSHIFT) additiveExpression)*
    ;

additiveExpression
    : multiplicativeExpression ((PLUS | MINUS) multiplicativeExpression)*
    ;

multiplicativeExpression
    : unaryExpression ((STAR | DIV | MOD) unaryExpression)*
    ;

unaryExpression
    : postfixExpression
    | unaryOperator unaryExpression
    | NEW typeReference (LPAREN argumentExpressionList? RPAREN)?
    | DELETE unaryExpression
    | SIZEOF unaryExpression
    ;

unaryOperator
    : PLUS
    | MINUS
    | BANG
    | TILDE
    | STAR
    | AMP
    | PLUSPLUS
    | MINUSMINUS
    ;

postfixExpression
    : primaryExpression postfixSuffix*
    ;

postfixSuffix
    : LBRACK expression RBRACK
    | LPAREN argumentExpressionList? RPAREN
    | DOT unqualifiedIdentifier
    | ARROW unqualifiedIdentifier
    | PLUSPLUS
    | MINUSMINUS
    ;

argumentExpressionList
    : assignmentExpression (COMMA assignmentExpression)*
    ;

primaryExpression
    : literal
    | qualifiedIdentifier
    | THIS
    | NULLPTR
    | LPAREN expression RPAREN
    ;

literal
    : IntegerLiteral
    | FloatingLiteral
    | CharacterLiteral
    | StringLiteral+
    | TRUE
    | FALSE
    ;
