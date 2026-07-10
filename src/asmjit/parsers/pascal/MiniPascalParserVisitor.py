# Generated from grammar/MiniPascalParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MiniPascalParser import MiniPascalParser
else:
    from MiniPascalParser import MiniPascalParser

# This class defines a complete generic visitor for a parse tree produced by MiniPascalParser.

class MiniPascalParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MiniPascalParser#sourceFile.
    def visitSourceFile(self, ctx:MiniPascalParser.SourceFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#externalRoutineSpec.
    def visitExternalRoutineSpec(self, ctx:MiniPascalParser.ExternalRoutineSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#callingConvention.
    def visitCallingConvention(self, ctx:MiniPascalParser.CallingConventionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#programFile.
    def visitProgramFile(self, ctx:MiniPascalParser.ProgramFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#unitFile.
    def visitUnitFile(self, ctx:MiniPascalParser.UnitFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#libraryFile.
    def visitLibraryFile(self, ctx:MiniPascalParser.LibraryFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#compilerDirective.
    def visitCompilerDirective(self, ctx:MiniPascalParser.CompilerDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#exportsClause.
    def visitExportsClause(self, ctx:MiniPascalParser.ExportsClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#exportItem.
    def visitExportItem(self, ctx:MiniPascalParser.ExportItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#exportSignature.
    def visitExportSignature(self, ctx:MiniPascalParser.ExportSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#exportTypeList.
    def visitExportTypeList(self, ctx:MiniPascalParser.ExportTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#usesClause.
    def visitUsesClause(self, ctx:MiniPascalParser.UsesClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#qualifiedIdentList.
    def visitQualifiedIdentList(self, ctx:MiniPascalParser.QualifiedIdentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#interfaceSection.
    def visitInterfaceSection(self, ctx:MiniPascalParser.InterfaceSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#implementationSection.
    def visitImplementationSection(self, ctx:MiniPascalParser.ImplementationSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#interfaceDeclarationPart.
    def visitInterfaceDeclarationPart(self, ctx:MiniPascalParser.InterfaceDeclarationPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#implementationDeclarationPart.
    def visitImplementationDeclarationPart(self, ctx:MiniPascalParser.ImplementationDeclarationPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#unitInitBlock.
    def visitUnitInitBlock(self, ctx:MiniPascalParser.UnitInitBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#qualifiedIdent.
    def visitQualifiedIdent(self, ctx:MiniPascalParser.QualifiedIdentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#declarationPart.
    def visitDeclarationPart(self, ctx:MiniPascalParser.DeclarationPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#classMethodImplementation.
    def visitClassMethodImplementation(self, ctx:MiniPascalParser.ClassMethodImplementationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#procedureHeader.
    def visitProcedureHeader(self, ctx:MiniPascalParser.ProcedureHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#functionHeader.
    def visitFunctionHeader(self, ctx:MiniPascalParser.FunctionHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#constSection.
    def visitConstSection(self, ctx:MiniPascalParser.ConstSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#constDeclaration.
    def visitConstDeclaration(self, ctx:MiniPascalParser.ConstDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#constItem.
    def visitConstItem(self, ctx:MiniPascalParser.ConstItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#constValue.
    def visitConstValue(self, ctx:MiniPascalParser.ConstValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#typeSection.
    def visitTypeSection(self, ctx:MiniPascalParser.TypeSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#typeIdentifier.
    def visitTypeIdentifier(self, ctx:MiniPascalParser.TypeIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:MiniPascalParser.TypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#classDeclaration.
    def visitClassDeclaration(self, ctx:MiniPascalParser.ClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#classParent.
    def visitClassParent(self, ctx:MiniPascalParser.ClassParentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#classBody.
    def visitClassBody(self, ctx:MiniPascalParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#classMember.
    def visitClassMember(self, ctx:MiniPascalParser.ClassMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#visibilitySection.
    def visitVisibilitySection(self, ctx:MiniPascalParser.VisibilitySectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#propertyDeclaration.
    def visitPropertyDeclaration(self, ctx:MiniPascalParser.PropertyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#propertyAccessor.
    def visitPropertyAccessor(self, ctx:MiniPascalParser.PropertyAccessorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#classFunctionDeclaration.
    def visitClassFunctionDeclaration(self, ctx:MiniPascalParser.ClassFunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#classProcedureDeclaration.
    def visitClassProcedureDeclaration(self, ctx:MiniPascalParser.ClassProcedureDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#classFieldDeclaration.
    def visitClassFieldDeclaration(self, ctx:MiniPascalParser.ClassFieldDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#inheritedStatement.
    def visitInheritedStatement(self, ctx:MiniPascalParser.InheritedStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#constructorDeclaration.
    def visitConstructorDeclaration(self, ctx:MiniPascalParser.ConstructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#destructorDeclaration.
    def visitDestructorDeclaration(self, ctx:MiniPascalParser.DestructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#arrayDeclaration.
    def visitArrayDeclaration(self, ctx:MiniPascalParser.ArrayDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#arrayInitializer.
    def visitArrayInitializer(self, ctx:MiniPascalParser.ArrayInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#arrayValueList.
    def visitArrayValueList(self, ctx:MiniPascalParser.ArrayValueListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#arrayType.
    def visitArrayType(self, ctx:MiniPascalParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#arrayRange.
    def visitArrayRange(self, ctx:MiniPascalParser.ArrayRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#typeName.
    def visitTypeName(self, ctx:MiniPascalParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#simpleType.
    def visitSimpleType(self, ctx:MiniPascalParser.SimpleTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#signedInteger.
    def visitSignedInteger(self, ctx:MiniPascalParser.SignedIntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#subrangeType.
    def visitSubrangeType(self, ctx:MiniPascalParser.SubrangeTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#enumDeclaration.
    def visitEnumDeclaration(self, ctx:MiniPascalParser.EnumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#enumValueList.
    def visitEnumValueList(self, ctx:MiniPascalParser.EnumValueListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#enumValue.
    def visitEnumValue(self, ctx:MiniPascalParser.EnumValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#recordDeclaration.
    def visitRecordDeclaration(self, ctx:MiniPascalParser.RecordDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#recordFieldDeclaration.
    def visitRecordFieldDeclaration(self, ctx:MiniPascalParser.RecordFieldDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#functionDeclaration.
    def visitFunctionDeclaration(self, ctx:MiniPascalParser.FunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#procedureDeclaration.
    def visitProcedureDeclaration(self, ctx:MiniPascalParser.ProcedureDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#formalParamList.
    def visitFormalParamList(self, ctx:MiniPascalParser.FormalParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#formalParam.
    def visitFormalParam(self, ctx:MiniPascalParser.FormalParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#paramModifier.
    def visitParamModifier(self, ctx:MiniPascalParser.ParamModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#paramType.
    def visitParamType(self, ctx:MiniPascalParser.ParamTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#openArrayType.
    def visitOpenArrayType(self, ctx:MiniPascalParser.OpenArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#declaration.
    def visitDeclaration(self, ctx:MiniPascalParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#builtinDiskFunctionName.
    def visitBuiltinDiskFunctionName(self, ctx:MiniPascalParser.BuiltinDiskFunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#builtinHashFunctionName.
    def visitBuiltinHashFunctionName(self, ctx:MiniPascalParser.BuiltinHashFunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#functionName.
    def visitFunctionName(self, ctx:MiniPascalParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#functionCallExpr.
    def visitFunctionCallExpr(self, ctx:MiniPascalParser.FunctionCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#procedureCallStatement.
    def visitProcedureCallStatement(self, ctx:MiniPascalParser.ProcedureCallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#actualParamList.
    def visitActualParamList(self, ctx:MiniPascalParser.ActualParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#actualParam.
    def visitActualParam(self, ctx:MiniPascalParser.ActualParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#varSection.
    def visitVarSection(self, ctx:MiniPascalParser.VarSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#varDeclaration.
    def visitVarDeclaration(self, ctx:MiniPascalParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#varType.
    def visitVarType(self, ctx:MiniPascalParser.VarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#identList.
    def visitIdentList(self, ctx:MiniPascalParser.IdentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#block.
    def visitBlock(self, ctx:MiniPascalParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#localDeclaration.
    def visitLocalDeclaration(self, ctx:MiniPascalParser.LocalDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#statementList.
    def visitStatementList(self, ctx:MiniPascalParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#statement.
    def visitStatement(self, ctx:MiniPascalParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#incstatement.
    def visitIncstatement(self, ctx:MiniPascalParser.IncstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#decstatement.
    def visitDecstatement(self, ctx:MiniPascalParser.DecstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#caseStatement.
    def visitCaseStatement(self, ctx:MiniPascalParser.CaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#caseItem.
    def visitCaseItem(self, ctx:MiniPascalParser.CaseItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#caseLabelList.
    def visitCaseLabelList(self, ctx:MiniPascalParser.CaseLabelListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#caseLabel.
    def visitCaseLabel(self, ctx:MiniPascalParser.CaseLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#caseElse.
    def visitCaseElse(self, ctx:MiniPascalParser.CaseElseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#breakStatement.
    def visitBreakStatement(self, ctx:MiniPascalParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#continueStatement.
    def visitContinueStatement(self, ctx:MiniPascalParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#tryStatement.
    def visitTryStatement(self, ctx:MiniPascalParser.TryStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#exitStatement.
    def visitExitStatement(self, ctx:MiniPascalParser.ExitStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#forStatement.
    def visitForStatement(self, ctx:MiniPascalParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#repeatStatement.
    def visitRepeatStatement(self, ctx:MiniPascalParser.RepeatStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#argumentList.
    def visitArgumentList(self, ctx:MiniPascalParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#whileStatement.
    def visitWhileStatement(self, ctx:MiniPascalParser.WhileStatementContext):
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


    # Visit a parse tree produced by MiniPascalParser#compoundStatement.
    def visitCompoundStatement(self, ctx:MiniPascalParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#assignment.
    def visitAssignment(self, ctx:MiniPascalParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#variableRef.
    def visitVariableRef(self, ctx:MiniPascalParser.VariableRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#variableSuffix.
    def visitVariableSuffix(self, ctx:MiniPascalParser.VariableSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#expr.
    def visitExpr(self, ctx:MiniPascalParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#boolOrExpr.
    def visitBoolOrExpr(self, ctx:MiniPascalParser.BoolOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#boolXorExpr.
    def visitBoolXorExpr(self, ctx:MiniPascalParser.BoolXorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#boolAndExpr.
    def visitBoolAndExpr(self, ctx:MiniPascalParser.BoolAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#compareExpr.
    def visitCompareExpr(self, ctx:MiniPascalParser.CompareExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#addExpr.
    def visitAddExpr(self, ctx:MiniPascalParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#arrayConstructor.
    def visitArrayConstructor(self, ctx:MiniPascalParser.ArrayConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#arrayConstructorItems.
    def visitArrayConstructorItems(self, ctx:MiniPascalParser.ArrayConstructorItemsContext):
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