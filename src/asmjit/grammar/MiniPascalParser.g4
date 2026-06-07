parser grammar MiniPascalParser;

options {
    tokenVocab = MiniPascalLexer;
}

programFile
    : PROGRAM IDENT SEMI declarationPart* block DOT
    ;

declarationPart
    : constSection
    | typeSection
    | varSection
    | procedureDeclaration
    | functionDeclaration
    ;

constSection
    : CONST constDeclaration+
    ;

constDeclaration
    : constItem (COMMA constItem)* SEMI
    ;

constItem
    : IDENT EQ_OP constValue
    ;

constValue
    : STRING
    | FLOATNUMBER
    | NUMBER
    ;

typeSection
    : TYPE typeDeclaration+
    ;

typeDeclaration
    : IDENT EQ_OP typeName SEMI
    | enumDeclaration
    | recordDeclaration
    | arrayDeclaration
    ;

arrayDeclaration
    : IDENT EQ_OP arrayType arrayInitializer? SEMI
    ;
    
arrayInitializer
    : EQ_OP LPAREN arrayValueList? RPAREN
    ;

arrayValueList
    : constValue (COMMA constValue)* COMMA?
    ;

arrayType
    : ARRAY LBRACK arrayRange (COMMA arrayRange)* RBRACK OF typeName
    | ARRAY OF typeName
    ;

arrayRange
    : expr DOTDOT expr
    ;

typeName
    : simpleType
    | CARET simpleType
    ;

simpleType
    : IDENT
    | INTEGER
    | DOUBLE
    | STRING
    ;

enumDeclaration
    : IDENT EQ_OP LPAREN enumValueList RPAREN SEMI
    ;

enumValueList
    : enumValue (COMMA enumValue)*
    ;

enumValue
    : IDENT (EQ_OP NUMBER)?
    ;

recordDeclaration
    : IDENT EQ_OP RECORD recordFieldDeclaration* END SEMI
    ;

recordFieldDeclaration
    : identList COLON typeName SEMI
    ;

functionDeclaration
    : FUNCTION IDENT formalParamList? COLON typeName SEMI block SEMI?
    ;

procedureDeclaration
    : PROCEDURE IDENT formalParamList? SEMI block SEMI?
    ;

formalParamList
    : LPAREN formalParam (SEMI formalParam)* RPAREN
    ;

formalParam
    : VAR? identList COLON typeName
    ;

declaration
    : varSection
    | procedureDeclaration
    | functionDeclaration
    ;

functionCallExpr
    : IDENT LPAREN argumentList? RPAREN
    ;

procedureCallStatement
    : IDENT actualParamList? SEMI?
    ;

actualParamList
    : LPAREN actualParam (COMMA actualParam)* RPAREN
    ;

actualParam
    : STRING
    | expr
    ;

varSection
    : VAR varDeclaration+
    ;

varDeclaration
    : identList COLON varType SEMI
    ;

varType
    : typeName
    | arrayType
    ;

identList
    : IDENT (COMMA IDENT)*
    ;

block
    : localDeclaration* BEGIN_ statementList END
    ;

localDeclaration
    : procedureDeclaration
    | functionDeclaration
    | varSection
    | constSection
    ;
    
statementList
    : (statement SEMI?)* 
    ;

statement
    : assignment
    | writeLnStatement
    | ifStatement
    | whileStatement
    | repeatStatement
    | forStatement
    | procedureCallStatement
    | exitStatement
    | compoundStatement
    ;
    
exitStatement
    : EXIT SEMI?
    ;

forStatement
    : FOR IDENT ASSIGN expr (TO | DOWNTO) expr DO statement
    ;

repeatStatement
    : REPEAT statementList UNTIL condition SEMI?
    ;

argumentList
    : expr (COMMA expr)*
    ;

whileStatement
    : WHILE condition DO statement
    ;

ifStatement
    : IF condition THEN statement (ELSE statement)?
    ;

condition
    : expr compareOp expr
    ;

compareOp
    : EQ_OP
    | NE_OP
    | LT_OP
    | LE_OP
    | GT_OP
    | GE_OP
    ;

compoundStatement
    : BEGIN_ statementList END
    ;

assignment
    : variableRef ASSIGN expr SEMI?
    ;

variableRef
    : RESULT
    | IDENT variableSuffix*
    ;

variableSuffix
    : DOT IDENT
    | LBRACK expr (COMMA expr)* RBRACK
    | CARET
    ;

expr
    : term ((PLUS | MINUS) term)*
    ;

term
    : factor ((STAR | SLASH) factor)*
    ;

factor
    : AT variableRef
    | variableRef
    | functionCallExpr
    | NIL
    | NUMBER
    | FLOATNUMBER
    | STRING
    | LPAREN expr RPAREN
    ;

writeLnStatement
    : WRITELN
    | WRITELN LPAREN writeArgList? RPAREN
    ;

writeArgList
    : writeArg (COMMA writeArg)*
    ;

writeArg
    : STRING
    | expr
    ;
