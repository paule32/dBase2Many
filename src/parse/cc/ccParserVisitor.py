# Generated from gramm/cc/ccParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ccParser import ccParser
else:
    from ccParser import ccParser

# This class defines a complete generic visitor for a parse tree produced by ccParser.

class ccParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ccParser#translationUnit.
    def visitTranslationUnit(self, ctx:ccParser.TranslationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#topLevelDeclaration.
    def visitTopLevelDeclaration(self, ctx:ccParser.TopLevelDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#preprocessorDirective.
    def visitPreprocessorDirective(self, ctx:ccParser.PreprocessorDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#templateDeclaration.
    def visitTemplateDeclaration(self, ctx:ccParser.TemplateDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#templateParameterList.
    def visitTemplateParameterList(self, ctx:ccParser.TemplateParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#templateParameter.
    def visitTemplateParameter(self, ctx:ccParser.TemplateParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#namespaceDefinition.
    def visitNamespaceDefinition(self, ctx:ccParser.NamespaceDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#linkageSpecification.
    def visitLinkageSpecification(self, ctx:ccParser.LinkageSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#classDefinition.
    def visitClassDefinition(self, ctx:ccParser.ClassDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#classKey.
    def visitClassKey(self, ctx:ccParser.ClassKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#baseClause.
    def visitBaseClause(self, ctx:ccParser.BaseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#baseSpecifier.
    def visitBaseSpecifier(self, ctx:ccParser.BaseSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#classMemberDeclaration.
    def visitClassMemberDeclaration(self, ctx:ccParser.ClassMemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#accessSpecifier.
    def visitAccessSpecifier(self, ctx:ccParser.AccessSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#enumDefinition.
    def visitEnumDefinition(self, ctx:ccParser.EnumDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#enumeratorList.
    def visitEnumeratorList(self, ctx:ccParser.EnumeratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#enumerator.
    def visitEnumerator(self, ctx:ccParser.EnumeratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#usingDeclaration.
    def visitUsingDeclaration(self, ctx:ccParser.UsingDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#typedefDeclaration.
    def visitTypedefDeclaration(self, ctx:ccParser.TypedefDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:ccParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#functionDeclarator.
    def visitFunctionDeclarator(self, ctx:ccParser.FunctionDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#functionBody.
    def visitFunctionBody(self, ctx:ccParser.FunctionBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#declaration.
    def visitDeclaration(self, ctx:ccParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#initDeclaratorList.
    def visitInitDeclaratorList(self, ctx:ccParser.InitDeclaratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#initDeclarator.
    def visitInitDeclarator(self, ctx:ccParser.InitDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#declaratorList.
    def visitDeclaratorList(self, ctx:ccParser.DeclaratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#declarator.
    def visitDeclarator(self, ctx:ccParser.DeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#arraySuffix.
    def visitArraySuffix(self, ctx:ccParser.ArraySuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#ptrOperator.
    def visitPtrOperator(self, ctx:ccParser.PtrOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#refQualifier.
    def visitRefQualifier(self, ctx:ccParser.RefQualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#noexceptSpecification.
    def visitNoexceptSpecification(self, ctx:ccParser.NoexceptSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#trailingReturnType.
    def visitTrailingReturnType(self, ctx:ccParser.TrailingReturnTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#parameterDeclarationList.
    def visitParameterDeclarationList(self, ctx:ccParser.ParameterDeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx:ccParser.ParameterDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#declSpecifierSeq.
    def visitDeclSpecifierSeq(self, ctx:ccParser.DeclSpecifierSeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#declSpecifier.
    def visitDeclSpecifier(self, ctx:ccParser.DeclSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#storageClassSpecifier.
    def visitStorageClassSpecifier(self, ctx:ccParser.StorageClassSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#functionSpecifier.
    def visitFunctionSpecifier(self, ctx:ccParser.FunctionSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#cvQualifier.
    def visitCvQualifier(self, ctx:ccParser.CvQualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#simpleTypeSpecifier.
    def visitSimpleTypeSpecifier(self, ctx:ccParser.SimpleTypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#typeReference.
    def visitTypeReference(self, ctx:ccParser.TypeReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#qualifiedIdentifier.
    def visitQualifiedIdentifier(self, ctx:ccParser.QualifiedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#unqualifiedIdentifier.
    def visitUnqualifiedIdentifier(self, ctx:ccParser.UnqualifiedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#operatorToken.
    def visitOperatorToken(self, ctx:ccParser.OperatorTokenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#initializer.
    def visitInitializer(self, ctx:ccParser.InitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#braceInitializer.
    def visitBraceInitializer(self, ctx:ccParser.BraceInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#compoundStatement.
    def visitCompoundStatement(self, ctx:ccParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#statement.
    def visitStatement(self, ctx:ccParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#declarationStatement.
    def visitDeclarationStatement(self, ctx:ccParser.DeclarationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#ifStatement.
    def visitIfStatement(self, ctx:ccParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#switchStatement.
    def visitSwitchStatement(self, ctx:ccParser.SwitchStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#whileStatement.
    def visitWhileStatement(self, ctx:ccParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:ccParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#forStatement.
    def visitForStatement(self, ctx:ccParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#forInitStatement.
    def visitForInitStatement(self, ctx:ccParser.ForInitStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#returnStatement.
    def visitReturnStatement(self, ctx:ccParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#breakStatement.
    def visitBreakStatement(self, ctx:ccParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#continueStatement.
    def visitContinueStatement(self, ctx:ccParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#tryStatement.
    def visitTryStatement(self, ctx:ccParser.TryStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#handler.
    def visitHandler(self, ctx:ccParser.HandlerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#exceptionDeclaration.
    def visitExceptionDeclaration(self, ctx:ccParser.ExceptionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#labeledStatement.
    def visitLabeledStatement(self, ctx:ccParser.LabeledStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#expressionStatement.
    def visitExpressionStatement(self, ctx:ccParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#constantExpression.
    def visitConstantExpression(self, ctx:ccParser.ConstantExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#expression.
    def visitExpression(self, ctx:ccParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:ccParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:ccParser.AssignmentOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#conditionalExpression.
    def visitConditionalExpression(self, ctx:ccParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#logicalOrExpression.
    def visitLogicalOrExpression(self, ctx:ccParser.LogicalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#logicalAndExpression.
    def visitLogicalAndExpression(self, ctx:ccParser.LogicalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#inclusiveOrExpression.
    def visitInclusiveOrExpression(self, ctx:ccParser.InclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#exclusiveOrExpression.
    def visitExclusiveOrExpression(self, ctx:ccParser.ExclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#andExpression.
    def visitAndExpression(self, ctx:ccParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#equalityExpression.
    def visitEqualityExpression(self, ctx:ccParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#relationalExpression.
    def visitRelationalExpression(self, ctx:ccParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#shiftExpression.
    def visitShiftExpression(self, ctx:ccParser.ShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:ccParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:ccParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#unaryExpression.
    def visitUnaryExpression(self, ctx:ccParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#unaryOperator.
    def visitUnaryOperator(self, ctx:ccParser.UnaryOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#postfixExpression.
    def visitPostfixExpression(self, ctx:ccParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#postfixSuffix.
    def visitPostfixSuffix(self, ctx:ccParser.PostfixSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#argumentExpressionList.
    def visitArgumentExpressionList(self, ctx:ccParser.ArgumentExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:ccParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ccParser#literal.
    def visitLiteral(self, ctx:ccParser.LiteralContext):
        return self.visitChildren(ctx)



del ccParser