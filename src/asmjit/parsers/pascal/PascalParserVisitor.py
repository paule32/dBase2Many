# Generated from compiler/grammar/PascalParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PascalParser import PascalParser
else:
    from PascalParser import PascalParser

# This class defines a complete generic visitor for a parse tree produced by PascalParser.

class PascalParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PascalParser#sourceFile.
    def visitSourceFile(self, ctx:PascalParser.SourceFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#externalImportTarget.
    def visitExternalImportTarget(self, ctx:PascalParser.ExternalImportTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#routineCallingConvention.
    def visitRoutineCallingConvention(self, ctx:PascalParser.RoutineCallingConventionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#callingConvention.
    def visitCallingConvention(self, ctx:PascalParser.CallingConventionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#externalRoutineDirective.
    def visitExternalRoutineDirective(self, ctx:PascalParser.ExternalRoutineDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#externalLibrary.
    def visitExternalLibrary(self, ctx:PascalParser.ExternalLibraryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#externalNameClause.
    def visitExternalNameClause(self, ctx:PascalParser.ExternalNameClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#externalOrdinalClause.
    def visitExternalOrdinalClause(self, ctx:PascalParser.ExternalOrdinalClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#programFile.
    def visitProgramFile(self, ctx:PascalParser.ProgramFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#unitFile.
    def visitUnitFile(self, ctx:PascalParser.UnitFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#libraryFile.
    def visitLibraryFile(self, ctx:PascalParser.LibraryFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#compilerDirective.
    def visitCompilerDirective(self, ctx:PascalParser.CompilerDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#exportsClause.
    def visitExportsClause(self, ctx:PascalParser.ExportsClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#exportItem.
    def visitExportItem(self, ctx:PascalParser.ExportItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#exportSignature.
    def visitExportSignature(self, ctx:PascalParser.ExportSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#exportTypeList.
    def visitExportTypeList(self, ctx:PascalParser.ExportTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#usesClause.
    def visitUsesClause(self, ctx:PascalParser.UsesClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#qualifiedIdentList.
    def visitQualifiedIdentList(self, ctx:PascalParser.QualifiedIdentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#interfaceSection.
    def visitInterfaceSection(self, ctx:PascalParser.InterfaceSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#implementationSection.
    def visitImplementationSection(self, ctx:PascalParser.ImplementationSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#interfaceDeclarationPart.
    def visitInterfaceDeclarationPart(self, ctx:PascalParser.InterfaceDeclarationPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#implementationDeclarationPart.
    def visitImplementationDeclarationPart(self, ctx:PascalParser.ImplementationDeclarationPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#unitInitBlock.
    def visitUnitInitBlock(self, ctx:PascalParser.UnitInitBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#qualifiedIdent.
    def visitQualifiedIdent(self, ctx:PascalParser.QualifiedIdentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#methodDirective.
    def visitMethodDirective(self, ctx:PascalParser.MethodDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#methodDirectiveList.
    def visitMethodDirectiveList(self, ctx:PascalParser.MethodDirectiveListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#declarationPart.
    def visitDeclarationPart(self, ctx:PascalParser.DeclarationPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#classMethodImplementation.
    def visitClassMethodImplementation(self, ctx:PascalParser.ClassMethodImplementationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#procedureHeader.
    def visitProcedureHeader(self, ctx:PascalParser.ProcedureHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#functionHeader.
    def visitFunctionHeader(self, ctx:PascalParser.FunctionHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#constSection.
    def visitConstSection(self, ctx:PascalParser.ConstSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#constDeclaration.
    def visitConstDeclaration(self, ctx:PascalParser.ConstDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#constItem.
    def visitConstItem(self, ctx:PascalParser.ConstItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#constValue.
    def visitConstValue(self, ctx:PascalParser.ConstValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#typeSection.
    def visitTypeSection(self, ctx:PascalParser.TypeSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#typeIdentifier.
    def visitTypeIdentifier(self, ctx:PascalParser.TypeIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:PascalParser.TypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#classDeclaration.
    def visitClassDeclaration(self, ctx:PascalParser.ClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#classParent.
    def visitClassParent(self, ctx:PascalParser.ClassParentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#classBody.
    def visitClassBody(self, ctx:PascalParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#classMember.
    def visitClassMember(self, ctx:PascalParser.ClassMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#visibilitySection.
    def visitVisibilitySection(self, ctx:PascalParser.VisibilitySectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#propertyDeclaration.
    def visitPropertyDeclaration(self, ctx:PascalParser.PropertyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#propertyAccessor.
    def visitPropertyAccessor(self, ctx:PascalParser.PropertyAccessorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#classFunctionDeclaration.
    def visitClassFunctionDeclaration(self, ctx:PascalParser.ClassFunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#classProcedureDeclaration.
    def visitClassProcedureDeclaration(self, ctx:PascalParser.ClassProcedureDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#classFieldDeclaration.
    def visitClassFieldDeclaration(self, ctx:PascalParser.ClassFieldDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#inheritedStatement.
    def visitInheritedStatement(self, ctx:PascalParser.InheritedStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#inheritedExpression.
    def visitInheritedExpression(self, ctx:PascalParser.InheritedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#constructorDeclaration.
    def visitConstructorDeclaration(self, ctx:PascalParser.ConstructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#destructorDeclaration.
    def visitDestructorDeclaration(self, ctx:PascalParser.DestructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#arrayDeclaration.
    def visitArrayDeclaration(self, ctx:PascalParser.ArrayDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#arrayInitializer.
    def visitArrayInitializer(self, ctx:PascalParser.ArrayInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#arrayValueList.
    def visitArrayValueList(self, ctx:PascalParser.ArrayValueListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#arrayType.
    def visitArrayType(self, ctx:PascalParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#arrayRange.
    def visitArrayRange(self, ctx:PascalParser.ArrayRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#arrayConstructor.
    def visitArrayConstructor(self, ctx:PascalParser.ArrayConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#arrayConstructorItems.
    def visitArrayConstructorItems(self, ctx:PascalParser.ArrayConstructorItemsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#typeName.
    def visitTypeName(self, ctx:PascalParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#simpleType.
    def visitSimpleType(self, ctx:PascalParser.SimpleTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#signedInteger.
    def visitSignedInteger(self, ctx:PascalParser.SignedIntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#subrangeType.
    def visitSubrangeType(self, ctx:PascalParser.SubrangeTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#enumDeclaration.
    def visitEnumDeclaration(self, ctx:PascalParser.EnumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#enumValueList.
    def visitEnumValueList(self, ctx:PascalParser.EnumValueListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#enumValue.
    def visitEnumValue(self, ctx:PascalParser.EnumValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#recordDeclaration.
    def visitRecordDeclaration(self, ctx:PascalParser.RecordDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#recordFieldDeclaration.
    def visitRecordFieldDeclaration(self, ctx:PascalParser.RecordFieldDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#functionDeclaration.
    def visitFunctionDeclaration(self, ctx:PascalParser.FunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#procedureDeclaration.
    def visitProcedureDeclaration(self, ctx:PascalParser.ProcedureDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#formalParamList.
    def visitFormalParamList(self, ctx:PascalParser.FormalParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#formalParam.
    def visitFormalParam(self, ctx:PascalParser.FormalParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#paramModifier.
    def visitParamModifier(self, ctx:PascalParser.ParamModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#paramType.
    def visitParamType(self, ctx:PascalParser.ParamTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#openArrayType.
    def visitOpenArrayType(self, ctx:PascalParser.OpenArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#declaration.
    def visitDeclaration(self, ctx:PascalParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#builtinDiskFunctionName.
    def visitBuiltinDiskFunctionName(self, ctx:PascalParser.BuiltinDiskFunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#functionName.
    def visitFunctionName(self, ctx:PascalParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#functionCallExpr.
    def visitFunctionCallExpr(self, ctx:PascalParser.FunctionCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#procedureCallStatement.
    def visitProcedureCallStatement(self, ctx:PascalParser.ProcedureCallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#actualParamList.
    def visitActualParamList(self, ctx:PascalParser.ActualParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#actualParam.
    def visitActualParam(self, ctx:PascalParser.ActualParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#varSection.
    def visitVarSection(self, ctx:PascalParser.VarSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#varDeclaration.
    def visitVarDeclaration(self, ctx:PascalParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#varType.
    def visitVarType(self, ctx:PascalParser.VarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#identList.
    def visitIdentList(self, ctx:PascalParser.IdentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#block.
    def visitBlock(self, ctx:PascalParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#localDeclaration.
    def visitLocalDeclaration(self, ctx:PascalParser.LocalDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#statementList.
    def visitStatementList(self, ctx:PascalParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#statement.
    def visitStatement(self, ctx:PascalParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#incstatement.
    def visitIncstatement(self, ctx:PascalParser.IncstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#decstatement.
    def visitDecstatement(self, ctx:PascalParser.DecstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#caseStatement.
    def visitCaseStatement(self, ctx:PascalParser.CaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#caseItem.
    def visitCaseItem(self, ctx:PascalParser.CaseItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#caseLabelList.
    def visitCaseLabelList(self, ctx:PascalParser.CaseLabelListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#caseLabel.
    def visitCaseLabel(self, ctx:PascalParser.CaseLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#caseElse.
    def visitCaseElse(self, ctx:PascalParser.CaseElseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#breakStatement.
    def visitBreakStatement(self, ctx:PascalParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#continueStatement.
    def visitContinueStatement(self, ctx:PascalParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#tryStatement.
    def visitTryStatement(self, ctx:PascalParser.TryStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#raiseStatement.
    def visitRaiseStatement(self, ctx:PascalParser.RaiseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#exitStatement.
    def visitExitStatement(self, ctx:PascalParser.ExitStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#forStatement.
    def visitForStatement(self, ctx:PascalParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#repeatStatement.
    def visitRepeatStatement(self, ctx:PascalParser.RepeatStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#argumentList.
    def visitArgumentList(self, ctx:PascalParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#whileStatement.
    def visitWhileStatement(self, ctx:PascalParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#ifStatement.
    def visitIfStatement(self, ctx:PascalParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#condition.
    def visitCondition(self, ctx:PascalParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#compareOp.
    def visitCompareOp(self, ctx:PascalParser.CompareOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#compoundStatement.
    def visitCompoundStatement(self, ctx:PascalParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#assignment.
    def visitAssignment(self, ctx:PascalParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#variableRef.
    def visitVariableRef(self, ctx:PascalParser.VariableRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#variableSuffix.
    def visitVariableSuffix(self, ctx:PascalParser.VariableSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#pointerDereference.
    def visitPointerDereference(self, ctx:PascalParser.PointerDereferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#fieldAccess.
    def visitFieldAccess(self, ctx:PascalParser.FieldAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#arrayIndex.
    def visitArrayIndex(self, ctx:PascalParser.ArrayIndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#exprList.
    def visitExprList(self, ctx:PascalParser.ExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#expr.
    def visitExpr(self, ctx:PascalParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#conditionalExpression.
    def visitConditionalExpression(self, ctx:PascalParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#boolOrExpr.
    def visitBoolOrExpr(self, ctx:PascalParser.BoolOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#boolXorExpr.
    def visitBoolXorExpr(self, ctx:PascalParser.BoolXorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#boolAndExpr.
    def visitBoolAndExpr(self, ctx:PascalParser.BoolAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#compareExpr.
    def visitCompareExpr(self, ctx:PascalParser.CompareExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#addExpr.
    def visitAddExpr(self, ctx:PascalParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#shiftExpr.
    def visitShiftExpr(self, ctx:PascalParser.ShiftExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#term.
    def visitTerm(self, ctx:PascalParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#factor.
    def visitFactor(self, ctx:PascalParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#writeLnStatement.
    def visitWriteLnStatement(self, ctx:PascalParser.WriteLnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#writeArgList.
    def visitWriteArgList(self, ctx:PascalParser.WriteArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#writeArg.
    def visitWriteArg(self, ctx:PascalParser.WriteArgContext):
        return self.visitChildren(ctx)



del PascalParser