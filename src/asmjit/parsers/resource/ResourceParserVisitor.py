# Generated from compiler/grammar/ResourceParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ResourceParser import ResourceParser
else:
    from ResourceParser import ResourceParser

# This class defines a complete generic visitor for a parse tree produced by ResourceParser.

class ResourceParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ResourceParser#resourceScript.
    def visitResourceScript(self, ctx:ResourceParser.ResourceScriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#resourceStatement.
    def visitResourceStatement(self, ctx:ResourceParser.ResourceStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#languageStatement.
    def visitLanguageStatement(self, ctx:ResourceParser.LanguageStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#characteristicsStatement.
    def visitCharacteristicsStatement(self, ctx:ResourceParser.CharacteristicsStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#versionStatement.
    def visitVersionStatement(self, ctx:ResourceParser.VersionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#resourceId.
    def visitResourceId(self, ctx:ResourceParser.ResourceIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#resourceType.
    def visitResourceType(self, ctx:ResourceParser.ResourceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#resourceOptions.
    def visitResourceOptions(self, ctx:ResourceParser.ResourceOptionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#fileResource.
    def visitFileResource(self, ctx:ResourceParser.FileResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#fileResourceKind.
    def visitFileResourceKind(self, ctx:ResourceParser.FileResourceKindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#fileResourceType.
    def visitFileResourceType(self, ctx:ResourceParser.FileResourceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#rawResource.
    def visitRawResource(self, ctx:ResourceParser.RawResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#rawResourceType.
    def visitRawResourceType(self, ctx:ResourceParser.RawResourceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#rawDataBlock.
    def visitRawDataBlock(self, ctx:ResourceParser.RawDataBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#rawDataItemList.
    def visitRawDataItemList(self, ctx:ResourceParser.RawDataItemListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#rawDataItem.
    def visitRawDataItem(self, ctx:ResourceParser.RawDataItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#stringTableResource.
    def visitStringTableResource(self, ctx:ResourceParser.StringTableResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#stringEntry.
    def visitStringEntry(self, ctx:ResourceParser.StringEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#versionInfoResource.
    def visitVersionInfoResource(self, ctx:ResourceParser.VersionInfoResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#fixedVersionLine.
    def visitFixedVersionLine(self, ctx:ResourceParser.FixedVersionLineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#quadExpression.
    def visitQuadExpression(self, ctx:ResourceParser.QuadExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#versionElement.
    def visitVersionElement(self, ctx:ResourceParser.VersionElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#versionBlock.
    def visitVersionBlock(self, ctx:ResourceParser.VersionBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#versionValue.
    def visitVersionValue(self, ctx:ResourceParser.VersionValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#versionValueItem.
    def visitVersionValueItem(self, ctx:ResourceParser.VersionValueItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#menuResource.
    def visitMenuResource(self, ctx:ResourceParser.MenuResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#menuItem.
    def visitMenuItem(self, ctx:ResourceParser.MenuItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#menuFlags.
    def visitMenuFlags(self, ctx:ResourceParser.MenuFlagsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#acceleratorsResource.
    def visitAcceleratorsResource(self, ctx:ResourceParser.AcceleratorsResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#acceleratorEntry.
    def visitAcceleratorEntry(self, ctx:ResourceParser.AcceleratorEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#acceleratorKey.
    def visitAcceleratorKey(self, ctx:ResourceParser.AcceleratorKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#acceleratorFlags.
    def visitAcceleratorFlags(self, ctx:ResourceParser.AcceleratorFlagsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#dialogResource.
    def visitDialogResource(self, ctx:ResourceParser.DialogResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#dialogKind.
    def visitDialogKind(self, ctx:ResourceParser.DialogKindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#dialogHeaderLine.
    def visitDialogHeaderLine(self, ctx:ResourceParser.DialogHeaderLineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#dialogControl.
    def visitDialogControl(self, ctx:ResourceParser.DialogControlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#controlWithText.
    def visitControlWithText(self, ctx:ResourceParser.ControlWithTextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#controlWithoutText.
    def visitControlWithoutText(self, ctx:ResourceParser.ControlWithoutTextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#stringLiteral.
    def visitStringLiteral(self, ctx:ResourceParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#separator.
    def visitSeparator(self, ctx:ResourceParser.SeparatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#blockStart.
    def visitBlockStart(self, ctx:ResourceParser.BlockStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#blockEnd.
    def visitBlockEnd(self, ctx:ResourceParser.BlockEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#eol.
    def visitEol(self, ctx:ResourceParser.EolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#expression.
    def visitExpression(self, ctx:ResourceParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#bitOrExpression.
    def visitBitOrExpression(self, ctx:ResourceParser.BitOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#bitXorExpression.
    def visitBitXorExpression(self, ctx:ResourceParser.BitXorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#bitAndExpression.
    def visitBitAndExpression(self, ctx:ResourceParser.BitAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#shiftExpression.
    def visitShiftExpression(self, ctx:ResourceParser.ShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:ResourceParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:ResourceParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#unaryExpression.
    def visitUnaryExpression(self, ctx:ResourceParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ResourceParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:ResourceParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)



del ResourceParser