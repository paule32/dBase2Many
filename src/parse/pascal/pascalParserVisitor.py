# Generated from pascalParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .pascalParser import pascalParser
else:
    from pascalParser import pascalParser

# This class defines a complete generic visitor for a parse tree produced by pascalParser.

class pascalParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by pascalParser#program.
    def visitProgram(self, ctx:pascalParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#module.
    def visitModule(self, ctx:pascalParser.ModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#programModule.
    def visitProgramModule(self, ctx:pascalParser.ProgramModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#libraryModule.
    def visitLibraryModule(self, ctx:pascalParser.LibraryModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#packageModule.
    def visitPackageModule(self, ctx:pascalParser.PackageModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#packageRequiresClause.
    def visitPackageRequiresClause(self, ctx:pascalParser.PackageRequiresClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#packageContainsClause.
    def visitPackageContainsClause(self, ctx:pascalParser.PackageContainsClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#unitModule.
    def visitUnitModule(self, ctx:pascalParser.UnitModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#interfaceSection.
    def visitInterfaceSection(self, ctx:pascalParser.InterfaceSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#implementationSection.
    def visitImplementationSection(self, ctx:pascalParser.ImplementationSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#initializationSection.
    def visitInitializationSection(self, ctx:pascalParser.InitializationSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#finalizationSection.
    def visitFinalizationSection(self, ctx:pascalParser.FinalizationSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#usesClause.
    def visitUsesClause(self, ctx:pascalParser.UsesClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#block.
    def visitBlock(self, ctx:pascalParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#declarationPart.
    def visitDeclarationPart(self, ctx:pascalParser.DeclarationPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#declaration.
    def visitDeclaration(self, ctx:pascalParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#labelSection.
    def visitLabelSection(self, ctx:pascalParser.LabelSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#labelIdentifierList.
    def visitLabelIdentifierList(self, ctx:pascalParser.LabelIdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#labelIdentifier.
    def visitLabelIdentifier(self, ctx:pascalParser.LabelIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#constSection.
    def visitConstSection(self, ctx:pascalParser.ConstSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#constDeclaration.
    def visitConstDeclaration(self, ctx:pascalParser.ConstDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#resourceStringSection.
    def visitResourceStringSection(self, ctx:pascalParser.ResourceStringSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#typeSection.
    def visitTypeSection(self, ctx:pascalParser.TypeSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:pascalParser.TypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#varSection.
    def visitVarSection(self, ctx:pascalParser.VarSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:pascalParser.VariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#routineDeclaration.
    def visitRoutineDeclaration(self, ctx:pascalParser.RoutineDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#routineImplementation.
    def visitRoutineImplementation(self, ctx:pascalParser.RoutineImplementationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#routineHeading.
    def visitRoutineHeading(self, ctx:pascalParser.RoutineHeadingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#procedureHeading.
    def visitProcedureHeading(self, ctx:pascalParser.ProcedureHeadingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#functionHeading.
    def visitFunctionHeading(self, ctx:pascalParser.FunctionHeadingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#constructorHeading.
    def visitConstructorHeading(self, ctx:pascalParser.ConstructorHeadingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#destructorHeading.
    def visitDestructorHeading(self, ctx:pascalParser.DestructorHeadingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#formalParameters.
    def visitFormalParameters(self, ctx:pascalParser.FormalParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#formalParameterSection.
    def visitFormalParameterSection(self, ctx:pascalParser.FormalParameterSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#parameterModifier.
    def visitParameterModifier(self, ctx:pascalParser.ParameterModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#routineDirectiveList.
    def visitRoutineDirectiveList(self, ctx:pascalParser.RoutineDirectiveListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#routineDirective.
    def visitRoutineDirective(self, ctx:pascalParser.RoutineDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#typeSpec.
    def visitTypeSpec(self, ctx:pascalParser.TypeSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#simpleType.
    def visitSimpleType(self, ctx:pascalParser.SimpleTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#subrangeType.
    def visitSubrangeType(self, ctx:pascalParser.SubrangeTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#enumeratedType.
    def visitEnumeratedType(self, ctx:pascalParser.EnumeratedTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#arrayType.
    def visitArrayType(self, ctx:pascalParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#typeList.
    def visitTypeList(self, ctx:pascalParser.TypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#setType.
    def visitSetType(self, ctx:pascalParser.SetTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#fileType.
    def visitFileType(self, ctx:pascalParser.FileTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#pointerType.
    def visitPointerType(self, ctx:pascalParser.PointerTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#procedureType.
    def visitProcedureType(self, ctx:pascalParser.ProcedureTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#classType.
    def visitClassType(self, ctx:pascalParser.ClassTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#classHeritage.
    def visitClassHeritage(self, ctx:pascalParser.ClassHeritageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#typeRefList.
    def visitTypeRefList(self, ctx:pascalParser.TypeRefListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#classBody.
    def visitClassBody(self, ctx:pascalParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#classMember.
    def visitClassMember(self, ctx:pascalParser.ClassMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#visibilitySection.
    def visitVisibilitySection(self, ctx:pascalParser.VisibilitySectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#classField.
    def visitClassField(self, ctx:pascalParser.ClassFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#classMethod.
    def visitClassMethod(self, ctx:pascalParser.ClassMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#propertyDeclaration.
    def visitPropertyDeclaration(self, ctx:pascalParser.PropertyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#propertySpec.
    def visitPropertySpec(self, ctx:pascalParser.PropertySpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#recordType.
    def visitRecordType(self, ctx:pascalParser.RecordTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#recordField.
    def visitRecordField(self, ctx:pascalParser.RecordFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#typeRef.
    def visitTypeRef(self, ctx:pascalParser.TypeRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#statementBlock.
    def visitStatementBlock(self, ctx:pascalParser.StatementBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#statementList.
    def visitStatementList(self, ctx:pascalParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#statement.
    def visitStatement(self, ctx:pascalParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#compoundStatement.
    def visitCompoundStatement(self, ctx:pascalParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:pascalParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#procedureCallStatement.
    def visitProcedureCallStatement(self, ctx:pascalParser.ProcedureCallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#ifStatement.
    def visitIfStatement(self, ctx:pascalParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#caseStatement.
    def visitCaseStatement(self, ctx:pascalParser.CaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#caseBranch.
    def visitCaseBranch(self, ctx:pascalParser.CaseBranchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#caseLabelList.
    def visitCaseLabelList(self, ctx:pascalParser.CaseLabelListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#whileStatement.
    def visitWhileStatement(self, ctx:pascalParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#repeatStatement.
    def visitRepeatStatement(self, ctx:pascalParser.RepeatStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#forStatement.
    def visitForStatement(self, ctx:pascalParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#withStatement.
    def visitWithStatement(self, ctx:pascalParser.WithStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#variableList.
    def visitVariableList(self, ctx:pascalParser.VariableListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#tryStatement.
    def visitTryStatement(self, ctx:pascalParser.TryStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#exceptionHandlerList.
    def visitExceptionHandlerList(self, ctx:pascalParser.ExceptionHandlerListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#exceptionHandler.
    def visitExceptionHandler(self, ctx:pascalParser.ExceptionHandlerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#raiseStatement.
    def visitRaiseStatement(self, ctx:pascalParser.RaiseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#gotoStatement.
    def visitGotoStatement(self, ctx:pascalParser.GotoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#breakStatement.
    def visitBreakStatement(self, ctx:pascalParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#continueStatement.
    def visitContinueStatement(self, ctx:pascalParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#exitStatement.
    def visitExitStatement(self, ctx:pascalParser.ExitStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#emptyStatement.
    def visitEmptyStatement(self, ctx:pascalParser.EmptyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#actualParameterList.
    def visitActualParameterList(self, ctx:pascalParser.ActualParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#expressionList.
    def visitExpressionList(self, ctx:pascalParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#expression.
    def visitExpression(self, ctx:pascalParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#relationalExpression.
    def visitRelationalExpression(self, ctx:pascalParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:pascalParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:pascalParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#unaryExpression.
    def visitUnaryExpression(self, ctx:pascalParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:pascalParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#setConstructor.
    def visitSetConstructor(self, ctx:pascalParser.SetConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#variable.
    def visitVariable(self, ctx:pascalParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#designator.
    def visitDesignator(self, ctx:pascalParser.DesignatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#designatorSuffix.
    def visitDesignatorSuffix(self, ctx:pascalParser.DesignatorSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#constantExpression.
    def visitConstantExpression(self, ctx:pascalParser.ConstantExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#literal.
    def visitLiteral(self, ctx:pascalParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#identifierList.
    def visitIdentifierList(self, ctx:pascalParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#qualifiedIdentifier.
    def visitQualifiedIdentifier(self, ctx:pascalParser.QualifiedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pascalParser#identifier.
    def visitIdentifier(self, ctx:pascalParser.IdentifierContext):
        return self.visitChildren(ctx)



del pascalParser