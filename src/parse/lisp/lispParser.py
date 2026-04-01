# Generated from lispParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,35,245,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,1,0,5,0,52,8,0,10,0,
        12,0,55,9,0,1,0,1,0,1,1,1,1,1,1,1,1,3,1,63,8,1,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,3,2,73,8,2,1,3,1,3,5,3,77,8,3,10,3,12,3,80,9,3,1,3,
        1,3,1,4,1,4,3,4,86,8,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,
        5,1,5,1,5,1,5,3,5,102,8,5,1,6,1,6,1,6,1,6,5,6,108,8,6,10,6,12,6,
        111,9,6,1,6,1,6,1,7,1,7,1,7,5,7,118,8,7,10,7,12,7,121,9,7,1,7,1,
        7,1,8,1,8,1,8,5,8,128,8,8,10,8,12,8,131,9,8,1,8,1,8,5,8,135,8,8,
        10,8,12,8,138,9,8,1,8,1,8,1,9,1,9,1,9,1,9,3,9,146,8,9,1,9,3,9,149,
        8,9,1,10,1,10,1,10,1,10,3,10,155,8,10,1,11,1,11,4,11,159,8,11,11,
        11,12,11,160,1,12,1,12,1,12,5,12,166,8,12,10,12,12,12,169,9,12,1,
        12,1,12,1,13,1,13,4,13,175,8,13,11,13,12,13,176,1,14,1,14,1,14,4,
        14,182,8,14,11,14,12,14,183,1,15,1,15,1,15,3,15,189,8,15,1,15,3,
        15,192,8,15,1,16,1,16,1,16,1,17,1,17,1,17,1,18,4,18,201,8,18,11,
        18,12,18,202,1,19,4,19,206,8,19,11,19,12,19,207,1,19,1,19,1,19,1,
        20,1,20,5,20,215,8,20,10,20,12,20,218,9,20,1,20,1,20,1,21,1,21,1,
        21,1,21,1,21,1,21,1,21,1,21,1,21,3,21,231,8,21,1,21,3,21,234,8,21,
        1,22,1,22,1,23,4,23,239,8,23,11,23,12,23,240,1,24,1,24,1,24,0,0,
        25,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,
        44,46,48,0,3,1,0,15,16,1,0,21,23,1,0,26,32,262,0,53,1,0,0,0,2,62,
        1,0,0,0,4,72,1,0,0,0,6,74,1,0,0,0,8,83,1,0,0,0,10,101,1,0,0,0,12,
        103,1,0,0,0,14,114,1,0,0,0,16,124,1,0,0,0,18,148,1,0,0,0,20,150,
        1,0,0,0,22,156,1,0,0,0,24,162,1,0,0,0,26,172,1,0,0,0,28,178,1,0,
        0,0,30,185,1,0,0,0,32,193,1,0,0,0,34,196,1,0,0,0,36,200,1,0,0,0,
        38,205,1,0,0,0,40,212,1,0,0,0,42,233,1,0,0,0,44,235,1,0,0,0,46,238,
        1,0,0,0,48,242,1,0,0,0,50,52,3,2,1,0,51,50,1,0,0,0,52,55,1,0,0,0,
        53,51,1,0,0,0,53,54,1,0,0,0,54,56,1,0,0,0,55,53,1,0,0,0,56,57,5,
        0,0,1,57,1,1,0,0,0,58,63,3,48,24,0,59,63,3,8,4,0,60,63,3,6,3,0,61,
        63,3,4,2,0,62,58,1,0,0,0,62,59,1,0,0,0,62,60,1,0,0,0,62,61,1,0,0,
        0,63,3,1,0,0,0,64,65,5,3,0,0,65,73,3,2,1,0,66,67,5,4,0,0,67,73,3,
        2,1,0,68,69,5,6,0,0,69,73,3,2,1,0,70,71,5,5,0,0,71,73,3,2,1,0,72,
        64,1,0,0,0,72,66,1,0,0,0,72,68,1,0,0,0,72,70,1,0,0,0,73,5,1,0,0,
        0,74,78,5,8,0,0,75,77,3,2,1,0,76,75,1,0,0,0,77,80,1,0,0,0,78,76,
        1,0,0,0,78,79,1,0,0,0,79,81,1,0,0,0,80,78,1,0,0,0,81,82,5,2,0,0,
        82,7,1,0,0,0,83,85,5,1,0,0,84,86,3,10,5,0,85,84,1,0,0,0,85,86,1,
        0,0,0,86,87,1,0,0,0,87,88,5,2,0,0,88,9,1,0,0,0,89,102,3,12,6,0,90,
        102,3,14,7,0,91,102,3,16,8,0,92,102,3,20,10,0,93,102,3,22,11,0,94,
        102,3,26,13,0,95,102,3,28,14,0,96,102,3,30,15,0,97,102,3,32,16,0,
        98,102,3,34,17,0,99,102,3,38,19,0,100,102,3,36,18,0,101,89,1,0,0,
        0,101,90,1,0,0,0,101,91,1,0,0,0,101,92,1,0,0,0,101,93,1,0,0,0,101,
        94,1,0,0,0,101,95,1,0,0,0,101,96,1,0,0,0,101,97,1,0,0,0,101,98,1,
        0,0,0,101,99,1,0,0,0,101,100,1,0,0,0,102,11,1,0,0,0,103,104,5,13,
        0,0,104,105,5,32,0,0,105,109,3,40,20,0,106,108,3,44,22,0,107,106,
        1,0,0,0,108,111,1,0,0,0,109,107,1,0,0,0,109,110,1,0,0,0,110,112,
        1,0,0,0,111,109,1,0,0,0,112,113,3,46,23,0,113,13,1,0,0,0,114,115,
        5,14,0,0,115,119,3,40,20,0,116,118,3,44,22,0,117,116,1,0,0,0,118,
        121,1,0,0,0,119,117,1,0,0,0,119,120,1,0,0,0,120,122,1,0,0,0,121,
        119,1,0,0,0,122,123,3,46,23,0,123,15,1,0,0,0,124,125,7,0,0,0,125,
        129,5,1,0,0,126,128,3,18,9,0,127,126,1,0,0,0,128,131,1,0,0,0,129,
        127,1,0,0,0,129,130,1,0,0,0,130,132,1,0,0,0,131,129,1,0,0,0,132,
        136,5,2,0,0,133,135,3,44,22,0,134,133,1,0,0,0,135,138,1,0,0,0,136,
        134,1,0,0,0,136,137,1,0,0,0,137,139,1,0,0,0,138,136,1,0,0,0,139,
        140,3,46,23,0,140,17,1,0,0,0,141,149,5,32,0,0,142,143,5,1,0,0,143,
        145,5,32,0,0,144,146,3,2,1,0,145,144,1,0,0,0,145,146,1,0,0,0,146,
        147,1,0,0,0,147,149,5,2,0,0,148,141,1,0,0,0,148,142,1,0,0,0,149,
        19,1,0,0,0,150,151,5,17,0,0,151,152,3,2,1,0,152,154,3,2,1,0,153,
        155,3,2,1,0,154,153,1,0,0,0,154,155,1,0,0,0,155,21,1,0,0,0,156,158,
        5,18,0,0,157,159,3,24,12,0,158,157,1,0,0,0,159,160,1,0,0,0,160,158,
        1,0,0,0,160,161,1,0,0,0,161,23,1,0,0,0,162,163,5,1,0,0,163,167,3,
        2,1,0,164,166,3,2,1,0,165,164,1,0,0,0,166,169,1,0,0,0,167,165,1,
        0,0,0,167,168,1,0,0,0,168,170,1,0,0,0,169,167,1,0,0,0,170,171,5,
        2,0,0,171,25,1,0,0,0,172,174,5,19,0,0,173,175,3,2,1,0,174,173,1,
        0,0,0,175,176,1,0,0,0,176,174,1,0,0,0,176,177,1,0,0,0,177,27,1,0,
        0,0,178,181,5,20,0,0,179,180,5,32,0,0,180,182,3,2,1,0,181,179,1,
        0,0,0,182,183,1,0,0,0,183,181,1,0,0,0,183,184,1,0,0,0,184,29,1,0,
        0,0,185,186,7,1,0,0,186,188,5,32,0,0,187,189,3,2,1,0,188,187,1,0,
        0,0,188,189,1,0,0,0,189,191,1,0,0,0,190,192,5,31,0,0,191,190,1,0,
        0,0,191,192,1,0,0,0,192,31,1,0,0,0,193,194,5,24,0,0,194,195,3,2,
        1,0,195,33,1,0,0,0,196,197,5,25,0,0,197,198,3,2,1,0,198,35,1,0,0,
        0,199,201,3,2,1,0,200,199,1,0,0,0,201,202,1,0,0,0,202,200,1,0,0,
        0,202,203,1,0,0,0,203,37,1,0,0,0,204,206,3,2,1,0,205,204,1,0,0,0,
        206,207,1,0,0,0,207,205,1,0,0,0,207,208,1,0,0,0,208,209,1,0,0,0,
        209,210,5,7,0,0,210,211,3,2,1,0,211,39,1,0,0,0,212,216,5,1,0,0,213,
        215,3,42,21,0,214,213,1,0,0,0,215,218,1,0,0,0,216,214,1,0,0,0,216,
        217,1,0,0,0,217,219,1,0,0,0,218,216,1,0,0,0,219,220,5,2,0,0,220,
        41,1,0,0,0,221,234,5,32,0,0,222,234,5,9,0,0,223,224,5,10,0,0,224,
        234,5,32,0,0,225,234,5,11,0,0,226,234,5,12,0,0,227,228,5,1,0,0,228,
        230,5,32,0,0,229,231,3,2,1,0,230,229,1,0,0,0,230,231,1,0,0,0,231,
        232,1,0,0,0,232,234,5,2,0,0,233,221,1,0,0,0,233,222,1,0,0,0,233,
        223,1,0,0,0,233,225,1,0,0,0,233,226,1,0,0,0,233,227,1,0,0,0,234,
        43,1,0,0,0,235,236,5,31,0,0,236,45,1,0,0,0,237,239,3,2,1,0,238,237,
        1,0,0,0,239,240,1,0,0,0,240,238,1,0,0,0,240,241,1,0,0,0,241,47,1,
        0,0,0,242,243,7,2,0,0,243,49,1,0,0,0,25,53,62,72,78,85,101,109,119,
        129,136,145,148,154,160,167,176,183,188,191,202,207,216,230,233,
        240
    ]

