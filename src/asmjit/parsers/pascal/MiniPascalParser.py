# Generated from grammar/MiniPascalParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,45,265,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,1,0,1,0,1,0,1,0,3,0,63,8,0,1,0,5,0,66,8,0,10,
        0,12,0,69,9,0,1,0,1,0,1,0,1,1,1,1,1,1,3,1,77,8,1,1,1,1,1,1,1,3,1,
        82,8,1,1,2,1,2,1,2,1,2,5,2,88,8,2,10,2,12,2,91,9,2,1,2,1,2,1,3,1,
        3,1,3,1,3,1,4,1,4,3,4,101,8,4,1,4,3,4,104,8,4,1,5,1,5,1,5,1,5,5,
        5,110,8,5,10,5,12,5,113,9,5,1,5,1,5,1,6,1,6,3,6,119,8,6,1,7,1,7,
        4,7,123,8,7,11,7,12,7,124,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,5,9,135,
        8,9,10,9,12,9,138,9,9,1,10,1,10,1,11,1,11,1,11,1,11,1,12,1,12,3,
        12,148,8,12,5,12,150,8,12,10,12,12,12,153,9,12,1,13,1,13,1,13,1,
        13,1,13,1,13,1,13,1,13,3,13,163,8,13,1,14,1,14,1,14,1,14,1,14,1,
        14,1,14,1,14,1,14,1,15,1,15,1,15,1,15,1,15,3,15,179,8,15,1,16,1,
        16,1,16,5,16,184,8,16,10,16,12,16,187,9,16,1,17,1,17,1,17,1,17,1,
        17,1,18,1,18,1,18,1,18,1,18,1,18,3,18,200,8,18,1,19,1,19,1,19,1,
        19,1,20,1,20,1,21,1,21,1,21,1,21,1,22,1,22,1,22,1,22,3,22,216,8,
        22,1,23,1,23,1,23,5,23,221,8,23,10,23,12,23,224,9,23,1,24,1,24,1,
        24,5,24,229,8,24,10,24,12,24,232,9,24,1,25,1,25,1,25,1,25,1,25,1,
        25,1,25,1,25,3,25,242,8,25,1,26,1,26,1,26,3,26,247,8,26,1,26,1,26,
        3,26,251,8,26,1,27,1,27,1,27,5,27,256,8,27,10,27,12,27,259,9,27,
        1,28,1,28,3,28,263,8,28,1,28,0,0,29,0,2,4,6,8,10,12,14,16,18,20,
        22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,0,5,2,0,5,
        6,38,38,1,0,15,16,1,0,31,36,1,0,25,26,1,0,27,28,269,0,58,1,0,0,0,
        2,73,1,0,0,0,4,83,1,0,0,0,6,94,1,0,0,0,8,98,1,0,0,0,10,105,1,0,0,
        0,12,118,1,0,0,0,14,120,1,0,0,0,16,126,1,0,0,0,18,131,1,0,0,0,20,
        139,1,0,0,0,22,141,1,0,0,0,24,151,1,0,0,0,26,162,1,0,0,0,28,164,
        1,0,0,0,30,173,1,0,0,0,32,180,1,0,0,0,34,188,1,0,0,0,36,193,1,0,
        0,0,38,201,1,0,0,0,40,205,1,0,0,0,42,207,1,0,0,0,44,211,1,0,0,0,
        46,217,1,0,0,0,48,225,1,0,0,0,50,241,1,0,0,0,52,243,1,0,0,0,54,252,
        1,0,0,0,56,262,1,0,0,0,58,59,5,1,0,0,59,60,5,38,0,0,60,62,5,22,0,
        0,61,63,3,14,7,0,62,61,1,0,0,0,62,63,1,0,0,0,63,67,1,0,0,0,64,66,
        3,2,1,0,65,64,1,0,0,0,66,69,1,0,0,0,67,65,1,0,0,0,67,68,1,0,0,0,
        68,70,1,0,0,0,69,67,1,0,0,0,70,71,3,22,11,0,71,72,5,23,0,0,72,1,
        1,0,0,0,73,74,5,17,0,0,74,76,5,38,0,0,75,77,3,4,2,0,76,75,1,0,0,
        0,76,77,1,0,0,0,77,78,1,0,0,0,78,79,5,22,0,0,79,81,3,22,11,0,80,
        82,5,22,0,0,81,80,1,0,0,0,81,82,1,0,0,0,82,3,1,0,0,0,83,84,5,29,
        0,0,84,89,3,6,3,0,85,86,5,22,0,0,86,88,3,6,3,0,87,85,1,0,0,0,88,
        91,1,0,0,0,89,87,1,0,0,0,89,90,1,0,0,0,90,92,1,0,0,0,91,89,1,0,0,
        0,92,93,5,30,0,0,93,5,1,0,0,0,94,95,3,18,9,0,95,96,5,21,0,0,96,97,
        3,20,10,0,97,7,1,0,0,0,98,100,5,38,0,0,99,101,3,10,5,0,100,99,1,
        0,0,0,100,101,1,0,0,0,101,103,1,0,0,0,102,104,5,22,0,0,103,102,1,
        0,0,0,103,104,1,0,0,0,104,9,1,0,0,0,105,106,5,29,0,0,106,111,3,12,
        6,0,107,108,5,24,0,0,108,110,3,12,6,0,109,107,1,0,0,0,110,113,1,
        0,0,0,111,109,1,0,0,0,111,112,1,0,0,0,112,114,1,0,0,0,113,111,1,
        0,0,0,114,115,5,30,0,0,115,11,1,0,0,0,116,119,5,37,0,0,117,119,3,
        46,23,0,118,116,1,0,0,0,118,117,1,0,0,0,119,13,1,0,0,0,120,122,5,
        4,0,0,121,123,3,16,8,0,122,121,1,0,0,0,123,124,1,0,0,0,124,122,1,
        0,0,0,124,125,1,0,0,0,125,15,1,0,0,0,126,127,3,18,9,0,127,128,5,
        21,0,0,128,129,3,20,10,0,129,130,5,22,0,0,130,17,1,0,0,0,131,136,
        5,38,0,0,132,133,5,24,0,0,133,135,5,38,0,0,134,132,1,0,0,0,135,138,
        1,0,0,0,136,134,1,0,0,0,136,137,1,0,0,0,137,19,1,0,0,0,138,136,1,
        0,0,0,139,140,7,0,0,0,140,21,1,0,0,0,141,142,5,2,0,0,142,143,3,24,
        12,0,143,144,5,3,0,0,144,23,1,0,0,0,145,147,3,26,13,0,146,148,5,
        22,0,0,147,146,1,0,0,0,147,148,1,0,0,0,148,150,1,0,0,0,149,145,1,
        0,0,0,150,153,1,0,0,0,151,149,1,0,0,0,151,152,1,0,0,0,152,25,1,0,
        0,0,153,151,1,0,0,0,154,163,3,44,22,0,155,163,3,52,26,0,156,163,
        3,36,18,0,157,163,3,34,17,0,158,163,3,30,15,0,159,163,3,28,14,0,
        160,163,3,8,4,0,161,163,3,42,21,0,162,154,1,0,0,0,162,155,1,0,0,
        0,162,156,1,0,0,0,162,157,1,0,0,0,162,158,1,0,0,0,162,159,1,0,0,
        0,162,160,1,0,0,0,162,161,1,0,0,0,163,27,1,0,0,0,164,165,5,14,0,
        0,165,166,5,38,0,0,166,167,5,20,0,0,167,168,3,46,23,0,168,169,7,
        1,0,0,169,170,3,46,23,0,170,171,5,11,0,0,171,172,3,26,13,0,172,29,
        1,0,0,0,173,174,5,12,0,0,174,175,3,24,12,0,175,176,5,13,0,0,176,
        178,3,38,19,0,177,179,5,22,0,0,178,177,1,0,0,0,178,179,1,0,0,0,179,
        31,1,0,0,0,180,185,3,46,23,0,181,182,5,24,0,0,182,184,3,46,23,0,
        183,181,1,0,0,0,184,187,1,0,0,0,185,183,1,0,0,0,185,186,1,0,0,0,
        186,33,1,0,0,0,187,185,1,0,0,0,188,189,5,10,0,0,189,190,3,38,19,
        0,190,191,5,11,0,0,191,192,3,26,13,0,192,35,1,0,0,0,193,194,5,7,
        0,0,194,195,3,38,19,0,195,196,5,8,0,0,196,199,3,26,13,0,197,198,
        5,9,0,0,198,200,3,26,13,0,199,197,1,0,0,0,199,200,1,0,0,0,200,37,
        1,0,0,0,201,202,3,46,23,0,202,203,3,40,20,0,203,204,3,46,23,0,204,
        39,1,0,0,0,205,206,7,2,0,0,206,41,1,0,0,0,207,208,5,2,0,0,208,209,
        3,24,12,0,209,210,5,3,0,0,210,43,1,0,0,0,211,212,5,38,0,0,212,213,
        5,20,0,0,213,215,3,46,23,0,214,216,5,22,0,0,215,214,1,0,0,0,215,
        216,1,0,0,0,216,45,1,0,0,0,217,222,3,48,24,0,218,219,7,3,0,0,219,
        221,3,48,24,0,220,218,1,0,0,0,221,224,1,0,0,0,222,220,1,0,0,0,222,
        223,1,0,0,0,223,47,1,0,0,0,224,222,1,0,0,0,225,230,3,50,25,0,226,
        227,7,4,0,0,227,229,3,50,25,0,228,226,1,0,0,0,229,232,1,0,0,0,230,
        228,1,0,0,0,230,231,1,0,0,0,231,49,1,0,0,0,232,230,1,0,0,0,233,242,
        5,41,0,0,234,242,5,40,0,0,235,242,5,39,0,0,236,242,5,38,0,0,237,
        238,5,29,0,0,238,239,3,46,23,0,239,240,5,30,0,0,240,242,1,0,0,0,
        241,233,1,0,0,0,241,234,1,0,0,0,241,235,1,0,0,0,241,236,1,0,0,0,
        241,237,1,0,0,0,242,51,1,0,0,0,243,244,5,19,0,0,244,246,5,29,0,0,
        245,247,3,54,27,0,246,245,1,0,0,0,246,247,1,0,0,0,247,248,1,0,0,
        0,248,250,5,30,0,0,249,251,5,22,0,0,250,249,1,0,0,0,250,251,1,0,
        0,0,251,53,1,0,0,0,252,257,3,56,28,0,253,254,5,24,0,0,254,256,3,
        56,28,0,255,253,1,0,0,0,256,259,1,0,0,0,257,255,1,0,0,0,257,258,
        1,0,0,0,258,55,1,0,0,0,259,257,1,0,0,0,260,263,5,37,0,0,261,263,
        3,46,23,0,262,260,1,0,0,0,262,261,1,0,0,0,263,57,1,0,0,0,25,62,67,
        76,81,89,100,103,111,118,124,136,147,151,162,178,185,199,215,222,
        230,241,246,250,257,262
    ]

