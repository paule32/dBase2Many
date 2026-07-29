parser grammar PascalParser;

options {
    tokenVocab = PascalLexer;
}

sourceFile
    : compilerDirective*
    ( programFile
    | unitFile
    | libraryFile
    ) EOF
    ;

externalImportTarget
    : externalLibrary
      (NAME (STRING | IDENT))?
    ;

routineCallingConvention
    : callingConvention SEMI
    ;

callingConvention
    : CDECL
    | STDCALL
    | PASCAL
    ;

externalRoutineDirective
    : EXTERNAL 
      ( externalLibrary
        externalNameClause?
        externalOrdinalClause?
      )?
      SEMI
    ;

externalLibrary
    : STRING | IDENT
    ;

externalNameClause
    : NAME STRING
    ;

externalOrdinalClause
    : ORDINAL NUMBER
    ;

programFile
    : PROGRAM IDENT SEMI usesClause? declarationPart* block DOT
    ;

unitFile
    : UNIT qualifiedIdent SEMI
      interfaceSection
      implementationSection
      ( unitInitBlock | END )
      DOT
    ;

libraryFile
    : LIBRARY IDENT SEMI
      usesClause?
      declarationPart*
      exportsClause?
      block
      DOT
    ;

compilerDirective
    : COMPILER_DIRECTIVE
    ;

exportsClause
    : EXPORTS exportItem (COMMA exportItem)* SEMI
    ;

exportItem
    : qualifiedIdent exportSignature?
    ;

exportSignature
    : LPAREN exportTypeList? RPAREN
    ;

exportTypeList
    : typeName (COMMA typeName)*
    ;

usesClause
    : USES qualifiedIdentList SEMI
    ;

qualifiedIdentList
    : qualifiedIdent (COMMA qualifiedIdent)*
    ;

interfaceSection
    : INTERFACE usesClause? interfaceDeclarationPart*
    ;

implementationSection
    : IMPLEMENTATION usesClause? implementationDeclarationPart*
    ;

interfaceDeclarationPart
    : constSection
    | typeSection
    | varSection
    | procedureHeader
    | functionHeader
    ;

implementationDeclarationPart
    : constSection
    | typeSection
    | varSection
    | procedureDeclaration
    | functionDeclaration
    | classMethodImplementation
    ;
    
unitInitBlock
    : BEGIN_ statementList END
    ;

qualifiedIdent
    : IDENT (DOT IDENT)*
    ;

methodDirective
    : VIRTUAL
    | OVERRIDE
    ;

methodDirectiveList
    : methodDirective SEMI
     (methodDirective SEMI)*
    ;

declarationPart
    : constSection
    | typeSection
    | varSection
    | procedureDeclaration
    | functionDeclaration
    | classMethodImplementation
    ;

classMethodImplementation
    : (CONSTRUCTOR | DESTRUCTOR | FUNCTION | PROCEDURE)
      IDENT DOT IDENT formalParamList? (COLON typeName)? SEMI
      block
      SEMI?
    ;

procedureHeader
    : PROCEDURE IDENT formalParamList?
      SEMI
      routineCallingConvention?
      externalRoutineDirective?
    ;

functionHeader
    : FUNCTION IDENT formalParamList?
      COLON typeName
      SEMI
      routineCallingConvention?
      externalRoutineDirective?
    ;

constSection
    : CONST constDeclaration+
    ;

constDeclaration
    : constItem (COMMA constItem)* SEMI
    ;

constItem
    : IDENT EQ_OP constValue
    | IDENT COLON arrayType EQ_OP
      LPAREN arrayValueList? RPAREN
    ;

constValue
    : STRING
    | CHARCODE
    | (PLUS | MINUS)? (FLOATNUMBER | HEXNUMBER | NUMBER)
    ;

typeSection
    : TYPE typeDeclaration+
    ;

typeIdentifier
    : IDENT
    | BOOLEAN
    ;

typeDeclaration
    : typeIdentifier EQ_OP typeName SEMI
    | typeIdentifier EQ_OP subrangeType SEMI
    | enumDeclaration
    | recordDeclaration
    | arrayDeclaration
    | classDeclaration
    ;

classDeclaration
    : IDENT EQ_OP CLASS classParent? classBody END SEMI
    ;

classParent
    : LPAREN IDENT RPAREN
    ;

classBody
    : classMember*
    ;

classMember
    : visibilitySection
    | propertyDeclaration
    | classFieldDeclaration
    | constructorDeclaration
    | destructorDeclaration
    | classFunctionDeclaration
    | classProcedureDeclaration
    ;

visibilitySection
    : PRIVATE
    | PROTECTED
    | PUBLIC
    | PUBLISHED
    ;

propertyDeclaration
    : PROPERTY IDENT COLON typeName propertyAccessor* SEMI
    ;

propertyAccessor
    : READ IDENT
    | WRITE IDENT
    ;

classFunctionDeclaration
    : FUNCTION IDENT formalParamList?
      COLON typeName SEMI
      methodDirectiveList?
    ;

classProcedureDeclaration
    : PROCEDURE IDENT formalParamList?
      SEMI
      methodDirectiveList?
    ;

