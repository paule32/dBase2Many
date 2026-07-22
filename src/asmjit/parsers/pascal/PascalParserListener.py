# Generated from compiler/grammar/PascalParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PascalParser import PascalParser
else:
    from PascalParser import PascalParser

# This class defines a complete listener for a parse tree produced by PascalParser.
class PascalParserListener(ParseTreeListener):

    # Enter a parse tree produced by PascalParser#sourceFile.
    def enterSourceFile(self, ctx:PascalParser.SourceFileContext):
        pass

    # Exit a parse tree produced by PascalParser#sourceFile.
    def exitSourceFile(self, ctx:PascalParser.SourceFileContext):
        pass


    # Enter a parse tree produced by PascalParser#externalImportTarget.
    def enterExternalImportTarget(self, ctx:PascalParser.ExternalImportTargetContext):
        pass

    # Exit a parse tree produced by PascalParser#externalImportTarget.
    def exitExternalImportTarget(self, ctx:PascalParser.ExternalImportTargetContext):
        pass


    # Enter a parse tree produced by PascalParser#routineCallingConvention.
    def enterRoutineCallingConvention(self, ctx:PascalParser.RoutineCallingConventionContext):
        pass

    # Exit a parse tree produced by PascalParser#routineCallingConvention.
    def exitRoutineCallingConvention(self, ctx:PascalParser.RoutineCallingConventionContext):
        pass


    # Enter a parse tree produced by PascalParser#callingConvention.
    def enterCallingConvention(self, ctx:PascalParser.CallingConventionContext):
        pass

    # Exit a parse tree produced by PascalParser#callingConvention.
    def exitCallingConvention(self, ctx:PascalParser.CallingConventionContext):
        pass


    # Enter a parse tree produced by PascalParser#externalRoutineDirective.
    def enterExternalRoutineDirective(self, ctx:PascalParser.ExternalRoutineDirectiveContext):
        pass

    # Exit a parse tree produced by PascalParser#externalRoutineDirective.
    def exitExternalRoutineDirective(self, ctx:PascalParser.ExternalRoutineDirectiveContext):
        pass


    # Enter a parse tree produced by PascalParser#externalLibrary.
    def enterExternalLibrary(self, ctx:PascalParser.ExternalLibraryContext):
        pass

    # Exit a parse tree produced by PascalParser#externalLibrary.
    def exitExternalLibrary(self, ctx:PascalParser.ExternalLibraryContext):
        pass


    # Enter a parse tree produced by PascalParser#externalNameClause.
    def enterExternalNameClause(self, ctx:PascalParser.ExternalNameClauseContext):
        pass

    # Exit a parse tree produced by PascalParser#externalNameClause.
    def exitExternalNameClause(self, ctx:PascalParser.ExternalNameClauseContext):
        pass


    # Enter a parse tree produced by PascalParser#externalOrdinalClause.
    def enterExternalOrdinalClause(self, ctx:PascalParser.ExternalOrdinalClauseContext):
        pass

    # Exit a parse tree produced by PascalParser#externalOrdinalClause.
    def exitExternalOrdinalClause(self, ctx:PascalParser.ExternalOrdinalClauseContext):
        pass


    # Enter a parse tree produced by PascalParser#programFile.
    def enterProgramFile(self, ctx:PascalParser.ProgramFileContext):
        pass

    # Exit a parse tree produced by PascalParser#programFile.
    def exitProgramFile(self, ctx:PascalParser.ProgramFileContext):
        pass


    # Enter a parse tree produced by PascalParser#unitFile.
    def enterUnitFile(self, ctx:PascalParser.UnitFileContext):
        pass

    # Exit a parse tree produced by PascalParser#unitFile.
    def exitUnitFile(self, ctx:PascalParser.UnitFileContext):
        pass


    # Enter a parse tree produced by PascalParser#libraryFile.
    def enterLibraryFile(self, ctx:PascalParser.LibraryFileContext):
        pass

    # Exit a parse tree produced by PascalParser#libraryFile.
    def exitLibraryFile(self, ctx:PascalParser.LibraryFileContext):
        pass


    # Enter a parse tree produced by PascalParser#compilerDirective.
    def enterCompilerDirective(self, ctx:PascalParser.CompilerDirectiveContext):
        pass

    # Exit a parse tree produced by PascalParser#compilerDirective.
    def exitCompilerDirective(self, ctx:PascalParser.CompilerDirectiveContext):
        pass


    # Enter a parse tree produced by PascalParser#exportsClause.
    def enterExportsClause(self, ctx:PascalParser.ExportsClauseContext):
        pass

    # Exit a parse tree produced by PascalParser#exportsClause.
    def exitExportsClause(self, ctx:PascalParser.ExportsClauseContext):
        pass


    # Enter a parse tree produced by PascalParser#exportItem.
    def enterExportItem(self, ctx:PascalParser.ExportItemContext):
        pass

    # Exit a parse tree produced by PascalParser#exportItem.
    def exitExportItem(self, ctx:PascalParser.ExportItemContext):
        pass


    # Enter a parse tree produced by PascalParser#exportSignature.
    def enterExportSignature(self, ctx:PascalParser.ExportSignatureContext):
        pass

    # Exit a parse tree produced by PascalParser#exportSignature.
    def exitExportSignature(self, ctx:PascalParser.ExportSignatureContext):
        pass


    # Enter a parse tree produced by PascalParser#exportTypeList.
    def enterExportTypeList(self, ctx:PascalParser.ExportTypeListContext):
        pass

    # Exit a parse tree produced by PascalParser#exportTypeList.
    def exitExportTypeList(self, ctx:PascalParser.ExportTypeListContext):
        pass


    # Enter a parse tree produced by PascalParser#usesClause.
    def enterUsesClause(self, ctx:PascalParser.UsesClauseContext):
        pass

    # Exit a parse tree produced by PascalParser#usesClause.
    def exitUsesClause(self, ctx:PascalParser.UsesClauseContext):
        pass


    # Enter a parse tree produced by PascalParser#qualifiedIdentList.
    def enterQualifiedIdentList(self, ctx:PascalParser.QualifiedIdentListContext):
        pass

    # Exit a parse tree produced by PascalParser#qualifiedIdentList.
    def exitQualifiedIdentList(self, ctx:PascalParser.QualifiedIdentListContext):
        pass


    # Enter a parse tree produced by PascalParser#interfaceSection.
    def enterInterfaceSection(self, ctx:PascalParser.InterfaceSectionContext):
        pass

    # Exit a parse tree produced by PascalParser#interfaceSection.
    def exitInterfaceSection(self, ctx:PascalParser.InterfaceSectionContext):
        pass


    # Enter a parse tree produced by PascalParser#implementationSection.
    def enterImplementationSection(self, ctx:PascalParser.ImplementationSectionContext):
        pass

    # Exit a parse tree produced by PascalParser#implementationSection.
    def exitImplementationSection(self, ctx:PascalParser.ImplementationSectionContext):
        pass


    # Enter a parse tree produced by PascalParser#interfaceDeclarationPart.
    def enterInterfaceDeclarationPart(self, ctx:PascalParser.InterfaceDeclarationPartContext):
        pass

    # Exit a parse tree produced by PascalParser#interfaceDeclarationPart.
    def exitInterfaceDeclarationPart(self, ctx:PascalParser.InterfaceDeclarationPartContext):
        pass


    # Enter a parse tree produced by PascalParser#implementationDeclarationPart.
    def enterImplementationDeclarationPart(self, ctx:PascalParser.ImplementationDeclarationPartContext):
        pass

    # Exit a parse tree produced by PascalParser#implementationDeclarationPart.
    def exitImplementationDeclarationPart(self, ctx:PascalParser.ImplementationDeclarationPartContext):
        pass


    # Enter a parse tree produced by PascalParser#unitInitBlock.
    def enterUnitInitBlock(self, ctx:PascalParser.UnitInitBlockContext):
        pass

    # Exit a parse tree produced by PascalParser#unitInitBlock.
    def exitUnitInitBlock(self, ctx:PascalParser.UnitInitBlockContext):
        pass


    # Enter a parse tree produced by PascalParser#qualifiedIdent.
    def enterQualifiedIdent(self, ctx:PascalParser.QualifiedIdentContext):
        pass

    # Exit a parse tree produced by PascalParser#qualifiedIdent.
    def exitQualifiedIdent(self, ctx:PascalParser.QualifiedIdentContext):
        pass


    # Enter a parse tree produced by PascalParser#methodDirective.
    def enterMethodDirective(self, ctx:PascalParser.MethodDirectiveContext):
        pass

    # Exit a parse tree produced by PascalParser#methodDirective.
    def exitMethodDirective(self, ctx:PascalParser.MethodDirectiveContext):
        pass


    # Enter a parse tree produced by PascalParser#methodDirectiveList.
    def enterMethodDirectiveList(self, ctx:PascalParser.MethodDirectiveListContext):
        pass

    # Exit a parse tree produced by PascalParser#methodDirectiveList.
    def exitMethodDirectiveList(self, ctx:PascalParser.MethodDirectiveListContext):
        pass


    # Enter a parse tree produced by PascalParser#declarationPart.
    def enterDeclarationPart(self, ctx:PascalParser.DeclarationPartContext):
        pass

    # Exit a parse tree produced by PascalParser#declarationPart.
    def exitDeclarationPart(self, ctx:PascalParser.DeclarationPartContext):
        pass


    # Enter a parse tree produced by PascalParser#classMethodImplementation.
    def enterClassMethodImplementation(self, ctx:PascalParser.ClassMethodImplementationContext):
        pass

    # Exit a parse tree produced by PascalParser#classMethodImplementation.
    def exitClassMethodImplementation(self, ctx:PascalParser.ClassMethodImplementationContext):
        pass


    # Enter a parse tree produced by PascalParser#procedureHeader.
    def enterProcedureHeader(self, ctx:PascalParser.ProcedureHeaderContext):
        pass

    # Exit a parse tree produced by PascalParser#procedureHeader.
    def exitProcedureHeader(self, ctx:PascalParser.ProcedureHeaderContext):
        pass


    # Enter a parse tree produced by PascalParser#functionHeader.
    def enterFunctionHeader(self, ctx:PascalParser.FunctionHeaderContext):
        pass

    # Exit a parse tree produced by PascalParser#functionHeader.
    def exitFunctionHeader(self, ctx:PascalParser.FunctionHeaderContext):
        pass


    # Enter a parse tree produced by PascalParser#constSection.
    def enterConstSection(self, ctx:PascalParser.ConstSectionContext):
        pass

    # Exit a parse tree produced by PascalParser#constSection.
    def exitConstSection(self, ctx:PascalParser.ConstSectionContext):
        pass


    # Enter a parse tree produced by PascalParser#constDeclaration.
    def enterConstDeclaration(self, ctx:PascalParser.ConstDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#constDeclaration.
    def exitConstDeclaration(self, ctx:PascalParser.ConstDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#constItem.
    def enterConstItem(self, ctx:PascalParser.ConstItemContext):
        pass

    # Exit a parse tree produced by PascalParser#constItem.
    def exitConstItem(self, ctx:PascalParser.ConstItemContext):
        pass


    # Enter a parse tree produced by PascalParser#constValue.
    def enterConstValue(self, ctx:PascalParser.ConstValueContext):
        pass

    # Exit a parse tree produced by PascalParser#constValue.
    def exitConstValue(self, ctx:PascalParser.ConstValueContext):
        pass


    # Enter a parse tree produced by PascalParser#typeSection.
    def enterTypeSection(self, ctx:PascalParser.TypeSectionContext):
        pass

    # Exit a parse tree produced by PascalParser#typeSection.
    def exitTypeSection(self, ctx:PascalParser.TypeSectionContext):
        pass


    # Enter a parse tree produced by PascalParser#typeIdentifier.
    def enterTypeIdentifier(self, ctx:PascalParser.TypeIdentifierContext):
        pass

    # Exit a parse tree produced by PascalParser#typeIdentifier.
    def exitTypeIdentifier(self, ctx:PascalParser.TypeIdentifierContext):
        pass


    # Enter a parse tree produced by PascalParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:PascalParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:PascalParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#classDeclaration.
    def enterClassDeclaration(self, ctx:PascalParser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#classDeclaration.
    def exitClassDeclaration(self, ctx:PascalParser.ClassDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#classParent.
    def enterClassParent(self, ctx:PascalParser.ClassParentContext):
        pass

    # Exit a parse tree produced by PascalParser#classParent.
    def exitClassParent(self, ctx:PascalParser.ClassParentContext):
        pass


    # Enter a parse tree produced by PascalParser#classBody.
    def enterClassBody(self, ctx:PascalParser.ClassBodyContext):
        pass

    # Exit a parse tree produced by PascalParser#classBody.
    def exitClassBody(self, ctx:PascalParser.ClassBodyContext):
        pass


    # Enter a parse tree produced by PascalParser#classMember.
    def enterClassMember(self, ctx:PascalParser.ClassMemberContext):
        pass

    # Exit a parse tree produced by PascalParser#classMember.
    def exitClassMember(self, ctx:PascalParser.ClassMemberContext):
        pass


    # Enter a parse tree produced by PascalParser#visibilitySection.
    def enterVisibilitySection(self, ctx:PascalParser.VisibilitySectionContext):
        pass

    # Exit a parse tree produced by PascalParser#visibilitySection.
    def exitVisibilitySection(self, ctx:PascalParser.VisibilitySectionContext):
        pass


    # Enter a parse tree produced by PascalParser#propertyDeclaration.
    def enterPropertyDeclaration(self, ctx:PascalParser.PropertyDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#propertyDeclaration.
    def exitPropertyDeclaration(self, ctx:PascalParser.PropertyDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#propertyAccessor.
    def enterPropertyAccessor(self, ctx:PascalParser.PropertyAccessorContext):
        pass

    # Exit a parse tree produced by PascalParser#propertyAccessor.
    def exitPropertyAccessor(self, ctx:PascalParser.PropertyAccessorContext):
        pass


    # Enter a parse tree produced by PascalParser#classFunctionDeclaration.
    def enterClassFunctionDeclaration(self, ctx:PascalParser.ClassFunctionDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#classFunctionDeclaration.
    def exitClassFunctionDeclaration(self, ctx:PascalParser.ClassFunctionDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#classProcedureDeclaration.
    def enterClassProcedureDeclaration(self, ctx:PascalParser.ClassProcedureDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#classProcedureDeclaration.
    def exitClassProcedureDeclaration(self, ctx:PascalParser.ClassProcedureDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#classFieldDeclaration.
    def enterClassFieldDeclaration(self, ctx:PascalParser.ClassFieldDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#classFieldDeclaration.
    def exitClassFieldDeclaration(self, ctx:PascalParser.ClassFieldDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#inheritedStatement.
    def enterInheritedStatement(self, ctx:PascalParser.InheritedStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#inheritedStatement.
    def exitInheritedStatement(self, ctx:PascalParser.InheritedStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#constructorDeclaration.
    def enterConstructorDeclaration(self, ctx:PascalParser.ConstructorDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#constructorDeclaration.
    def exitConstructorDeclaration(self, ctx:PascalParser.ConstructorDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#destructorDeclaration.
    def enterDestructorDeclaration(self, ctx:PascalParser.DestructorDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#destructorDeclaration.
    def exitDestructorDeclaration(self, ctx:PascalParser.DestructorDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#arrayDeclaration.
    def enterArrayDeclaration(self, ctx:PascalParser.ArrayDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#arrayDeclaration.
    def exitArrayDeclaration(self, ctx:PascalParser.ArrayDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#arrayInitializer.
    def enterArrayInitializer(self, ctx:PascalParser.ArrayInitializerContext):
        pass

    # Exit a parse tree produced by PascalParser#arrayInitializer.
    def exitArrayInitializer(self, ctx:PascalParser.ArrayInitializerContext):
        pass


    # Enter a parse tree produced by PascalParser#arrayValueList.
    def enterArrayValueList(self, ctx:PascalParser.ArrayValueListContext):
        pass

    # Exit a parse tree produced by PascalParser#arrayValueList.
    def exitArrayValueList(self, ctx:PascalParser.ArrayValueListContext):
        pass


    # Enter a parse tree produced by PascalParser#arrayType.
    def enterArrayType(self, ctx:PascalParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by PascalParser#arrayType.
    def exitArrayType(self, ctx:PascalParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by PascalParser#arrayRange.
    def enterArrayRange(self, ctx:PascalParser.ArrayRangeContext):
        pass

    # Exit a parse tree produced by PascalParser#arrayRange.
    def exitArrayRange(self, ctx:PascalParser.ArrayRangeContext):
        pass


    # Enter a parse tree produced by PascalParser#arrayConstructor.
    def enterArrayConstructor(self, ctx:PascalParser.ArrayConstructorContext):
        pass

    # Exit a parse tree produced by PascalParser#arrayConstructor.
    def exitArrayConstructor(self, ctx:PascalParser.ArrayConstructorContext):
        pass


    # Enter a parse tree produced by PascalParser#arrayConstructorItems.
    def enterArrayConstructorItems(self, ctx:PascalParser.ArrayConstructorItemsContext):
        pass

    # Exit a parse tree produced by PascalParser#arrayConstructorItems.
    def exitArrayConstructorItems(self, ctx:PascalParser.ArrayConstructorItemsContext):
        pass


    # Enter a parse tree produced by PascalParser#typeName.
    def enterTypeName(self, ctx:PascalParser.TypeNameContext):
        pass

    # Exit a parse tree produced by PascalParser#typeName.
    def exitTypeName(self, ctx:PascalParser.TypeNameContext):
        pass


    # Enter a parse tree produced by PascalParser#simpleType.
    def enterSimpleType(self, ctx:PascalParser.SimpleTypeContext):
        pass

    # Exit a parse tree produced by PascalParser#simpleType.
    def exitSimpleType(self, ctx:PascalParser.SimpleTypeContext):
        pass


    # Enter a parse tree produced by PascalParser#signedInteger.
    def enterSignedInteger(self, ctx:PascalParser.SignedIntegerContext):
        pass

    # Exit a parse tree produced by PascalParser#signedInteger.
    def exitSignedInteger(self, ctx:PascalParser.SignedIntegerContext):
        pass


    # Enter a parse tree produced by PascalParser#subrangeType.
    def enterSubrangeType(self, ctx:PascalParser.SubrangeTypeContext):
        pass

    # Exit a parse tree produced by PascalParser#subrangeType.
    def exitSubrangeType(self, ctx:PascalParser.SubrangeTypeContext):
        pass


    # Enter a parse tree produced by PascalParser#enumDeclaration.
    def enterEnumDeclaration(self, ctx:PascalParser.EnumDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#enumDeclaration.
    def exitEnumDeclaration(self, ctx:PascalParser.EnumDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#enumValueList.
    def enterEnumValueList(self, ctx:PascalParser.EnumValueListContext):
        pass

    # Exit a parse tree produced by PascalParser#enumValueList.
    def exitEnumValueList(self, ctx:PascalParser.EnumValueListContext):
        pass


    # Enter a parse tree produced by PascalParser#enumValue.
    def enterEnumValue(self, ctx:PascalParser.EnumValueContext):
        pass

    # Exit a parse tree produced by PascalParser#enumValue.
    def exitEnumValue(self, ctx:PascalParser.EnumValueContext):
        pass


    # Enter a parse tree produced by PascalParser#recordDeclaration.
    def enterRecordDeclaration(self, ctx:PascalParser.RecordDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#recordDeclaration.
    def exitRecordDeclaration(self, ctx:PascalParser.RecordDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#recordFieldDeclaration.
    def enterRecordFieldDeclaration(self, ctx:PascalParser.RecordFieldDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#recordFieldDeclaration.
    def exitRecordFieldDeclaration(self, ctx:PascalParser.RecordFieldDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:PascalParser.FunctionDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:PascalParser.FunctionDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#procedureDeclaration.
    def enterProcedureDeclaration(self, ctx:PascalParser.ProcedureDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#procedureDeclaration.
    def exitProcedureDeclaration(self, ctx:PascalParser.ProcedureDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#formalParamList.
    def enterFormalParamList(self, ctx:PascalParser.FormalParamListContext):
        pass

    # Exit a parse tree produced by PascalParser#formalParamList.
    def exitFormalParamList(self, ctx:PascalParser.FormalParamListContext):
        pass


    # Enter a parse tree produced by PascalParser#formalParam.
    def enterFormalParam(self, ctx:PascalParser.FormalParamContext):
        pass

    # Exit a parse tree produced by PascalParser#formalParam.
    def exitFormalParam(self, ctx:PascalParser.FormalParamContext):
        pass


    # Enter a parse tree produced by PascalParser#paramModifier.
    def enterParamModifier(self, ctx:PascalParser.ParamModifierContext):
        pass

    # Exit a parse tree produced by PascalParser#paramModifier.
    def exitParamModifier(self, ctx:PascalParser.ParamModifierContext):
        pass


    # Enter a parse tree produced by PascalParser#paramType.
    def enterParamType(self, ctx:PascalParser.ParamTypeContext):
        pass

    # Exit a parse tree produced by PascalParser#paramType.
    def exitParamType(self, ctx:PascalParser.ParamTypeContext):
        pass


    # Enter a parse tree produced by PascalParser#openArrayType.
    def enterOpenArrayType(self, ctx:PascalParser.OpenArrayTypeContext):
        pass

    # Exit a parse tree produced by PascalParser#openArrayType.
    def exitOpenArrayType(self, ctx:PascalParser.OpenArrayTypeContext):
        pass


    # Enter a parse tree produced by PascalParser#declaration.
    def enterDeclaration(self, ctx:PascalParser.DeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#declaration.
    def exitDeclaration(self, ctx:PascalParser.DeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#builtinDiskFunctionName.
    def enterBuiltinDiskFunctionName(self, ctx:PascalParser.BuiltinDiskFunctionNameContext):
        pass

    # Exit a parse tree produced by PascalParser#builtinDiskFunctionName.
    def exitBuiltinDiskFunctionName(self, ctx:PascalParser.BuiltinDiskFunctionNameContext):
        pass


    # Enter a parse tree produced by PascalParser#functionName.
    def enterFunctionName(self, ctx:PascalParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by PascalParser#functionName.
    def exitFunctionName(self, ctx:PascalParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by PascalParser#functionCallExpr.
    def enterFunctionCallExpr(self, ctx:PascalParser.FunctionCallExprContext):
        pass

    # Exit a parse tree produced by PascalParser#functionCallExpr.
    def exitFunctionCallExpr(self, ctx:PascalParser.FunctionCallExprContext):
        pass


    # Enter a parse tree produced by PascalParser#procedureCallStatement.
    def enterProcedureCallStatement(self, ctx:PascalParser.ProcedureCallStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#procedureCallStatement.
    def exitProcedureCallStatement(self, ctx:PascalParser.ProcedureCallStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#actualParamList.
    def enterActualParamList(self, ctx:PascalParser.ActualParamListContext):
        pass

    # Exit a parse tree produced by PascalParser#actualParamList.
    def exitActualParamList(self, ctx:PascalParser.ActualParamListContext):
        pass


    # Enter a parse tree produced by PascalParser#actualParam.
    def enterActualParam(self, ctx:PascalParser.ActualParamContext):
        pass

    # Exit a parse tree produced by PascalParser#actualParam.
    def exitActualParam(self, ctx:PascalParser.ActualParamContext):
        pass


    # Enter a parse tree produced by PascalParser#varSection.
    def enterVarSection(self, ctx:PascalParser.VarSectionContext):
        pass

    # Exit a parse tree produced by PascalParser#varSection.
    def exitVarSection(self, ctx:PascalParser.VarSectionContext):
        pass


    # Enter a parse tree produced by PascalParser#varDeclaration.
    def enterVarDeclaration(self, ctx:PascalParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#varDeclaration.
    def exitVarDeclaration(self, ctx:PascalParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#varType.
    def enterVarType(self, ctx:PascalParser.VarTypeContext):
        pass

    # Exit a parse tree produced by PascalParser#varType.
    def exitVarType(self, ctx:PascalParser.VarTypeContext):
        pass


    # Enter a parse tree produced by PascalParser#identList.
    def enterIdentList(self, ctx:PascalParser.IdentListContext):
        pass

    # Exit a parse tree produced by PascalParser#identList.
    def exitIdentList(self, ctx:PascalParser.IdentListContext):
        pass


    # Enter a parse tree produced by PascalParser#block.
    def enterBlock(self, ctx:PascalParser.BlockContext):
        pass

    # Exit a parse tree produced by PascalParser#block.
    def exitBlock(self, ctx:PascalParser.BlockContext):
        pass


    # Enter a parse tree produced by PascalParser#localDeclaration.
    def enterLocalDeclaration(self, ctx:PascalParser.LocalDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#localDeclaration.
    def exitLocalDeclaration(self, ctx:PascalParser.LocalDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#statementList.
    def enterStatementList(self, ctx:PascalParser.StatementListContext):
        pass

    # Exit a parse tree produced by PascalParser#statementList.
    def exitStatementList(self, ctx:PascalParser.StatementListContext):
        pass


    # Enter a parse tree produced by PascalParser#statement.
    def enterStatement(self, ctx:PascalParser.StatementContext):
        pass

    # Exit a parse tree produced by PascalParser#statement.
    def exitStatement(self, ctx:PascalParser.StatementContext):
        pass


    # Enter a parse tree produced by PascalParser#incstatement.
    def enterIncstatement(self, ctx:PascalParser.IncstatementContext):
        pass

    # Exit a parse tree produced by PascalParser#incstatement.
    def exitIncstatement(self, ctx:PascalParser.IncstatementContext):
        pass


    # Enter a parse tree produced by PascalParser#decstatement.
    def enterDecstatement(self, ctx:PascalParser.DecstatementContext):
        pass

    # Exit a parse tree produced by PascalParser#decstatement.
    def exitDecstatement(self, ctx:PascalParser.DecstatementContext):
        pass


    # Enter a parse tree produced by PascalParser#caseStatement.
    def enterCaseStatement(self, ctx:PascalParser.CaseStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#caseStatement.
    def exitCaseStatement(self, ctx:PascalParser.CaseStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#caseItem.
    def enterCaseItem(self, ctx:PascalParser.CaseItemContext):
        pass

    # Exit a parse tree produced by PascalParser#caseItem.
    def exitCaseItem(self, ctx:PascalParser.CaseItemContext):
        pass


    # Enter a parse tree produced by PascalParser#caseLabelList.
    def enterCaseLabelList(self, ctx:PascalParser.CaseLabelListContext):
        pass

    # Exit a parse tree produced by PascalParser#caseLabelList.
    def exitCaseLabelList(self, ctx:PascalParser.CaseLabelListContext):
        pass


    # Enter a parse tree produced by PascalParser#caseLabel.
    def enterCaseLabel(self, ctx:PascalParser.CaseLabelContext):
        pass

    # Exit a parse tree produced by PascalParser#caseLabel.
    def exitCaseLabel(self, ctx:PascalParser.CaseLabelContext):
        pass


    # Enter a parse tree produced by PascalParser#caseElse.
    def enterCaseElse(self, ctx:PascalParser.CaseElseContext):
        pass

    # Exit a parse tree produced by PascalParser#caseElse.
    def exitCaseElse(self, ctx:PascalParser.CaseElseContext):
        pass


    # Enter a parse tree produced by PascalParser#breakStatement.
    def enterBreakStatement(self, ctx:PascalParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#breakStatement.
    def exitBreakStatement(self, ctx:PascalParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#continueStatement.
    def enterContinueStatement(self, ctx:PascalParser.ContinueStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#continueStatement.
    def exitContinueStatement(self, ctx:PascalParser.ContinueStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#tryStatement.
    def enterTryStatement(self, ctx:PascalParser.TryStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#tryStatement.
    def exitTryStatement(self, ctx:PascalParser.TryStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#exitStatement.
    def enterExitStatement(self, ctx:PascalParser.ExitStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#exitStatement.
    def exitExitStatement(self, ctx:PascalParser.ExitStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#forStatement.
    def enterForStatement(self, ctx:PascalParser.ForStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#forStatement.
    def exitForStatement(self, ctx:PascalParser.ForStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#repeatStatement.
    def enterRepeatStatement(self, ctx:PascalParser.RepeatStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#repeatStatement.
    def exitRepeatStatement(self, ctx:PascalParser.RepeatStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#argumentList.
    def enterArgumentList(self, ctx:PascalParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by PascalParser#argumentList.
    def exitArgumentList(self, ctx:PascalParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by PascalParser#whileStatement.
    def enterWhileStatement(self, ctx:PascalParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#whileStatement.
    def exitWhileStatement(self, ctx:PascalParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#ifStatement.
    def enterIfStatement(self, ctx:PascalParser.IfStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#ifStatement.
    def exitIfStatement(self, ctx:PascalParser.IfStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#condition.
    def enterCondition(self, ctx:PascalParser.ConditionContext):
        pass

    # Exit a parse tree produced by PascalParser#condition.
    def exitCondition(self, ctx:PascalParser.ConditionContext):
        pass


    # Enter a parse tree produced by PascalParser#compareOp.
    def enterCompareOp(self, ctx:PascalParser.CompareOpContext):
        pass

    # Exit a parse tree produced by PascalParser#compareOp.
    def exitCompareOp(self, ctx:PascalParser.CompareOpContext):
        pass


    # Enter a parse tree produced by PascalParser#compoundStatement.
    def enterCompoundStatement(self, ctx:PascalParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#compoundStatement.
    def exitCompoundStatement(self, ctx:PascalParser.CompoundStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#assignment.
    def enterAssignment(self, ctx:PascalParser.AssignmentContext):
        pass

    # Exit a parse tree produced by PascalParser#assignment.
    def exitAssignment(self, ctx:PascalParser.AssignmentContext):
        pass


    # Enter a parse tree produced by PascalParser#variableRef.
    def enterVariableRef(self, ctx:PascalParser.VariableRefContext):
        pass

    # Exit a parse tree produced by PascalParser#variableRef.
    def exitVariableRef(self, ctx:PascalParser.VariableRefContext):
        pass


    # Enter a parse tree produced by PascalParser#variableSuffix.
    def enterVariableSuffix(self, ctx:PascalParser.VariableSuffixContext):
        pass

    # Exit a parse tree produced by PascalParser#variableSuffix.
    def exitVariableSuffix(self, ctx:PascalParser.VariableSuffixContext):
        pass


    # Enter a parse tree produced by PascalParser#pointerDereference.
    def enterPointerDereference(self, ctx:PascalParser.PointerDereferenceContext):
        pass

    # Exit a parse tree produced by PascalParser#pointerDereference.
    def exitPointerDereference(self, ctx:PascalParser.PointerDereferenceContext):
        pass


    # Enter a parse tree produced by PascalParser#fieldAccess.
    def enterFieldAccess(self, ctx:PascalParser.FieldAccessContext):
        pass

    # Exit a parse tree produced by PascalParser#fieldAccess.
    def exitFieldAccess(self, ctx:PascalParser.FieldAccessContext):
        pass


    # Enter a parse tree produced by PascalParser#arrayIndex.
    def enterArrayIndex(self, ctx:PascalParser.ArrayIndexContext):
        pass

    # Exit a parse tree produced by PascalParser#arrayIndex.
    def exitArrayIndex(self, ctx:PascalParser.ArrayIndexContext):
        pass


    # Enter a parse tree produced by PascalParser#exprList.
    def enterExprList(self, ctx:PascalParser.ExprListContext):
        pass

    # Exit a parse tree produced by PascalParser#exprList.
    def exitExprList(self, ctx:PascalParser.ExprListContext):
        pass


    # Enter a parse tree produced by PascalParser#expr.
    def enterExpr(self, ctx:PascalParser.ExprContext):
        pass

    # Exit a parse tree produced by PascalParser#expr.
    def exitExpr(self, ctx:PascalParser.ExprContext):
        pass


    # Enter a parse tree produced by PascalParser#boolOrExpr.
    def enterBoolOrExpr(self, ctx:PascalParser.BoolOrExprContext):
        pass

    # Exit a parse tree produced by PascalParser#boolOrExpr.
    def exitBoolOrExpr(self, ctx:PascalParser.BoolOrExprContext):
        pass


    # Enter a parse tree produced by PascalParser#boolXorExpr.
    def enterBoolXorExpr(self, ctx:PascalParser.BoolXorExprContext):
        pass

    # Exit a parse tree produced by PascalParser#boolXorExpr.
    def exitBoolXorExpr(self, ctx:PascalParser.BoolXorExprContext):
        pass


    # Enter a parse tree produced by PascalParser#boolAndExpr.
    def enterBoolAndExpr(self, ctx:PascalParser.BoolAndExprContext):
        pass

    # Exit a parse tree produced by PascalParser#boolAndExpr.
    def exitBoolAndExpr(self, ctx:PascalParser.BoolAndExprContext):
        pass


    # Enter a parse tree produced by PascalParser#compareExpr.
    def enterCompareExpr(self, ctx:PascalParser.CompareExprContext):
        pass

    # Exit a parse tree produced by PascalParser#compareExpr.
    def exitCompareExpr(self, ctx:PascalParser.CompareExprContext):
        pass


    # Enter a parse tree produced by PascalParser#addExpr.
    def enterAddExpr(self, ctx:PascalParser.AddExprContext):
        pass

    # Exit a parse tree produced by PascalParser#addExpr.
    def exitAddExpr(self, ctx:PascalParser.AddExprContext):
        pass


    # Enter a parse tree produced by PascalParser#shiftExpr.
    def enterShiftExpr(self, ctx:PascalParser.ShiftExprContext):
        pass

    # Exit a parse tree produced by PascalParser#shiftExpr.
    def exitShiftExpr(self, ctx:PascalParser.ShiftExprContext):
        pass


    # Enter a parse tree produced by PascalParser#term.
    def enterTerm(self, ctx:PascalParser.TermContext):
        pass

    # Exit a parse tree produced by PascalParser#term.
    def exitTerm(self, ctx:PascalParser.TermContext):
        pass


    # Enter a parse tree produced by PascalParser#factor.
    def enterFactor(self, ctx:PascalParser.FactorContext):
        pass

    # Exit a parse tree produced by PascalParser#factor.
    def exitFactor(self, ctx:PascalParser.FactorContext):
        pass


    # Enter a parse tree produced by PascalParser#writeLnStatement.
    def enterWriteLnStatement(self, ctx:PascalParser.WriteLnStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#writeLnStatement.
    def exitWriteLnStatement(self, ctx:PascalParser.WriteLnStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#writeArgList.
    def enterWriteArgList(self, ctx:PascalParser.WriteArgListContext):
        pass

    # Exit a parse tree produced by PascalParser#writeArgList.
    def exitWriteArgList(self, ctx:PascalParser.WriteArgListContext):
        pass


    # Enter a parse tree produced by PascalParser#writeArg.
    def enterWriteArg(self, ctx:PascalParser.WriteArgContext):
        pass

    # Exit a parse tree produced by PascalParser#writeArg.
    def exitWriteArg(self, ctx:PascalParser.WriteArgContext):
        pass



del PascalParser