# Generated from compiler/grammar/ResourceParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ResourceParser import ResourceParser
else:
    from ResourceParser import ResourceParser

# This class defines a complete listener for a parse tree produced by ResourceParser.
class ResourceParserListener(ParseTreeListener):

    # Enter a parse tree produced by ResourceParser#resourceScript.
    def enterResourceScript(self, ctx:ResourceParser.ResourceScriptContext):
        pass

    # Exit a parse tree produced by ResourceParser#resourceScript.
    def exitResourceScript(self, ctx:ResourceParser.ResourceScriptContext):
        pass


    # Enter a parse tree produced by ResourceParser#resourceStatement.
    def enterResourceStatement(self, ctx:ResourceParser.ResourceStatementContext):
        pass

    # Exit a parse tree produced by ResourceParser#resourceStatement.
    def exitResourceStatement(self, ctx:ResourceParser.ResourceStatementContext):
        pass


    # Enter a parse tree produced by ResourceParser#languageStatement.
    def enterLanguageStatement(self, ctx:ResourceParser.LanguageStatementContext):
        pass

    # Exit a parse tree produced by ResourceParser#languageStatement.
    def exitLanguageStatement(self, ctx:ResourceParser.LanguageStatementContext):
        pass


    # Enter a parse tree produced by ResourceParser#characteristicsStatement.
    def enterCharacteristicsStatement(self, ctx:ResourceParser.CharacteristicsStatementContext):
        pass

    # Exit a parse tree produced by ResourceParser#characteristicsStatement.
    def exitCharacteristicsStatement(self, ctx:ResourceParser.CharacteristicsStatementContext):
        pass


    # Enter a parse tree produced by ResourceParser#versionStatement.
    def enterVersionStatement(self, ctx:ResourceParser.VersionStatementContext):
        pass

    # Exit a parse tree produced by ResourceParser#versionStatement.
    def exitVersionStatement(self, ctx:ResourceParser.VersionStatementContext):
        pass


    # Enter a parse tree produced by ResourceParser#resourceId.
    def enterResourceId(self, ctx:ResourceParser.ResourceIdContext):
        pass

    # Exit a parse tree produced by ResourceParser#resourceId.
    def exitResourceId(self, ctx:ResourceParser.ResourceIdContext):
        pass


    # Enter a parse tree produced by ResourceParser#resourceType.
    def enterResourceType(self, ctx:ResourceParser.ResourceTypeContext):
        pass

    # Exit a parse tree produced by ResourceParser#resourceType.
    def exitResourceType(self, ctx:ResourceParser.ResourceTypeContext):
        pass


    # Enter a parse tree produced by ResourceParser#resourceOptions.
    def enterResourceOptions(self, ctx:ResourceParser.ResourceOptionsContext):
        pass

    # Exit a parse tree produced by ResourceParser#resourceOptions.
    def exitResourceOptions(self, ctx:ResourceParser.ResourceOptionsContext):
        pass


    # Enter a parse tree produced by ResourceParser#fileResource.
    def enterFileResource(self, ctx:ResourceParser.FileResourceContext):
        pass

    # Exit a parse tree produced by ResourceParser#fileResource.
    def exitFileResource(self, ctx:ResourceParser.FileResourceContext):
        pass


    # Enter a parse tree produced by ResourceParser#fileResourceKind.
    def enterFileResourceKind(self, ctx:ResourceParser.FileResourceKindContext):
        pass

    # Exit a parse tree produced by ResourceParser#fileResourceKind.
    def exitFileResourceKind(self, ctx:ResourceParser.FileResourceKindContext):
        pass


    # Enter a parse tree produced by ResourceParser#fileResourceType.
    def enterFileResourceType(self, ctx:ResourceParser.FileResourceTypeContext):
        pass

    # Exit a parse tree produced by ResourceParser#fileResourceType.
    def exitFileResourceType(self, ctx:ResourceParser.FileResourceTypeContext):
        pass


    # Enter a parse tree produced by ResourceParser#rawResource.
    def enterRawResource(self, ctx:ResourceParser.RawResourceContext):
        pass

    # Exit a parse tree produced by ResourceParser#rawResource.
    def exitRawResource(self, ctx:ResourceParser.RawResourceContext):
        pass


    # Enter a parse tree produced by ResourceParser#rawResourceType.
    def enterRawResourceType(self, ctx:ResourceParser.RawResourceTypeContext):
        pass

    # Exit a parse tree produced by ResourceParser#rawResourceType.
    def exitRawResourceType(self, ctx:ResourceParser.RawResourceTypeContext):
        pass


    # Enter a parse tree produced by ResourceParser#rawDataBlock.
    def enterRawDataBlock(self, ctx:ResourceParser.RawDataBlockContext):
        pass

    # Exit a parse tree produced by ResourceParser#rawDataBlock.
    def exitRawDataBlock(self, ctx:ResourceParser.RawDataBlockContext):
        pass


    # Enter a parse tree produced by ResourceParser#rawDataItemList.
    def enterRawDataItemList(self, ctx:ResourceParser.RawDataItemListContext):
        pass

    # Exit a parse tree produced by ResourceParser#rawDataItemList.
    def exitRawDataItemList(self, ctx:ResourceParser.RawDataItemListContext):
        pass


    # Enter a parse tree produced by ResourceParser#rawDataItem.
    def enterRawDataItem(self, ctx:ResourceParser.RawDataItemContext):
        pass

    # Exit a parse tree produced by ResourceParser#rawDataItem.
    def exitRawDataItem(self, ctx:ResourceParser.RawDataItemContext):
        pass


    # Enter a parse tree produced by ResourceParser#stringTableResource.
    def enterStringTableResource(self, ctx:ResourceParser.StringTableResourceContext):
        pass

    # Exit a parse tree produced by ResourceParser#stringTableResource.
    def exitStringTableResource(self, ctx:ResourceParser.StringTableResourceContext):
        pass


    # Enter a parse tree produced by ResourceParser#stringEntry.
    def enterStringEntry(self, ctx:ResourceParser.StringEntryContext):
        pass

    # Exit a parse tree produced by ResourceParser#stringEntry.
    def exitStringEntry(self, ctx:ResourceParser.StringEntryContext):
        pass


    # Enter a parse tree produced by ResourceParser#versionInfoResource.
    def enterVersionInfoResource(self, ctx:ResourceParser.VersionInfoResourceContext):
        pass

    # Exit a parse tree produced by ResourceParser#versionInfoResource.
    def exitVersionInfoResource(self, ctx:ResourceParser.VersionInfoResourceContext):
        pass


    # Enter a parse tree produced by ResourceParser#fixedVersionLine.
    def enterFixedVersionLine(self, ctx:ResourceParser.FixedVersionLineContext):
        pass

    # Exit a parse tree produced by ResourceParser#fixedVersionLine.
    def exitFixedVersionLine(self, ctx:ResourceParser.FixedVersionLineContext):
        pass


    # Enter a parse tree produced by ResourceParser#quadExpression.
    def enterQuadExpression(self, ctx:ResourceParser.QuadExpressionContext):
        pass

    # Exit a parse tree produced by ResourceParser#quadExpression.
    def exitQuadExpression(self, ctx:ResourceParser.QuadExpressionContext):
        pass


    # Enter a parse tree produced by ResourceParser#versionElement.
    def enterVersionElement(self, ctx:ResourceParser.VersionElementContext):
        pass

    # Exit a parse tree produced by ResourceParser#versionElement.
    def exitVersionElement(self, ctx:ResourceParser.VersionElementContext):
        pass


    # Enter a parse tree produced by ResourceParser#versionBlock.
    def enterVersionBlock(self, ctx:ResourceParser.VersionBlockContext):
        pass

    # Exit a parse tree produced by ResourceParser#versionBlock.
    def exitVersionBlock(self, ctx:ResourceParser.VersionBlockContext):
        pass


    # Enter a parse tree produced by ResourceParser#versionValue.
    def enterVersionValue(self, ctx:ResourceParser.VersionValueContext):
        pass

    # Exit a parse tree produced by ResourceParser#versionValue.
    def exitVersionValue(self, ctx:ResourceParser.VersionValueContext):
        pass


    # Enter a parse tree produced by ResourceParser#versionValueItem.
    def enterVersionValueItem(self, ctx:ResourceParser.VersionValueItemContext):
        pass

    # Exit a parse tree produced by ResourceParser#versionValueItem.
    def exitVersionValueItem(self, ctx:ResourceParser.VersionValueItemContext):
        pass


    # Enter a parse tree produced by ResourceParser#menuResource.
    def enterMenuResource(self, ctx:ResourceParser.MenuResourceContext):
        pass

    # Exit a parse tree produced by ResourceParser#menuResource.
    def exitMenuResource(self, ctx:ResourceParser.MenuResourceContext):
        pass


    # Enter a parse tree produced by ResourceParser#menuItem.
    def enterMenuItem(self, ctx:ResourceParser.MenuItemContext):
        pass

    # Exit a parse tree produced by ResourceParser#menuItem.
    def exitMenuItem(self, ctx:ResourceParser.MenuItemContext):
        pass


    # Enter a parse tree produced by ResourceParser#menuFlags.
    def enterMenuFlags(self, ctx:ResourceParser.MenuFlagsContext):
        pass

    # Exit a parse tree produced by ResourceParser#menuFlags.
    def exitMenuFlags(self, ctx:ResourceParser.MenuFlagsContext):
        pass


    # Enter a parse tree produced by ResourceParser#acceleratorsResource.
    def enterAcceleratorsResource(self, ctx:ResourceParser.AcceleratorsResourceContext):
        pass

    # Exit a parse tree produced by ResourceParser#acceleratorsResource.
    def exitAcceleratorsResource(self, ctx:ResourceParser.AcceleratorsResourceContext):
        pass


    # Enter a parse tree produced by ResourceParser#acceleratorEntry.
    def enterAcceleratorEntry(self, ctx:ResourceParser.AcceleratorEntryContext):
        pass

    # Exit a parse tree produced by ResourceParser#acceleratorEntry.
    def exitAcceleratorEntry(self, ctx:ResourceParser.AcceleratorEntryContext):
        pass


    # Enter a parse tree produced by ResourceParser#acceleratorKey.
    def enterAcceleratorKey(self, ctx:ResourceParser.AcceleratorKeyContext):
        pass

    # Exit a parse tree produced by ResourceParser#acceleratorKey.
    def exitAcceleratorKey(self, ctx:ResourceParser.AcceleratorKeyContext):
        pass


    # Enter a parse tree produced by ResourceParser#acceleratorFlags.
    def enterAcceleratorFlags(self, ctx:ResourceParser.AcceleratorFlagsContext):
        pass

    # Exit a parse tree produced by ResourceParser#acceleratorFlags.
    def exitAcceleratorFlags(self, ctx:ResourceParser.AcceleratorFlagsContext):
        pass


    # Enter a parse tree produced by ResourceParser#dialogResource.
    def enterDialogResource(self, ctx:ResourceParser.DialogResourceContext):
        pass

    # Exit a parse tree produced by ResourceParser#dialogResource.
    def exitDialogResource(self, ctx:ResourceParser.DialogResourceContext):
        pass


    # Enter a parse tree produced by ResourceParser#dialogKind.
    def enterDialogKind(self, ctx:ResourceParser.DialogKindContext):
        pass

    # Exit a parse tree produced by ResourceParser#dialogKind.
    def exitDialogKind(self, ctx:ResourceParser.DialogKindContext):
        pass


    # Enter a parse tree produced by ResourceParser#dialogHeaderLine.
    def enterDialogHeaderLine(self, ctx:ResourceParser.DialogHeaderLineContext):
        pass

    # Exit a parse tree produced by ResourceParser#dialogHeaderLine.
    def exitDialogHeaderLine(self, ctx:ResourceParser.DialogHeaderLineContext):
        pass


    # Enter a parse tree produced by ResourceParser#dialogControl.
    def enterDialogControl(self, ctx:ResourceParser.DialogControlContext):
        pass

    # Exit a parse tree produced by ResourceParser#dialogControl.
    def exitDialogControl(self, ctx:ResourceParser.DialogControlContext):
        pass


    # Enter a parse tree produced by ResourceParser#controlWithText.
    def enterControlWithText(self, ctx:ResourceParser.ControlWithTextContext):
        pass

    # Exit a parse tree produced by ResourceParser#controlWithText.
    def exitControlWithText(self, ctx:ResourceParser.ControlWithTextContext):
        pass


    # Enter a parse tree produced by ResourceParser#controlWithoutText.
    def enterControlWithoutText(self, ctx:ResourceParser.ControlWithoutTextContext):
        pass

    # Exit a parse tree produced by ResourceParser#controlWithoutText.
    def exitControlWithoutText(self, ctx:ResourceParser.ControlWithoutTextContext):
        pass


    # Enter a parse tree produced by ResourceParser#stringLiteral.
    def enterStringLiteral(self, ctx:ResourceParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by ResourceParser#stringLiteral.
    def exitStringLiteral(self, ctx:ResourceParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by ResourceParser#separator.
    def enterSeparator(self, ctx:ResourceParser.SeparatorContext):
        pass

    # Exit a parse tree produced by ResourceParser#separator.
    def exitSeparator(self, ctx:ResourceParser.SeparatorContext):
        pass


    # Enter a parse tree produced by ResourceParser#blockStart.
    def enterBlockStart(self, ctx:ResourceParser.BlockStartContext):
        pass

    # Exit a parse tree produced by ResourceParser#blockStart.
    def exitBlockStart(self, ctx:ResourceParser.BlockStartContext):
        pass


    # Enter a parse tree produced by ResourceParser#blockEnd.
    def enterBlockEnd(self, ctx:ResourceParser.BlockEndContext):
        pass

    # Exit a parse tree produced by ResourceParser#blockEnd.
    def exitBlockEnd(self, ctx:ResourceParser.BlockEndContext):
        pass


    # Enter a parse tree produced by ResourceParser#eol.
    def enterEol(self, ctx:ResourceParser.EolContext):
        pass

    # Exit a parse tree produced by ResourceParser#eol.
    def exitEol(self, ctx:ResourceParser.EolContext):
        pass


    # Enter a parse tree produced by ResourceParser#expression.
    def enterExpression(self, ctx:ResourceParser.ExpressionContext):
        pass

    # Exit a parse tree produced by ResourceParser#expression.
    def exitExpression(self, ctx:ResourceParser.ExpressionContext):
        pass


    # Enter a parse tree produced by ResourceParser#bitOrExpression.
    def enterBitOrExpression(self, ctx:ResourceParser.BitOrExpressionContext):
        pass

    # Exit a parse tree produced by ResourceParser#bitOrExpression.
    def exitBitOrExpression(self, ctx:ResourceParser.BitOrExpressionContext):
        pass


    # Enter a parse tree produced by ResourceParser#bitXorExpression.
    def enterBitXorExpression(self, ctx:ResourceParser.BitXorExpressionContext):
        pass

    # Exit a parse tree produced by ResourceParser#bitXorExpression.
    def exitBitXorExpression(self, ctx:ResourceParser.BitXorExpressionContext):
        pass


    # Enter a parse tree produced by ResourceParser#bitAndExpression.
    def enterBitAndExpression(self, ctx:ResourceParser.BitAndExpressionContext):
        pass

    # Exit a parse tree produced by ResourceParser#bitAndExpression.
    def exitBitAndExpression(self, ctx:ResourceParser.BitAndExpressionContext):
        pass


    # Enter a parse tree produced by ResourceParser#shiftExpression.
    def enterShiftExpression(self, ctx:ResourceParser.ShiftExpressionContext):
        pass

    # Exit a parse tree produced by ResourceParser#shiftExpression.
    def exitShiftExpression(self, ctx:ResourceParser.ShiftExpressionContext):
        pass


    # Enter a parse tree produced by ResourceParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:ResourceParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by ResourceParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:ResourceParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by ResourceParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:ResourceParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by ResourceParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:ResourceParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by ResourceParser#unaryExpression.
    def enterUnaryExpression(self, ctx:ResourceParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by ResourceParser#unaryExpression.
    def exitUnaryExpression(self, ctx:ResourceParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by ResourceParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:ResourceParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by ResourceParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:ResourceParser.PrimaryExpressionContext):
        pass



del ResourceParser