parser grammar lispParser;

options { tokenVocab=lispLexer; }

program
    : form* EOF
    ;

form
    : atom
    | list
    | vector
    | quotedForm
    ;

quotedForm
    : QUOTE form
    | BACKQUOTE form
    | COMMA form
    | COMMA_AT form
    ;

vector
    : VECTOR_START form* RPAREN
    ;

list
    : LPAREN listContent? RPAREN
    ;

listContent
    : defunForm
    | lambdaForm
    | letForm
    | ifForm
    | condForm
    | prognForm
    | setqForm
    | definitionForm
    | quoteSpecialForm
    | functionSpecialForm
    | dottedList
    | applicationForm
    ;

defunForm
    : DEFUN SYMBOL lambdaList declaration* body
    ;

lambdaForm
    : LAMBDA lambdaList declaration* body
    ;

letForm
    : (LET | LETSTAR) LPAREN bindingSpec* RPAREN declaration* body
    ;

bindingSpec
    : SYMBOL
    | LPAREN SYMBOL form? RPAREN
    ;

ifForm
    : IF form form form?
    ;

condForm
    : COND condClause+
    ;

condClause
    : LPAREN form form* RPAREN
    ;

prognForm
    : PROGN form+
    ;

setqForm
    : SETQ (SYMBOL form)+
    ;

definitionForm
    : (DEFVAR | DEFPARAMETER | DEFCONSTANT) SYMBOL form? StringLiteral?
    ;

quoteSpecialForm
    : QUOTE_KW form
    ;

functionSpecialForm
    : FUNCTION_KW form
    ;

applicationForm
    : form+
    ;

dottedList
    : form+ DOT form
    ;

lambdaList
    : LPAREN lambdaListElement* RPAREN
    ;

lambdaListElement
    : SYMBOL
    | AMP_OPTIONAL
    | AMP_REST SYMBOL
    | AMP_KEY
    | AMP_AUX
    | LPAREN SYMBOL form? RPAREN
    ;

declaration
    : StringLiteral
    ;

body
    : form+
    ;

atom
    : Number
    | StringLiteral
    | CharacterLiteral
    | BOOLEAN
    | NIL
    | TRUE
    | SYMBOL
    ;
