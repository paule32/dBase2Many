# Generated from grammar/MiniPascalParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MiniPascalParser import MiniPascalParser
else:
    from MiniPascalParser import MiniPascalParser

# This class defines a complete generic visitor for a parse tree produced by MiniPascalParser.

class MiniPascalParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MiniPascalParser#programFile.
    def visitProgramFile(self, ctx:MiniPascalParser.ProgramFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#declarationPart.
    def visitDeclarationPart(self, ctx:MiniPascalParser.DeclarationPartContext):
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


    # Visit a parse tree produced by MiniPascalParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:MiniPascalParser.TypeDeclarationContext):
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


    # Visit a parse tree produced by MiniPascalParser#typeName.
    def visitTypeName(self, ctx:MiniPascalParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniPascalParser#simpleType.
    def visitSimpleType(self, ctx:MiniPascalParser.SimpleTypeContext):
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


    # Visit a parse tree produced by MiniPascalParser#declaration.
    def visitDeclaration(self, ctx:MiniPascalParser.DeclarationContext):
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