classFieldDeclaration
    : identList COLON typeName SEMI
    ;

inheritedStatement
    : INHERITED IDENT? actualParamList?
    ;

inheritedExpression
    : INHERITED IDENT? actualParamList?
    ;

constructorDeclaration
    : CONSTRUCTOR IDENT formalParamList?
      SEMI
      methodDirectiveList?
    ;

destructorDeclaration
    : DESTRUCTOR IDENT formalParamList?
      SEMI
      methodDirectiveList?
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

arrayConstructor
    : LBRACK arrayConstructorItems? RBRACK
    ;

arrayConstructorItems
    : expr (COMMA expr)*
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
    | BOOLEAN
    ;

signedInteger
    : (PLUS | MINUS)? NUMBER
    ;

subrangeType
    : signedInteger DOTDOT signedInteger
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
    : IDENT EQ_OP PACKED? RECORD
      recordFieldDeclaration*
      END SEMI
    ;

recordFieldDeclaration
    : identList COLON typeName SEMI
    ;

functionDeclaration
    : FUNCTION IDENT formalParamList?
      COLON typeName
      SEMI
      routineCallingConvention?
      (
          externalRoutineDirective
        | declarationPart*
          block
          SEMI
      )
    ;

procedureDeclaration
    : PROCEDURE IDENT formalParamList?
      SEMI
      routineCallingConvention?
      (
          externalRoutineDirective
        | declarationPart*
          block
          SEMI
      )
    ;

formalParamList
    : LPAREN formalParam (SEMI formalParam)* RPAREN
    ;

formalParam
    : paramModifier? identList COLON paramType
    ;
    
paramModifier
    : VAR
    | CONST
    ;

paramType
    : openArrayType
    | typeName
    ;

openArrayType
    : ARRAY OF typeName
    | ARRAY OF CONST
    ;

declaration
    : compilerDirective*
    | varSection
    | procedureDeclaration
    | functionDeclaration
    ;

builtinDiskFunctionName
    : DISKFREE
    | DISKTOTAL
    | DISKLABEL
    | DISKSERIAL
    | DISKFILESYSTEM
    | DISKTYPE
    | DISKSHARE
    ;

functionName
    : IDENT
    | LENGTH
    | LOW
    | HIGH
    | COPY
    | POS
    | builtinDiskFunctionName
    | ASSIGNED
    ;

functionCallExpr
    : functionName (DOT functionName)? LPAREN argumentList? RPAREN
    | functionName DOT functionName
    ;

procedureCallStatement
    : IDENT (DOT IDENT)? actualParamList? SEMI?
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
    | IDENT ASSIGN conditionalExpression SEMI
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
    | tryStatement
    | ifStatement
    | whileStatement
    | repeatStatement
    | forStatement
    | incstatement
    | decstatement
    | breakStatement
    | continueStatement
    | caseStatement
    | procedureCallStatement
    | inheritedStatement
    | raiseStatement
    | exitStatement
    | compoundStatement
    ;

incstatement
    : INC LPAREN expr (COMMA expr)? RPAREN
    ;

decstatement
    : DEC LPAREN expr (COMMA expr)? RPAREN
    ;

caseStatement
    : CASE expr OF caseItem* caseElse? END
    ;

caseItem
    : caseLabelList COLON statement SEMI?
    ;

caseLabelList
    : caseLabel (COMMA caseLabel)*
    ;

caseLabel
    : NUMBER
    | IDENT
    ;

caseElse
    : ELSE statementList SEMI?
    ;

breakStatement
    : BREAK
    ;

continueStatement
    : CONTINUE
    ;

tryStatement
    : TRY statementList FINALLY statementList END
    | TRY statementList EXCEPT  statementList END
    ;

raiseStatement
    : RAISE expr
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
    : expr (compareOp expr)?
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
    : (IDENT | RESULT) variableSuffix*
    ;

variableSuffix
    : pointerDereference
    | arrayIndex
    | fieldAccess
    ;

pointerDereference
    : CARET
    ;

fieldAccess
    : DOT IDENT
    ;

arrayIndex
    : LBRACK exprList RBRACK
    ;

exprList
    : expr (COMMA expr)*
    ;

expr
    : boolOrExpr
    ;

conditionalExpression
    : IF addExpr compareOp addExpr ELSE expr
    ;

boolOrExpr
    : boolXorExpr (OR boolXorExpr)*
    ;

boolXorExpr
    : boolAndExpr (XOR boolAndExpr)*
    ;

boolAndExpr
    : compareExpr (AND compareExpr)*
    ;

compareExpr
    : addExpr (compareOp addExpr)?
    ;

addExpr
    : shiftExpr ((PLUS | MINUS) shiftExpr)*
    ;

shiftExpr
    : term ((SHL | SHR) term)*
    ;

term
    : factor ((STAR | SLASH) factor)*
    ;

factor
    : PLUS factor
    | MINUS factor
    | NOT factor
    | conditionalExpression
    | inheritedExpression
    | AT variableRef
    | variableRef
    | functionCallExpr
    | arrayConstructor
    | NIL
    | FALSE
    | TRUE
    | CHARCODE
    | HEXNUMBER
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
