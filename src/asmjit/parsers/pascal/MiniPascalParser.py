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
        4,1,46,311,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,1,0,
        1,0,1,0,1,0,3,0,71,8,0,1,0,1,0,5,0,75,8,0,10,0,12,0,78,9,0,1,0,1,
        0,1,0,1,1,1,1,1,1,3,1,86,8,1,1,1,1,1,1,1,1,1,1,1,3,1,93,8,1,1,2,
        1,2,1,2,3,2,98,8,2,1,2,1,2,1,2,3,2,103,8,2,1,3,1,3,1,3,1,3,5,3,109,
        8,3,10,3,12,3,112,9,3,1,3,1,3,1,4,1,4,1,4,1,4,1,5,1,5,1,5,3,5,123,
        8,5,1,6,1,6,1,6,3,6,128,8,6,1,6,1,6,1,7,1,7,3,7,134,8,7,1,7,3,7,
        137,8,7,1,8,1,8,1,8,1,8,5,8,143,8,8,10,8,12,8,146,9,8,1,8,1,8,1,
        9,1,9,3,9,152,8,9,1,10,1,10,4,10,156,8,10,11,10,12,10,157,1,11,1,
        11,1,11,1,11,1,11,1,12,1,12,1,12,5,12,168,8,12,10,12,12,12,171,9,
        12,1,13,1,13,1,14,5,14,176,8,14,10,14,12,14,179,9,14,1,14,1,14,1,
        14,1,14,1,15,1,15,1,15,3,15,188,8,15,1,16,1,16,3,16,192,8,16,5,16,
        194,8,16,10,16,12,16,197,9,16,1,17,1,17,1,17,1,17,1,17,1,17,1,17,
        1,17,3,17,207,8,17,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,
        1,19,1,19,1,19,1,19,1,19,3,19,223,8,19,1,20,1,20,1,20,5,20,228,8,
        20,10,20,12,20,231,9,20,1,21,1,21,1,21,1,21,1,21,1,22,1,22,1,22,
        1,22,1,22,1,22,3,22,244,8,22,1,23,1,23,1,23,1,23,1,24,1,24,1,25,
        1,25,1,25,1,25,1,26,1,26,1,26,1,26,3,26,260,8,26,1,27,1,27,1,27,
        5,27,265,8,27,10,27,12,27,268,9,27,1,28,1,28,1,28,5,28,273,8,28,
        10,28,12,28,276,9,28,1,29,1,29,1,29,1,29,1,29,1,29,1,29,1,29,1,29,
        1,29,3,29,288,8,29,1,30,1,30,1,30,3,30,293,8,30,1,30,1,30,3,30,297,
        8,30,1,31,1,31,1,31,5,31,302,8,31,10,31,12,31,305,9,31,1,32,1,32,
        3,32,309,8,32,1,32,0,0,33,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,
        30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,0,6,2,0,5,
        6,39,39,1,0,15,16,1,0,32,37,2,0,19,19,39,39,1,0,26,27,1,0,28,29,
        322,0,66,1,0,0,0,2,82,1,0,0,0,4,94,1,0,0,0,6,104,1,0,0,0,8,115,1,
        0,0,0,10,122,1,0,0,0,12,124,1,0,0,0,14,131,1,0,0,0,16,138,1,0,0,
        0,18,151,1,0,0,0,20,153,1,0,0,0,22,159,1,0,0,0,24,164,1,0,0,0,26,
        172,1,0,0,0,28,177,1,0,0,0,30,187,1,0,0,0,32,195,1,0,0,0,34,206,
        1,0,0,0,36,208,1,0,0,0,38,217,1,0,0,0,40,224,1,0,0,0,42,232,1,0,
        0,0,44,237,1,0,0,0,46,245,1,0,0,0,48,249,1,0,0,0,50,251,1,0,0,0,
        52,255,1,0,0,0,54,261,1,0,0,0,56,269,1,0,0,0,58,287,1,0,0,0,60,289,
        1,0,0,0,62,298,1,0,0,0,64,308,1,0,0,0,66,67,5,1,0,0,67,68,5,39,0,
        0,68,70,5,23,0,0,69,71,3,20,10,0,70,69,1,0,0,0,70,71,1,0,0,0,71,
        76,1,0,0,0,72,75,3,4,2,0,73,75,3,2,1,0,74,72,1,0,0,0,74,73,1,0,0,
        0,75,78,1,0,0,0,76,74,1,0,0,0,76,77,1,0,0,0,77,79,1,0,0,0,78,76,
        1,0,0,0,79,80,3,28,14,0,80,81,5,24,0,0,81,1,1,0,0,0,82,83,5,18,0,
        0,83,85,5,39,0,0,84,86,3,6,3,0,85,84,1,0,0,0,85,86,1,0,0,0,86,87,
        1,0,0,0,87,88,5,22,0,0,88,89,3,26,13,0,89,90,5,23,0,0,90,92,3,28,
        14,0,91,93,5,23,0,0,92,91,1,0,0,0,92,93,1,0,0,0,93,3,1,0,0,0,94,
        95,5,17,0,0,95,97,5,39,0,0,96,98,3,6,3,0,97,96,1,0,0,0,97,98,1,0,
        0,0,98,99,1,0,0,0,99,100,5,23,0,0,100,102,3,28,14,0,101,103,5,23,
        0,0,102,101,1,0,0,0,102,103,1,0,0,0,103,5,1,0,0,0,104,105,5,30,0,
        0,105,110,3,8,4,0,106,107,5,23,0,0,107,109,3,8,4,0,108,106,1,0,0,
        0,109,112,1,0,0,0,110,108,1,0,0,0,110,111,1,0,0,0,111,113,1,0,0,
        0,112,110,1,0,0,0,113,114,5,31,0,0,114,7,1,0,0,0,115,116,3,24,12,
        0,116,117,5,22,0,0,117,118,3,26,13,0,118,9,1,0,0,0,119,123,3,20,
        10,0,120,123,3,4,2,0,121,123,3,2,1,0,122,119,1,0,0,0,122,120,1,0,
        0,0,122,121,1,0,0,0,123,11,1,0,0,0,124,125,5,39,0,0,125,127,5,30,
        0,0,126,128,3,40,20,0,127,126,1,0,0,0,127,128,1,0,0,0,128,129,1,
        0,0,0,129,130,5,31,0,0,130,13,1,0,0,0,131,133,5,39,0,0,132,134,3,
        16,8,0,133,132,1,0,0,0,133,134,1,0,0,0,134,136,1,0,0,0,135,137,5,
        23,0,0,136,135,1,0,0,0,136,137,1,0,0,0,137,15,1,0,0,0,138,139,5,
        30,0,0,139,144,3,18,9,0,140,141,5,25,0,0,141,143,3,18,9,0,142,140,
        1,0,0,0,143,146,1,0,0,0,144,142,1,0,0,0,144,145,1,0,0,0,145,147,
        1,0,0,0,146,144,1,0,0,0,147,148,5,31,0,0,148,17,1,0,0,0,149,152,
        5,38,0,0,150,152,3,54,27,0,151,149,1,0,0,0,151,150,1,0,0,0,152,19,
        1,0,0,0,153,155,5,4,0,0,154,156,3,22,11,0,155,154,1,0,0,0,156,157,
        1,0,0,0,157,155,1,0,0,0,157,158,1,0,0,0,158,21,1,0,0,0,159,160,3,
        24,12,0,160,161,5,22,0,0,161,162,3,26,13,0,162,163,5,23,0,0,163,
        23,1,0,0,0,164,169,5,39,0,0,165,166,5,25,0,0,166,168,5,39,0,0,167,
        165,1,0,0,0,168,171,1,0,0,0,169,167,1,0,0,0,169,170,1,0,0,0,170,
        25,1,0,0,0,171,169,1,0,0,0,172,173,7,0,0,0,173,27,1,0,0,0,174,176,
        3,30,15,0,175,174,1,0,0,0,176,179,1,0,0,0,177,175,1,0,0,0,177,178,
        1,0,0,0,178,180,1,0,0,0,179,177,1,0,0,0,180,181,5,2,0,0,181,182,
        3,32,16,0,182,183,5,3,0,0,183,29,1,0,0,0,184,188,3,4,2,0,185,188,
        3,2,1,0,186,188,3,20,10,0,187,184,1,0,0,0,187,185,1,0,0,0,187,186,
        1,0,0,0,188,31,1,0,0,0,189,191,3,34,17,0,190,192,5,23,0,0,191,190,
        1,0,0,0,191,192,1,0,0,0,192,194,1,0,0,0,193,189,1,0,0,0,194,197,
        1,0,0,0,195,193,1,0,0,0,195,196,1,0,0,0,196,33,1,0,0,0,197,195,1,
        0,0,0,198,207,3,52,26,0,199,207,3,60,30,0,200,207,3,44,22,0,201,
        207,3,42,21,0,202,207,3,38,19,0,203,207,3,36,18,0,204,207,3,14,7,
        0,205,207,3,50,25,0,206,198,1,0,0,0,206,199,1,0,0,0,206,200,1,0,
        0,0,206,201,1,0,0,0,206,202,1,0,0,0,206,203,1,0,0,0,206,204,1,0,
        0,0,206,205,1,0,0,0,207,35,1,0,0,0,208,209,5,14,0,0,209,210,5,39,
        0,0,210,211,5,21,0,0,211,212,3,54,27,0,212,213,7,1,0,0,213,214,3,
        54,27,0,214,215,5,11,0,0,215,216,3,34,17,0,216,37,1,0,0,0,217,218,
        5,12,0,0,218,219,3,32,16,0,219,220,5,13,0,0,220,222,3,46,23,0,221,
        223,5,23,0,0,222,221,1,0,0,0,222,223,1,0,0,0,223,39,1,0,0,0,224,
        229,3,54,27,0,225,226,5,25,0,0,226,228,3,54,27,0,227,225,1,0,0,0,
        228,231,1,0,0,0,229,227,1,0,0,0,229,230,1,0,0,0,230,41,1,0,0,0,231,
        229,1,0,0,0,232,233,5,10,0,0,233,234,3,46,23,0,234,235,5,11,0,0,
        235,236,3,34,17,0,236,43,1,0,0,0,237,238,5,7,0,0,238,239,3,46,23,
        0,239,240,5,8,0,0,240,243,3,34,17,0,241,242,5,9,0,0,242,244,3,34,
        17,0,243,241,1,0,0,0,243,244,1,0,0,0,244,45,1,0,0,0,245,246,3,54,
        27,0,246,247,3,48,24,0,247,248,3,54,27,0,248,47,1,0,0,0,249,250,
        7,2,0,0,250,49,1,0,0,0,251,252,5,2,0,0,252,253,3,32,16,0,253,254,
        5,3,0,0,254,51,1,0,0,0,255,256,7,3,0,0,256,257,5,21,0,0,257,259,
        3,54,27,0,258,260,5,23,0,0,259,258,1,0,0,0,259,260,1,0,0,0,260,53,
        1,0,0,0,261,266,3,56,28,0,262,263,7,4,0,0,263,265,3,56,28,0,264,
        262,1,0,0,0,265,268,1,0,0,0,266,264,1,0,0,0,266,267,1,0,0,0,267,
        55,1,0,0,0,268,266,1,0,0,0,269,274,3,58,29,0,270,271,7,5,0,0,271,
        273,3,58,29,0,272,270,1,0,0,0,273,276,1,0,0,0,274,272,1,0,0,0,274,
        275,1,0,0,0,275,57,1,0,0,0,276,274,1,0,0,0,277,288,5,42,0,0,278,
        288,5,41,0,0,279,288,5,40,0,0,280,288,5,38,0,0,281,288,5,39,0,0,
        282,288,3,12,6,0,283,284,5,30,0,0,284,285,3,54,27,0,285,286,5,31,
        0,0,286,288,1,0,0,0,287,277,1,0,0,0,287,278,1,0,0,0,287,279,1,0,
        0,0,287,280,1,0,0,0,287,281,1,0,0,0,287,282,1,0,0,0,287,283,1,0,
        0,0,288,59,1,0,0,0,289,290,5,20,0,0,290,292,5,30,0,0,291,293,3,62,
        31,0,292,291,1,0,0,0,292,293,1,0,0,0,293,294,1,0,0,0,294,296,5,31,
        0,0,295,297,5,23,0,0,296,295,1,0,0,0,296,297,1,0,0,0,297,61,1,0,
        0,0,298,303,3,64,32,0,299,300,5,25,0,0,300,302,3,64,32,0,301,299,
        1,0,0,0,302,305,1,0,0,0,303,301,1,0,0,0,303,304,1,0,0,0,304,63,1,
        0,0,0,305,303,1,0,0,0,306,309,5,38,0,0,307,309,3,54,27,0,308,306,
        1,0,0,0,308,307,1,0,0,0,309,65,1,0,0,0,32,70,74,76,85,92,97,102,
        110,122,127,133,136,144,151,157,169,177,187,191,195,206,222,229,
        243,259,266,274,287,292,296,303,308
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
                     "<INVALID>", "':='", "':'", "';'", "'.'", "','", "'+'", 
                     "'-'", "'*'", "'/'", "'('", "')'", "'='", "'<='", "'<>'", 
                     "'<'", "'>='", "'>'" ]

    symbolicNames = [ "<INVALID>", "PROGRAM", "BEGIN_", "END", "VAR", "DOUBLE", 
                      "INTEGER", "IF", "THEN", "ELSE", "WHILE", "DO", "REPEAT", 
                      "UNTIL", "FOR", "TO", "DOWNTO", "PROCEDURE", "FUNCTION", 
                      "RESULT", "WRITELN", "ASSIGN", "COLON", "SEMI", "DOT", 
                      "COMMA", "PLUS", "MINUS", "STAR", "SLASH", "LPAREN", 
                      "RPAREN", "EQ_OP", "LE_OP", "NE_OP", "LT_OP", "GE_OP", 
                      "GT_OP", "STRING", "IDENT", "HEXNUMBER", "FLOATNUMBER", 
                      "NUMBER", "WS", "COMMENT1", "COMMENT2", "COMMENT3" ]

    RULE_programFile = 0
    RULE_functionDeclaration = 1
    RULE_procedureDeclaration = 2
    RULE_formalParamList = 3
    RULE_formalParam = 4
    RULE_declaration = 5
    RULE_functionCallExpr = 6
    RULE_procedureCallStatement = 7
    RULE_actualParamList = 8
    RULE_actualParam = 9
    RULE_varSection = 10
    RULE_varDeclaration = 11
    RULE_identList = 12
    RULE_typeName = 13
    RULE_block = 14
    RULE_localDeclaration = 15
    RULE_statementList = 16
    RULE_statement = 17
    RULE_forStatement = 18
    RULE_repeatStatement = 19
    RULE_argumentList = 20
    RULE_whileStatement = 21
    RULE_ifStatement = 22
    RULE_condition = 23
    RULE_compareOp = 24
    RULE_compoundStatement = 25
    RULE_assignment = 26
    RULE_expr = 27
    RULE_term = 28
    RULE_factor = 29
    RULE_writeLnStatement = 30
    RULE_writeArgList = 31
    RULE_writeArg = 32

    ruleNames =  [ "programFile", "functionDeclaration", "procedureDeclaration", 
                   "formalParamList", "formalParam", "declaration", "functionCallExpr", 
                   "procedureCallStatement", "actualParamList", "actualParam", 
                   "varSection", "varDeclaration", "identList", "typeName", 
                   "block", "localDeclaration", "statementList", "statement", 
                   "forStatement", "repeatStatement", "argumentList", "whileStatement", 
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
    RESULT=19
    WRITELN=20
    ASSIGN=21
    COLON=22
    SEMI=23
    DOT=24
    COMMA=25
    PLUS=26
    MINUS=27
    STAR=28
    SLASH=29
    LPAREN=30
    RPAREN=31
    EQ_OP=32
    LE_OP=33
    NE_OP=34
    LT_OP=35
    GE_OP=36
    GT_OP=37
    STRING=38
    IDENT=39
    HEXNUMBER=40
    FLOATNUMBER=41
    NUMBER=42
    WS=43
    COMMENT1=44
    COMMENT2=45
    COMMENT3=46

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


        def functionDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.FunctionDeclarationContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.FunctionDeclarationContext,i)


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
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.match(MiniPascalParser.PROGRAM)
            self.state = 67
            self.match(MiniPascalParser.IDENT)
            self.state = 68
            self.match(MiniPascalParser.SEMI)
            self.state = 70
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 69
                self.varSection()


            self.state = 76
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 74
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [17]:
                        self.state = 72
                        self.procedureDeclaration()
                        pass
                    elif token in [18]:
                        self.state = 73
                        self.functionDeclaration()
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 78
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

            self.state = 79
            self.block()
            self.state = 80
            self.match(MiniPascalParser.DOT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNCTION(self):
            return self.getToken(MiniPascalParser.FUNCTION, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def COLON(self):
            return self.getToken(MiniPascalParser.COLON, 0)

        def typeName(self):
            return self.getTypedRuleContext(MiniPascalParser.TypeNameContext,0)


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
            return MiniPascalParser.RULE_functionDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionDeclaration" ):
                listener.enterFunctionDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionDeclaration" ):
                listener.exitFunctionDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionDeclaration" ):
                return visitor.visitFunctionDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def functionDeclaration(self):

        localctx = MiniPascalParser.FunctionDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_functionDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(MiniPascalParser.FUNCTION)
            self.state = 83
            self.match(MiniPascalParser.IDENT)
            self.state = 85
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==30:
                self.state = 84
                self.formalParamList()


            self.state = 87
            self.match(MiniPascalParser.COLON)
            self.state = 88
            self.typeName()
            self.state = 89
            self.match(MiniPascalParser.SEMI)
            self.state = 90
            self.block()
            self.state = 92
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==23:
                self.state = 91
                self.match(MiniPascalParser.SEMI)


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
        self.enterRule(localctx, 4, self.RULE_procedureDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.match(MiniPascalParser.PROCEDURE)
            self.state = 95
            self.match(MiniPascalParser.IDENT)
            self.state = 97
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==30:
                self.state = 96
                self.formalParamList()


            self.state = 99
            self.match(MiniPascalParser.SEMI)
            self.state = 100
            self.block()
            self.state = 102
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==23:
                self.state = 101
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
        self.enterRule(localctx, 6, self.RULE_formalParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            self.match(MiniPascalParser.LPAREN)
            self.state = 105
            self.formalParam()
            self.state = 110
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==23:
                self.state = 106
                self.match(MiniPascalParser.SEMI)
                self.state = 107
                self.formalParam()
                self.state = 112
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 113
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
        self.enterRule(localctx, 8, self.RULE_formalParam)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.identList()
            self.state = 116
            self.match(MiniPascalParser.COLON)
            self.state = 117
            self.typeName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varSection(self):
            return self.getTypedRuleContext(MiniPascalParser.VarSectionContext,0)


        def procedureDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.ProcedureDeclarationContext,0)


        def functionDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.FunctionDeclarationContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaration" ):
                return visitor.visitDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def declaration(self):

        localctx = MiniPascalParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_declaration)
        try:
            self.state = 122
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 119
                self.varSection()
                pass
            elif token in [17]:
                self.enterOuterAlt(localctx, 2)
                self.state = 120
                self.procedureDeclaration()
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 3)
                self.state = 121
                self.functionDeclaration()
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


    class FunctionCallExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def LPAREN(self):
            return self.getToken(MiniPascalParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(MiniPascalParser.RPAREN, 0)

        def argumentList(self):
            return self.getTypedRuleContext(MiniPascalParser.ArgumentListContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_functionCallExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCallExpr" ):
                listener.enterFunctionCallExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCallExpr" ):
                listener.exitFunctionCallExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCallExpr" ):
                return visitor.visitFunctionCallExpr(self)
            else:
                return visitor.visitChildren(self)




    def functionCallExpr(self):

        localctx = MiniPascalParser.FunctionCallExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_functionCallExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self.match(MiniPascalParser.IDENT)
            self.state = 125
            self.match(MiniPascalParser.LPAREN)
            self.state = 127
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8522288857088) != 0):
                self.state = 126
                self.argumentList()


            self.state = 129
            self.match(MiniPascalParser.RPAREN)
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
        self.enterRule(localctx, 14, self.RULE_procedureCallStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self.match(MiniPascalParser.IDENT)
            self.state = 133
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==30:
                self.state = 132
                self.actualParamList()


            self.state = 136
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.state = 135
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
        self.enterRule(localctx, 16, self.RULE_actualParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.match(MiniPascalParser.LPAREN)
            self.state = 139
            self.actualParam()
            self.state = 144
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==25:
                self.state = 140
                self.match(MiniPascalParser.COMMA)
                self.state = 141
                self.actualParam()
                self.state = 146
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 147
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
        self.enterRule(localctx, 18, self.RULE_actualParam)
        try:
            self.state = 151
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 149
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 150
                self.expr()
                pass


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
        self.enterRule(localctx, 20, self.RULE_varSection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 153
            self.match(MiniPascalParser.VAR)
            self.state = 155 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 154
                self.varDeclaration()
                self.state = 157 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==39):
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
        self.enterRule(localctx, 22, self.RULE_varDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 159
            self.identList()
            self.state = 160
            self.match(MiniPascalParser.COLON)
            self.state = 161
            self.typeName()
            self.state = 162
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
        self.enterRule(localctx, 24, self.RULE_identList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 164
            self.match(MiniPascalParser.IDENT)
            self.state = 169
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==25:
                self.state = 165
                self.match(MiniPascalParser.COMMA)
                self.state = 166
                self.match(MiniPascalParser.IDENT)
                self.state = 171
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
        self.enterRule(localctx, 26, self.RULE_typeName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 172
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 549755813984) != 0)):
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

        def localDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.LocalDeclarationContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.LocalDeclarationContext,i)


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
        self.enterRule(localctx, 28, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 177
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 393232) != 0):
                self.state = 174
                self.localDeclaration()
                self.state = 179
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 180
            self.match(MiniPascalParser.BEGIN_)
            self.state = 181
            self.statementList()
            self.state = 182
            self.match(MiniPascalParser.END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LocalDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def procedureDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.ProcedureDeclarationContext,0)


        def functionDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.FunctionDeclarationContext,0)


        def varSection(self):
            return self.getTypedRuleContext(MiniPascalParser.VarSectionContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_localDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLocalDeclaration" ):
                listener.enterLocalDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLocalDeclaration" ):
                listener.exitLocalDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLocalDeclaration" ):
                return visitor.visitLocalDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def localDeclaration(self):

        localctx = MiniPascalParser.LocalDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_localDeclaration)
        try:
            self.state = 187
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                self.enterOuterAlt(localctx, 1)
                self.state = 184
                self.procedureDeclaration()
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 2)
                self.state = 185
                self.functionDeclaration()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 3)
                self.state = 186
                self.varSection()
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
        self.enterRule(localctx, 32, self.RULE_statementList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 195
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 549757408388) != 0):
                self.state = 189
                self.statement()
                self.state = 191
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==23:
                    self.state = 190
                    self.match(MiniPascalParser.SEMI)


                self.state = 197
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
        self.enterRule(localctx, 34, self.RULE_statement)
        try:
            self.state = 206
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 198
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 199
                self.writeLnStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 200
                self.ifStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 201
                self.whileStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 202
                self.repeatStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 203
                self.forStatement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 204
                self.procedureCallStatement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 205
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
        self.enterRule(localctx, 36, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 208
            self.match(MiniPascalParser.FOR)
            self.state = 209
            self.match(MiniPascalParser.IDENT)
            self.state = 210
            self.match(MiniPascalParser.ASSIGN)
            self.state = 211
            self.expr()
            self.state = 212
            _la = self._input.LA(1)
            if not(_la==15 or _la==16):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 213
            self.expr()
            self.state = 214
            self.match(MiniPascalParser.DO)
            self.state = 215
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
        self.enterRule(localctx, 38, self.RULE_repeatStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 217
            self.match(MiniPascalParser.REPEAT)
            self.state = 218
            self.statementList()
            self.state = 219
            self.match(MiniPascalParser.UNTIL)
            self.state = 220
            self.condition()
            self.state = 222
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.state = 221
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
        self.enterRule(localctx, 40, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 224
            self.expr()
            self.state = 229
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==25:
                self.state = 225
                self.match(MiniPascalParser.COMMA)
                self.state = 226
                self.expr()
                self.state = 231
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
        self.enterRule(localctx, 42, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 232
            self.match(MiniPascalParser.WHILE)
            self.state = 233
            self.condition()
            self.state = 234
            self.match(MiniPascalParser.DO)
            self.state = 235
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
        self.enterRule(localctx, 44, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 237
            self.match(MiniPascalParser.IF)
            self.state = 238
            self.condition()
            self.state = 239
            self.match(MiniPascalParser.THEN)
            self.state = 240
            self.statement()
            self.state = 243
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
            if la_ == 1:
                self.state = 241
                self.match(MiniPascalParser.ELSE)
                self.state = 242
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
        self.enterRule(localctx, 46, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 245
            self.expr()
            self.state = 246
            self.compareOp()
            self.state = 247
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
        self.enterRule(localctx, 48, self.RULE_compareOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 249
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 270582939648) != 0)):
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
        self.enterRule(localctx, 50, self.RULE_compoundStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 251
            self.match(MiniPascalParser.BEGIN_)
            self.state = 252
            self.statementList()
            self.state = 253
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

        def ASSIGN(self):
            return self.getToken(MiniPascalParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(MiniPascalParser.ExprContext,0)


        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def RESULT(self):
            return self.getToken(MiniPascalParser.RESULT, 0)

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
        self.enterRule(localctx, 52, self.RULE_assignment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 255
            _la = self._input.LA(1)
            if not(_la==19 or _la==39):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 256
            self.match(MiniPascalParser.ASSIGN)
            self.state = 257
            self.expr()
            self.state = 259
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,24,self._ctx)
            if la_ == 1:
                self.state = 258
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
        self.enterRule(localctx, 54, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 261
            self.term()
            self.state = 266
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==26 or _la==27:
                self.state = 262
                _la = self._input.LA(1)
                if not(_la==26 or _la==27):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 263
                self.term()
                self.state = 268
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
        self.enterRule(localctx, 56, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 269
            self.factor()
            self.state = 274
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==28 or _la==29:
                self.state = 270
                _la = self._input.LA(1)
                if not(_la==28 or _la==29):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 271
                self.factor()
                self.state = 276
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

        def STRING(self):
            return self.getToken(MiniPascalParser.STRING, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def functionCallExpr(self):
            return self.getTypedRuleContext(MiniPascalParser.FunctionCallExprContext,0)


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
        self.enterRule(localctx, 58, self.RULE_factor)
        try:
            self.state = 287
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,27,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 277
                self.match(MiniPascalParser.NUMBER)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 278
                self.match(MiniPascalParser.FLOATNUMBER)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 279
                self.match(MiniPascalParser.HEXNUMBER)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 280
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 281
                self.match(MiniPascalParser.IDENT)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 282
                self.functionCallExpr()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 283
                self.match(MiniPascalParser.LPAREN)
                self.state = 284
                self.expr()
                self.state = 285
                self.match(MiniPascalParser.RPAREN)
                pass


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
        self.enterRule(localctx, 60, self.RULE_writeLnStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 289
            self.match(MiniPascalParser.WRITELN)
            self.state = 290
            self.match(MiniPascalParser.LPAREN)
            self.state = 292
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8522288857088) != 0):
                self.state = 291
                self.writeArgList()


            self.state = 294
            self.match(MiniPascalParser.RPAREN)
            self.state = 296
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,29,self._ctx)
            if la_ == 1:
                self.state = 295
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
        self.enterRule(localctx, 62, self.RULE_writeArgList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 298
            self.writeArg()
            self.state = 303
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==25:
                self.state = 299
                self.match(MiniPascalParser.COMMA)
                self.state = 300
                self.writeArg()
                self.state = 305
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
        self.enterRule(localctx, 64, self.RULE_writeArg)
        try:
            self.state = 308
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,31,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 306
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 307
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





