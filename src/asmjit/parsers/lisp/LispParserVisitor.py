# Generated from compiler/grammar/LispParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LispParser import LispParser
else:
    from LispParser import LispParser

# This class defines a complete generic visitor for a parse tree produced by LispParser.

class LispParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LispParser#program.
    def visitProgram(self, ctx:LispParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LispParser#expression.
    def visitExpression(self, ctx:LispParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LispParser#list.
    def visitList(self, ctx:LispParser.ListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LispParser#quotedExpression.
    def visitQuotedExpression(self, ctx:LispParser.QuotedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LispParser#atom.
    def visitAtom(self, ctx:LispParser.AtomContext):
        return self.visitChildren(ctx)



del LispParser