class lispParser ( Parser ):

    grammarFileName = "lispParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'''", "'`'", "',@'", "','", 
                     "'.'", "'#('", "'&optional'", "'&rest'", "'&key'", 
                     "'&aux'" ]

    symbolicNames = [ "<INVALID>", "LPAREN", "RPAREN", "QUOTE", "BACKQUOTE", 
                      "COMMA_AT", "COMMA", "DOT", "VECTOR_START", "AMP_OPTIONAL", 
                      "AMP_REST", "AMP_KEY", "AMP_AUX", "DEFUN", "LAMBDA", 
                      "LETSTAR", "LET", "IF", "COND", "PROGN", "SETQ", "DEFVAR", 
                      "DEFPARAMETER", "DEFCONSTANT", "QUOTE_KW", "FUNCTION_KW", 
                      "NIL", "TRUE", "BOOLEAN", "CharacterLiteral", "Number", 
                      "StringLiteral", "SYMBOL", "LineComment", "BlockComment", 
                      "WS" ]

    RULE_program = 0
    RULE_form = 1
    RULE_quotedForm = 2
    RULE_vector = 3
    RULE_list = 4
    RULE_listContent = 5
    RULE_defunForm = 6
    RULE_lambdaForm = 7
    RULE_letForm = 8
    RULE_bindingSpec = 9
    RULE_ifForm = 10
    RULE_condForm = 11
    RULE_condClause = 12
    RULE_prognForm = 13
    RULE_setqForm = 14
    RULE_definitionForm = 15
    RULE_quoteSpecialForm = 16
    RULE_functionSpecialForm = 17
    RULE_applicationForm = 18
    RULE_dottedList = 19
    RULE_lambdaList = 20
    RULE_lambdaListElement = 21
    RULE_declaration = 22
    RULE_body = 23
    RULE_atom = 24

    ruleNames =  [ "program", "form", "quotedForm", "vector", "list", "listContent", 
                   "defunForm", "lambdaForm", "letForm", "bindingSpec", 
                   "ifForm", "condForm", "condClause", "prognForm", "setqForm", 
                   "definitionForm", "quoteSpecialForm", "functionSpecialForm", 
                   "applicationForm", "dottedList", "lambdaList", "lambdaListElement", 
                   "declaration", "body", "atom" ]

    EOF = Token.EOF
    LPAREN=1
    RPAREN=2
    QUOTE=3
    BACKQUOTE=4
    COMMA_AT=5
    COMMA=6
    DOT=7
    VECTOR_START=8
    AMP_OPTIONAL=9
    AMP_REST=10
    AMP_KEY=11
    AMP_AUX=12
    DEFUN=13
    LAMBDA=14
    LETSTAR=15
    LET=16
    IF=17
    COND=18
    PROGN=19
    SETQ=20
    DEFVAR=21
    DEFPARAMETER=22
    DEFCONSTANT=23
    QUOTE_KW=24
    FUNCTION_KW=25
    NIL=26
    TRUE=27
    BOOLEAN=28
    CharacterLiteral=29
    Number=30
    StringLiteral=31
    SYMBOL=32
    LineComment=33
    BlockComment=34
    WS=35

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(lispParser.EOF, 0)

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.FormContext)
            else:
                return self.getTypedRuleContext(lispParser.FormContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = lispParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 8522826106) != 0):
                self.state = 50
                self.form()
                self.state = 55
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 56
            self.match(lispParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def atom(self):
            return self.getTypedRuleContext(lispParser.AtomContext,0)


        def list_(self):
            return self.getTypedRuleContext(lispParser.ListContext,0)


        def vector(self):
            return self.getTypedRuleContext(lispParser.VectorContext,0)


        def quotedForm(self):
            return self.getTypedRuleContext(lispParser.QuotedFormContext,0)


        def getRuleIndex(self):
            return lispParser.RULE_form

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForm" ):
                listener.enterForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForm" ):
                listener.exitForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForm" ):
                return visitor.visitForm(self)
            else:
                return visitor.visitChildren(self)




    def form(self):

        localctx = lispParser.FormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_form)
        try:
            self.state = 62
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [26, 27, 28, 29, 30, 31, 32]:
                self.enterOuterAlt(localctx, 1)
                self.state = 58
                self.atom()
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 59
                self.list_()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 3)
                self.state = 60
                self.vector()
                pass
            elif token in [3, 4, 5, 6]:
                self.enterOuterAlt(localctx, 4)
                self.state = 61
                self.quotedForm()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuotedFormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTE(self):
            return self.getToken(lispParser.QUOTE, 0)

        def form(self):
            return self.getTypedRuleContext(lispParser.FormContext,0)


        def BACKQUOTE(self):
            return self.getToken(lispParser.BACKQUOTE, 0)

        def COMMA(self):
            return self.getToken(lispParser.COMMA, 0)

        def COMMA_AT(self):
            return self.getToken(lispParser.COMMA_AT, 0)

        def getRuleIndex(self):
            return lispParser.RULE_quotedForm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuotedForm" ):
                listener.enterQuotedForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuotedForm" ):
                listener.exitQuotedForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuotedForm" ):
                return visitor.visitQuotedForm(self)
            else:
                return visitor.visitChildren(self)




    def quotedForm(self):

        localctx = lispParser.QuotedFormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_quotedForm)
        try:
            self.state = 72
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.enterOuterAlt(localctx, 1)
                self.state = 64
                self.match(lispParser.QUOTE)
                self.state = 65
                self.form()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 66
                self.match(lispParser.BACKQUOTE)
                self.state = 67
                self.form()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 3)
                self.state = 68
                self.match(lispParser.COMMA)
                self.state = 69
                self.form()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 4)
                self.state = 70
                self.match(lispParser.COMMA_AT)
                self.state = 71
                self.form()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VectorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VECTOR_START(self):
            return self.getToken(lispParser.VECTOR_START, 0)

        def RPAREN(self):
            return self.getToken(lispParser.RPAREN, 0)

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.FormContext)
            else:
                return self.getTypedRuleContext(lispParser.FormContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_vector

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVector" ):
                listener.enterVector(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVector" ):
                listener.exitVector(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVector" ):
                return visitor.visitVector(self)
            else:
                return visitor.visitChildren(self)




    def vector(self):

        localctx = lispParser.VectorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_vector)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            self.match(lispParser.VECTOR_START)
            self.state = 78
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 8522826106) != 0):
                self.state = 75
                self.form()
                self.state = 80
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 81
            self.match(lispParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(lispParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(lispParser.RPAREN, 0)

        def listContent(self):
            return self.getTypedRuleContext(lispParser.ListContentContext,0)


        def getRuleIndex(self):
            return lispParser.RULE_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterList" ):
                listener.enterList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitList" ):
                listener.exitList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitList" ):
                return visitor.visitList(self)
            else:
                return visitor.visitChildren(self)




    def list_(self):

        localctx = lispParser.ListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            self.match(lispParser.LPAREN)
            self.state = 85
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8589926778) != 0):
                self.state = 84
                self.listContent()


            self.state = 87
            self.match(lispParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ListContentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def defunForm(self):
            return self.getTypedRuleContext(lispParser.DefunFormContext,0)


        def lambdaForm(self):
            return self.getTypedRuleContext(lispParser.LambdaFormContext,0)


        def letForm(self):
            return self.getTypedRuleContext(lispParser.LetFormContext,0)


        def ifForm(self):
            return self.getTypedRuleContext(lispParser.IfFormContext,0)


        def condForm(self):
            return self.getTypedRuleContext(lispParser.CondFormContext,0)


        def prognForm(self):
            return self.getTypedRuleContext(lispParser.PrognFormContext,0)


        def setqForm(self):
            return self.getTypedRuleContext(lispParser.SetqFormContext,0)


        def definitionForm(self):
            return self.getTypedRuleContext(lispParser.DefinitionFormContext,0)


        def quoteSpecialForm(self):
            return self.getTypedRuleContext(lispParser.QuoteSpecialFormContext,0)


        def functionSpecialForm(self):
            return self.getTypedRuleContext(lispParser.FunctionSpecialFormContext,0)


        def dottedList(self):
            return self.getTypedRuleContext(lispParser.DottedListContext,0)


        def applicationForm(self):
            return self.getTypedRuleContext(lispParser.ApplicationFormContext,0)


        def getRuleIndex(self):
            return lispParser.RULE_listContent

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterListContent" ):
                listener.enterListContent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitListContent" ):
                listener.exitListContent(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitListContent" ):
                return visitor.visitListContent(self)
            else:
                return visitor.visitChildren(self)




    def listContent(self):

        localctx = lispParser.ListContentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_listContent)
        try:
            self.state = 101
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 89
                self.defunForm()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 90
                self.lambdaForm()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 91
                self.letForm()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 92
                self.ifForm()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 93
                self.condForm()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 94
                self.prognForm()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 95
                self.setqForm()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 96
                self.definitionForm()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 97
                self.quoteSpecialForm()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 98
                self.functionSpecialForm()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 99
                self.dottedList()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 100
                self.applicationForm()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefunFormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DEFUN(self):
            return self.getToken(lispParser.DEFUN, 0)

        def SYMBOL(self):
            return self.getToken(lispParser.SYMBOL, 0)

        def lambdaList(self):
            return self.getTypedRuleContext(lispParser.LambdaListContext,0)


        def body(self):
            return self.getTypedRuleContext(lispParser.BodyContext,0)


        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(lispParser.DeclarationContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_defunForm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefunForm" ):
                listener.enterDefunForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefunForm" ):
                listener.exitDefunForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefunForm" ):
                return visitor.visitDefunForm(self)
            else:
                return visitor.visitChildren(self)




    def defunForm(self):

        localctx = lispParser.DefunFormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_defunForm)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 103
            self.match(lispParser.DEFUN)
            self.state = 104
            self.match(lispParser.SYMBOL)
            self.state = 105
            self.lambdaList()
            self.state = 109
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 106
                    self.declaration() 
                self.state = 111
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

            self.state = 112
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LambdaFormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LAMBDA(self):
            return self.getToken(lispParser.LAMBDA, 0)

        def lambdaList(self):
            return self.getTypedRuleContext(lispParser.LambdaListContext,0)


        def body(self):
            return self.getTypedRuleContext(lispParser.BodyContext,0)


        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(lispParser.DeclarationContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_lambdaForm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLambdaForm" ):
                listener.enterLambdaForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLambdaForm" ):
                listener.exitLambdaForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLambdaForm" ):
                return visitor.visitLambdaForm(self)
            else:
                return visitor.visitChildren(self)




    def lambdaForm(self):

        localctx = lispParser.LambdaFormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_lambdaForm)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 114
            self.match(lispParser.LAMBDA)
            self.state = 115
            self.lambdaList()
            self.state = 119
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 116
                    self.declaration() 
                self.state = 121
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

            self.state = 122
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LetFormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(lispParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(lispParser.RPAREN, 0)

        def body(self):
            return self.getTypedRuleContext(lispParser.BodyContext,0)


        def LET(self):
            return self.getToken(lispParser.LET, 0)

        def LETSTAR(self):
            return self.getToken(lispParser.LETSTAR, 0)

        def bindingSpec(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.BindingSpecContext)
            else:
                return self.getTypedRuleContext(lispParser.BindingSpecContext,i)


        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(lispParser.DeclarationContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_letForm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLetForm" ):
                listener.enterLetForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLetForm" ):
                listener.exitLetForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetForm" ):
                return visitor.visitLetForm(self)
            else:
                return visitor.visitChildren(self)




    def letForm(self):

        localctx = lispParser.LetFormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_letForm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            _la = self._input.LA(1)
            if not(_la==15 or _la==16):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 125
            self.match(lispParser.LPAREN)
            self.state = 129
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1 or _la==32:
                self.state = 126
                self.bindingSpec()
                self.state = 131
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 132
            self.match(lispParser.RPAREN)
            self.state = 136
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,9,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 133
                    self.declaration() 
                self.state = 138
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,9,self._ctx)

            self.state = 139
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BindingSpecContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL(self):
            return self.getToken(lispParser.SYMBOL, 0)

        def LPAREN(self):
            return self.getToken(lispParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(lispParser.RPAREN, 0)

        def form(self):
            return self.getTypedRuleContext(lispParser.FormContext,0)


        def getRuleIndex(self):
            return lispParser.RULE_bindingSpec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBindingSpec" ):
                listener.enterBindingSpec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBindingSpec" ):
                listener.exitBindingSpec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBindingSpec" ):
                return visitor.visitBindingSpec(self)
            else:
                return visitor.visitChildren(self)




    def bindingSpec(self):

        localctx = lispParser.BindingSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_bindingSpec)
        self._la = 0 # Token type
        try:
            self.state = 148
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [32]:
                self.enterOuterAlt(localctx, 1)
                self.state = 141
                self.match(lispParser.SYMBOL)
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 142
                self.match(lispParser.LPAREN)
                self.state = 143
                self.match(lispParser.SYMBOL)
                self.state = 145
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8522826106) != 0):
                    self.state = 144
                    self.form()


                self.state = 147
                self.match(lispParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfFormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(lispParser.IF, 0)

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.FormContext)
            else:
                return self.getTypedRuleContext(lispParser.FormContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_ifForm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfForm" ):
                listener.enterIfForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfForm" ):
                listener.exitIfForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfForm" ):
                return visitor.visitIfForm(self)
            else:
                return visitor.visitChildren(self)




    def ifForm(self):

        localctx = lispParser.IfFormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_ifForm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 150
            self.match(lispParser.IF)
            self.state = 151
            self.form()
            self.state = 152
            self.form()
            self.state = 154
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8522826106) != 0):
                self.state = 153
                self.form()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CondFormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COND(self):
            return self.getToken(lispParser.COND, 0)

        def condClause(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.CondClauseContext)
            else:
                return self.getTypedRuleContext(lispParser.CondClauseContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_condForm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondForm" ):
                listener.enterCondForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondForm" ):
                listener.exitCondForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondForm" ):
                return visitor.visitCondForm(self)
            else:
                return visitor.visitChildren(self)




    def condForm(self):

        localctx = lispParser.CondFormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_condForm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 156
            self.match(lispParser.COND)
            self.state = 158 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 157
                self.condClause()
                self.state = 160 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CondClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(lispParser.LPAREN, 0)

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.FormContext)
            else:
                return self.getTypedRuleContext(lispParser.FormContext,i)


        def RPAREN(self):
            return self.getToken(lispParser.RPAREN, 0)

        def getRuleIndex(self):
            return lispParser.RULE_condClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondClause" ):
                listener.enterCondClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondClause" ):
                listener.exitCondClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondClause" ):
                return visitor.visitCondClause(self)
            else:
                return visitor.visitChildren(self)




    def condClause(self):

        localctx = lispParser.CondClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_condClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 162
            self.match(lispParser.LPAREN)
            self.state = 163
            self.form()
            self.state = 167
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 8522826106) != 0):
                self.state = 164
                self.form()
                self.state = 169
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 170
            self.match(lispParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrognFormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROGN(self):
            return self.getToken(lispParser.PROGN, 0)

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.FormContext)
            else:
                return self.getTypedRuleContext(lispParser.FormContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_prognForm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrognForm" ):
                listener.enterPrognForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrognForm" ):
                listener.exitPrognForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrognForm" ):
                return visitor.visitPrognForm(self)
            else:
                return visitor.visitChildren(self)




    def prognForm(self):

        localctx = lispParser.PrognFormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_prognForm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 172
            self.match(lispParser.PROGN)
            self.state = 174 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 173
                self.form()
                self.state = 176 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 8522826106) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SetqFormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SETQ(self):
            return self.getToken(lispParser.SETQ, 0)

        def SYMBOL(self, i:int=None):
            if i is None:
                return self.getTokens(lispParser.SYMBOL)
            else:
                return self.getToken(lispParser.SYMBOL, i)

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.FormContext)
            else:
                return self.getTypedRuleContext(lispParser.FormContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_setqForm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetqForm" ):
                listener.enterSetqForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetqForm" ):
                listener.exitSetqForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetqForm" ):
                return visitor.visitSetqForm(self)
            else:
                return visitor.visitChildren(self)




    def setqForm(self):

        localctx = lispParser.SetqFormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_setqForm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            self.match(lispParser.SETQ)
            self.state = 181 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 179
                self.match(lispParser.SYMBOL)
                self.state = 180
                self.form()
                self.state = 183 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==32):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefinitionFormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL(self):
            return self.getToken(lispParser.SYMBOL, 0)

        def DEFVAR(self):
            return self.getToken(lispParser.DEFVAR, 0)

        def DEFPARAMETER(self):
            return self.getToken(lispParser.DEFPARAMETER, 0)

        def DEFCONSTANT(self):
            return self.getToken(lispParser.DEFCONSTANT, 0)

        def form(self):
            return self.getTypedRuleContext(lispParser.FormContext,0)


        def StringLiteral(self):
            return self.getToken(lispParser.StringLiteral, 0)

        def getRuleIndex(self):
            return lispParser.RULE_definitionForm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefinitionForm" ):
                listener.enterDefinitionForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefinitionForm" ):
                listener.exitDefinitionForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefinitionForm" ):
                return visitor.visitDefinitionForm(self)
            else:
                return visitor.visitChildren(self)




    def definitionForm(self):

        localctx = lispParser.DefinitionFormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_definitionForm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 185
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 14680064) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 186
            self.match(lispParser.SYMBOL)
            self.state = 188
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.state = 187
                self.form()


            self.state = 191
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==31:
                self.state = 190
                self.match(lispParser.StringLiteral)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuoteSpecialFormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTE_KW(self):
            return self.getToken(lispParser.QUOTE_KW, 0)

        def form(self):
            return self.getTypedRuleContext(lispParser.FormContext,0)


        def getRuleIndex(self):
            return lispParser.RULE_quoteSpecialForm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuoteSpecialForm" ):
                listener.enterQuoteSpecialForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuoteSpecialForm" ):
                listener.exitQuoteSpecialForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuoteSpecialForm" ):
                return visitor.visitQuoteSpecialForm(self)
            else:
                return visitor.visitChildren(self)




    def quoteSpecialForm(self):

        localctx = lispParser.QuoteSpecialFormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_quoteSpecialForm)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 193
            self.match(lispParser.QUOTE_KW)
            self.state = 194
            self.form()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionSpecialFormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNCTION_KW(self):
            return self.getToken(lispParser.FUNCTION_KW, 0)

        def form(self):
            return self.getTypedRuleContext(lispParser.FormContext,0)


        def getRuleIndex(self):
            return lispParser.RULE_functionSpecialForm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionSpecialForm" ):
                listener.enterFunctionSpecialForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionSpecialForm" ):
                listener.exitFunctionSpecialForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionSpecialForm" ):
                return visitor.visitFunctionSpecialForm(self)
            else:
                return visitor.visitChildren(self)




    def functionSpecialForm(self):

        localctx = lispParser.FunctionSpecialFormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_functionSpecialForm)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
            self.match(lispParser.FUNCTION_KW)
            self.state = 197
            self.form()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ApplicationFormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.FormContext)
            else:
                return self.getTypedRuleContext(lispParser.FormContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_applicationForm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterApplicationForm" ):
                listener.enterApplicationForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitApplicationForm" ):
                listener.exitApplicationForm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitApplicationForm" ):
                return visitor.visitApplicationForm(self)
            else:
                return visitor.visitChildren(self)




    def applicationForm(self):

        localctx = lispParser.ApplicationFormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_applicationForm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 199
                self.form()
                self.state = 202 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 8522826106) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DottedListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOT(self):
            return self.getToken(lispParser.DOT, 0)

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.FormContext)
            else:
                return self.getTypedRuleContext(lispParser.FormContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_dottedList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDottedList" ):
                listener.enterDottedList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDottedList" ):
                listener.exitDottedList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDottedList" ):
                return visitor.visitDottedList(self)
            else:
                return visitor.visitChildren(self)




    def dottedList(self):

        localctx = lispParser.DottedListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_dottedList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 205 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 204
                self.form()
                self.state = 207 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 8522826106) != 0)):
                    break

            self.state = 209
            self.match(lispParser.DOT)
            self.state = 210
            self.form()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LambdaListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(lispParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(lispParser.RPAREN, 0)

        def lambdaListElement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.LambdaListElementContext)
            else:
                return self.getTypedRuleContext(lispParser.LambdaListElementContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_lambdaList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLambdaList" ):
                listener.enterLambdaList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLambdaList" ):
                listener.exitLambdaList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLambdaList" ):
                return visitor.visitLambdaList(self)
            else:
                return visitor.visitChildren(self)




    def lambdaList(self):

        localctx = lispParser.LambdaListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_lambdaList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 212
            self.match(lispParser.LPAREN)
            self.state = 216
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 4294974978) != 0):
                self.state = 213
                self.lambdaListElement()
                self.state = 218
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 219
            self.match(lispParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LambdaListElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL(self):
            return self.getToken(lispParser.SYMBOL, 0)

        def AMP_OPTIONAL(self):
            return self.getToken(lispParser.AMP_OPTIONAL, 0)

        def AMP_REST(self):
            return self.getToken(lispParser.AMP_REST, 0)

        def AMP_KEY(self):
            return self.getToken(lispParser.AMP_KEY, 0)

        def AMP_AUX(self):
            return self.getToken(lispParser.AMP_AUX, 0)

        def LPAREN(self):
            return self.getToken(lispParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(lispParser.RPAREN, 0)

        def form(self):
            return self.getTypedRuleContext(lispParser.FormContext,0)


        def getRuleIndex(self):
            return lispParser.RULE_lambdaListElement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLambdaListElement" ):
                listener.enterLambdaListElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLambdaListElement" ):
                listener.exitLambdaListElement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLambdaListElement" ):
                return visitor.visitLambdaListElement(self)
            else:
                return visitor.visitChildren(self)




    def lambdaListElement(self):

        localctx = lispParser.LambdaListElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_lambdaListElement)
        self._la = 0 # Token type
        try:
            self.state = 233
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [32]:
                self.enterOuterAlt(localctx, 1)
                self.state = 221
                self.match(lispParser.SYMBOL)
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 2)
                self.state = 222
                self.match(lispParser.AMP_OPTIONAL)
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 3)
                self.state = 223
                self.match(lispParser.AMP_REST)
                self.state = 224
                self.match(lispParser.SYMBOL)
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 4)
                self.state = 225
                self.match(lispParser.AMP_KEY)
                pass
            elif token in [12]:
                self.enterOuterAlt(localctx, 5)
                self.state = 226
                self.match(lispParser.AMP_AUX)
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 6)
                self.state = 227
                self.match(lispParser.LPAREN)
                self.state = 228
                self.match(lispParser.SYMBOL)
                self.state = 230
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8522826106) != 0):
                    self.state = 229
                    self.form()


                self.state = 232
                self.match(lispParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def StringLiteral(self):
            return self.getToken(lispParser.StringLiteral, 0)

        def getRuleIndex(self):
            return lispParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaration" ):
                return visitor.visitDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def declaration(self):

        localctx = lispParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 235
            self.match(lispParser.StringLiteral)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lispParser.FormContext)
            else:
                return self.getTypedRuleContext(lispParser.FormContext,i)


        def getRuleIndex(self):
            return lispParser.RULE_body

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBody" ):
                listener.enterBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBody" ):
                listener.exitBody(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBody" ):
                return visitor.visitBody(self)
            else:
                return visitor.visitChildren(self)




    def body(self):

        localctx = lispParser.BodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_body)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 238 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 237
                self.form()
                self.state = 240 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 8522826106) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Number(self):
            return self.getToken(lispParser.Number, 0)

        def StringLiteral(self):
            return self.getToken(lispParser.StringLiteral, 0)

        def CharacterLiteral(self):
            return self.getToken(lispParser.CharacterLiteral, 0)

        def BOOLEAN(self):
            return self.getToken(lispParser.BOOLEAN, 0)

        def NIL(self):
            return self.getToken(lispParser.NIL, 0)

        def TRUE(self):
            return self.getToken(lispParser.TRUE, 0)

        def SYMBOL(self):
            return self.getToken(lispParser.SYMBOL, 0)

        def getRuleIndex(self):
            return lispParser.RULE_atom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom" ):
                listener.enterAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom" ):
                listener.exitAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom" ):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)




    def atom(self):

        localctx = lispParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 242
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8522825728) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





