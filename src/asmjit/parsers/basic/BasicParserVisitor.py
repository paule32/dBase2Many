# Generated from compiler/grammar/BasicParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .BasicParser import BasicParser
else:
    from BasicParser import BasicParser

# This class defines a complete generic visitor for a parse tree produced by BasicParser.

class BasicParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by BasicParser#program.
    def visitProgram(self, ctx:BasicParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#topLevelItem.
    def visitTopLevelItem(self, ctx:BasicParser.TopLevelItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#separators.
    def visitSeparators(self, ctx:BasicParser.SeparatorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#separator.
    def visitSeparator(self, ctx:BasicParser.SeparatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#subDeclaration.
    def visitSubDeclaration(self, ctx:BasicParser.SubDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#functionDeclaration.
    def visitFunctionDeclaration(self, ctx:BasicParser.FunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#parameterList.
    def visitParameterList(self, ctx:BasicParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#parameterDeclList.
    def visitParameterDeclList(self, ctx:BasicParser.ParameterDeclListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#parameterDecl.
    def visitParameterDecl(self, ctx:BasicParser.ParameterDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#statement.
    def visitStatement(self, ctx:BasicParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#lineNumber.
    def visitLineNumber(self, ctx:BasicParser.LineNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#statementCore.
    def visitStatementCore(self, ctx:BasicParser.StatementCoreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#statementBlock.
    def visitStatementBlock(self, ctx:BasicParser.StatementBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#inlineStatement.
    def visitInlineStatement(self, ctx:BasicParser.InlineStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:BasicParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#constStatement.
    def visitConstStatement(self, ctx:BasicParser.ConstStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#dimStatement.
    def visitDimStatement(self, ctx:BasicParser.DimStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#variableDecl.
    def visitVariableDecl(self, ctx:BasicParser.VariableDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#arrayBounds.
    def visitArrayBounds(self, ctx:BasicParser.ArrayBoundsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#lvalue.
    def visitLvalue(self, ctx:BasicParser.LvalueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#printStatement.
    def visitPrintStatement(self, ctx:BasicParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#printList.
    def visitPrintList(self, ctx:BasicParser.PrintListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#inputStatement.
    def visitInputStatement(self, ctx:BasicParser.InputStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#inlineIf.
    def visitInlineIf(self, ctx:BasicParser.InlineIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#blockIf.
    def visitBlockIf(self, ctx:BasicParser.BlockIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#forStatement.
    def visitForStatement(self, ctx:BasicParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#whileStatement.
    def visitWhileStatement(self, ctx:BasicParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#doWhilePre.
    def visitDoWhilePre(self, ctx:BasicParser.DoWhilePreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#doUntilPre.
    def visitDoUntilPre(self, ctx:BasicParser.DoUntilPreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#doWhilePost.
    def visitDoWhilePost(self, ctx:BasicParser.DoWhilePostContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#doUntilPost.
    def visitDoUntilPost(self, ctx:BasicParser.DoUntilPostContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#doForever.
    def visitDoForever(self, ctx:BasicParser.DoForeverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#gotoStatement.
    def visitGotoStatement(self, ctx:BasicParser.GotoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#gosubStatement.
    def visitGosubStatement(self, ctx:BasicParser.GosubStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#jumpTarget.
    def visitJumpTarget(self, ctx:BasicParser.JumpTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#returnStatement.
    def visitReturnStatement(self, ctx:BasicParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#callStatement.
    def visitCallStatement(self, ctx:BasicParser.CallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#exitStatement.
    def visitExitStatement(self, ctx:BasicParser.ExitStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#labelStatement.
    def visitLabelStatement(self, ctx:BasicParser.LabelStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#stopStatement.
    def visitStopStatement(self, ctx:BasicParser.StopStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#typeName.
    def visitTypeName(self, ctx:BasicParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#expression.
    def visitExpression(self, ctx:BasicParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#orExpression.
    def visitOrExpression(self, ctx:BasicParser.OrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#xorExpression.
    def visitXorExpression(self, ctx:BasicParser.XorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#andExpression.
    def visitAndExpression(self, ctx:BasicParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#notExpression.
    def visitNotExpression(self, ctx:BasicParser.NotExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#comparisonExpression.
    def visitComparisonExpression(self, ctx:BasicParser.ComparisonExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:BasicParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:BasicParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#powerExpression.
    def visitPowerExpression(self, ctx:BasicParser.PowerExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#unaryExpression.
    def visitUnaryExpression(self, ctx:BasicParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:BasicParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#argumentList.
    def visitArgumentList(self, ctx:BasicParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BasicParser#literal.
    def visitLiteral(self, ctx:BasicParser.LiteralContext):
        return self.visitChildren(ctx)



del BasicParser