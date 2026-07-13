# Generated from compiler/grammar/ElanParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ElanParser import ElanParser
else:
    from ElanParser import ElanParser

# This class defines a complete listener for a parse tree produced by ElanParser.
class ElanParserListener(ParseTreeListener):

    # Enter a parse tree produced by ElanParser#sourceFile.
    def enterSourceFile(self, ctx:ElanParser.SourceFileContext):
        pass

    # Exit a parse tree produced by ElanParser#sourceFile.
    def exitSourceFile(self, ctx:ElanParser.SourceFileContext):
        pass


    # Enter a parse tree produced by ElanParser#topLevelElement.
    def enterTopLevelElement(self, ctx:ElanParser.TopLevelElementContext):
        pass

    # Exit a parse tree produced by ElanParser#topLevelElement.
    def exitTopLevelElement(self, ctx:ElanParser.TopLevelElementContext):
        pass


    # Enter a parse tree produced by ElanParser#refinement.
    def enterRefinement(self, ctx:ElanParser.RefinementContext):
        pass

    # Exit a parse tree produced by ElanParser#refinement.
    def exitRefinement(self, ctx:ElanParser.RefinementContext):
        pass


    # Enter a parse tree produced by ElanParser#refinementName.
    def enterRefinementName(self, ctx:ElanParser.RefinementNameContext):
        pass

    # Exit a parse tree produced by ElanParser#refinementName.
    def exitRefinementName(self, ctx:ElanParser.RefinementNameContext):
        pass


    # Enter a parse tree produced by ElanParser#procedureDeclaration.
    def enterProcedureDeclaration(self, ctx:ElanParser.ProcedureDeclarationContext):
        pass

    # Exit a parse tree produced by ElanParser#procedureDeclaration.
    def exitProcedureDeclaration(self, ctx:ElanParser.ProcedureDeclarationContext):
        pass


    # Enter a parse tree produced by ElanParser#procedureBody.
    def enterProcedureBody(self, ctx:ElanParser.ProcedureBodyContext):
        pass

    # Exit a parse tree produced by ElanParser#procedureBody.
    def exitProcedureBody(self, ctx:ElanParser.ProcedureBodyContext):
        pass


    # Enter a parse tree produced by ElanParser#resultExpression.
    def enterResultExpression(self, ctx:ElanParser.ResultExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#resultExpression.
    def exitResultExpression(self, ctx:ElanParser.ResultExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#formalParameterList.
    def enterFormalParameterList(self, ctx:ElanParser.FormalParameterListContext):
        pass

    # Exit a parse tree produced by ElanParser#formalParameterList.
    def exitFormalParameterList(self, ctx:ElanParser.FormalParameterListContext):
        pass


    # Enter a parse tree produced by ElanParser#formalParameterGroup.
    def enterFormalParameterGroup(self, ctx:ElanParser.FormalParameterGroupContext):
        pass

    # Exit a parse tree produced by ElanParser#formalParameterGroup.
    def exitFormalParameterGroup(self, ctx:ElanParser.FormalParameterGroupContext):
        pass


    # Enter a parse tree produced by ElanParser#parameterAccess.
    def enterParameterAccess(self, ctx:ElanParser.ParameterAccessContext):
        pass

    # Exit a parse tree produced by ElanParser#parameterAccess.
    def exitParameterAccess(self, ctx:ElanParser.ParameterAccessContext):
        pass


    # Enter a parse tree produced by ElanParser#resultType.
    def enterResultType(self, ctx:ElanParser.ResultTypeContext):
        pass

    # Exit a parse tree produced by ElanParser#resultType.
    def exitResultType(self, ctx:ElanParser.ResultTypeContext):
        pass


    # Enter a parse tree produced by ElanParser#packetDeclaration.
    def enterPacketDeclaration(self, ctx:ElanParser.PacketDeclarationContext):
        pass

    # Exit a parse tree produced by ElanParser#packetDeclaration.
    def exitPacketDeclaration(self, ctx:ElanParser.PacketDeclarationContext):
        pass


    # Enter a parse tree produced by ElanParser#packetEnd.
    def enterPacketEnd(self, ctx:ElanParser.PacketEndContext):
        pass

    # Exit a parse tree produced by ElanParser#packetEnd.
    def exitPacketEnd(self, ctx:ElanParser.PacketEndContext):
        pass


    # Enter a parse tree produced by ElanParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:ElanParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by ElanParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:ElanParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by ElanParser#typeSpec.
    def enterTypeSpec(self, ctx:ElanParser.TypeSpecContext):
        pass

    # Exit a parse tree produced by ElanParser#typeSpec.
    def exitTypeSpec(self, ctx:ElanParser.TypeSpecContext):
        pass


    # Enter a parse tree produced by ElanParser#primitiveType.
    def enterPrimitiveType(self, ctx:ElanParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by ElanParser#primitiveType.
    def exitPrimitiveType(self, ctx:ElanParser.PrimitiveTypeContext):
        pass


    # Enter a parse tree produced by ElanParser#structType.
    def enterStructType(self, ctx:ElanParser.StructTypeContext):
        pass

    # Exit a parse tree produced by ElanParser#structType.
    def exitStructType(self, ctx:ElanParser.StructTypeContext):
        pass


    # Enter a parse tree produced by ElanParser#structField.
    def enterStructField(self, ctx:ElanParser.StructFieldContext):
        pass

    # Exit a parse tree produced by ElanParser#structField.
    def exitStructField(self, ctx:ElanParser.StructFieldContext):
        pass


    # Enter a parse tree produced by ElanParser#rowType.
    def enterRowType(self, ctx:ElanParser.RowTypeContext):
        pass

    # Exit a parse tree produced by ElanParser#rowType.
    def exitRowType(self, ctx:ElanParser.RowTypeContext):
        pass


    # Enter a parse tree produced by ElanParser#rowBounds.
    def enterRowBounds(self, ctx:ElanParser.RowBoundsContext):
        pass

    # Exit a parse tree produced by ElanParser#rowBounds.
    def exitRowBounds(self, ctx:ElanParser.RowBoundsContext):
        pass


    # Enter a parse tree produced by ElanParser#typeName.
    def enterTypeName(self, ctx:ElanParser.TypeNameContext):
        pass

    # Exit a parse tree produced by ElanParser#typeName.
    def exitTypeName(self, ctx:ElanParser.TypeNameContext):
        pass


    # Enter a parse tree produced by ElanParser#letDeclaration.
    def enterLetDeclaration(self, ctx:ElanParser.LetDeclarationContext):
        pass

    # Exit a parse tree produced by ElanParser#letDeclaration.
    def exitLetDeclaration(self, ctx:ElanParser.LetDeclarationContext):
        pass


    # Enter a parse tree produced by ElanParser#objectDeclaration.
    def enterObjectDeclaration(self, ctx:ElanParser.ObjectDeclarationContext):
        pass

    # Exit a parse tree produced by ElanParser#objectDeclaration.
    def exitObjectDeclaration(self, ctx:ElanParser.ObjectDeclarationContext):
        pass


    # Enter a parse tree produced by ElanParser#objectDeclarator.
    def enterObjectDeclarator(self, ctx:ElanParser.ObjectDeclaratorContext):
        pass

    # Exit a parse tree produced by ElanParser#objectDeclarator.
    def exitObjectDeclarator(self, ctx:ElanParser.ObjectDeclaratorContext):
        pass


    # Enter a parse tree produced by ElanParser#objectAccess.
    def enterObjectAccess(self, ctx:ElanParser.ObjectAccessContext):
        pass

    # Exit a parse tree produced by ElanParser#objectAccess.
    def exitObjectAccess(self, ctx:ElanParser.ObjectAccessContext):
        pass


    # Enter a parse tree produced by ElanParser#identifierInitList.
    def enterIdentifierInitList(self, ctx:ElanParser.IdentifierInitListContext):
        pass

    # Exit a parse tree produced by ElanParser#identifierInitList.
    def exitIdentifierInitList(self, ctx:ElanParser.IdentifierInitListContext):
        pass


    # Enter a parse tree produced by ElanParser#identifierInitializer.
    def enterIdentifierInitializer(self, ctx:ElanParser.IdentifierInitializerContext):
        pass

    # Exit a parse tree produced by ElanParser#identifierInitializer.
    def exitIdentifierInitializer(self, ctx:ElanParser.IdentifierInitializerContext):
        pass


    # Enter a parse tree produced by ElanParser#identifierList.
    def enterIdentifierList(self, ctx:ElanParser.IdentifierListContext):
        pass

    # Exit a parse tree produced by ElanParser#identifierList.
    def exitIdentifierList(self, ctx:ElanParser.IdentifierListContext):
        pass


    # Enter a parse tree produced by ElanParser#declarationOrStatement.
    def enterDeclarationOrStatement(self, ctx:ElanParser.DeclarationOrStatementContext):
        pass

    # Exit a parse tree produced by ElanParser#declarationOrStatement.
    def exitDeclarationOrStatement(self, ctx:ElanParser.DeclarationOrStatementContext):
        pass


    # Enter a parse tree produced by ElanParser#paragraph.
    def enterParagraph(self, ctx:ElanParser.ParagraphContext):
        pass

    # Exit a parse tree produced by ElanParser#paragraph.
    def exitParagraph(self, ctx:ElanParser.ParagraphContext):
        pass


    # Enter a parse tree produced by ElanParser#statement.
    def enterStatement(self, ctx:ElanParser.StatementContext):
        pass

    # Exit a parse tree produced by ElanParser#statement.
    def exitStatement(self, ctx:ElanParser.StatementContext):
        pass


    # Enter a parse tree produced by ElanParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:ElanParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by ElanParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:ElanParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by ElanParser#builtinProcedureStatement.
    def enterBuiltinProcedureStatement(self, ctx:ElanParser.BuiltinProcedureStatementContext):
        pass

    # Exit a parse tree produced by ElanParser#builtinProcedureStatement.
    def exitBuiltinProcedureStatement(self, ctx:ElanParser.BuiltinProcedureStatementContext):
        pass


    # Enter a parse tree produced by ElanParser#procedureCallStatement.
    def enterProcedureCallStatement(self, ctx:ElanParser.ProcedureCallStatementContext):
        pass

    # Exit a parse tree produced by ElanParser#procedureCallStatement.
    def exitProcedureCallStatement(self, ctx:ElanParser.ProcedureCallStatementContext):
        pass


    # Enter a parse tree produced by ElanParser#ifStatement.
    def enterIfStatement(self, ctx:ElanParser.IfStatementContext):
        pass

    # Exit a parse tree produced by ElanParser#ifStatement.
    def exitIfStatement(self, ctx:ElanParser.IfStatementContext):
        pass


    # Enter a parse tree produced by ElanParser#elifPart.
    def enterElifPart(self, ctx:ElanParser.ElifPartContext):
        pass

    # Exit a parse tree produced by ElanParser#elifPart.
    def exitElifPart(self, ctx:ElanParser.ElifPartContext):
        pass


    # Enter a parse tree produced by ElanParser#elsePart.
    def enterElsePart(self, ctx:ElanParser.ElsePartContext):
        pass

    # Exit a parse tree produced by ElanParser#elsePart.
    def exitElsePart(self, ctx:ElanParser.ElsePartContext):
        pass


    # Enter a parse tree produced by ElanParser#ifEnd.
    def enterIfEnd(self, ctx:ElanParser.IfEndContext):
        pass

    # Exit a parse tree produced by ElanParser#ifEnd.
    def exitIfEnd(self, ctx:ElanParser.IfEndContext):
        pass


    # Enter a parse tree produced by ElanParser#whileStatement.
    def enterWhileStatement(self, ctx:ElanParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by ElanParser#whileStatement.
    def exitWhileStatement(self, ctx:ElanParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by ElanParser#repeatUntilStatement.
    def enterRepeatUntilStatement(self, ctx:ElanParser.RepeatUntilStatementContext):
        pass

    # Exit a parse tree produced by ElanParser#repeatUntilStatement.
    def exitRepeatUntilStatement(self, ctx:ElanParser.RepeatUntilStatementContext):
        pass


    # Enter a parse tree produced by ElanParser#loopStatement.
    def enterLoopStatement(self, ctx:ElanParser.LoopStatementContext):
        pass

    # Exit a parse tree produced by ElanParser#loopStatement.
    def exitLoopStatement(self, ctx:ElanParser.LoopStatementContext):
        pass


    # Enter a parse tree produced by ElanParser#forStatement.
    def enterForStatement(self, ctx:ElanParser.ForStatementContext):
        pass

    # Exit a parse tree produced by ElanParser#forStatement.
    def exitForStatement(self, ctx:ElanParser.ForStatementContext):
        pass


    # Enter a parse tree produced by ElanParser#forDirection.
    def enterForDirection(self, ctx:ElanParser.ForDirectionContext):
        pass

    # Exit a parse tree produced by ElanParser#forDirection.
    def exitForDirection(self, ctx:ElanParser.ForDirectionContext):
        pass


    # Enter a parse tree produced by ElanParser#repeatKeyword.
    def enterRepeatKeyword(self, ctx:ElanParser.RepeatKeywordContext):
        pass

    # Exit a parse tree produced by ElanParser#repeatKeyword.
    def exitRepeatKeyword(self, ctx:ElanParser.RepeatKeywordContext):
        pass


    # Enter a parse tree produced by ElanParser#repeatEnd.
    def enterRepeatEnd(self, ctx:ElanParser.RepeatEndContext):
        pass

    # Exit a parse tree produced by ElanParser#repeatEnd.
    def exitRepeatEnd(self, ctx:ElanParser.RepeatEndContext):
        pass


    # Enter a parse tree produced by ElanParser#leaveStatement.
    def enterLeaveStatement(self, ctx:ElanParser.LeaveStatementContext):
        pass

    # Exit a parse tree produced by ElanParser#leaveStatement.
    def exitLeaveStatement(self, ctx:ElanParser.LeaveStatementContext):
        pass


    # Enter a parse tree produced by ElanParser#expression.
    def enterExpression(self, ctx:ElanParser.ExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#expression.
    def exitExpression(self, ctx:ElanParser.ExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#logicalOrExpression.
    def enterLogicalOrExpression(self, ctx:ElanParser.LogicalOrExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#logicalOrExpression.
    def exitLogicalOrExpression(self, ctx:ElanParser.LogicalOrExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#logicalXorExpression.
    def enterLogicalXorExpression(self, ctx:ElanParser.LogicalXorExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#logicalXorExpression.
    def exitLogicalXorExpression(self, ctx:ElanParser.LogicalXorExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#logicalAndExpression.
    def enterLogicalAndExpression(self, ctx:ElanParser.LogicalAndExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#logicalAndExpression.
    def exitLogicalAndExpression(self, ctx:ElanParser.LogicalAndExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#equalityExpression.
    def enterEqualityExpression(self, ctx:ElanParser.EqualityExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#equalityExpression.
    def exitEqualityExpression(self, ctx:ElanParser.EqualityExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#relationalExpression.
    def enterRelationalExpression(self, ctx:ElanParser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#relationalExpression.
    def exitRelationalExpression(self, ctx:ElanParser.RelationalExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:ElanParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:ElanParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:ElanParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:ElanParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#unaryExpression.
    def enterUnaryExpression(self, ctx:ElanParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#unaryExpression.
    def exitUnaryExpression(self, ctx:ElanParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#postfixExpression.
    def enterPostfixExpression(self, ctx:ElanParser.PostfixExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#postfixExpression.
    def exitPostfixExpression(self, ctx:ElanParser.PostfixExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#postfixPart.
    def enterPostfixPart(self, ctx:ElanParser.PostfixPartContext):
        pass

    # Exit a parse tree produced by ElanParser#postfixPart.
    def exitPostfixPart(self, ctx:ElanParser.PostfixPartContext):
        pass


    # Enter a parse tree produced by ElanParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:ElanParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:ElanParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#ifExpression.
    def enterIfExpression(self, ctx:ElanParser.IfExpressionContext):
        pass

    # Exit a parse tree produced by ElanParser#ifExpression.
    def exitIfExpression(self, ctx:ElanParser.IfExpressionContext):
        pass


    # Enter a parse tree produced by ElanParser#actualParameterList.
    def enterActualParameterList(self, ctx:ElanParser.ActualParameterListContext):
        pass

    # Exit a parse tree produced by ElanParser#actualParameterList.
    def exitActualParameterList(self, ctx:ElanParser.ActualParameterListContext):
        pass


    # Enter a parse tree produced by ElanParser#expressionList.
    def enterExpressionList(self, ctx:ElanParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by ElanParser#expressionList.
    def exitExpressionList(self, ctx:ElanParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by ElanParser#assignable.
    def enterAssignable(self, ctx:ElanParser.AssignableContext):
        pass

    # Exit a parse tree produced by ElanParser#assignable.
    def exitAssignable(self, ctx:ElanParser.AssignableContext):
        pass


    # Enter a parse tree produced by ElanParser#qualifiedName.
    def enterQualifiedName(self, ctx:ElanParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by ElanParser#qualifiedName.
    def exitQualifiedName(self, ctx:ElanParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by ElanParser#literal.
    def enterLiteral(self, ctx:ElanParser.LiteralContext):
        pass

    # Exit a parse tree produced by ElanParser#literal.
    def exitLiteral(self, ctx:ElanParser.LiteralContext):
        pass



del ElanParser