class MiniPascalParser ( Parser ):

    grammarFileName = "MiniPascalParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "':='", "':'", "';'", "'.'", "','", "'+'", "'-'", "'*'", 
                     "'/'", "'('", "')'", "'='", "'<='", "'<>'", "'<'", 
                     "'>='", "'>'" ]

    symbolicNames = [ "<INVALID>", "PROGRAM", "BEGIN_", "END", "VAR", "DOUBLE", 
                      "INTEGER", "IF", "THEN", "ELSE", "WHILE", "DO", "REPEAT", 
                      "UNTIL", "FOR", "TO", "DOWNTO", "PROCEDURE", "FUNCTION", 
                      "WRITELN", "ASSIGN", "COLON", "SEMI", "DOT", "COMMA", 
                      "PLUS", "MINUS", "STAR", "SLASH", "LPAREN", "RPAREN", 
                      "EQ_OP", "LE_OP", "NE_OP", "LT_OP", "GE_OP", "GT_OP", 
                      "STRING", "IDENT", "HEXNUMBER", "FLOATNUMBER", "NUMBER", 
                      "WS", "COMMENT1", "COMMENT2", "COMMENT3" ]

    RULE_programFile = 0
    RULE_procedureDeclaration = 1
    RULE_formalParamList = 2
    RULE_formalParam = 3
    RULE_procedureCallStatement = 4
    RULE_actualParamList = 5
    RULE_actualParam = 6
    RULE_varSection = 7
    RULE_varDeclaration = 8
    RULE_identList = 9
    RULE_typeName = 10
    RULE_block = 11
    RULE_statementList = 12
    RULE_statement = 13
    RULE_forStatement = 14
    RULE_repeatStatement = 15
    RULE_argumentList = 16
    RULE_whileStatement = 17
    RULE_ifStatement = 18
    RULE_condition = 19
    RULE_compareOp = 20
    RULE_compoundStatement = 21
    RULE_assignment = 22
    RULE_expr = 23
    RULE_term = 24
    RULE_factor = 25
    RULE_writeLnStatement = 26
    RULE_writeArgList = 27
    RULE_writeArg = 28

    ruleNames =  [ "programFile", "procedureDeclaration", "formalParamList", 
                   "formalParam", "procedureCallStatement", "actualParamList", 
                   "actualParam", "varSection", "varDeclaration", "identList", 
                   "typeName", "block", "statementList", "statement", "forStatement", 
                   "repeatStatement", "argumentList", "whileStatement", 
                   "ifStatement", "condition", "compareOp", "compoundStatement", 
                   "assignment", "expr", "term", "factor", "writeLnStatement", 
                   "writeArgList", "writeArg" ]

    EOF = Token.EOF
    PROGRAM=1
    BEGIN_=2
    END=3
    VAR=4
    DOUBLE=5
    INTEGER=6
    IF=7
    THEN=8
    ELSE=9
    WHILE=10
    DO=11
    REPEAT=12
    UNTIL=13
    FOR=14
    TO=15
    DOWNTO=16
    PROCEDURE=17
    FUNCTION=18
    WRITELN=19
    ASSIGN=20
    COLON=21
    SEMI=22
    DOT=23
    COMMA=24
    PLUS=25
    MINUS=26
    STAR=27
    SLASH=28
    LPAREN=29
    RPAREN=30
    EQ_OP=31
    LE_OP=32
    NE_OP=33
    LT_OP=34
    GE_OP=35
    GT_OP=36
    STRING=37
    IDENT=38
    HEXNUMBER=39
    FLOATNUMBER=40
    NUMBER=41
    WS=42
    COMMENT1=43
    COMMENT2=44
    COMMENT3=45

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramFileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROGRAM(self):
            return self.getToken(MiniPascalParser.PROGRAM, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def block(self):
            return self.getTypedRuleContext(MiniPascalParser.BlockContext,0)


        def DOT(self):
            return self.getToken(MiniPascalParser.DOT, 0)

        def varSection(self):
            return self.getTypedRuleContext(MiniPascalParser.VarSectionContext,0)


        def procedureDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.ProcedureDeclarationContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.ProcedureDeclarationContext,i)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_programFile

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgramFile" ):
                listener.enterProgramFile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgramFile" ):
                listener.exitProgramFile(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgramFile" ):
                return visitor.visitProgramFile(self)
            else:
                return visitor.visitChildren(self)




    def programFile(self):

        localctx = MiniPascalParser.ProgramFileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_programFile)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.match(MiniPascalParser.PROGRAM)
            self.state = 59
            self.match(MiniPascalParser.IDENT)
            self.state = 60
            self.match(MiniPascalParser.SEMI)
            self.state = 62
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 61
                self.varSection()


            self.state = 67
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==17:
                self.state = 64
                self.procedureDeclaration()
                self.state = 69
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 70
            self.block()
            self.state = 71
            self.match(MiniPascalParser.DOT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProcedureDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROCEDURE(self):
            return self.getToken(MiniPascalParser.PROCEDURE, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.SEMI)
            else:
                return self.getToken(MiniPascalParser.SEMI, i)

        def block(self):
            return self.getTypedRuleContext(MiniPascalParser.BlockContext,0)


        def formalParamList(self):
            return self.getTypedRuleContext(MiniPascalParser.FormalParamListContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_procedureDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProcedureDeclaration" ):
                listener.enterProcedureDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProcedureDeclaration" ):
                listener.exitProcedureDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProcedureDeclaration" ):
                return visitor.visitProcedureDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def procedureDeclaration(self):

        localctx = MiniPascalParser.ProcedureDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_procedureDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self.match(MiniPascalParser.PROCEDURE)
            self.state = 74
            self.match(MiniPascalParser.IDENT)
            self.state = 76
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==29:
                self.state = 75
                self.formalParamList()


            self.state = 78
            self.match(MiniPascalParser.SEMI)
            self.state = 79
            self.block()
            self.state = 81
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==22:
                self.state = 80
                self.match(MiniPascalParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormalParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(MiniPascalParser.LPAREN, 0)

        def formalParam(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.FormalParamContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.FormalParamContext,i)


        def RPAREN(self):
            return self.getToken(MiniPascalParser.RPAREN, 0)

        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.SEMI)
            else:
                return self.getToken(MiniPascalParser.SEMI, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_formalParamList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFormalParamList" ):
                listener.enterFormalParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFormalParamList" ):
                listener.exitFormalParamList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFormalParamList" ):
                return visitor.visitFormalParamList(self)
            else:
                return visitor.visitChildren(self)




    def formalParamList(self):

        localctx = MiniPascalParser.FormalParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_formalParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            self.match(MiniPascalParser.LPAREN)
            self.state = 84
            self.formalParam()
            self.state = 89
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==22:
                self.state = 85
                self.match(MiniPascalParser.SEMI)
                self.state = 86
                self.formalParam()
                self.state = 91
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 92
            self.match(MiniPascalParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormalParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identList(self):
            return self.getTypedRuleContext(MiniPascalParser.IdentListContext,0)


        def COLON(self):
            return self.getToken(MiniPascalParser.COLON, 0)

        def typeName(self):
            return self.getTypedRuleContext(MiniPascalParser.TypeNameContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_formalParam

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFormalParam" ):
                listener.enterFormalParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFormalParam" ):
                listener.exitFormalParam(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFormalParam" ):
                return visitor.visitFormalParam(self)
            else:
                return visitor.visitChildren(self)




    def formalParam(self):

        localctx = MiniPascalParser.FormalParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_formalParam)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.identList()
            self.state = 95
            self.match(MiniPascalParser.COLON)
            self.state = 96
            self.typeName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProcedureCallStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def actualParamList(self):
            return self.getTypedRuleContext(MiniPascalParser.ActualParamListContext,0)


        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_procedureCallStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProcedureCallStatement" ):
                listener.enterProcedureCallStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProcedureCallStatement" ):
                listener.exitProcedureCallStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProcedureCallStatement" ):
                return visitor.visitProcedureCallStatement(self)
            else:
                return visitor.visitChildren(self)




    def procedureCallStatement(self):

        localctx = MiniPascalParser.ProcedureCallStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_procedureCallStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 98
            self.match(MiniPascalParser.IDENT)
            self.state = 100
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==29:
                self.state = 99
                self.actualParamList()


            self.state = 103
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.state = 102
                self.match(MiniPascalParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ActualParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(MiniPascalParser.LPAREN, 0)

        def actualParam(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.ActualParamContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.ActualParamContext,i)


        def RPAREN(self):
            return self.getToken(MiniPascalParser.RPAREN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.COMMA)
            else:
                return self.getToken(MiniPascalParser.COMMA, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_actualParamList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterActualParamList" ):
                listener.enterActualParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitActualParamList" ):
                listener.exitActualParamList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitActualParamList" ):
                return visitor.visitActualParamList(self)
            else:
                return visitor.visitChildren(self)




    def actualParamList(self):

        localctx = MiniPascalParser.ActualParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_actualParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            self.match(MiniPascalParser.LPAREN)
            self.state = 106
            self.actualParam()
            self.state = 111
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==24:
                self.state = 107
                self.match(MiniPascalParser.COMMA)
                self.state = 108
                self.actualParam()
                self.state = 113
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 114
            self.match(MiniPascalParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ActualParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(MiniPascalParser.STRING, 0)

        def expr(self):
            return self.getTypedRuleContext(MiniPascalParser.ExprContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_actualParam

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterActualParam" ):
                listener.enterActualParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitActualParam" ):
                listener.exitActualParam(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitActualParam" ):
                return visitor.visitActualParam(self)
            else:
                return visitor.visitChildren(self)




    def actualParam(self):

        localctx = MiniPascalParser.ActualParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_actualParam)
        try:
            self.state = 118
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [37]:
                self.enterOuterAlt(localctx, 1)
                self.state = 116
                self.match(MiniPascalParser.STRING)
                pass
            elif token in [29, 38, 39, 40, 41]:
                self.enterOuterAlt(localctx, 2)
                self.state = 117
                self.expr()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VAR(self):
            return self.getToken(MiniPascalParser.VAR, 0)

        def varDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.VarDeclarationContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.VarDeclarationContext,i)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_varSection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarSection" ):
                listener.enterVarSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarSection" ):
                listener.exitVarSection(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarSection" ):
                return visitor.visitVarSection(self)
            else:
                return visitor.visitChildren(self)




    def varSection(self):

        localctx = MiniPascalParser.VarSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_varSection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 120
            self.match(MiniPascalParser.VAR)
            self.state = 122 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 121
                self.varDeclaration()
                self.state = 124 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==38):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identList(self):
            return self.getTypedRuleContext(MiniPascalParser.IdentListContext,0)


        def COLON(self):
            return self.getToken(MiniPascalParser.COLON, 0)

        def typeName(self):
            return self.getTypedRuleContext(MiniPascalParser.TypeNameContext,0)


        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_varDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarDeclaration" ):
                listener.enterVarDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarDeclaration" ):
                listener.exitVarDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDeclaration" ):
                return visitor.visitVarDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def varDeclaration(self):

        localctx = MiniPascalParser.VarDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_varDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 126
            self.identList()
            self.state = 127
            self.match(MiniPascalParser.COLON)
            self.state = 128
            self.typeName()
            self.state = 129
            self.match(MiniPascalParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdentListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.IDENT)
            else:
                return self.getToken(MiniPascalParser.IDENT, i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.COMMA)
            else:
                return self.getToken(MiniPascalParser.COMMA, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_identList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentList" ):
                listener.enterIdentList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentList" ):
                listener.exitIdentList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentList" ):
                return visitor.visitIdentList(self)
            else:
                return visitor.visitChildren(self)




    def identList(self):

        localctx = MiniPascalParser.IdentListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_identList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self.match(MiniPascalParser.IDENT)
            self.state = 136
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==24:
                self.state = 132
                self.match(MiniPascalParser.COMMA)
                self.state = 133
                self.match(MiniPascalParser.IDENT)
                self.state = 138
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOUBLE(self):
            return self.getToken(MiniPascalParser.DOUBLE, 0)

        def INTEGER(self):
            return self.getToken(MiniPascalParser.INTEGER, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_typeName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeName" ):
                listener.enterTypeName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeName" ):
                listener.exitTypeName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeName" ):
                return visitor.visitTypeName(self)
            else:
                return visitor.visitChildren(self)




    def typeName(self):

        localctx = MiniPascalParser.TypeNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_typeName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 274877907040) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_(self):
            return self.getToken(MiniPascalParser.BEGIN_, 0)

        def statementList(self):
            return self.getTypedRuleContext(MiniPascalParser.StatementListContext,0)


        def END(self):
            return self.getToken(MiniPascalParser.END, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = MiniPascalParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_block)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 141
            self.match(MiniPascalParser.BEGIN_)
            self.state = 142
            self.statementList()
            self.state = 143
            self.match(MiniPascalParser.END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.StatementContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.StatementContext,i)


        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.SEMI)
            else:
                return self.getToken(MiniPascalParser.SEMI, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_statementList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatementList" ):
                listener.enterStatementList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatementList" ):
                listener.exitStatementList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatementList" ):
                return visitor.visitStatementList(self)
            else:
                return visitor.visitChildren(self)




    def statementList(self):

        localctx = MiniPascalParser.StatementListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_statementList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 274878452868) != 0):
                self.state = 145
                self.statement()
                self.state = 147
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==22:
                    self.state = 146
                    self.match(MiniPascalParser.SEMI)


                self.state = 153
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment(self):
            return self.getTypedRuleContext(MiniPascalParser.AssignmentContext,0)


        def writeLnStatement(self):
            return self.getTypedRuleContext(MiniPascalParser.WriteLnStatementContext,0)


        def ifStatement(self):
            return self.getTypedRuleContext(MiniPascalParser.IfStatementContext,0)


        def whileStatement(self):
            return self.getTypedRuleContext(MiniPascalParser.WhileStatementContext,0)


        def repeatStatement(self):
            return self.getTypedRuleContext(MiniPascalParser.RepeatStatementContext,0)


        def forStatement(self):
            return self.getTypedRuleContext(MiniPascalParser.ForStatementContext,0)


        def procedureCallStatement(self):
            return self.getTypedRuleContext(MiniPascalParser.ProcedureCallStatementContext,0)


        def compoundStatement(self):
            return self.getTypedRuleContext(MiniPascalParser.CompoundStatementContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = MiniPascalParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_statement)
        try:
            self.state = 162
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 154
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 155
                self.writeLnStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 156
                self.ifStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 157
                self.whileStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 158
                self.repeatStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 159
                self.forStatement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 160
                self.procedureCallStatement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 161
                self.compoundStatement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(MiniPascalParser.FOR, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def ASSIGN(self):
            return self.getToken(MiniPascalParser.ASSIGN, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.ExprContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.ExprContext,i)


        def DO(self):
            return self.getToken(MiniPascalParser.DO, 0)

        def statement(self):
            return self.getTypedRuleContext(MiniPascalParser.StatementContext,0)


        def TO(self):
            return self.getToken(MiniPascalParser.TO, 0)

        def DOWNTO(self):
            return self.getToken(MiniPascalParser.DOWNTO, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_forStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStatement" ):
                listener.enterForStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStatement" ):
                listener.exitForStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStatement" ):
                return visitor.visitForStatement(self)
            else:
                return visitor.visitChildren(self)




    def forStatement(self):

        localctx = MiniPascalParser.ForStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 164
            self.match(MiniPascalParser.FOR)
            self.state = 165
            self.match(MiniPascalParser.IDENT)
            self.state = 166
            self.match(MiniPascalParser.ASSIGN)
            self.state = 167
            self.expr()
            self.state = 168
            _la = self._input.LA(1)
            if not(_la==15 or _la==16):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 169
            self.expr()
            self.state = 170
            self.match(MiniPascalParser.DO)
            self.state = 171
            self.statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RepeatStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REPEAT(self):
            return self.getToken(MiniPascalParser.REPEAT, 0)

        def statementList(self):
            return self.getTypedRuleContext(MiniPascalParser.StatementListContext,0)


        def UNTIL(self):
            return self.getToken(MiniPascalParser.UNTIL, 0)

        def condition(self):
            return self.getTypedRuleContext(MiniPascalParser.ConditionContext,0)


        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_repeatStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRepeatStatement" ):
                listener.enterRepeatStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRepeatStatement" ):
                listener.exitRepeatStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRepeatStatement" ):
                return visitor.visitRepeatStatement(self)
            else:
                return visitor.visitChildren(self)




    def repeatStatement(self):

        localctx = MiniPascalParser.RepeatStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_repeatStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 173
            self.match(MiniPascalParser.REPEAT)
            self.state = 174
            self.statementList()
            self.state = 175
            self.match(MiniPascalParser.UNTIL)
            self.state = 176
            self.condition()
            self.state = 178
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.state = 177
                self.match(MiniPascalParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.ExprContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.ExprContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.COMMA)
            else:
                return self.getToken(MiniPascalParser.COMMA, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_argumentList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgumentList" ):
                listener.enterArgumentList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgumentList" ):
                listener.exitArgumentList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgumentList" ):
                return visitor.visitArgumentList(self)
            else:
                return visitor.visitChildren(self)




    def argumentList(self):

        localctx = MiniPascalParser.ArgumentListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 180
            self.expr()
            self.state = 185
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==24:
                self.state = 181
                self.match(MiniPascalParser.COMMA)
                self.state = 182
                self.expr()
                self.state = 187
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(MiniPascalParser.WHILE, 0)

        def condition(self):
            return self.getTypedRuleContext(MiniPascalParser.ConditionContext,0)


        def DO(self):
            return self.getToken(MiniPascalParser.DO, 0)

        def statement(self):
            return self.getTypedRuleContext(MiniPascalParser.StatementContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_whileStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhileStatement" ):
                listener.enterWhileStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhileStatement" ):
                listener.exitWhileStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStatement" ):
                return visitor.visitWhileStatement(self)
            else:
                return visitor.visitChildren(self)




    def whileStatement(self):

        localctx = MiniPascalParser.WhileStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 188
            self.match(MiniPascalParser.WHILE)
            self.state = 189
            self.condition()
            self.state = 190
            self.match(MiniPascalParser.DO)
            self.state = 191
            self.statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(MiniPascalParser.IF, 0)

        def condition(self):
            return self.getTypedRuleContext(MiniPascalParser.ConditionContext,0)


        def THEN(self):
            return self.getToken(MiniPascalParser.THEN, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.StatementContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.StatementContext,i)


        def ELSE(self):
            return self.getToken(MiniPascalParser.ELSE, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_ifStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStatement" ):
                listener.enterIfStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStatement" ):
                listener.exitIfStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStatement" ):
                return visitor.visitIfStatement(self)
            else:
                return visitor.visitChildren(self)




    def ifStatement(self):

        localctx = MiniPascalParser.IfStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 193
            self.match(MiniPascalParser.IF)
            self.state = 194
            self.condition()
            self.state = 195
            self.match(MiniPascalParser.THEN)
            self.state = 196
            self.statement()
            self.state = 199
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.state = 197
                self.match(MiniPascalParser.ELSE)
                self.state = 198
                self.statement()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.ExprContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.ExprContext,i)


        def compareOp(self):
            return self.getTypedRuleContext(MiniPascalParser.CompareOpContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_condition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondition" ):
                listener.enterCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondition" ):
                listener.exitCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondition" ):
                return visitor.visitCondition(self)
            else:
                return visitor.visitChildren(self)




    def condition(self):

        localctx = MiniPascalParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 201
            self.expr()
            self.state = 202
            self.compareOp()
            self.state = 203
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompareOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ_OP(self):
            return self.getToken(MiniPascalParser.EQ_OP, 0)

        def NE_OP(self):
            return self.getToken(MiniPascalParser.NE_OP, 0)

        def LT_OP(self):
            return self.getToken(MiniPascalParser.LT_OP, 0)

        def LE_OP(self):
            return self.getToken(MiniPascalParser.LE_OP, 0)

        def GT_OP(self):
            return self.getToken(MiniPascalParser.GT_OP, 0)

        def GE_OP(self):
            return self.getToken(MiniPascalParser.GE_OP, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_compareOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompareOp" ):
                listener.enterCompareOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompareOp" ):
                listener.exitCompareOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompareOp" ):
                return visitor.visitCompareOp(self)
            else:
                return visitor.visitChildren(self)




    def compareOp(self):

        localctx = MiniPascalParser.CompareOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_compareOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 205
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 135291469824) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompoundStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_(self):
            return self.getToken(MiniPascalParser.BEGIN_, 0)

        def statementList(self):
            return self.getTypedRuleContext(MiniPascalParser.StatementListContext,0)


        def END(self):
            return self.getToken(MiniPascalParser.END, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_compoundStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompoundStatement" ):
                listener.enterCompoundStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompoundStatement" ):
                listener.exitCompoundStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompoundStatement" ):
                return visitor.visitCompoundStatement(self)
            else:
                return visitor.visitChildren(self)




    def compoundStatement(self):

        localctx = MiniPascalParser.CompoundStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_compoundStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 207
            self.match(MiniPascalParser.BEGIN_)
            self.state = 208
            self.statementList()
            self.state = 209
            self.match(MiniPascalParser.END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def ASSIGN(self):
            return self.getToken(MiniPascalParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(MiniPascalParser.ExprContext,0)


        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = MiniPascalParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 211
            self.match(MiniPascalParser.IDENT)
            self.state = 212
            self.match(MiniPascalParser.ASSIGN)
            self.state = 213
            self.expr()
            self.state = 215
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.state = 214
                self.match(MiniPascalParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.TermContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.TermContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.PLUS)
            else:
                return self.getToken(MiniPascalParser.PLUS, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.MINUS)
            else:
                return self.getToken(MiniPascalParser.MINUS, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = MiniPascalParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 217
            self.term()
            self.state = 222
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==25 or _la==26:
                self.state = 218
                _la = self._input.LA(1)
                if not(_la==25 or _la==26):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 219
                self.term()
                self.state = 224
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def factor(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.FactorContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.FactorContext,i)


        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.STAR)
            else:
                return self.getToken(MiniPascalParser.STAR, i)

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.SLASH)
            else:
                return self.getToken(MiniPascalParser.SLASH, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_term

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerm" ):
                listener.enterTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerm" ):
                listener.exitTerm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerm" ):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = MiniPascalParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 225
            self.factor()
            self.state = 230
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==27 or _la==28:
                self.state = 226
                _la = self._input.LA(1)
                if not(_la==27 or _la==28):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 227
                self.factor()
                self.state = 232
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FactorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(MiniPascalParser.NUMBER, 0)

        def FLOATNUMBER(self):
            return self.getToken(MiniPascalParser.FLOATNUMBER, 0)

        def HEXNUMBER(self):
            return self.getToken(MiniPascalParser.HEXNUMBER, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def LPAREN(self):
            return self.getToken(MiniPascalParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(MiniPascalParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(MiniPascalParser.RPAREN, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_factor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFactor" ):
                listener.enterFactor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFactor" ):
                listener.exitFactor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFactor" ):
                return visitor.visitFactor(self)
            else:
                return visitor.visitChildren(self)




    def factor(self):

        localctx = MiniPascalParser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_factor)
        try:
            self.state = 241
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [41]:
                self.enterOuterAlt(localctx, 1)
                self.state = 233
                self.match(MiniPascalParser.NUMBER)
                pass
            elif token in [40]:
                self.enterOuterAlt(localctx, 2)
                self.state = 234
                self.match(MiniPascalParser.FLOATNUMBER)
                pass
            elif token in [39]:
                self.enterOuterAlt(localctx, 3)
                self.state = 235
                self.match(MiniPascalParser.HEXNUMBER)
                pass
            elif token in [38]:
                self.enterOuterAlt(localctx, 4)
                self.state = 236
                self.match(MiniPascalParser.IDENT)
                pass
            elif token in [29]:
                self.enterOuterAlt(localctx, 5)
                self.state = 237
                self.match(MiniPascalParser.LPAREN)
                self.state = 238
                self.expr()
                self.state = 239
                self.match(MiniPascalParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WriteLnStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WRITELN(self):
            return self.getToken(MiniPascalParser.WRITELN, 0)

        def LPAREN(self):
            return self.getToken(MiniPascalParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(MiniPascalParser.RPAREN, 0)

        def writeArgList(self):
            return self.getTypedRuleContext(MiniPascalParser.WriteArgListContext,0)


        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_writeLnStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWriteLnStatement" ):
                listener.enterWriteLnStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWriteLnStatement" ):
                listener.exitWriteLnStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWriteLnStatement" ):
                return visitor.visitWriteLnStatement(self)
            else:
                return visitor.visitChildren(self)




    def writeLnStatement(self):

        localctx = MiniPascalParser.WriteLnStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_writeLnStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 243
            self.match(MiniPascalParser.WRITELN)
            self.state = 244
            self.match(MiniPascalParser.LPAREN)
            self.state = 246
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 4261144428544) != 0):
                self.state = 245
                self.writeArgList()


            self.state = 248
            self.match(MiniPascalParser.RPAREN)
            self.state = 250
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
            if la_ == 1:
                self.state = 249
                self.match(MiniPascalParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WriteArgListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def writeArg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.WriteArgContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.WriteArgContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.COMMA)
            else:
                return self.getToken(MiniPascalParser.COMMA, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_writeArgList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWriteArgList" ):
                listener.enterWriteArgList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWriteArgList" ):
                listener.exitWriteArgList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWriteArgList" ):
                return visitor.visitWriteArgList(self)
            else:
                return visitor.visitChildren(self)




    def writeArgList(self):

        localctx = MiniPascalParser.WriteArgListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_writeArgList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 252
            self.writeArg()
            self.state = 257
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==24:
                self.state = 253
                self.match(MiniPascalParser.COMMA)
                self.state = 254
                self.writeArg()
                self.state = 259
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WriteArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(MiniPascalParser.STRING, 0)

        def expr(self):
            return self.getTypedRuleContext(MiniPascalParser.ExprContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_writeArg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWriteArg" ):
                listener.enterWriteArg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWriteArg" ):
                listener.exitWriteArg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWriteArg" ):
                return visitor.visitWriteArg(self)
            else:
                return visitor.visitChildren(self)




    def writeArg(self):

        localctx = MiniPascalParser.WriteArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_writeArg)
        try:
            self.state = 262
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [37]:
                self.enterOuterAlt(localctx, 1)
                self.state = 260
                self.match(MiniPascalParser.STRING)
                pass
            elif token in [29, 38, 39, 40, 41]:
                self.enterOuterAlt(localctx, 2)
                self.state = 261
                self.expr()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





