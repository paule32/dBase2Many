# Generated from gramm/pascal/pascalParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .pascalParser import pascalParser
else:
    from pascalParser import pascalParser

# This class defines a complete listener for a parse tree produced by pascalParser.
class pascalParserListener(ParseTreeListener):

    # Enter a parse tree produced by pascalParser#program.
    def enterProgram(self, ctx:pascalParser.ProgramContext):
        pass

    # Exit a parse tree produced by pascalParser#program.
    def exitProgram(self, ctx:pascalParser.ProgramContext):
        pass


    # Enter a parse tree produced by pascalParser#module.
    def enterModule(self, ctx:pascalParser.ModuleContext):
        pass

    # Exit a parse tree produced by pascalParser#module.
    def exitModule(self, ctx:pascalParser.ModuleContext):
        pass


    # Enter a parse tree produced by pascalParser#programModule.
    def enterProgramModule(self, ctx:pascalParser.ProgramModuleContext):
        pass

    # Exit a parse tree produced by pascalParser#programModule.
    def exitProgramModule(self, ctx:pascalParser.ProgramModuleContext):
        pass


    # Enter a parse tree produced by pascalParser#libraryModule.
    def enterLibraryModule(self, ctx:pascalParser.LibraryModuleContext):
        pass

    # Exit a parse tree produced by pascalParser#libraryModule.
    def exitLibraryModule(self, ctx:pascalParser.LibraryModuleContext):
        pass


    # Enter a parse tree produced by pascalParser#packageModule.
    def enterPackageModule(self, ctx:pascalParser.PackageModuleContext):
        pass

    # Exit a parse tree produced by pascalParser#packageModule.
    def exitPackageModule(self, ctx:pascalParser.PackageModuleContext):
        pass


    # Enter a parse tree produced by pascalParser#packageRequiresClause.
    def enterPackageRequiresClause(self, ctx:pascalParser.PackageRequiresClauseContext):
        pass

    # Exit a parse tree produced by pascalParser#packageRequiresClause.
    def exitPackageRequiresClause(self, ctx:pascalParser.PackageRequiresClauseContext):
        pass


    # Enter a parse tree produced by pascalParser#packageContainsClause.
    def enterPackageContainsClause(self, ctx:pascalParser.PackageContainsClauseContext):
        pass

    # Exit a parse tree produced by pascalParser#packageContainsClause.
    def exitPackageContainsClause(self, ctx:pascalParser.PackageContainsClauseContext):
        pass


    # Enter a parse tree produced by pascalParser#unitModule.
    def enterUnitModule(self, ctx:pascalParser.UnitModuleContext):
        pass

    # Exit a parse tree produced by pascalParser#unitModule.
    def exitUnitModule(self, ctx:pascalParser.UnitModuleContext):
        pass


    # Enter a parse tree produced by pascalParser#interfaceSection.
    def enterInterfaceSection(self, ctx:pascalParser.InterfaceSectionContext):
        pass

    # Exit a parse tree produced by pascalParser#interfaceSection.
    def exitInterfaceSection(self, ctx:pascalParser.InterfaceSectionContext):
        pass


    # Enter a parse tree produced by pascalParser#implementationSection.
    def enterImplementationSection(self, ctx:pascalParser.ImplementationSectionContext):
        pass

    # Exit a parse tree produced by pascalParser#implementationSection.
    def exitImplementationSection(self, ctx:pascalParser.ImplementationSectionContext):
        pass


    # Enter a parse tree produced by pascalParser#initializationSection.
    def enterInitializationSection(self, ctx:pascalParser.InitializationSectionContext):
        pass

    # Exit a parse tree produced by pascalParser#initializationSection.
    def exitInitializationSection(self, ctx:pascalParser.InitializationSectionContext):
        pass


    # Enter a parse tree produced by pascalParser#finalizationSection.
    def enterFinalizationSection(self, ctx:pascalParser.FinalizationSectionContext):
        pass

    # Exit a parse tree produced by pascalParser#finalizationSection.
    def exitFinalizationSection(self, ctx:pascalParser.FinalizationSectionContext):
        pass


    # Enter a parse tree produced by pascalParser#usesClause.
    def enterUsesClause(self, ctx:pascalParser.UsesClauseContext):
        pass

    # Exit a parse tree produced by pascalParser#usesClause.
    def exitUsesClause(self, ctx:pascalParser.UsesClauseContext):
        pass


    # Enter a parse tree produced by pascalParser#block.
    def enterBlock(self, ctx:pascalParser.BlockContext):
        pass

    # Exit a parse tree produced by pascalParser#block.
    def exitBlock(self, ctx:pascalParser.BlockContext):
        pass


    # Enter a parse tree produced by pascalParser#declarationPart.
    def enterDeclarationPart(self, ctx:pascalParser.DeclarationPartContext):
        pass

    # Exit a parse tree produced by pascalParser#declarationPart.
    def exitDeclarationPart(self, ctx:pascalParser.DeclarationPartContext):
        pass


    # Enter a parse tree produced by pascalParser#declaration.
    def enterDeclaration(self, ctx:pascalParser.DeclarationContext):
        pass

    # Exit a parse tree produced by pascalParser#declaration.
    def exitDeclaration(self, ctx:pascalParser.DeclarationContext):
        pass


    # Enter a parse tree produced by pascalParser#labelSection.
    def enterLabelSection(self, ctx:pascalParser.LabelSectionContext):
        pass

    # Exit a parse tree produced by pascalParser#labelSection.
    def exitLabelSection(self, ctx:pascalParser.LabelSectionContext):
        pass


    # Enter a parse tree produced by pascalParser#labelIdentifierList.
    def enterLabelIdentifierList(self, ctx:pascalParser.LabelIdentifierListContext):
        pass

    # Exit a parse tree produced by pascalParser#labelIdentifierList.
    def exitLabelIdentifierList(self, ctx:pascalParser.LabelIdentifierListContext):
        pass


    # Enter a parse tree produced by pascalParser#labelIdentifier.
    def enterLabelIdentifier(self, ctx:pascalParser.LabelIdentifierContext):
        pass

    # Exit a parse tree produced by pascalParser#labelIdentifier.
    def exitLabelIdentifier(self, ctx:pascalParser.LabelIdentifierContext):
        pass


    # Enter a parse tree produced by pascalParser#constSection.
    def enterConstSection(self, ctx:pascalParser.ConstSectionContext):
        pass

    # Exit a parse tree produced by pascalParser#constSection.
    def exitConstSection(self, ctx:pascalParser.ConstSectionContext):
        pass


    # Enter a parse tree produced by pascalParser#constDeclaration.
    def enterConstDeclaration(self, ctx:pascalParser.ConstDeclarationContext):
        pass

    # Exit a parse tree produced by pascalParser#constDeclaration.
    def exitConstDeclaration(self, ctx:pascalParser.ConstDeclarationContext):
        pass


    # Enter a parse tree produced by pascalParser#resourceStringSection.
    def enterResourceStringSection(self, ctx:pascalParser.ResourceStringSectionContext):
        pass

    # Exit a parse tree produced by pascalParser#resourceStringSection.
    def exitResourceStringSection(self, ctx:pascalParser.ResourceStringSectionContext):
        pass


    # Enter a parse tree produced by pascalParser#typeSection.
    def enterTypeSection(self, ctx:pascalParser.TypeSectionContext):
        pass

    # Exit a parse tree produced by pascalParser#typeSection.
    def exitTypeSection(self, ctx:pascalParser.TypeSectionContext):
        pass


    # Enter a parse tree produced by pascalParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:pascalParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by pascalParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:pascalParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by pascalParser#varSection.
    def enterVarSection(self, ctx:pascalParser.VarSectionContext):
        pass

    # Exit a parse tree produced by pascalParser#varSection.
    def exitVarSection(self, ctx:pascalParser.VarSectionContext):
        pass


    # Enter a parse tree produced by pascalParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx:pascalParser.VariableDeclarationContext):
        pass

    # Exit a parse tree produced by pascalParser#variableDeclaration.
    def exitVariableDeclaration(self, ctx:pascalParser.VariableDeclarationContext):
        pass


    # Enter a parse tree produced by pascalParser#routineDeclaration.
    def enterRoutineDeclaration(self, ctx:pascalParser.RoutineDeclarationContext):
        pass

    # Exit a parse tree produced by pascalParser#routineDeclaration.
    def exitRoutineDeclaration(self, ctx:pascalParser.RoutineDeclarationContext):
        pass


    # Enter a parse tree produced by pascalParser#routineImplementation.
    def enterRoutineImplementation(self, ctx:pascalParser.RoutineImplementationContext):
        pass

    # Exit a parse tree produced by pascalParser#routineImplementation.
    def exitRoutineImplementation(self, ctx:pascalParser.RoutineImplementationContext):
        pass


    # Enter a parse tree produced by pascalParser#routineHeading.
    def enterRoutineHeading(self, ctx:pascalParser.RoutineHeadingContext):
        pass

    # Exit a parse tree produced by pascalParser#routineHeading.
    def exitRoutineHeading(self, ctx:pascalParser.RoutineHeadingContext):
        pass


    # Enter a parse tree produced by pascalParser#procedureHeading.
    def enterProcedureHeading(self, ctx:pascalParser.ProcedureHeadingContext):
        pass

    # Exit a parse tree produced by pascalParser#procedureHeading.
    def exitProcedureHeading(self, ctx:pascalParser.ProcedureHeadingContext):
        pass


    # Enter a parse tree produced by pascalParser#functionHeading.
    def enterFunctionHeading(self, ctx:pascalParser.FunctionHeadingContext):
        pass

    # Exit a parse tree produced by pascalParser#functionHeading.
    def exitFunctionHeading(self, ctx:pascalParser.FunctionHeadingContext):
        pass


    # Enter a parse tree produced by pascalParser#constructorHeading.
    def enterConstructorHeading(self, ctx:pascalParser.ConstructorHeadingContext):
        pass

    # Exit a parse tree produced by pascalParser#constructorHeading.
    def exitConstructorHeading(self, ctx:pascalParser.ConstructorHeadingContext):
        pass


    # Enter a parse tree produced by pascalParser#destructorHeading.
    def enterDestructorHeading(self, ctx:pascalParser.DestructorHeadingContext):
        pass

    # Exit a parse tree produced by pascalParser#destructorHeading.
    def exitDestructorHeading(self, ctx:pascalParser.DestructorHeadingContext):
        pass


    # Enter a parse tree produced by pascalParser#formalParameters.
    def enterFormalParameters(self, ctx:pascalParser.FormalParametersContext):
        pass

    # Exit a parse tree produced by pascalParser#formalParameters.
    def exitFormalParameters(self, ctx:pascalParser.FormalParametersContext):
        pass


    # Enter a parse tree produced by pascalParser#formalParameterSection.
    def enterFormalParameterSection(self, ctx:pascalParser.FormalParameterSectionContext):
        pass

    # Exit a parse tree produced by pascalParser#formalParameterSection.
    def exitFormalParameterSection(self, ctx:pascalParser.FormalParameterSectionContext):
        pass


    # Enter a parse tree produced by pascalParser#parameterModifier.
    def enterParameterModifier(self, ctx:pascalParser.ParameterModifierContext):
        pass

    # Exit a parse tree produced by pascalParser#parameterModifier.
    def exitParameterModifier(self, ctx:pascalParser.ParameterModifierContext):
        pass


    # Enter a parse tree produced by pascalParser#routineDirectiveList.
    def enterRoutineDirectiveList(self, ctx:pascalParser.RoutineDirectiveListContext):
        pass

    # Exit a parse tree produced by pascalParser#routineDirectiveList.
    def exitRoutineDirectiveList(self, ctx:pascalParser.RoutineDirectiveListContext):
        pass


    # Enter a parse tree produced by pascalParser#routineDirective.
    def enterRoutineDirective(self, ctx:pascalParser.RoutineDirectiveContext):
        pass

    # Exit a parse tree produced by pascalParser#routineDirective.
    def exitRoutineDirective(self, ctx:pascalParser.RoutineDirectiveContext):
        pass


    # Enter a parse tree produced by pascalParser#typeSpec.
    def enterTypeSpec(self, ctx:pascalParser.TypeSpecContext):
        pass

    # Exit a parse tree produced by pascalParser#typeSpec.
    def exitTypeSpec(self, ctx:pascalParser.TypeSpecContext):
        pass


    # Enter a parse tree produced by pascalParser#simpleType.
    def enterSimpleType(self, ctx:pascalParser.SimpleTypeContext):
        pass

    # Exit a parse tree produced by pascalParser#simpleType.
    def exitSimpleType(self, ctx:pascalParser.SimpleTypeContext):
        pass


    # Enter a parse tree produced by pascalParser#subrangeType.
    def enterSubrangeType(self, ctx:pascalParser.SubrangeTypeContext):
        pass

    # Exit a parse tree produced by pascalParser#subrangeType.
    def exitSubrangeType(self, ctx:pascalParser.SubrangeTypeContext):
        pass


    # Enter a parse tree produced by pascalParser#enumeratedType.
    def enterEnumeratedType(self, ctx:pascalParser.EnumeratedTypeContext):
        pass

    # Exit a parse tree produced by pascalParser#enumeratedType.
    def exitEnumeratedType(self, ctx:pascalParser.EnumeratedTypeContext):
        pass


    # Enter a parse tree produced by pascalParser#arrayType.
    def enterArrayType(self, ctx:pascalParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by pascalParser#arrayType.
    def exitArrayType(self, ctx:pascalParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by pascalParser#typeList.
    def enterTypeList(self, ctx:pascalParser.TypeListContext):
        pass

    # Exit a parse tree produced by pascalParser#typeList.
    def exitTypeList(self, ctx:pascalParser.TypeListContext):
        pass


    # Enter a parse tree produced by pascalParser#setType.
    def enterSetType(self, ctx:pascalParser.SetTypeContext):
        pass

    # Exit a parse tree produced by pascalParser#setType.
    def exitSetType(self, ctx:pascalParser.SetTypeContext):
        pass


    # Enter a parse tree produced by pascalParser#fileType.
    def enterFileType(self, ctx:pascalParser.FileTypeContext):
        pass

    # Exit a parse tree produced by pascalParser#fileType.
    def exitFileType(self, ctx:pascalParser.FileTypeContext):
        pass


    # Enter a parse tree produced by pascalParser#pointerType.
    def enterPointerType(self, ctx:pascalParser.PointerTypeContext):
        pass

    # Exit a parse tree produced by pascalParser#pointerType.
    def exitPointerType(self, ctx:pascalParser.PointerTypeContext):
        pass


    # Enter a parse tree produced by pascalParser#procedureType.
    def enterProcedureType(self, ctx:pascalParser.ProcedureTypeContext):
        pass

    # Exit a parse tree produced by pascalParser#procedureType.
    def exitProcedureType(self, ctx:pascalParser.ProcedureTypeContext):
        pass


    # Enter a parse tree produced by pascalParser#classType.
    def enterClassType(self, ctx:pascalParser.ClassTypeContext):
        pass

    # Exit a parse tree produced by pascalParser#classType.
    def exitClassType(self, ctx:pascalParser.ClassTypeContext):
        pass


    # Enter a parse tree produced by pascalParser#classHeritage.
    def enterClassHeritage(self, ctx:pascalParser.ClassHeritageContext):
        pass

    # Exit a parse tree produced by pascalParser#classHeritage.
    def exitClassHeritage(self, ctx:pascalParser.ClassHeritageContext):
        pass


    # Enter a parse tree produced by pascalParser#typeRefList.
    def enterTypeRefList(self, ctx:pascalParser.TypeRefListContext):
        pass

    # Exit a parse tree produced by pascalParser#typeRefList.
    def exitTypeRefList(self, ctx:pascalParser.TypeRefListContext):
        pass


    # Enter a parse tree produced by pascalParser#classBody.
    def enterClassBody(self, ctx:pascalParser.ClassBodyContext):
        pass

    # Exit a parse tree produced by pascalParser#classBody.
    def exitClassBody(self, ctx:pascalParser.ClassBodyContext):
        pass


    # Enter a parse tree produced by pascalParser#classMember.
    def enterClassMember(self, ctx:pascalParser.ClassMemberContext):
        pass

    # Exit a parse tree produced by pascalParser#classMember.
    def exitClassMember(self, ctx:pascalParser.ClassMemberContext):
        pass


    # Enter a parse tree produced by pascalParser#visibilitySection.
    def enterVisibilitySection(self, ctx:pascalParser.VisibilitySectionContext):
        pass

    # Exit a parse tree produced by pascalParser#visibilitySection.
    def exitVisibilitySection(self, ctx:pascalParser.VisibilitySectionContext):
        pass


    # Enter a parse tree produced by pascalParser#classField.
    def enterClassField(self, ctx:pascalParser.ClassFieldContext):
        pass

    # Exit a parse tree produced by pascalParser#classField.
    def exitClassField(self, ctx:pascalParser.ClassFieldContext):
        pass


    # Enter a parse tree produced by pascalParser#classMethod.
    def enterClassMethod(self, ctx:pascalParser.ClassMethodContext):
        pass

    # Exit a parse tree produced by pascalParser#classMethod.
    def exitClassMethod(self, ctx:pascalParser.ClassMethodContext):
        pass


    # Enter a parse tree produced by pascalParser#propertyDeclaration.
    def enterPropertyDeclaration(self, ctx:pascalParser.PropertyDeclarationContext):
        pass

    # Exit a parse tree produced by pascalParser#propertyDeclaration.
    def exitPropertyDeclaration(self, ctx:pascalParser.PropertyDeclarationContext):
        pass


    # Enter a parse tree produced by pascalParser#propertySpec.
    def enterPropertySpec(self, ctx:pascalParser.PropertySpecContext):
        pass

    # Exit a parse tree produced by pascalParser#propertySpec.
    def exitPropertySpec(self, ctx:pascalParser.PropertySpecContext):
        pass


    # Enter a parse tree produced by pascalParser#recordType.
    def enterRecordType(self, ctx:pascalParser.RecordTypeContext):
        pass

    # Exit a parse tree produced by pascalParser#recordType.
    def exitRecordType(self, ctx:pascalParser.RecordTypeContext):
        pass


    # Enter a parse tree produced by pascalParser#recordField.
    def enterRecordField(self, ctx:pascalParser.RecordFieldContext):
        pass

    # Exit a parse tree produced by pascalParser#recordField.
    def exitRecordField(self, ctx:pascalParser.RecordFieldContext):
        pass


    # Enter a parse tree produced by pascalParser#typeRef.
    def enterTypeRef(self, ctx:pascalParser.TypeRefContext):
        pass

    # Exit a parse tree produced by pascalParser#typeRef.
    def exitTypeRef(self, ctx:pascalParser.TypeRefContext):
        pass


    # Enter a parse tree produced by pascalParser#statementBlock.
    def enterStatementBlock(self, ctx:pascalParser.StatementBlockContext):
        pass

    # Exit a parse tree produced by pascalParser#statementBlock.
    def exitStatementBlock(self, ctx:pascalParser.StatementBlockContext):
        pass


    # Enter a parse tree produced by pascalParser#statementList.
    def enterStatementList(self, ctx:pascalParser.StatementListContext):
        pass

    # Exit a parse tree produced by pascalParser#statementList.
    def exitStatementList(self, ctx:pascalParser.StatementListContext):
        pass


    # Enter a parse tree produced by pascalParser#statement.
    def enterStatement(self, ctx:pascalParser.StatementContext):
        pass

    # Exit a parse tree produced by pascalParser#statement.
    def exitStatement(self, ctx:pascalParser.StatementContext):
        pass


    # Enter a parse tree produced by pascalParser#compoundStatement.
    def enterCompoundStatement(self, ctx:pascalParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#compoundStatement.
    def exitCompoundStatement(self, ctx:pascalParser.CompoundStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:pascalParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:pascalParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#procedureCallStatement.
    def enterProcedureCallStatement(self, ctx:pascalParser.ProcedureCallStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#procedureCallStatement.
    def exitProcedureCallStatement(self, ctx:pascalParser.ProcedureCallStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#ifStatement.
    def enterIfStatement(self, ctx:pascalParser.IfStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#ifStatement.
    def exitIfStatement(self, ctx:pascalParser.IfStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#caseStatement.
    def enterCaseStatement(self, ctx:pascalParser.CaseStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#caseStatement.
    def exitCaseStatement(self, ctx:pascalParser.CaseStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#caseBranch.
    def enterCaseBranch(self, ctx:pascalParser.CaseBranchContext):
        pass

    # Exit a parse tree produced by pascalParser#caseBranch.
    def exitCaseBranch(self, ctx:pascalParser.CaseBranchContext):
        pass


    # Enter a parse tree produced by pascalParser#caseLabelList.
    def enterCaseLabelList(self, ctx:pascalParser.CaseLabelListContext):
        pass

    # Exit a parse tree produced by pascalParser#caseLabelList.
    def exitCaseLabelList(self, ctx:pascalParser.CaseLabelListContext):
        pass


    # Enter a parse tree produced by pascalParser#whileStatement.
    def enterWhileStatement(self, ctx:pascalParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#whileStatement.
    def exitWhileStatement(self, ctx:pascalParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#repeatStatement.
    def enterRepeatStatement(self, ctx:pascalParser.RepeatStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#repeatStatement.
    def exitRepeatStatement(self, ctx:pascalParser.RepeatStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#forStatement.
    def enterForStatement(self, ctx:pascalParser.ForStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#forStatement.
    def exitForStatement(self, ctx:pascalParser.ForStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#withStatement.
    def enterWithStatement(self, ctx:pascalParser.WithStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#withStatement.
    def exitWithStatement(self, ctx:pascalParser.WithStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#variableList.
    def enterVariableList(self, ctx:pascalParser.VariableListContext):
        pass

    # Exit a parse tree produced by pascalParser#variableList.
    def exitVariableList(self, ctx:pascalParser.VariableListContext):
        pass


    # Enter a parse tree produced by pascalParser#tryStatement.
    def enterTryStatement(self, ctx:pascalParser.TryStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#tryStatement.
    def exitTryStatement(self, ctx:pascalParser.TryStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#exceptionHandlerList.
    def enterExceptionHandlerList(self, ctx:pascalParser.ExceptionHandlerListContext):
        pass

    # Exit a parse tree produced by pascalParser#exceptionHandlerList.
    def exitExceptionHandlerList(self, ctx:pascalParser.ExceptionHandlerListContext):
        pass


    # Enter a parse tree produced by pascalParser#exceptionHandler.
    def enterExceptionHandler(self, ctx:pascalParser.ExceptionHandlerContext):
        pass

    # Exit a parse tree produced by pascalParser#exceptionHandler.
    def exitExceptionHandler(self, ctx:pascalParser.ExceptionHandlerContext):
        pass


    # Enter a parse tree produced by pascalParser#raiseStatement.
    def enterRaiseStatement(self, ctx:pascalParser.RaiseStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#raiseStatement.
    def exitRaiseStatement(self, ctx:pascalParser.RaiseStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#gotoStatement.
    def enterGotoStatement(self, ctx:pascalParser.GotoStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#gotoStatement.
    def exitGotoStatement(self, ctx:pascalParser.GotoStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#breakStatement.
    def enterBreakStatement(self, ctx:pascalParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#breakStatement.
    def exitBreakStatement(self, ctx:pascalParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#continueStatement.
    def enterContinueStatement(self, ctx:pascalParser.ContinueStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#continueStatement.
    def exitContinueStatement(self, ctx:pascalParser.ContinueStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#exitStatement.
    def enterExitStatement(self, ctx:pascalParser.ExitStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#exitStatement.
    def exitExitStatement(self, ctx:pascalParser.ExitStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#emptyStatement.
    def enterEmptyStatement(self, ctx:pascalParser.EmptyStatementContext):
        pass

    # Exit a parse tree produced by pascalParser#emptyStatement.
    def exitEmptyStatement(self, ctx:pascalParser.EmptyStatementContext):
        pass


    # Enter a parse tree produced by pascalParser#actualParameterList.
    def enterActualParameterList(self, ctx:pascalParser.ActualParameterListContext):
        pass

    # Exit a parse tree produced by pascalParser#actualParameterList.
    def exitActualParameterList(self, ctx:pascalParser.ActualParameterListContext):
        pass


    # Enter a parse tree produced by pascalParser#expressionList.
    def enterExpressionList(self, ctx:pascalParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by pascalParser#expressionList.
    def exitExpressionList(self, ctx:pascalParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by pascalParser#expression.
    def enterExpression(self, ctx:pascalParser.ExpressionContext):
        pass

    # Exit a parse tree produced by pascalParser#expression.
    def exitExpression(self, ctx:pascalParser.ExpressionContext):
        pass


    # Enter a parse tree produced by pascalParser#relationalExpression.
    def enterRelationalExpression(self, ctx:pascalParser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by pascalParser#relationalExpression.
    def exitRelationalExpression(self, ctx:pascalParser.RelationalExpressionContext):
        pass


    # Enter a parse tree produced by pascalParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:pascalParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by pascalParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:pascalParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by pascalParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:pascalParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by pascalParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:pascalParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by pascalParser#unaryExpression.
    def enterUnaryExpression(self, ctx:pascalParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by pascalParser#unaryExpression.
    def exitUnaryExpression(self, ctx:pascalParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by pascalParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:pascalParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by pascalParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:pascalParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by pascalParser#setConstructor.
    def enterSetConstructor(self, ctx:pascalParser.SetConstructorContext):
        pass

    # Exit a parse tree produced by pascalParser#setConstructor.
    def exitSetConstructor(self, ctx:pascalParser.SetConstructorContext):
        pass


    # Enter a parse tree produced by pascalParser#variable.
    def enterVariable(self, ctx:pascalParser.VariableContext):
        pass

    # Exit a parse tree produced by pascalParser#variable.
    def exitVariable(self, ctx:pascalParser.VariableContext):
        pass


    # Enter a parse tree produced by pascalParser#designator.
    def enterDesignator(self, ctx:pascalParser.DesignatorContext):
        pass

    # Exit a parse tree produced by pascalParser#designator.
    def exitDesignator(self, ctx:pascalParser.DesignatorContext):
        pass


    # Enter a parse tree produced by pascalParser#designatorSuffix.
    def enterDesignatorSuffix(self, ctx:pascalParser.DesignatorSuffixContext):
        pass

    # Exit a parse tree produced by pascalParser#designatorSuffix.
    def exitDesignatorSuffix(self, ctx:pascalParser.DesignatorSuffixContext):
        pass


    # Enter a parse tree produced by pascalParser#constantExpression.
    def enterConstantExpression(self, ctx:pascalParser.ConstantExpressionContext):
        pass

    # Exit a parse tree produced by pascalParser#constantExpression.
    def exitConstantExpression(self, ctx:pascalParser.ConstantExpressionContext):
        pass


    # Enter a parse tree produced by pascalParser#literal.
    def enterLiteral(self, ctx:pascalParser.LiteralContext):
        pass

    # Exit a parse tree produced by pascalParser#literal.
    def exitLiteral(self, ctx:pascalParser.LiteralContext):
        pass


    # Enter a parse tree produced by pascalParser#identifierList.
    def enterIdentifierList(self, ctx:pascalParser.IdentifierListContext):
        pass

    # Exit a parse tree produced by pascalParser#identifierList.
    def exitIdentifierList(self, ctx:pascalParser.IdentifierListContext):
        pass


    # Enter a parse tree produced by pascalParser#qualifiedIdentifier.
    def enterQualifiedIdentifier(self, ctx:pascalParser.QualifiedIdentifierContext):
        pass

    # Exit a parse tree produced by pascalParser#qualifiedIdentifier.
    def exitQualifiedIdentifier(self, ctx:pascalParser.QualifiedIdentifierContext):
        pass


    # Enter a parse tree produced by pascalParser#identifier.
    def enterIdentifier(self, ctx:pascalParser.IdentifierContext):
        pass

    # Exit a parse tree produced by pascalParser#identifier.
    def exitIdentifier(self, ctx:pascalParser.IdentifierContext):
        pass



del pascalParser