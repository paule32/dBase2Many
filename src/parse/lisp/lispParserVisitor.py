# Generated from lispParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .lispParser import lispParser
else:
    from lispParser import lispParser

# This class defines a complete generic visitor for a parse tree produced by lispParser.

class lispParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by lispParser#program.
    def visitProgram(self, ctx:lispParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#form.
    def visitForm(self, ctx:lispParser.FormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#quotedForm.
    def visitQuotedForm(self, ctx:lispParser.QuotedFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#vector.
    def visitVector(self, ctx:lispParser.VectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#list.
    def visitList(self, ctx:lispParser.ListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#listContent.
    def visitListContent(self, ctx:lispParser.ListContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#defunForm.
    def visitDefunForm(self, ctx:lispParser.DefunFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#lambdaForm.
    def visitLambdaForm(self, ctx:lispParser.LambdaFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#letForm.
    def visitLetForm(self, ctx:lispParser.LetFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#bindingSpec.
    def visitBindingSpec(self, ctx:lispParser.BindingSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#ifForm.
    def visitIfForm(self, ctx:lispParser.IfFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#condForm.
    def visitCondForm(self, ctx:lispParser.CondFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#condClause.
    def visitCondClause(self, ctx:lispParser.CondClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#prognForm.
    def visitPrognForm(self, ctx:lispParser.PrognFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#setqForm.
    def visitSetqForm(self, ctx:lispParser.SetqFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#definitionForm.
    def visitDefinitionForm(self, ctx:lispParser.DefinitionFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#quoteSpecialForm.
    def visitQuoteSpecialForm(self, ctx:lispParser.QuoteSpecialFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#functionSpecialForm.
    def visitFunctionSpecialForm(self, ctx:lispParser.FunctionSpecialFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#applicationForm.
    def visitApplicationForm(self, ctx:lispParser.ApplicationFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#dottedList.
    def visitDottedList(self, ctx:lispParser.DottedListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#lambdaList.
    def visitLambdaList(self, ctx:lispParser.LambdaListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#lambdaListElement.
    def visitLambdaListElement(self, ctx:lispParser.LambdaListElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#declaration.
    def visitDeclaration(self, ctx:lispParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#body.
    def visitBody(self, ctx:lispParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lispParser#atom.
    def visitAtom(self, ctx:lispParser.AtomContext):
        return self.visitChildren(ctx)



del lispParser