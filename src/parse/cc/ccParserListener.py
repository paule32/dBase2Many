# Generated from gramm/cc/ccParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ccParser import ccParser
else:
    from ccParser import ccParser

# This class defines a complete listener for a parse tree produced by ccParser.
class ccParserListener(ParseTreeListener):

    # Enter a parse tree produced by ccParser#translationUnit.
    def enterTranslationUnit(self, ctx:ccParser.TranslationUnitContext):
        pass

    # Exit a parse tree produced by ccParser#translationUnit.
    def exitTranslationUnit(self, ctx:ccParser.TranslationUnitContext):
        pass


    # Enter a parse tree produced by ccParser#topLevelDeclaration.
    def enterTopLevelDeclaration(self, ctx:ccParser.TopLevelDeclarationContext):
        pass

    # Exit a parse tree produced by ccParser#topLevelDeclaration.
    def exitTopLevelDeclaration(self, ctx:ccParser.TopLevelDeclarationContext):
        pass


    # Enter a parse tree produced by ccParser#preprocessorDirective.
    def enterPreprocessorDirective(self, ctx:ccParser.PreprocessorDirectiveContext):
        pass

    # Exit a parse tree produced by ccParser#preprocessorDirective.
    def exitPreprocessorDirective(self, ctx:ccParser.PreprocessorDirectiveContext):
        pass


    # Enter a parse tree produced by ccParser#templateDeclaration.
    def enterTemplateDeclaration(self, ctx:ccParser.TemplateDeclarationContext):
        pass

    # Exit a parse tree produced by ccParser#templateDeclaration.
    def exitTemplateDeclaration(self, ctx:ccParser.TemplateDeclarationContext):
        pass


    # Enter a parse tree produced by ccParser#templateParameterList.
    def enterTemplateParameterList(self, ctx:ccParser.TemplateParameterListContext):
        pass

    # Exit a parse tree produced by ccParser#templateParameterList.
    def exitTemplateParameterList(self, ctx:ccParser.TemplateParameterListContext):
        pass


    # Enter a parse tree produced by ccParser#templateParameter.
    def enterTemplateParameter(self, ctx:ccParser.TemplateParameterContext):
        pass

    # Exit a parse tree produced by ccParser#templateParameter.
    def exitTemplateParameter(self, ctx:ccParser.TemplateParameterContext):
        pass


    # Enter a parse tree produced by ccParser#namespaceDefinition.
    def enterNamespaceDefinition(self, ctx:ccParser.NamespaceDefinitionContext):
        pass

    # Exit a parse tree produced by ccParser#namespaceDefinition.
    def exitNamespaceDefinition(self, ctx:ccParser.NamespaceDefinitionContext):
        pass


    # Enter a parse tree produced by ccParser#linkageSpecification.
    def enterLinkageSpecification(self, ctx:ccParser.LinkageSpecificationContext):
        pass

    # Exit a parse tree produced by ccParser#linkageSpecification.
    def exitLinkageSpecification(self, ctx:ccParser.LinkageSpecificationContext):
        pass


    # Enter a parse tree produced by ccParser#classDefinition.
    def enterClassDefinition(self, ctx:ccParser.ClassDefinitionContext):
        pass

    # Exit a parse tree produced by ccParser#classDefinition.
    def exitClassDefinition(self, ctx:ccParser.ClassDefinitionContext):
        pass


    # Enter a parse tree produced by ccParser#classKey.
    def enterClassKey(self, ctx:ccParser.ClassKeyContext):
        pass

    # Exit a parse tree produced by ccParser#classKey.
    def exitClassKey(self, ctx:ccParser.ClassKeyContext):
        pass


    # Enter a parse tree produced by ccParser#baseClause.
    def enterBaseClause(self, ctx:ccParser.BaseClauseContext):
        pass

    # Exit a parse tree produced by ccParser#baseClause.
    def exitBaseClause(self, ctx:ccParser.BaseClauseContext):
        pass


    # Enter a parse tree produced by ccParser#baseSpecifier.
    def enterBaseSpecifier(self, ctx:ccParser.BaseSpecifierContext):
        pass

    # Exit a parse tree produced by ccParser#baseSpecifier.
    def exitBaseSpecifier(self, ctx:ccParser.BaseSpecifierContext):
        pass


    # Enter a parse tree produced by ccParser#classMemberDeclaration.
    def enterClassMemberDeclaration(self, ctx:ccParser.ClassMemberDeclarationContext):
        pass

    # Exit a parse tree produced by ccParser#classMemberDeclaration.
    def exitClassMemberDeclaration(self, ctx:ccParser.ClassMemberDeclarationContext):
        pass


    # Enter a parse tree produced by ccParser#accessSpecifier.
    def enterAccessSpecifier(self, ctx:ccParser.AccessSpecifierContext):
        pass

    # Exit a parse tree produced by ccParser#accessSpecifier.
    def exitAccessSpecifier(self, ctx:ccParser.AccessSpecifierContext):
        pass


    # Enter a parse tree produced by ccParser#enumDefinition.
    def enterEnumDefinition(self, ctx:ccParser.EnumDefinitionContext):
        pass

    # Exit a parse tree produced by ccParser#enumDefinition.
    def exitEnumDefinition(self, ctx:ccParser.EnumDefinitionContext):
        pass


    # Enter a parse tree produced by ccParser#enumeratorList.
    def enterEnumeratorList(self, ctx:ccParser.EnumeratorListContext):
        pass

    # Exit a parse tree produced by ccParser#enumeratorList.
    def exitEnumeratorList(self, ctx:ccParser.EnumeratorListContext):
        pass


    # Enter a parse tree produced by ccParser#enumerator.
    def enterEnumerator(self, ctx:ccParser.EnumeratorContext):
        pass

    # Exit a parse tree produced by ccParser#enumerator.
    def exitEnumerator(self, ctx:ccParser.EnumeratorContext):
        pass


    # Enter a parse tree produced by ccParser#usingDeclaration.
    def enterUsingDeclaration(self, ctx:ccParser.UsingDeclarationContext):
        pass

    # Exit a parse tree produced by ccParser#usingDeclaration.
    def exitUsingDeclaration(self, ctx:ccParser.UsingDeclarationContext):
        pass


    # Enter a parse tree produced by ccParser#typedefDeclaration.
    def enterTypedefDeclaration(self, ctx:ccParser.TypedefDeclarationContext):
        pass

    # Exit a parse tree produced by ccParser#typedefDeclaration.
    def exitTypedefDeclaration(self, ctx:ccParser.TypedefDeclarationContext):
        pass


    # Enter a parse tree produced by ccParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:ccParser.FunctionDefinitionContext):
        pass

    # Exit a parse tree produced by ccParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:ccParser.FunctionDefinitionContext):
        pass


    # Enter a parse tree produced by ccParser#functionDeclarator.
    def enterFunctionDeclarator(self, ctx:ccParser.FunctionDeclaratorContext):
        pass

    # Exit a parse tree produced by ccParser#functionDeclarator.
    def exitFunctionDeclarator(self, ctx:ccParser.FunctionDeclaratorContext):
        pass


    # Enter a parse tree produced by ccParser#functionBody.
    def enterFunctionBody(self, ctx:ccParser.FunctionBodyContext):
        pass

    # Exit a parse tree produced by ccParser#functionBody.
    def exitFunctionBody(self, ctx:ccParser.FunctionBodyContext):
        pass


    # Enter a parse tree produced by ccParser#declaration.
    def enterDeclaration(self, ctx:ccParser.DeclarationContext):
        pass

    # Exit a parse tree produced by ccParser#declaration.
    def exitDeclaration(self, ctx:ccParser.DeclarationContext):
        pass


    # Enter a parse tree produced by ccParser#initDeclaratorList.
    def enterInitDeclaratorList(self, ctx:ccParser.InitDeclaratorListContext):
        pass

    # Exit a parse tree produced by ccParser#initDeclaratorList.
    def exitInitDeclaratorList(self, ctx:ccParser.InitDeclaratorListContext):
        pass


    # Enter a parse tree produced by ccParser#initDeclarator.
    def enterInitDeclarator(self, ctx:ccParser.InitDeclaratorContext):
        pass

    # Exit a parse tree produced by ccParser#initDeclarator.
    def exitInitDeclarator(self, ctx:ccParser.InitDeclaratorContext):
        pass


    # Enter a parse tree produced by ccParser#declaratorList.
    def enterDeclaratorList(self, ctx:ccParser.DeclaratorListContext):
        pass

    # Exit a parse tree produced by ccParser#declaratorList.
    def exitDeclaratorList(self, ctx:ccParser.DeclaratorListContext):
        pass


    # Enter a parse tree produced by ccParser#declarator.
    def enterDeclarator(self, ctx:ccParser.DeclaratorContext):
        pass

    # Exit a parse tree produced by ccParser#declarator.
    def exitDeclarator(self, ctx:ccParser.DeclaratorContext):
        pass


    # Enter a parse tree produced by ccParser#arraySuffix.
    def enterArraySuffix(self, ctx:ccParser.ArraySuffixContext):
        pass

    # Exit a parse tree produced by ccParser#arraySuffix.
    def exitArraySuffix(self, ctx:ccParser.ArraySuffixContext):
        pass


    # Enter a parse tree produced by ccParser#ptrOperator.
    def enterPtrOperator(self, ctx:ccParser.PtrOperatorContext):
        pass

    # Exit a parse tree produced by ccParser#ptrOperator.
    def exitPtrOperator(self, ctx:ccParser.PtrOperatorContext):
        pass


    # Enter a parse tree produced by ccParser#refQualifier.
    def enterRefQualifier(self, ctx:ccParser.RefQualifierContext):
        pass

    # Exit a parse tree produced by ccParser#refQualifier.
    def exitRefQualifier(self, ctx:ccParser.RefQualifierContext):
        pass


    # Enter a parse tree produced by ccParser#noexceptSpecification.
    def enterNoexceptSpecification(self, ctx:ccParser.NoexceptSpecificationContext):
        pass

    # Exit a parse tree produced by ccParser#noexceptSpecification.
    def exitNoexceptSpecification(self, ctx:ccParser.NoexceptSpecificationContext):
        pass


    # Enter a parse tree produced by ccParser#trailingReturnType.
    def enterTrailingReturnType(self, ctx:ccParser.TrailingReturnTypeContext):
        pass

    # Exit a parse tree produced by ccParser#trailingReturnType.
    def exitTrailingReturnType(self, ctx:ccParser.TrailingReturnTypeContext):
        pass


    # Enter a parse tree produced by ccParser#parameterDeclarationList.
    def enterParameterDeclarationList(self, ctx:ccParser.ParameterDeclarationListContext):
        pass

    # Exit a parse tree produced by ccParser#parameterDeclarationList.
    def exitParameterDeclarationList(self, ctx:ccParser.ParameterDeclarationListContext):
        pass


    # Enter a parse tree produced by ccParser#parameterDeclaration.
    def enterParameterDeclaration(self, ctx:ccParser.ParameterDeclarationContext):
        pass

    # Exit a parse tree produced by ccParser#parameterDeclaration.
    def exitParameterDeclaration(self, ctx:ccParser.ParameterDeclarationContext):
        pass


    # Enter a parse tree produced by ccParser#declSpecifierSeq.
    def enterDeclSpecifierSeq(self, ctx:ccParser.DeclSpecifierSeqContext):
        pass

    # Exit a parse tree produced by ccParser#declSpecifierSeq.
    def exitDeclSpecifierSeq(self, ctx:ccParser.DeclSpecifierSeqContext):
        pass


    # Enter a parse tree produced by ccParser#declSpecifier.
    def enterDeclSpecifier(self, ctx:ccParser.DeclSpecifierContext):
        pass

    # Exit a parse tree produced by ccParser#declSpecifier.
    def exitDeclSpecifier(self, ctx:ccParser.DeclSpecifierContext):
        pass


    # Enter a parse tree produced by ccParser#storageClassSpecifier.
    def enterStorageClassSpecifier(self, ctx:ccParser.StorageClassSpecifierContext):
        pass

    # Exit a parse tree produced by ccParser#storageClassSpecifier.
    def exitStorageClassSpecifier(self, ctx:ccParser.StorageClassSpecifierContext):
        pass


    # Enter a parse tree produced by ccParser#functionSpecifier.
    def enterFunctionSpecifier(self, ctx:ccParser.FunctionSpecifierContext):
        pass

    # Exit a parse tree produced by ccParser#functionSpecifier.
    def exitFunctionSpecifier(self, ctx:ccParser.FunctionSpecifierContext):
        pass


    # Enter a parse tree produced by ccParser#cvQualifier.
    def enterCvQualifier(self, ctx:ccParser.CvQualifierContext):
        pass

    # Exit a parse tree produced by ccParser#cvQualifier.
    def exitCvQualifier(self, ctx:ccParser.CvQualifierContext):
        pass


    # Enter a parse tree produced by ccParser#simpleTypeSpecifier.
    def enterSimpleTypeSpecifier(self, ctx:ccParser.SimpleTypeSpecifierContext):
        pass

    # Exit a parse tree produced by ccParser#simpleTypeSpecifier.
    def exitSimpleTypeSpecifier(self, ctx:ccParser.SimpleTypeSpecifierContext):
        pass


    # Enter a parse tree produced by ccParser#typeReference.
    def enterTypeReference(self, ctx:ccParser.TypeReferenceContext):
        pass

    # Exit a parse tree produced by ccParser#typeReference.
    def exitTypeReference(self, ctx:ccParser.TypeReferenceContext):
        pass


    # Enter a parse tree produced by ccParser#qualifiedIdentifier.
    def enterQualifiedIdentifier(self, ctx:ccParser.QualifiedIdentifierContext):
        pass

    # Exit a parse tree produced by ccParser#qualifiedIdentifier.
    def exitQualifiedIdentifier(self, ctx:ccParser.QualifiedIdentifierContext):
        pass


    # Enter a parse tree produced by ccParser#unqualifiedIdentifier.
    def enterUnqualifiedIdentifier(self, ctx:ccParser.UnqualifiedIdentifierContext):
        pass

    # Exit a parse tree produced by ccParser#unqualifiedIdentifier.
    def exitUnqualifiedIdentifier(self, ctx:ccParser.UnqualifiedIdentifierContext):
        pass


    # Enter a parse tree produced by ccParser#operatorToken.
    def enterOperatorToken(self, ctx:ccParser.OperatorTokenContext):
        pass

    # Exit a parse tree produced by ccParser#operatorToken.
    def exitOperatorToken(self, ctx:ccParser.OperatorTokenContext):
        pass


    # Enter a parse tree produced by ccParser#initializer.
    def enterInitializer(self, ctx:ccParser.InitializerContext):
        pass

    # Exit a parse tree produced by ccParser#initializer.
    def exitInitializer(self, ctx:ccParser.InitializerContext):
        pass


    # Enter a parse tree produced by ccParser#braceInitializer.
    def enterBraceInitializer(self, ctx:ccParser.BraceInitializerContext):
        pass

    # Exit a parse tree produced by ccParser#braceInitializer.
    def exitBraceInitializer(self, ctx:ccParser.BraceInitializerContext):
        pass


    # Enter a parse tree produced by ccParser#compoundStatement.
    def enterCompoundStatement(self, ctx:ccParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by ccParser#compoundStatement.
    def exitCompoundStatement(self, ctx:ccParser.CompoundStatementContext):
        pass


    # Enter a parse tree produced by ccParser#statement.
    def enterStatement(self, ctx:ccParser.StatementContext):
        pass

    # Exit a parse tree produced by ccParser#statement.
    def exitStatement(self, ctx:ccParser.StatementContext):
        pass


    # Enter a parse tree produced by ccParser#declarationStatement.
    def enterDeclarationStatement(self, ctx:ccParser.DeclarationStatementContext):
        pass

    # Exit a parse tree produced by ccParser#declarationStatement.
    def exitDeclarationStatement(self, ctx:ccParser.DeclarationStatementContext):
        pass


    # Enter a parse tree produced by ccParser#ifStatement.
    def enterIfStatement(self, ctx:ccParser.IfStatementContext):
        pass

    # Exit a parse tree produced by ccParser#ifStatement.
    def exitIfStatement(self, ctx:ccParser.IfStatementContext):
        pass


    # Enter a parse tree produced by ccParser#switchStatement.
    def enterSwitchStatement(self, ctx:ccParser.SwitchStatementContext):
        pass

    # Exit a parse tree produced by ccParser#switchStatement.
    def exitSwitchStatement(self, ctx:ccParser.SwitchStatementContext):
        pass


    # Enter a parse tree produced by ccParser#whileStatement.
    def enterWhileStatement(self, ctx:ccParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by ccParser#whileStatement.
    def exitWhileStatement(self, ctx:ccParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by ccParser#doWhileStatement.
    def enterDoWhileStatement(self, ctx:ccParser.DoWhileStatementContext):
        pass

    # Exit a parse tree produced by ccParser#doWhileStatement.
    def exitDoWhileStatement(self, ctx:ccParser.DoWhileStatementContext):
        pass


    # Enter a parse tree produced by ccParser#forStatement.
    def enterForStatement(self, ctx:ccParser.ForStatementContext):
        pass

    # Exit a parse tree produced by ccParser#forStatement.
    def exitForStatement(self, ctx:ccParser.ForStatementContext):
        pass


    # Enter a parse tree produced by ccParser#forInitStatement.
    def enterForInitStatement(self, ctx:ccParser.ForInitStatementContext):
        pass

    # Exit a parse tree produced by ccParser#forInitStatement.
    def exitForInitStatement(self, ctx:ccParser.ForInitStatementContext):
        pass


    # Enter a parse tree produced by ccParser#returnStatement.
    def enterReturnStatement(self, ctx:ccParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by ccParser#returnStatement.
    def exitReturnStatement(self, ctx:ccParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by ccParser#breakStatement.
    def enterBreakStatement(self, ctx:ccParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by ccParser#breakStatement.
    def exitBreakStatement(self, ctx:ccParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by ccParser#continueStatement.
    def enterContinueStatement(self, ctx:ccParser.ContinueStatementContext):
        pass

    # Exit a parse tree produced by ccParser#continueStatement.
    def exitContinueStatement(self, ctx:ccParser.ContinueStatementContext):
        pass


    # Enter a parse tree produced by ccParser#tryStatement.
    def enterTryStatement(self, ctx:ccParser.TryStatementContext):
        pass

    # Exit a parse tree produced by ccParser#tryStatement.
    def exitTryStatement(self, ctx:ccParser.TryStatementContext):
        pass


    # Enter a parse tree produced by ccParser#handler.
    def enterHandler(self, ctx:ccParser.HandlerContext):
        pass

    # Exit a parse tree produced by ccParser#handler.
    def exitHandler(self, ctx:ccParser.HandlerContext):
        pass


    # Enter a parse tree produced by ccParser#exceptionDeclaration.
    def enterExceptionDeclaration(self, ctx:ccParser.ExceptionDeclarationContext):
        pass

    # Exit a parse tree produced by ccParser#exceptionDeclaration.
    def exitExceptionDeclaration(self, ctx:ccParser.ExceptionDeclarationContext):
        pass


    # Enter a parse tree produced by ccParser#labeledStatement.
    def enterLabeledStatement(self, ctx:ccParser.LabeledStatementContext):
        pass

    # Exit a parse tree produced by ccParser#labeledStatement.
    def exitLabeledStatement(self, ctx:ccParser.LabeledStatementContext):
        pass


    # Enter a parse tree produced by ccParser#expressionStatement.
    def enterExpressionStatement(self, ctx:ccParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by ccParser#expressionStatement.
    def exitExpressionStatement(self, ctx:ccParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by ccParser#constantExpression.
    def enterConstantExpression(self, ctx:ccParser.ConstantExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#constantExpression.
    def exitConstantExpression(self, ctx:ccParser.ConstantExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#expression.
    def enterExpression(self, ctx:ccParser.ExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#expression.
    def exitExpression(self, ctx:ccParser.ExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:ccParser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:ccParser.AssignmentExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#assignmentOperator.
    def enterAssignmentOperator(self, ctx:ccParser.AssignmentOperatorContext):
        pass

    # Exit a parse tree produced by ccParser#assignmentOperator.
    def exitAssignmentOperator(self, ctx:ccParser.AssignmentOperatorContext):
        pass


    # Enter a parse tree produced by ccParser#conditionalExpression.
    def enterConditionalExpression(self, ctx:ccParser.ConditionalExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#conditionalExpression.
    def exitConditionalExpression(self, ctx:ccParser.ConditionalExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#logicalOrExpression.
    def enterLogicalOrExpression(self, ctx:ccParser.LogicalOrExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#logicalOrExpression.
    def exitLogicalOrExpression(self, ctx:ccParser.LogicalOrExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#logicalAndExpression.
    def enterLogicalAndExpression(self, ctx:ccParser.LogicalAndExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#logicalAndExpression.
    def exitLogicalAndExpression(self, ctx:ccParser.LogicalAndExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#inclusiveOrExpression.
    def enterInclusiveOrExpression(self, ctx:ccParser.InclusiveOrExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#inclusiveOrExpression.
    def exitInclusiveOrExpression(self, ctx:ccParser.InclusiveOrExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#exclusiveOrExpression.
    def enterExclusiveOrExpression(self, ctx:ccParser.ExclusiveOrExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#exclusiveOrExpression.
    def exitExclusiveOrExpression(self, ctx:ccParser.ExclusiveOrExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#andExpression.
    def enterAndExpression(self, ctx:ccParser.AndExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#andExpression.
    def exitAndExpression(self, ctx:ccParser.AndExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#equalityExpression.
    def enterEqualityExpression(self, ctx:ccParser.EqualityExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#equalityExpression.
    def exitEqualityExpression(self, ctx:ccParser.EqualityExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#relationalExpression.
    def enterRelationalExpression(self, ctx:ccParser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#relationalExpression.
    def exitRelationalExpression(self, ctx:ccParser.RelationalExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#shiftExpression.
    def enterShiftExpression(self, ctx:ccParser.ShiftExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#shiftExpression.
    def exitShiftExpression(self, ctx:ccParser.ShiftExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:ccParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:ccParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:ccParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:ccParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#unaryExpression.
    def enterUnaryExpression(self, ctx:ccParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#unaryExpression.
    def exitUnaryExpression(self, ctx:ccParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#unaryOperator.
    def enterUnaryOperator(self, ctx:ccParser.UnaryOperatorContext):
        pass

    # Exit a parse tree produced by ccParser#unaryOperator.
    def exitUnaryOperator(self, ctx:ccParser.UnaryOperatorContext):
        pass


    # Enter a parse tree produced by ccParser#postfixExpression.
    def enterPostfixExpression(self, ctx:ccParser.PostfixExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#postfixExpression.
    def exitPostfixExpression(self, ctx:ccParser.PostfixExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#postfixSuffix.
    def enterPostfixSuffix(self, ctx:ccParser.PostfixSuffixContext):
        pass

    # Exit a parse tree produced by ccParser#postfixSuffix.
    def exitPostfixSuffix(self, ctx:ccParser.PostfixSuffixContext):
        pass


    # Enter a parse tree produced by ccParser#argumentExpressionList.
    def enterArgumentExpressionList(self, ctx:ccParser.ArgumentExpressionListContext):
        pass

    # Exit a parse tree produced by ccParser#argumentExpressionList.
    def exitArgumentExpressionList(self, ctx:ccParser.ArgumentExpressionListContext):
        pass


    # Enter a parse tree produced by ccParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:ccParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by ccParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:ccParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by ccParser#literal.
    def enterLiteral(self, ctx:ccParser.LiteralContext):
        pass

    # Exit a parse tree produced by ccParser#literal.
    def exitLiteral(self, ctx:ccParser.LiteralContext):
        pass



del ccParser