# Generated from grammar/MiniPascalParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MiniPascalParser import MiniPascalParser
else:
    from MiniPascalParser import MiniPascalParser

# This class defines a complete generic visitor for a parse tree produced by MiniPascalParser.

class MiniPascalParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MiniPascalParser#programFile.
    def visitProgramFile(self, ctx:MiniPascalParser.ProgramFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#varSection.
    def visitVarSection(self, ctx:MiniPascalParser.VarSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#varDeclaration.
    def visitVarDeclaration(self, ctx:MiniPascalParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#identList.
    def visitIdentList(self, ctx:MiniPascalParser.IdentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#typeName.
    def visitTypeName(self, ctx:MiniPascalParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#block.
    def visitBlock(self, ctx:MiniPascalParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#statementList.
    def visitStatementList(self, ctx:MiniPascalParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#statement.
    def visitStatement(self, ctx:MiniPascalParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#ifStatement.
    def visitIfStatement(self, ctx:MiniPascalParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#condition.
    def visitCondition(self, ctx:MiniPascalParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#compareOp.
    def visitCompareOp(self, ctx:MiniPascalParser.CompareOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#assignment.
    def visitAssignment(self, ctx:MiniPascalParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#expr.
    def visitExpr(self, ctx:MiniPascalParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#term.
    def visitTerm(self, ctx:MiniPascalParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#factor.
    def visitFactor(self, ctx:MiniPascalParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#writeLnStatement.
    def visitWriteLnStatement(self, ctx:MiniPascalParser.WriteLnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#writeArgList.
    def visitWriteArgList(self, ctx:MiniPascalParser.WriteArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#writeArg.
    def visitWriteArg(self, ctx:MiniPascalParser.WriteArgContext):
        return self.visitChildren(ctx)



del MiniPascalParser