# Generated from compiler/grammar/ElanParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ElanParser import ElanParser
else:
    from ElanParser import ElanParser

# This class defines a complete generic visitor for a parse tree produced by ElanParser.

class ElanParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ElanParser#sourceFile.
    def visitSourceFile(self, ctx:ElanParser.SourceFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#topLevelElement.
    def visitTopLevelElement(self, ctx:ElanParser.TopLevelElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#refinement.
    def visitRefinement(self, ctx:ElanParser.RefinementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#refinementName.
    def visitRefinementName(self, ctx:ElanParser.RefinementNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#procedureDeclaration.
    def visitProcedureDeclaration(self, ctx:ElanParser.ProcedureDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#procedureBody.
    def visitProcedureBody(self, ctx:ElanParser.ProcedureBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#resultExpression.
    def visitResultExpression(self, ctx:ElanParser.ResultExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#formalParameterList.
    def visitFormalParameterList(self, ctx:ElanParser.FormalParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#formalParameterGroup.
    def visitFormalParameterGroup(self, ctx:ElanParser.FormalParameterGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#parameterAccess.
    def visitParameterAccess(self, ctx:ElanParser.ParameterAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#resultType.
    def visitResultType(self, ctx:ElanParser.ResultTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#packetDeclaration.
    def visitPacketDeclaration(self, ctx:ElanParser.PacketDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#packetEnd.
    def visitPacketEnd(self, ctx:ElanParser.PacketEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:ElanParser.TypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#typeSpec.
    def visitTypeSpec(self, ctx:ElanParser.TypeSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#primitiveType.
    def visitPrimitiveType(self, ctx:ElanParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#structType.
    def visitStructType(self, ctx:ElanParser.StructTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#structField.
    def visitStructField(self, ctx:ElanParser.StructFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#rowType.
    def visitRowType(self, ctx:ElanParser.RowTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#rowBounds.
    def visitRowBounds(self, ctx:ElanParser.RowBoundsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#typeName.
    def visitTypeName(self, ctx:ElanParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#letDeclaration.
    def visitLetDeclaration(self, ctx:ElanParser.LetDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#objectDeclaration.
    def visitObjectDeclaration(self, ctx:ElanParser.ObjectDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#objectDeclarator.
    def visitObjectDeclarator(self, ctx:ElanParser.ObjectDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#objectAccess.
    def visitObjectAccess(self, ctx:ElanParser.ObjectAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#identifierInitList.
    def visitIdentifierInitList(self, ctx:ElanParser.IdentifierInitListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#identifierInitializer.
    def visitIdentifierInitializer(self, ctx:ElanParser.IdentifierInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#identifierList.
    def visitIdentifierList(self, ctx:ElanParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#declarationOrStatement.
    def visitDeclarationOrStatement(self, ctx:ElanParser.DeclarationOrStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#paragraph.
    def visitParagraph(self, ctx:ElanParser.ParagraphContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#statement.
    def visitStatement(self, ctx:ElanParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:ElanParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#builtinProcedureStatement.
    def visitBuiltinProcedureStatement(self, ctx:ElanParser.BuiltinProcedureStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#procedureCallStatement.
    def visitProcedureCallStatement(self, ctx:ElanParser.ProcedureCallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#ifStatement.
    def visitIfStatement(self, ctx:ElanParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#elifPart.
    def visitElifPart(self, ctx:ElanParser.ElifPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#elsePart.
    def visitElsePart(self, ctx:ElanParser.ElsePartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#ifEnd.
    def visitIfEnd(self, ctx:ElanParser.IfEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#whileStatement.
    def visitWhileStatement(self, ctx:ElanParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#repeatUntilStatement.
    def visitRepeatUntilStatement(self, ctx:ElanParser.RepeatUntilStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#loopStatement.
    def visitLoopStatement(self, ctx:ElanParser.LoopStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#forStatement.
    def visitForStatement(self, ctx:ElanParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#forDirection.
    def visitForDirection(self, ctx:ElanParser.ForDirectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#repeatKeyword.
    def visitRepeatKeyword(self, ctx:ElanParser.RepeatKeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#repeatEnd.
    def visitRepeatEnd(self, ctx:ElanParser.RepeatEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#leaveStatement.
    def visitLeaveStatement(self, ctx:ElanParser.LeaveStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#expression.
    def visitExpression(self, ctx:ElanParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#logicalOrExpression.
    def visitLogicalOrExpression(self, ctx:ElanParser.LogicalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#logicalXorExpression.
    def visitLogicalXorExpression(self, ctx:ElanParser.LogicalXorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#logicalAndExpression.
    def visitLogicalAndExpression(self, ctx:ElanParser.LogicalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#equalityExpression.
    def visitEqualityExpression(self, ctx:ElanParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#relationalExpression.
    def visitRelationalExpression(self, ctx:ElanParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:ElanParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:ElanParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#unaryExpression.
    def visitUnaryExpression(self, ctx:ElanParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#postfixExpression.
    def visitPostfixExpression(self, ctx:ElanParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#postfixPart.
    def visitPostfixPart(self, ctx:ElanParser.PostfixPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:ElanParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#ifExpression.
    def visitIfExpression(self, ctx:ElanParser.IfExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#actualParameterList.
    def visitActualParameterList(self, ctx:ElanParser.ActualParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#expressionList.
    def visitExpressionList(self, ctx:ElanParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#assignable.
    def visitAssignable(self, ctx:ElanParser.AssignableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#qualifiedName.
    def visitQualifiedName(self, ctx:ElanParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ElanParser#literal.
    def visitLiteral(self, ctx:ElanParser.LiteralContext):
        return self.visitChildren(ctx)



del ElanParser