# Generated from gramm/pascal/PasDocParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PasDocParser import PasDocParser
else:
    from PasDocParser import PasDocParser

# This class defines a complete generic visitor for a parse tree produced by PasDocParser.

class PasDocParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PasDocParser#unitFile.
    def visitUnitFile(self, ctx:PasDocParser.UnitFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#unitHeader.
    def visitUnitHeader(self, ctx:PasDocParser.UnitHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#unitSection.
    def visitUnitSection(self, ctx:PasDocParser.UnitSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#declaration.
    def visitDeclaration(self, ctx:PasDocParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#typeSection.
    def visitTypeSection(self, ctx:PasDocParser.TypeSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:PasDocParser.TypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#classDeclaration.
    def visitClassDeclaration(self, ctx:PasDocParser.ClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#recordDeclaration.
    def visitRecordDeclaration(self, ctx:PasDocParser.RecordDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#classType.
    def visitClassType(self, ctx:PasDocParser.ClassTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#recordType.
    def visitRecordType(self, ctx:PasDocParser.RecordTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#classInheritance.
    def visitClassInheritance(self, ctx:PasDocParser.ClassInheritanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#classBody.
    def visitClassBody(self, ctx:PasDocParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#classMember.
    def visitClassMember(self, ctx:PasDocParser.ClassMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#visibilitySection.
    def visitVisibilitySection(self, ctx:PasDocParser.VisibilitySectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#visibility.
    def visitVisibility(self, ctx:PasDocParser.VisibilityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#methodDeclaration.
    def visitMethodDeclaration(self, ctx:PasDocParser.MethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#methodDirectiveList.
    def visitMethodDirectiveList(self, ctx:PasDocParser.MethodDirectiveListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#methodKind.
    def visitMethodKind(self, ctx:PasDocParser.MethodKindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#parameterList.
    def visitParameterList(self, ctx:PasDocParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#parameterDecl.
    def visitParameterDecl(self, ctx:PasDocParser.ParameterDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#parameterItem.
    def visitParameterItem(self, ctx:PasDocParser.ParameterItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#returnType.
    def visitReturnType(self, ctx:PasDocParser.ReturnTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#methodDirective.
    def visitMethodDirective(self, ctx:PasDocParser.MethodDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#propertyDeclaration.
    def visitPropertyDeclaration(self, ctx:PasDocParser.PropertyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#propertyType.
    def visitPropertyType(self, ctx:PasDocParser.PropertyTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#propertyAccessor.
    def visitPropertyAccessor(self, ctx:PasDocParser.PropertyAccessorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#fieldDeclaration.
    def visitFieldDeclaration(self, ctx:PasDocParser.FieldDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#typeName.
    def visitTypeName(self, ctx:PasDocParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PasDocParser#otherToken.
    def visitOtherToken(self, ctx:PasDocParser.OtherTokenContext):
        return self.visitChildren(ctx)



del PasDocParser