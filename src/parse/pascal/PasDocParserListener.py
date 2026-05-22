# Generated from gramm/pascal/PasDocParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PasDocParser import PasDocParser
else:
    from PasDocParser import PasDocParser

# This class defines a complete listener for a parse tree produced by PasDocParser.
class PasDocParserListener(ParseTreeListener):

    # Enter a parse tree produced by PasDocParser#unitFile.
    def enterUnitFile(self, ctx:PasDocParser.UnitFileContext):
        pass

    # Exit a parse tree produced by PasDocParser#unitFile.
    def exitUnitFile(self, ctx:PasDocParser.UnitFileContext):
        pass


    # Enter a parse tree produced by PasDocParser#programHeader.
    def enterProgramHeader(self, ctx:PasDocParser.ProgramHeaderContext):
        pass

    # Exit a parse tree produced by PasDocParser#programHeader.
    def exitProgramHeader(self, ctx:PasDocParser.ProgramHeaderContext):
        pass


    # Enter a parse tree produced by PasDocParser#unitHeader.
    def enterUnitHeader(self, ctx:PasDocParser.UnitHeaderContext):
        pass

    # Exit a parse tree produced by PasDocParser#unitHeader.
    def exitUnitHeader(self, ctx:PasDocParser.UnitHeaderContext):
        pass


    # Enter a parse tree produced by PasDocParser#unitSection.
    def enterUnitSection(self, ctx:PasDocParser.UnitSectionContext):
        pass

    # Exit a parse tree produced by PasDocParser#unitSection.
    def exitUnitSection(self, ctx:PasDocParser.UnitSectionContext):
        pass


    # Enter a parse tree produced by PasDocParser#declaration.
    def enterDeclaration(self, ctx:PasDocParser.DeclarationContext):
        pass

    # Exit a parse tree produced by PasDocParser#declaration.
    def exitDeclaration(self, ctx:PasDocParser.DeclarationContext):
        pass


    # Enter a parse tree produced by PasDocParser#varSection.
    def enterVarSection(self, ctx:PasDocParser.VarSectionContext):
        pass

    # Exit a parse tree produced by PasDocParser#varSection.
    def exitVarSection(self, ctx:PasDocParser.VarSectionContext):
        pass


    # Enter a parse tree produced by PasDocParser#constSection.
    def enterConstSection(self, ctx:PasDocParser.ConstSectionContext):
        pass

    # Exit a parse tree produced by PasDocParser#constSection.
    def exitConstSection(self, ctx:PasDocParser.ConstSectionContext):
        pass


    # Enter a parse tree produced by PasDocParser#constDeclaration.
    def enterConstDeclaration(self, ctx:PasDocParser.ConstDeclarationContext):
        pass

    # Exit a parse tree produced by PasDocParser#constDeclaration.
    def exitConstDeclaration(self, ctx:PasDocParser.ConstDeclarationContext):
        pass


    # Enter a parse tree produced by PasDocParser#constItem.
    def enterConstItem(self, ctx:PasDocParser.ConstItemContext):
        pass

    # Exit a parse tree produced by PasDocParser#constItem.
    def exitConstItem(self, ctx:PasDocParser.ConstItemContext):
        pass


    # Enter a parse tree produced by PasDocParser#constValue.
    def enterConstValue(self, ctx:PasDocParser.ConstValueContext):
        pass

    # Exit a parse tree produced by PasDocParser#constValue.
    def exitConstValue(self, ctx:PasDocParser.ConstValueContext):
        pass


    # Enter a parse tree produced by PasDocParser#sign.
    def enterSign(self, ctx:PasDocParser.SignContext):
        pass

    # Exit a parse tree produced by PasDocParser#sign.
    def exitSign(self, ctx:PasDocParser.SignContext):
        pass


    # Enter a parse tree produced by PasDocParser#docComment.
    def enterDocComment(self, ctx:PasDocParser.DocCommentContext):
        pass

    # Exit a parse tree produced by PasDocParser#docComment.
    def exitDocComment(self, ctx:PasDocParser.DocCommentContext):
        pass


    # Enter a parse tree produced by PasDocParser#typeSection.
    def enterTypeSection(self, ctx:PasDocParser.TypeSectionContext):
        pass

    # Exit a parse tree produced by PasDocParser#typeSection.
    def exitTypeSection(self, ctx:PasDocParser.TypeSectionContext):
        pass


    # Enter a parse tree produced by PasDocParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:PasDocParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by PasDocParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:PasDocParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by PasDocParser#unknownTypeDeclaration.
    def enterUnknownTypeDeclaration(self, ctx:PasDocParser.UnknownTypeDeclarationContext):
        pass

    # Exit a parse tree produced by PasDocParser#unknownTypeDeclaration.
    def exitUnknownTypeDeclaration(self, ctx:PasDocParser.UnknownTypeDeclarationContext):
        pass


    # Enter a parse tree produced by PasDocParser#classDeclaration.
    def enterClassDeclaration(self, ctx:PasDocParser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by PasDocParser#classDeclaration.
    def exitClassDeclaration(self, ctx:PasDocParser.ClassDeclarationContext):
        pass


    # Enter a parse tree produced by PasDocParser#classType.
    def enterClassType(self, ctx:PasDocParser.ClassTypeContext):
        pass

    # Exit a parse tree produced by PasDocParser#classType.
    def exitClassType(self, ctx:PasDocParser.ClassTypeContext):
        pass


    # Enter a parse tree produced by PasDocParser#classInheritance.
    def enterClassInheritance(self, ctx:PasDocParser.ClassInheritanceContext):
        pass

    # Exit a parse tree produced by PasDocParser#classInheritance.
    def exitClassInheritance(self, ctx:PasDocParser.ClassInheritanceContext):
        pass


    # Enter a parse tree produced by PasDocParser#classBody.
    def enterClassBody(self, ctx:PasDocParser.ClassBodyContext):
        pass

    # Exit a parse tree produced by PasDocParser#classBody.
    def exitClassBody(self, ctx:PasDocParser.ClassBodyContext):
        pass


    # Enter a parse tree produced by PasDocParser#classMember.
    def enterClassMember(self, ctx:PasDocParser.ClassMemberContext):
        pass

    # Exit a parse tree produced by PasDocParser#classMember.
    def exitClassMember(self, ctx:PasDocParser.ClassMemberContext):
        pass


    # Enter a parse tree produced by PasDocParser#recordDeclaration.
    def enterRecordDeclaration(self, ctx:PasDocParser.RecordDeclarationContext):
        pass

    # Exit a parse tree produced by PasDocParser#recordDeclaration.
    def exitRecordDeclaration(self, ctx:PasDocParser.RecordDeclarationContext):
        pass


    # Enter a parse tree produced by PasDocParser#recordType.
    def enterRecordType(self, ctx:PasDocParser.RecordTypeContext):
        pass

    # Exit a parse tree produced by PasDocParser#recordType.
    def exitRecordType(self, ctx:PasDocParser.RecordTypeContext):
        pass


    # Enter a parse tree produced by PasDocParser#recordBody.
    def enterRecordBody(self, ctx:PasDocParser.RecordBodyContext):
        pass

    # Exit a parse tree produced by PasDocParser#recordBody.
    def exitRecordBody(self, ctx:PasDocParser.RecordBodyContext):
        pass


    # Enter a parse tree produced by PasDocParser#recordMember.
    def enterRecordMember(self, ctx:PasDocParser.RecordMemberContext):
        pass

    # Exit a parse tree produced by PasDocParser#recordMember.
    def exitRecordMember(self, ctx:PasDocParser.RecordMemberContext):
        pass


    # Enter a parse tree produced by PasDocParser#arrayDeclaration.
    def enterArrayDeclaration(self, ctx:PasDocParser.ArrayDeclarationContext):
        pass

    # Exit a parse tree produced by PasDocParser#arrayDeclaration.
    def exitArrayDeclaration(self, ctx:PasDocParser.ArrayDeclarationContext):
        pass


    # Enter a parse tree produced by PasDocParser#arrayType.
    def enterArrayType(self, ctx:PasDocParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by PasDocParser#arrayType.
    def exitArrayType(self, ctx:PasDocParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by PasDocParser#arrayIndex.
    def enterArrayIndex(self, ctx:PasDocParser.ArrayIndexContext):
        pass

    # Exit a parse tree produced by PasDocParser#arrayIndex.
    def exitArrayIndex(self, ctx:PasDocParser.ArrayIndexContext):
        pass


    # Enter a parse tree produced by PasDocParser#setDeclaration.
    def enterSetDeclaration(self, ctx:PasDocParser.SetDeclarationContext):
        pass

    # Exit a parse tree produced by PasDocParser#setDeclaration.
    def exitSetDeclaration(self, ctx:PasDocParser.SetDeclarationContext):
        pass


    # Enter a parse tree produced by PasDocParser#setType.
    def enterSetType(self, ctx:PasDocParser.SetTypeContext):
        pass

    # Exit a parse tree produced by PasDocParser#setType.
    def exitSetType(self, ctx:PasDocParser.SetTypeContext):
        pass


    # Enter a parse tree produced by PasDocParser#visibilitySection.
    def enterVisibilitySection(self, ctx:PasDocParser.VisibilitySectionContext):
        pass

    # Exit a parse tree produced by PasDocParser#visibilitySection.
    def exitVisibilitySection(self, ctx:PasDocParser.VisibilitySectionContext):
        pass


    # Enter a parse tree produced by PasDocParser#visibility.
    def enterVisibility(self, ctx:PasDocParser.VisibilityContext):
        pass

    # Exit a parse tree produced by PasDocParser#visibility.
    def exitVisibility(self, ctx:PasDocParser.VisibilityContext):
        pass


    # Enter a parse tree produced by PasDocParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:PasDocParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by PasDocParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:PasDocParser.MethodDeclarationContext):
        pass


    # Enter a parse tree produced by PasDocParser#methodDirectiveList.
    def enterMethodDirectiveList(self, ctx:PasDocParser.MethodDirectiveListContext):
        pass

    # Exit a parse tree produced by PasDocParser#methodDirectiveList.
    def exitMethodDirectiveList(self, ctx:PasDocParser.MethodDirectiveListContext):
        pass


    # Enter a parse tree produced by PasDocParser#methodKind.
    def enterMethodKind(self, ctx:PasDocParser.MethodKindContext):
        pass

    # Exit a parse tree produced by PasDocParser#methodKind.
    def exitMethodKind(self, ctx:PasDocParser.MethodKindContext):
        pass


    # Enter a parse tree produced by PasDocParser#parameterList.
    def enterParameterList(self, ctx:PasDocParser.ParameterListContext):
        pass

    # Exit a parse tree produced by PasDocParser#parameterList.
    def exitParameterList(self, ctx:PasDocParser.ParameterListContext):
        pass


    # Enter a parse tree produced by PasDocParser#parameterDecl.
    def enterParameterDecl(self, ctx:PasDocParser.ParameterDeclContext):
        pass

    # Exit a parse tree produced by PasDocParser#parameterDecl.
    def exitParameterDecl(self, ctx:PasDocParser.ParameterDeclContext):
        pass


    # Enter a parse tree produced by PasDocParser#parameterItem.
    def enterParameterItem(self, ctx:PasDocParser.ParameterItemContext):
        pass

    # Exit a parse tree produced by PasDocParser#parameterItem.
    def exitParameterItem(self, ctx:PasDocParser.ParameterItemContext):
        pass


    # Enter a parse tree produced by PasDocParser#parameterModifier.
    def enterParameterModifier(self, ctx:PasDocParser.ParameterModifierContext):
        pass

    # Exit a parse tree produced by PasDocParser#parameterModifier.
    def exitParameterModifier(self, ctx:PasDocParser.ParameterModifierContext):
        pass


    # Enter a parse tree produced by PasDocParser#returnType.
    def enterReturnType(self, ctx:PasDocParser.ReturnTypeContext):
        pass

    # Exit a parse tree produced by PasDocParser#returnType.
    def exitReturnType(self, ctx:PasDocParser.ReturnTypeContext):
        pass


    # Enter a parse tree produced by PasDocParser#methodDirective.
    def enterMethodDirective(self, ctx:PasDocParser.MethodDirectiveContext):
        pass

    # Exit a parse tree produced by PasDocParser#methodDirective.
    def exitMethodDirective(self, ctx:PasDocParser.MethodDirectiveContext):
        pass


    # Enter a parse tree produced by PasDocParser#propertyDeclaration.
    def enterPropertyDeclaration(self, ctx:PasDocParser.PropertyDeclarationContext):
        pass

    # Exit a parse tree produced by PasDocParser#propertyDeclaration.
    def exitPropertyDeclaration(self, ctx:PasDocParser.PropertyDeclarationContext):
        pass


    # Enter a parse tree produced by PasDocParser#propertyType.
    def enterPropertyType(self, ctx:PasDocParser.PropertyTypeContext):
        pass

    # Exit a parse tree produced by PasDocParser#propertyType.
    def exitPropertyType(self, ctx:PasDocParser.PropertyTypeContext):
        pass


    # Enter a parse tree produced by PasDocParser#propertyAccessor.
    def enterPropertyAccessor(self, ctx:PasDocParser.PropertyAccessorContext):
        pass

    # Exit a parse tree produced by PasDocParser#propertyAccessor.
    def exitPropertyAccessor(self, ctx:PasDocParser.PropertyAccessorContext):
        pass


    # Enter a parse tree produced by PasDocParser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx:PasDocParser.FieldDeclarationContext):
        pass

    # Exit a parse tree produced by PasDocParser#fieldDeclaration.
    def exitFieldDeclaration(self, ctx:PasDocParser.FieldDeclarationContext):
        pass


    # Enter a parse tree produced by PasDocParser#typeName.
    def enterTypeName(self, ctx:PasDocParser.TypeNameContext):
        pass

    # Exit a parse tree produced by PasDocParser#typeName.
    def exitTypeName(self, ctx:PasDocParser.TypeNameContext):
        pass


    # Enter a parse tree produced by PasDocParser#otherToken.
    def enterOtherToken(self, ctx:PasDocParser.OtherTokenContext):
        pass

    # Exit a parse tree produced by PasDocParser#otherToken.
    def exitOtherToken(self, ctx:PasDocParser.OtherTokenContext):
        pass



del PasDocParser