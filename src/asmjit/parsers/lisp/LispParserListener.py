# Generated from compiler/grammar/LispParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LispParser import LispParser
else:
    from LispParser import LispParser

# This class defines a complete listener for a parse tree produced by LispParser.
class LispParserListener(ParseTreeListener):

    # Enter a parse tree produced by LispParser#program.
    def enterProgram(self, ctx:LispParser.ProgramContext):
        pass

    # Exit a parse tree produced by LispParser#program.
    def exitProgram(self, ctx:LispParser.ProgramContext):
        pass


    # Enter a parse tree produced by LispParser#expression.
    def enterExpression(self, ctx:LispParser.ExpressionContext):
        pass

    # Exit a parse tree produced by LispParser#expression.
    def exitExpression(self, ctx:LispParser.ExpressionContext):
        pass


    # Enter a parse tree produced by LispParser#list.
    def enterList(self, ctx:LispParser.ListContext):
        pass

    # Exit a parse tree produced by LispParser#list.
    def exitList(self, ctx:LispParser.ListContext):
        pass


    # Enter a parse tree produced by LispParser#quotedExpression.
    def enterQuotedExpression(self, ctx:LispParser.QuotedExpressionContext):
        pass

    # Exit a parse tree produced by LispParser#quotedExpression.
    def exitQuotedExpression(self, ctx:LispParser.QuotedExpressionContext):
        pass


    # Enter a parse tree produced by LispParser#atom.
    def enterAtom(self, ctx:LispParser.AtomContext):
        pass

    # Exit a parse tree produced by LispParser#atom.
    def exitAtom(self, ctx:LispParser.AtomContext):
        pass



del LispParser