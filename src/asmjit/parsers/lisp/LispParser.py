# Generated from compiler/grammar/LispParser.g4 by ANTLR 4.13.2
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
        4,1,8,38,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,5,0,12,8,0,
        10,0,12,0,15,9,0,1,0,1,0,1,1,1,1,1,1,3,1,22,8,1,1,2,1,2,5,2,26,8,
        2,10,2,12,2,29,9,2,1,2,1,2,1,3,1,3,1,3,1,4,1,4,1,4,0,0,5,0,2,4,6,
        8,0,1,1,0,4,6,36,0,13,1,0,0,0,2,21,1,0,0,0,4,23,1,0,0,0,6,32,1,0,
        0,0,8,35,1,0,0,0,10,12,3,2,1,0,11,10,1,0,0,0,12,15,1,0,0,0,13,11,
        1,0,0,0,13,14,1,0,0,0,14,16,1,0,0,0,15,13,1,0,0,0,16,17,5,0,0,1,
        17,1,1,0,0,0,18,22,3,8,4,0,19,22,3,4,2,0,20,22,3,6,3,0,21,18,1,0,
        0,0,21,19,1,0,0,0,21,20,1,0,0,0,22,3,1,0,0,0,23,27,5,1,0,0,24,26,
        3,2,1,0,25,24,1,0,0,0,26,29,1,0,0,0,27,25,1,0,0,0,27,28,1,0,0,0,
        28,30,1,0,0,0,29,27,1,0,0,0,30,31,5,2,0,0,31,5,1,0,0,0,32,33,5,3,
        0,0,33,34,3,2,1,0,34,7,1,0,0,0,35,36,7,0,0,0,36,9,1,0,0,0,3,13,21,
        27
    ]

class LispParser ( Parser ):

    grammarFileName = "LispParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'''" ]

    symbolicNames = [ "<INVALID>", "LPAREN", "RPAREN", "QUOTE", "NUMBER", 
                      "STRING", "SYMBOL", "WS", "COMMENT" ]

    RULE_program = 0
    RULE_expression = 1
    RULE_list = 2
    RULE_quotedExpression = 3
    RULE_atom = 4

    ruleNames =  [ "program", "expression", "list", "quotedExpression", 
                   "atom" ]

    EOF = Token.EOF
    LPAREN=1
    RPAREN=2
    QUOTE=3
    NUMBER=4
    STRING=5
    SYMBOL=6
    WS=7
    COMMENT=8

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
            return self.getToken(LispParser.EOF, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LispParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(LispParser.ExpressionContext,i)


        def getRuleIndex(self):
            return LispParser.RULE_program

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

        localctx = LispParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 122) != 0):
                self.state = 10
                self.expression()
                self.state = 15
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 16
            self.match(LispParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def atom(self):
            return self.getTypedRuleContext(LispParser.AtomContext,0)


        def list_(self):
            return self.getTypedRuleContext(LispParser.ListContext,0)


        def quotedExpression(self):
            return self.getTypedRuleContext(LispParser.QuotedExpressionContext,0)


        def getRuleIndex(self):
            return LispParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = LispParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_expression)
        try:
            self.state = 21
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4, 5, 6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 18
                self.atom()
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 19
                self.list_()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 3)
                self.state = 20
                self.quotedExpression()
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


    class ListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(LispParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(LispParser.RPAREN, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LispParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(LispParser.ExpressionContext,i)


        def getRuleIndex(self):
            return LispParser.RULE_list

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

        localctx = LispParser.ListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self.match(LispParser.LPAREN)
            self.state = 27
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 122) != 0):
                self.state = 24
                self.expression()
                self.state = 29
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 30
            self.match(LispParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuotedExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTE(self):
            return self.getToken(LispParser.QUOTE, 0)

        def expression(self):
            return self.getTypedRuleContext(LispParser.ExpressionContext,0)


        def getRuleIndex(self):
            return LispParser.RULE_quotedExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuotedExpression" ):
                listener.enterQuotedExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuotedExpression" ):
                listener.exitQuotedExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuotedExpression" ):
                return visitor.visitQuotedExpression(self)
            else:
                return visitor.visitChildren(self)




    def quotedExpression(self):

        localctx = LispParser.QuotedExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_quotedExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            self.match(LispParser.QUOTE)
            self.state = 33
            self.expression()
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

        def NUMBER(self):
            return self.getToken(LispParser.NUMBER, 0)

        def STRING(self):
            return self.getToken(LispParser.STRING, 0)

        def SYMBOL(self):
            return self.getToken(LispParser.SYMBOL, 0)

        def getRuleIndex(self):
            return LispParser.RULE_atom

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

        localctx = LispParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 112) != 0)):
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





