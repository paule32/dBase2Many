# Generated from lispParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .lispParser import lispParser
else:
    from lispParser import lispParser

# This class defines a complete listener for a parse tree produced by lispParser.
class lispParserListener(ParseTreeListener):

    # Enter a parse tree produced by lispParser#program.
    def enterProgram(self, ctx:lispParser.ProgramContext):
        pass

    # Exit a parse tree produced by lispParser#program.
    def exitProgram(self, ctx:lispParser.ProgramContext):
        pass


    # Enter a parse tree produced by lispParser#form.
    def enterForm(self, ctx:lispParser.FormContext):
        pass

    # Exit a parse tree produced by lispParser#form.
    def exitForm(self, ctx:lispParser.FormContext):
        pass


    # Enter a parse tree produced by lispParser#quotedForm.
    def enterQuotedForm(self, ctx:lispParser.QuotedFormContext):
        pass

    # Exit a parse tree produced by lispParser#quotedForm.
    def exitQuotedForm(self, ctx:lispParser.QuotedFormContext):
        pass


    # Enter a parse tree produced by lispParser#vector.
    def enterVector(self, ctx:lispParser.VectorContext):
        pass

    # Exit a parse tree produced by lispParser#vector.
    def exitVector(self, ctx:lispParser.VectorContext):
        pass


    # Enter a parse tree produced by lispParser#list.
    def enterList(self, ctx:lispParser.ListContext):
        pass

    # Exit a parse tree produced by lispParser#list.
    def exitList(self, ctx:lispParser.ListContext):
        pass


    # Enter a parse tree produced by lispParser#listContent.
    def enterListContent(self, ctx:lispParser.ListContentContext):
        pass

    # Exit a parse tree produced by lispParser#listContent.
    def exitListContent(self, ctx:lispParser.ListContentContext):
        pass


    # Enter a parse tree produced by lispParser#defunForm.
    def enterDefunForm(self, ctx:lispParser.DefunFormContext):
        pass

    # Exit a parse tree produced by lispParser#defunForm.
    def exitDefunForm(self, ctx:lispParser.DefunFormContext):
        pass


    # Enter a parse tree produced by lispParser#lambdaForm.
    def enterLambdaForm(self, ctx:lispParser.LambdaFormContext):
        pass

    # Exit a parse tree produced by lispParser#lambdaForm.
    def exitLambdaForm(self, ctx:lispParser.LambdaFormContext):
        pass


    # Enter a parse tree produced by lispParser#letForm.
    def enterLetForm(self, ctx:lispParser.LetFormContext):
        pass

    # Exit a parse tree produced by lispParser#letForm.
    def exitLetForm(self, ctx:lispParser.LetFormContext):
        pass


    # Enter a parse tree produced by lispParser#bindingSpec.
    def enterBindingSpec(self, ctx:lispParser.BindingSpecContext):
        pass

    # Exit a parse tree produced by lispParser#bindingSpec.
    def exitBindingSpec(self, ctx:lispParser.BindingSpecContext):
        pass


    # Enter a parse tree produced by lispParser#ifForm.
    def enterIfForm(self, ctx:lispParser.IfFormContext):
        pass

    # Exit a parse tree produced by lispParser#ifForm.
    def exitIfForm(self, ctx:lispParser.IfFormContext):
        pass


    # Enter a parse tree produced by lispParser#condForm.
    def enterCondForm(self, ctx:lispParser.CondFormContext):
        pass

    # Exit a parse tree produced by lispParser#condForm.
    def exitCondForm(self, ctx:lispParser.CondFormContext):
        pass


    # Enter a parse tree produced by lispParser#condClause.
    def enterCondClause(self, ctx:lispParser.CondClauseContext):
        pass

    # Exit a parse tree produced by lispParser#condClause.
    def exitCondClause(self, ctx:lispParser.CondClauseContext):
        pass


    # Enter a parse tree produced by lispParser#prognForm.
    def enterPrognForm(self, ctx:lispParser.PrognFormContext):
        pass

    # Exit a parse tree produced by lispParser#prognForm.
    def exitPrognForm(self, ctx:lispParser.PrognFormContext):
        pass


    # Enter a parse tree produced by lispParser#setqForm.
    def enterSetqForm(self, ctx:lispParser.SetqFormContext):
        pass

    # Exit a parse tree produced by lispParser#setqForm.
    def exitSetqForm(self, ctx:lispParser.SetqFormContext):
        pass


    # Enter a parse tree produced by lispParser#definitionForm.
    def enterDefinitionForm(self, ctx:lispParser.DefinitionFormContext):
        pass

    # Exit a parse tree produced by lispParser#definitionForm.
    def exitDefinitionForm(self, ctx:lispParser.DefinitionFormContext):
        pass


    # Enter a parse tree produced by lispParser#quoteSpecialForm.
    def enterQuoteSpecialForm(self, ctx:lispParser.QuoteSpecialFormContext):
        pass

    # Exit a parse tree produced by lispParser#quoteSpecialForm.
    def exitQuoteSpecialForm(self, ctx:lispParser.QuoteSpecialFormContext):
        pass


    # Enter a parse tree produced by lispParser#functionSpecialForm.
    def enterFunctionSpecialForm(self, ctx:lispParser.FunctionSpecialFormContext):
        pass

    # Exit a parse tree produced by lispParser#functionSpecialForm.
    def exitFunctionSpecialForm(self, ctx:lispParser.FunctionSpecialFormContext):
        pass


    # Enter a parse tree produced by lispParser#applicationForm.
    def enterApplicationForm(self, ctx:lispParser.ApplicationFormContext):
        pass

    # Exit a parse tree produced by lispParser#applicationForm.
    def exitApplicationForm(self, ctx:lispParser.ApplicationFormContext):
        pass


    # Enter a parse tree produced by lispParser#dottedList.
    def enterDottedList(self, ctx:lispParser.DottedListContext):
        pass

    # Exit a parse tree produced by lispParser#dottedList.
    def exitDottedList(self, ctx:lispParser.DottedListContext):
        pass


    # Enter a parse tree produced by lispParser#lambdaList.
    def enterLambdaList(self, ctx:lispParser.LambdaListContext):
        pass

    # Exit a parse tree produced by lispParser#lambdaList.
    def exitLambdaList(self, ctx:lispParser.LambdaListContext):
        pass


    # Enter a parse tree produced by lispParser#lambdaListElement.
    def enterLambdaListElement(self, ctx:lispParser.LambdaListElementContext):
        pass

    # Exit a parse tree produced by lispParser#lambdaListElement.
    def exitLambdaListElement(self, ctx:lispParser.LambdaListElementContext):
        pass


    # Enter a parse tree produced by lispParser#declaration.
    def enterDeclaration(self, ctx:lispParser.DeclarationContext):
        pass

    # Exit a parse tree produced by lispParser#declaration.
    def exitDeclaration(self, ctx:lispParser.DeclarationContext):
        pass


    # Enter a parse tree produced by lispParser#body.
    def enterBody(self, ctx:lispParser.BodyContext):
        pass

    # Exit a parse tree produced by lispParser#body.
    def exitBody(self, ctx:lispParser.BodyContext):
        pass


    # Enter a parse tree produced by lispParser#atom.
    def enterAtom(self, ctx:lispParser.AtomContext):
        pass

    # Exit a parse tree produced by lispParser#atom.
    def exitAtom(self, ctx:lispParser.AtomContext):
        pass



del lispParser