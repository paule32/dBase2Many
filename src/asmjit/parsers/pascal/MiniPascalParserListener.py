# Generated from grammar/MiniPascalParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MiniPascalParser import MiniPascalParser
else:
    from MiniPascalParser import MiniPascalParser

# This class defines a complete listener for a parse tree produced by MiniPascalParser.
class MiniPascalParserListener(ParseTreeListener):

    # Enter a parse tree produced by MiniPascalParser#programFile.
    def enterProgramFile(self, ctx:MiniPascalParser.ProgramFileContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#programFile.
    def exitProgramFile(self, ctx:MiniPascalParser.ProgramFileContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#declarationPart.
    def enterDeclarationPart(self, ctx:MiniPascalParser.DeclarationPartContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#declarationPart.
    def exitDeclarationPart(self, ctx:MiniPascalParser.DeclarationPartContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#constSection.
    def enterConstSection(self, ctx:MiniPascalParser.ConstSectionContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#constSection.
    def exitConstSection(self, ctx:MiniPascalParser.ConstSectionContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#constDeclaration.
    def enterConstDeclaration(self, ctx:MiniPascalParser.ConstDeclarationContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#constDeclaration.
    def exitConstDeclaration(self, ctx:MiniPascalParser.ConstDeclarationContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#constItem.
    def enterConstItem(self, ctx:MiniPascalParser.ConstItemContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#constItem.
    def exitConstItem(self, ctx:MiniPascalParser.ConstItemContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#constValue.
    def enterConstValue(self, ctx:MiniPascalParser.ConstValueContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#constValue.
    def exitConstValue(self, ctx:MiniPascalParser.ConstValueContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#typeSection.
    def enterTypeSection(self, ctx:MiniPascalParser.TypeSectionContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#typeSection.
    def exitTypeSection(self, ctx:MiniPascalParser.TypeSectionContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:MiniPascalParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:MiniPascalParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#arrayDeclaration.
    def enterArrayDeclaration(self, ctx:MiniPascalParser.ArrayDeclarationContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#arrayDeclaration.
    def exitArrayDeclaration(self, ctx:MiniPascalParser.ArrayDeclarationContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#arrayInitializer.
    def enterArrayInitializer(self, ctx:MiniPascalParser.ArrayInitializerContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#arrayInitializer.
    def exitArrayInitializer(self, ctx:MiniPascalParser.ArrayInitializerContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#arrayValueList.
    def enterArrayValueList(self, ctx:MiniPascalParser.ArrayValueListContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#arrayValueList.
    def exitArrayValueList(self, ctx:MiniPascalParser.ArrayValueListContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#arrayType.
    def enterArrayType(self, ctx:MiniPascalParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#arrayType.
    def exitArrayType(self, ctx:MiniPascalParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#arrayRange.
    def enterArrayRange(self, ctx:MiniPascalParser.ArrayRangeContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#arrayRange.
    def exitArrayRange(self, ctx:MiniPascalParser.ArrayRangeContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#typeName.
    def enterTypeName(self, ctx:MiniPascalParser.TypeNameContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#typeName.
    def exitTypeName(self, ctx:MiniPascalParser.TypeNameContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#simpleType.
    def enterSimpleType(self, ctx:MiniPascalParser.SimpleTypeContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#simpleType.
    def exitSimpleType(self, ctx:MiniPascalParser.SimpleTypeContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#enumDeclaration.
    def enterEnumDeclaration(self, ctx:MiniPascalParser.EnumDeclarationContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#enumDeclaration.
    def exitEnumDeclaration(self, ctx:MiniPascalParser.EnumDeclarationContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#enumValueList.
    def enterEnumValueList(self, ctx:MiniPascalParser.EnumValueListContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#enumValueList.
    def exitEnumValueList(self, ctx:MiniPascalParser.EnumValueListContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#enumValue.
    def enterEnumValue(self, ctx:MiniPascalParser.EnumValueContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#enumValue.
    def exitEnumValue(self, ctx:MiniPascalParser.EnumValueContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#recordDeclaration.
    def enterRecordDeclaration(self, ctx:MiniPascalParser.RecordDeclarationContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#recordDeclaration.
    def exitRecordDeclaration(self, ctx:MiniPascalParser.RecordDeclarationContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#recordFieldDeclaration.
    def enterRecordFieldDeclaration(self, ctx:MiniPascalParser.RecordFieldDeclarationContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#recordFieldDeclaration.
    def exitRecordFieldDeclaration(self, ctx:MiniPascalParser.RecordFieldDeclarationContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:MiniPascalParser.FunctionDeclarationContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:MiniPascalParser.FunctionDeclarationContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#procedureDeclaration.
    def enterProcedureDeclaration(self, ctx:MiniPascalParser.ProcedureDeclarationContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#procedureDeclaration.
    def exitProcedureDeclaration(self, ctx:MiniPascalParser.ProcedureDeclarationContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#formalParamList.
    def enterFormalParamList(self, ctx:MiniPascalParser.FormalParamListContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#formalParamList.
    def exitFormalParamList(self, ctx:MiniPascalParser.FormalParamListContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#formalParam.
    def enterFormalParam(self, ctx:MiniPascalParser.FormalParamContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#formalParam.
    def exitFormalParam(self, ctx:MiniPascalParser.FormalParamContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#declaration.
    def enterDeclaration(self, ctx:MiniPascalParser.DeclarationContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#declaration.
    def exitDeclaration(self, ctx:MiniPascalParser.DeclarationContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#functionCallExpr.
    def enterFunctionCallExpr(self, ctx:MiniPascalParser.FunctionCallExprContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#functionCallExpr.
    def exitFunctionCallExpr(self, ctx:MiniPascalParser.FunctionCallExprContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#procedureCallStatement.
    def enterProcedureCallStatement(self, ctx:MiniPascalParser.ProcedureCallStatementContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#procedureCallStatement.
    def exitProcedureCallStatement(self, ctx:MiniPascalParser.ProcedureCallStatementContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#actualParamList.
    def enterActualParamList(self, ctx:MiniPascalParser.ActualParamListContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#actualParamList.
    def exitActualParamList(self, ctx:MiniPascalParser.ActualParamListContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#actualParam.
    def enterActualParam(self, ctx:MiniPascalParser.ActualParamContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#actualParam.
    def exitActualParam(self, ctx:MiniPascalParser.ActualParamContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#varSection.
    def enterVarSection(self, ctx:MiniPascalParser.VarSectionContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#varSection.
    def exitVarSection(self, ctx:MiniPascalParser.VarSectionContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#varDeclaration.
    def enterVarDeclaration(self, ctx:MiniPascalParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#varDeclaration.
    def exitVarDeclaration(self, ctx:MiniPascalParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#varType.
    def enterVarType(self, ctx:MiniPascalParser.VarTypeContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#varType.
    def exitVarType(self, ctx:MiniPascalParser.VarTypeContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#identList.
    def enterIdentList(self, ctx:MiniPascalParser.IdentListContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#identList.
    def exitIdentList(self, ctx:MiniPascalParser.IdentListContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#block.
    def enterBlock(self, ctx:MiniPascalParser.BlockContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#block.
    def exitBlock(self, ctx:MiniPascalParser.BlockContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#localDeclaration.
    def enterLocalDeclaration(self, ctx:MiniPascalParser.LocalDeclarationContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#localDeclaration.
    def exitLocalDeclaration(self, ctx:MiniPascalParser.LocalDeclarationContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#statementList.
    def enterStatementList(self, ctx:MiniPascalParser.StatementListContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#statementList.
    def exitStatementList(self, ctx:MiniPascalParser.StatementListContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#statement.
    def enterStatement(self, ctx:MiniPascalParser.StatementContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#statement.
    def exitStatement(self, ctx:MiniPascalParser.StatementContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#exitStatement.
    def enterExitStatement(self, ctx:MiniPascalParser.ExitStatementContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#exitStatement.
    def exitExitStatement(self, ctx:MiniPascalParser.ExitStatementContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#forStatement.
    def enterForStatement(self, ctx:MiniPascalParser.ForStatementContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#forStatement.
    def exitForStatement(self, ctx:MiniPascalParser.ForStatementContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#repeatStatement.
    def enterRepeatStatement(self, ctx:MiniPascalParser.RepeatStatementContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#repeatStatement.
    def exitRepeatStatement(self, ctx:MiniPascalParser.RepeatStatementContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#argumentList.
    def enterArgumentList(self, ctx:MiniPascalParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#argumentList.
    def exitArgumentList(self, ctx:MiniPascalParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#whileStatement.
    def enterWhileStatement(self, ctx:MiniPascalParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#whileStatement.
    def exitWhileStatement(self, ctx:MiniPascalParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#ifStatement.
    def enterIfStatement(self, ctx:MiniPascalParser.IfStatementContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#ifStatement.
    def exitIfStatement(self, ctx:MiniPascalParser.IfStatementContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#condition.
    def enterCondition(self, ctx:MiniPascalParser.ConditionContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#condition.
    def exitCondition(self, ctx:MiniPascalParser.ConditionContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#compareOp.
    def enterCompareOp(self, ctx:MiniPascalParser.CompareOpContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#compareOp.
    def exitCompareOp(self, ctx:MiniPascalParser.CompareOpContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#compoundStatement.
    def enterCompoundStatement(self, ctx:MiniPascalParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#compoundStatement.
    def exitCompoundStatement(self, ctx:MiniPascalParser.CompoundStatementContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#assignment.
    def enterAssignment(self, ctx:MiniPascalParser.AssignmentContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#assignment.
    def exitAssignment(self, ctx:MiniPascalParser.AssignmentContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#variableRef.
    def enterVariableRef(self, ctx:MiniPascalParser.VariableRefContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#variableRef.
    def exitVariableRef(self, ctx:MiniPascalParser.VariableRefContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#variableSuffix.
    def enterVariableSuffix(self, ctx:MiniPascalParser.VariableSuffixContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#variableSuffix.
    def exitVariableSuffix(self, ctx:MiniPascalParser.VariableSuffixContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#expr.
    def enterExpr(self, ctx:MiniPascalParser.ExprContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#expr.
    def exitExpr(self, ctx:MiniPascalParser.ExprContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#boolOrExpr.
    def enterBoolOrExpr(self, ctx:MiniPascalParser.BoolOrExprContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#boolOrExpr.
    def exitBoolOrExpr(self, ctx:MiniPascalParser.BoolOrExprContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#boolXorExpr.
    def enterBoolXorExpr(self, ctx:MiniPascalParser.BoolXorExprContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#boolXorExpr.
    def exitBoolXorExpr(self, ctx:MiniPascalParser.BoolXorExprContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#boolAndExpr.
    def enterBoolAndExpr(self, ctx:MiniPascalParser.BoolAndExprContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#boolAndExpr.
    def exitBoolAndExpr(self, ctx:MiniPascalParser.BoolAndExprContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#addExpr.
    def enterAddExpr(self, ctx:MiniPascalParser.AddExprContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#addExpr.
    def exitAddExpr(self, ctx:MiniPascalParser.AddExprContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#term.
    def enterTerm(self, ctx:MiniPascalParser.TermContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#term.
    def exitTerm(self, ctx:MiniPascalParser.TermContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#factor.
    def enterFactor(self, ctx:MiniPascalParser.FactorContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#factor.
    def exitFactor(self, ctx:MiniPascalParser.FactorContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#writeLnStatement.
    def enterWriteLnStatement(self, ctx:MiniPascalParser.WriteLnStatementContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#writeLnStatement.
    def exitWriteLnStatement(self, ctx:MiniPascalParser.WriteLnStatementContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#writeArgList.
    def enterWriteArgList(self, ctx:MiniPascalParser.WriteArgListContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#writeArgList.
    def exitWriteArgList(self, ctx:MiniPascalParser.WriteArgListContext):
        pass


    # Enter a parse tree produced by MiniPascalParser#writeArg.
    def enterWriteArg(self, ctx:MiniPascalParser.WriteArgContext):
        pass

    # Exit a parse tree produced by MiniPascalParser#writeArg.
    def exitWriteArg(self, ctx:MiniPascalParser.WriteArgContext):
        pass



del MiniPascalParser