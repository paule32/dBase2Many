# Generated from compiler/grammar/BasicParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .BasicParser import BasicParser
else:
    from BasicParser import BasicParser

# This class defines a complete listener for a parse tree produced by BasicParser.
class BasicParserListener(ParseTreeListener):

    # Enter a parse tree produced by BasicParser#program.
    def enterProgram(self, ctx:BasicParser.ProgramContext):
        pass

    # Exit a parse tree produced by BasicParser#program.
    def exitProgram(self, ctx:BasicParser.ProgramContext):
        pass


    # Enter a parse tree produced by BasicParser#topLevelItem.
    def enterTopLevelItem(self, ctx:BasicParser.TopLevelItemContext):
        pass

    # Exit a parse tree produced by BasicParser#topLevelItem.
    def exitTopLevelItem(self, ctx:BasicParser.TopLevelItemContext):
        pass


    # Enter a parse tree produced by BasicParser#separators.
    def enterSeparators(self, ctx:BasicParser.SeparatorsContext):
        pass

    # Exit a parse tree produced by BasicParser#separators.
    def exitSeparators(self, ctx:BasicParser.SeparatorsContext):
        pass


    # Enter a parse tree produced by BasicParser#separator.
    def enterSeparator(self, ctx:BasicParser.SeparatorContext):
        pass

    # Exit a parse tree produced by BasicParser#separator.
    def exitSeparator(self, ctx:BasicParser.SeparatorContext):
        pass


    # Enter a parse tree produced by BasicParser#subDeclaration.
    def enterSubDeclaration(self, ctx:BasicParser.SubDeclarationContext):
        pass

    # Exit a parse tree produced by BasicParser#subDeclaration.
    def exitSubDeclaration(self, ctx:BasicParser.SubDeclarationContext):
        pass


    # Enter a parse tree produced by BasicParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:BasicParser.FunctionDeclarationContext):
        pass

    # Exit a parse tree produced by BasicParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:BasicParser.FunctionDeclarationContext):
        pass


    # Enter a parse tree produced by BasicParser#parameterList.
    def enterParameterList(self, ctx:BasicParser.ParameterListContext):
        pass

    # Exit a parse tree produced by BasicParser#parameterList.
    def exitParameterList(self, ctx:BasicParser.ParameterListContext):
        pass


    # Enter a parse tree produced by BasicParser#parameterDeclList.
    def enterParameterDeclList(self, ctx:BasicParser.ParameterDeclListContext):
        pass

    # Exit a parse tree produced by BasicParser#parameterDeclList.
    def exitParameterDeclList(self, ctx:BasicParser.ParameterDeclListContext):
        pass


    # Enter a parse tree produced by BasicParser#parameterDecl.
    def enterParameterDecl(self, ctx:BasicParser.ParameterDeclContext):
        pass

    # Exit a parse tree produced by BasicParser#parameterDecl.
    def exitParameterDecl(self, ctx:BasicParser.ParameterDeclContext):
        pass


    # Enter a parse tree produced by BasicParser#statement.
    def enterStatement(self, ctx:BasicParser.StatementContext):
        pass

    # Exit a parse tree produced by BasicParser#statement.
    def exitStatement(self, ctx:BasicParser.StatementContext):
        pass


    # Enter a parse tree produced by BasicParser#lineNumber.
    def enterLineNumber(self, ctx:BasicParser.LineNumberContext):
        pass

    # Exit a parse tree produced by BasicParser#lineNumber.
    def exitLineNumber(self, ctx:BasicParser.LineNumberContext):
        pass


    # Enter a parse tree produced by BasicParser#statementCore.
    def enterStatementCore(self, ctx:BasicParser.StatementCoreContext):
        pass

    # Exit a parse tree produced by BasicParser#statementCore.
    def exitStatementCore(self, ctx:BasicParser.StatementCoreContext):
        pass


    # Enter a parse tree produced by BasicParser#statementBlock.
    def enterStatementBlock(self, ctx:BasicParser.StatementBlockContext):
        pass

    # Exit a parse tree produced by BasicParser#statementBlock.
    def exitStatementBlock(self, ctx:BasicParser.StatementBlockContext):
        pass


    # Enter a parse tree produced by BasicParser#inlineStatement.
    def enterInlineStatement(self, ctx:BasicParser.InlineStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#inlineStatement.
    def exitInlineStatement(self, ctx:BasicParser.InlineStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:BasicParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:BasicParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#constStatement.
    def enterConstStatement(self, ctx:BasicParser.ConstStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#constStatement.
    def exitConstStatement(self, ctx:BasicParser.ConstStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#dimStatement.
    def enterDimStatement(self, ctx:BasicParser.DimStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#dimStatement.
    def exitDimStatement(self, ctx:BasicParser.DimStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#variableDecl.
    def enterVariableDecl(self, ctx:BasicParser.VariableDeclContext):
        pass

    # Exit a parse tree produced by BasicParser#variableDecl.
    def exitVariableDecl(self, ctx:BasicParser.VariableDeclContext):
        pass


    # Enter a parse tree produced by BasicParser#arrayBounds.
    def enterArrayBounds(self, ctx:BasicParser.ArrayBoundsContext):
        pass

    # Exit a parse tree produced by BasicParser#arrayBounds.
    def exitArrayBounds(self, ctx:BasicParser.ArrayBoundsContext):
        pass


    # Enter a parse tree produced by BasicParser#lvalue.
    def enterLvalue(self, ctx:BasicParser.LvalueContext):
        pass

    # Exit a parse tree produced by BasicParser#lvalue.
    def exitLvalue(self, ctx:BasicParser.LvalueContext):
        pass


    # Enter a parse tree produced by BasicParser#printStatement.
    def enterPrintStatement(self, ctx:BasicParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#printStatement.
    def exitPrintStatement(self, ctx:BasicParser.PrintStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#printList.
    def enterPrintList(self, ctx:BasicParser.PrintListContext):
        pass

    # Exit a parse tree produced by BasicParser#printList.
    def exitPrintList(self, ctx:BasicParser.PrintListContext):
        pass


    # Enter a parse tree produced by BasicParser#inputStatement.
    def enterInputStatement(self, ctx:BasicParser.InputStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#inputStatement.
    def exitInputStatement(self, ctx:BasicParser.InputStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#inlineIf.
    def enterInlineIf(self, ctx:BasicParser.InlineIfContext):
        pass

    # Exit a parse tree produced by BasicParser#inlineIf.
    def exitInlineIf(self, ctx:BasicParser.InlineIfContext):
        pass


    # Enter a parse tree produced by BasicParser#blockIf.
    def enterBlockIf(self, ctx:BasicParser.BlockIfContext):
        pass

    # Exit a parse tree produced by BasicParser#blockIf.
    def exitBlockIf(self, ctx:BasicParser.BlockIfContext):
        pass


    # Enter a parse tree produced by BasicParser#forStatement.
    def enterForStatement(self, ctx:BasicParser.ForStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#forStatement.
    def exitForStatement(self, ctx:BasicParser.ForStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#whileStatement.
    def enterWhileStatement(self, ctx:BasicParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#whileStatement.
    def exitWhileStatement(self, ctx:BasicParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#doWhilePre.
    def enterDoWhilePre(self, ctx:BasicParser.DoWhilePreContext):
        pass

    # Exit a parse tree produced by BasicParser#doWhilePre.
    def exitDoWhilePre(self, ctx:BasicParser.DoWhilePreContext):
        pass


    # Enter a parse tree produced by BasicParser#doUntilPre.
    def enterDoUntilPre(self, ctx:BasicParser.DoUntilPreContext):
        pass

    # Exit a parse tree produced by BasicParser#doUntilPre.
    def exitDoUntilPre(self, ctx:BasicParser.DoUntilPreContext):
        pass


    # Enter a parse tree produced by BasicParser#doWhilePost.
    def enterDoWhilePost(self, ctx:BasicParser.DoWhilePostContext):
        pass

    # Exit a parse tree produced by BasicParser#doWhilePost.
    def exitDoWhilePost(self, ctx:BasicParser.DoWhilePostContext):
        pass


    # Enter a parse tree produced by BasicParser#doUntilPost.
    def enterDoUntilPost(self, ctx:BasicParser.DoUntilPostContext):
        pass

    # Exit a parse tree produced by BasicParser#doUntilPost.
    def exitDoUntilPost(self, ctx:BasicParser.DoUntilPostContext):
        pass


    # Enter a parse tree produced by BasicParser#doForever.
    def enterDoForever(self, ctx:BasicParser.DoForeverContext):
        pass

    # Exit a parse tree produced by BasicParser#doForever.
    def exitDoForever(self, ctx:BasicParser.DoForeverContext):
        pass


    # Enter a parse tree produced by BasicParser#gotoStatement.
    def enterGotoStatement(self, ctx:BasicParser.GotoStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#gotoStatement.
    def exitGotoStatement(self, ctx:BasicParser.GotoStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#gosubStatement.
    def enterGosubStatement(self, ctx:BasicParser.GosubStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#gosubStatement.
    def exitGosubStatement(self, ctx:BasicParser.GosubStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#jumpTarget.
    def enterJumpTarget(self, ctx:BasicParser.JumpTargetContext):
        pass

    # Exit a parse tree produced by BasicParser#jumpTarget.
    def exitJumpTarget(self, ctx:BasicParser.JumpTargetContext):
        pass


    # Enter a parse tree produced by BasicParser#returnStatement.
    def enterReturnStatement(self, ctx:BasicParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#returnStatement.
    def exitReturnStatement(self, ctx:BasicParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#callStatement.
    def enterCallStatement(self, ctx:BasicParser.CallStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#callStatement.
    def exitCallStatement(self, ctx:BasicParser.CallStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#exitStatement.
    def enterExitStatement(self, ctx:BasicParser.ExitStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#exitStatement.
    def exitExitStatement(self, ctx:BasicParser.ExitStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#labelStatement.
    def enterLabelStatement(self, ctx:BasicParser.LabelStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#labelStatement.
    def exitLabelStatement(self, ctx:BasicParser.LabelStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#stopStatement.
    def enterStopStatement(self, ctx:BasicParser.StopStatementContext):
        pass

    # Exit a parse tree produced by BasicParser#stopStatement.
    def exitStopStatement(self, ctx:BasicParser.StopStatementContext):
        pass


    # Enter a parse tree produced by BasicParser#typeName.
    def enterTypeName(self, ctx:BasicParser.TypeNameContext):
        pass

    # Exit a parse tree produced by BasicParser#typeName.
    def exitTypeName(self, ctx:BasicParser.TypeNameContext):
        pass


    # Enter a parse tree produced by BasicParser#expression.
    def enterExpression(self, ctx:BasicParser.ExpressionContext):
        pass

    # Exit a parse tree produced by BasicParser#expression.
    def exitExpression(self, ctx:BasicParser.ExpressionContext):
        pass


    # Enter a parse tree produced by BasicParser#orExpression.
    def enterOrExpression(self, ctx:BasicParser.OrExpressionContext):
        pass

    # Exit a parse tree produced by BasicParser#orExpression.
    def exitOrExpression(self, ctx:BasicParser.OrExpressionContext):
        pass


    # Enter a parse tree produced by BasicParser#xorExpression.
    def enterXorExpression(self, ctx:BasicParser.XorExpressionContext):
        pass

    # Exit a parse tree produced by BasicParser#xorExpression.
    def exitXorExpression(self, ctx:BasicParser.XorExpressionContext):
        pass


    # Enter a parse tree produced by BasicParser#andExpression.
    def enterAndExpression(self, ctx:BasicParser.AndExpressionContext):
        pass

    # Exit a parse tree produced by BasicParser#andExpression.
    def exitAndExpression(self, ctx:BasicParser.AndExpressionContext):
        pass


    # Enter a parse tree produced by BasicParser#notExpression.
    def enterNotExpression(self, ctx:BasicParser.NotExpressionContext):
        pass

    # Exit a parse tree produced by BasicParser#notExpression.
    def exitNotExpression(self, ctx:BasicParser.NotExpressionContext):
        pass


    # Enter a parse tree produced by BasicParser#comparisonExpression.
    def enterComparisonExpression(self, ctx:BasicParser.ComparisonExpressionContext):
        pass

    # Exit a parse tree produced by BasicParser#comparisonExpression.
    def exitComparisonExpression(self, ctx:BasicParser.ComparisonExpressionContext):
        pass


    # Enter a parse tree produced by BasicParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:BasicParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by BasicParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:BasicParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by BasicParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:BasicParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by BasicParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:BasicParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by BasicParser#powerExpression.
    def enterPowerExpression(self, ctx:BasicParser.PowerExpressionContext):
        pass

    # Exit a parse tree produced by BasicParser#powerExpression.
    def exitPowerExpression(self, ctx:BasicParser.PowerExpressionContext):
        pass


    # Enter a parse tree produced by BasicParser#unaryExpression.
    def enterUnaryExpression(self, ctx:BasicParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by BasicParser#unaryExpression.
    def exitUnaryExpression(self, ctx:BasicParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by BasicParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:BasicParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by BasicParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:BasicParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by BasicParser#argumentList.
    def enterArgumentList(self, ctx:BasicParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by BasicParser#argumentList.
    def exitArgumentList(self, ctx:BasicParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by BasicParser#literal.
    def enterLiteral(self, ctx:BasicParser.LiteralContext):
        pass

    # Exit a parse tree produced by BasicParser#literal.
    def exitLiteral(self, ctx:BasicParser.LiteralContext):
        pass



del BasicParser