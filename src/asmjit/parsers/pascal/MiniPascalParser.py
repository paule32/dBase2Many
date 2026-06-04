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
        4,1,47,335,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,1,0,1,0,1,0,1,0,5,0,79,8,0,10,
        0,12,0,82,9,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,3,1,91,8,1,1,2,1,2,4,2,
        95,8,2,11,2,12,2,96,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,5,1,5,1,5,3,5,
        109,8,5,1,5,1,5,1,5,1,5,1,5,3,5,116,8,5,1,6,1,6,1,6,3,6,121,8,6,
        1,6,1,6,1,6,3,6,126,8,6,1,7,1,7,1,7,1,7,5,7,132,8,7,10,7,12,7,135,
        9,7,1,7,1,7,1,8,1,8,1,8,1,8,1,9,1,9,1,9,3,9,146,8,9,1,10,1,10,1,
        10,3,10,151,8,10,1,10,1,10,1,11,1,11,3,11,157,8,11,1,11,3,11,160,
        8,11,1,12,1,12,1,12,1,12,5,12,166,8,12,10,12,12,12,169,9,12,1,12,
        1,12,1,13,1,13,3,13,175,8,13,1,14,1,14,4,14,179,8,14,11,14,12,14,
        180,1,15,1,15,1,15,1,15,1,15,1,16,1,16,1,16,5,16,191,8,16,10,16,
        12,16,194,9,16,1,17,1,17,1,18,5,18,199,8,18,10,18,12,18,202,9,18,
        1,18,1,18,1,18,1,18,1,19,1,19,1,19,1,19,3,19,212,8,19,1,20,1,20,
        3,20,216,8,20,5,20,218,8,20,10,20,12,20,221,9,20,1,21,1,21,1,21,
        1,21,1,21,1,21,1,21,1,21,3,21,231,8,21,1,22,1,22,1,22,1,22,1,22,
        1,22,1,22,1,22,1,22,1,23,1,23,1,23,1,23,1,23,3,23,247,8,23,1,24,
        1,24,1,24,5,24,252,8,24,10,24,12,24,255,9,24,1,25,1,25,1,25,1,25,
        1,25,1,26,1,26,1,26,1,26,1,26,1,26,3,26,268,8,26,1,27,1,27,1,27,
        1,27,1,28,1,28,1,29,1,29,1,29,1,29,1,30,1,30,1,30,1,30,3,30,284,
        8,30,1,31,1,31,1,31,5,31,289,8,31,10,31,12,31,292,9,31,1,32,1,32,
        1,32,5,32,297,8,32,10,32,12,32,300,9,32,1,33,1,33,1,33,1,33,1,33,
        1,33,1,33,1,33,1,33,1,33,3,33,312,8,33,1,34,1,34,1,34,1,34,3,34,
        318,8,34,1,34,3,34,321,8,34,1,35,1,35,1,35,5,35,326,8,35,10,35,12,
        35,329,9,35,1,36,1,36,3,36,333,8,36,1,36,0,0,37,0,2,4,6,8,10,12,
        14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,
        58,60,62,64,66,68,70,72,0,7,2,0,39,39,42,43,2,0,6,7,40,40,1,0,16,
        17,1,0,33,38,2,0,20,20,40,40,1,0,27,28,1,0,29,30,345,0,74,1,0,0,
        0,2,90,1,0,0,0,4,92,1,0,0,0,6,98,1,0,0,0,8,103,1,0,0,0,10,105,1,
        0,0,0,12,117,1,0,0,0,14,127,1,0,0,0,16,138,1,0,0,0,18,145,1,0,0,
        0,20,147,1,0,0,0,22,154,1,0,0,0,24,161,1,0,0,0,26,174,1,0,0,0,28,
        176,1,0,0,0,30,182,1,0,0,0,32,187,1,0,0,0,34,195,1,0,0,0,36,200,
        1,0,0,0,38,211,1,0,0,0,40,219,1,0,0,0,42,230,1,0,0,0,44,232,1,0,
        0,0,46,241,1,0,0,0,48,248,1,0,0,0,50,256,1,0,0,0,52,261,1,0,0,0,
        54,269,1,0,0,0,56,273,1,0,0,0,58,275,1,0,0,0,60,279,1,0,0,0,62,285,
        1,0,0,0,64,293,1,0,0,0,66,311,1,0,0,0,68,320,1,0,0,0,70,322,1,0,
        0,0,72,332,1,0,0,0,74,75,5,1,0,0,75,76,5,40,0,0,76,80,5,24,0,0,77,
        79,3,2,1,0,78,77,1,0,0,0,79,82,1,0,0,0,80,78,1,0,0,0,80,81,1,0,0,
        0,81,83,1,0,0,0,82,80,1,0,0,0,83,84,3,36,18,0,84,85,5,25,0,0,85,
        1,1,0,0,0,86,91,3,4,2,0,87,91,3,28,14,0,88,91,3,12,6,0,89,91,3,10,
        5,0,90,86,1,0,0,0,90,87,1,0,0,0,90,88,1,0,0,0,90,89,1,0,0,0,91,3,
        1,0,0,0,92,94,5,4,0,0,93,95,3,6,3,0,94,93,1,0,0,0,95,96,1,0,0,0,
        96,94,1,0,0,0,96,97,1,0,0,0,97,5,1,0,0,0,98,99,5,40,0,0,99,100,5,
        33,0,0,100,101,3,8,4,0,101,102,5,24,0,0,102,7,1,0,0,0,103,104,7,
        0,0,0,104,9,1,0,0,0,105,106,5,19,0,0,106,108,5,40,0,0,107,109,3,
        14,7,0,108,107,1,0,0,0,108,109,1,0,0,0,109,110,1,0,0,0,110,111,5,
        23,0,0,111,112,3,34,17,0,112,113,5,24,0,0,113,115,3,36,18,0,114,
        116,5,24,0,0,115,114,1,0,0,0,115,116,1,0,0,0,116,11,1,0,0,0,117,
        118,5,18,0,0,118,120,5,40,0,0,119,121,3,14,7,0,120,119,1,0,0,0,120,
        121,1,0,0,0,121,122,1,0,0,0,122,123,5,24,0,0,123,125,3,36,18,0,124,
        126,5,24,0,0,125,124,1,0,0,0,125,126,1,0,0,0,126,13,1,0,0,0,127,
        128,5,31,0,0,128,133,3,16,8,0,129,130,5,24,0,0,130,132,3,16,8,0,
        131,129,1,0,0,0,132,135,1,0,0,0,133,131,1,0,0,0,133,134,1,0,0,0,
        134,136,1,0,0,0,135,133,1,0,0,0,136,137,5,32,0,0,137,15,1,0,0,0,
        138,139,3,32,16,0,139,140,5,23,0,0,140,141,3,34,17,0,141,17,1,0,
        0,0,142,146,3,28,14,0,143,146,3,12,6,0,144,146,3,10,5,0,145,142,
        1,0,0,0,145,143,1,0,0,0,145,144,1,0,0,0,146,19,1,0,0,0,147,148,5,
        40,0,0,148,150,5,31,0,0,149,151,3,48,24,0,150,149,1,0,0,0,150,151,
        1,0,0,0,151,152,1,0,0,0,152,153,5,32,0,0,153,21,1,0,0,0,154,156,
        5,40,0,0,155,157,3,24,12,0,156,155,1,0,0,0,156,157,1,0,0,0,157,159,
        1,0,0,0,158,160,5,24,0,0,159,158,1,0,0,0,159,160,1,0,0,0,160,23,
        1,0,0,0,161,162,5,31,0,0,162,167,3,26,13,0,163,164,5,26,0,0,164,
        166,3,26,13,0,165,163,1,0,0,0,166,169,1,0,0,0,167,165,1,0,0,0,167,
        168,1,0,0,0,168,170,1,0,0,0,169,167,1,0,0,0,170,171,5,32,0,0,171,
        25,1,0,0,0,172,175,5,39,0,0,173,175,3,62,31,0,174,172,1,0,0,0,174,
        173,1,0,0,0,175,27,1,0,0,0,176,178,5,5,0,0,177,179,3,30,15,0,178,
        177,1,0,0,0,179,180,1,0,0,0,180,178,1,0,0,0,180,181,1,0,0,0,181,
        29,1,0,0,0,182,183,3,32,16,0,183,184,5,23,0,0,184,185,3,34,17,0,
        185,186,5,24,0,0,186,31,1,0,0,0,187,192,5,40,0,0,188,189,5,26,0,
        0,189,191,5,40,0,0,190,188,1,0,0,0,191,194,1,0,0,0,192,190,1,0,0,
        0,192,193,1,0,0,0,193,33,1,0,0,0,194,192,1,0,0,0,195,196,7,1,0,0,
        196,35,1,0,0,0,197,199,3,38,19,0,198,197,1,0,0,0,199,202,1,0,0,0,
        200,198,1,0,0,0,200,201,1,0,0,0,201,203,1,0,0,0,202,200,1,0,0,0,
        203,204,5,2,0,0,204,205,3,40,20,0,205,206,5,3,0,0,206,37,1,0,0,0,
        207,212,3,12,6,0,208,212,3,10,5,0,209,212,3,28,14,0,210,212,3,4,
        2,0,211,207,1,0,0,0,211,208,1,0,0,0,211,209,1,0,0,0,211,210,1,0,
        0,0,212,39,1,0,0,0,213,215,3,42,21,0,214,216,5,24,0,0,215,214,1,
        0,0,0,215,216,1,0,0,0,216,218,1,0,0,0,217,213,1,0,0,0,218,221,1,
        0,0,0,219,217,1,0,0,0,219,220,1,0,0,0,220,41,1,0,0,0,221,219,1,0,
        0,0,222,231,3,60,30,0,223,231,3,68,34,0,224,231,3,52,26,0,225,231,
        3,50,25,0,226,231,3,46,23,0,227,231,3,44,22,0,228,231,3,22,11,0,
        229,231,3,58,29,0,230,222,1,0,0,0,230,223,1,0,0,0,230,224,1,0,0,
        0,230,225,1,0,0,0,230,226,1,0,0,0,230,227,1,0,0,0,230,228,1,0,0,
        0,230,229,1,0,0,0,231,43,1,0,0,0,232,233,5,15,0,0,233,234,5,40,0,
        0,234,235,5,22,0,0,235,236,3,62,31,0,236,237,7,2,0,0,237,238,3,62,
        31,0,238,239,5,12,0,0,239,240,3,42,21,0,240,45,1,0,0,0,241,242,5,
        13,0,0,242,243,3,40,20,0,243,244,5,14,0,0,244,246,3,54,27,0,245,
        247,5,24,0,0,246,245,1,0,0,0,246,247,1,0,0,0,247,47,1,0,0,0,248,
        253,3,62,31,0,249,250,5,26,0,0,250,252,3,62,31,0,251,249,1,0,0,0,
        252,255,1,0,0,0,253,251,1,0,0,0,253,254,1,0,0,0,254,49,1,0,0,0,255,
        253,1,0,0,0,256,257,5,11,0,0,257,258,3,54,27,0,258,259,5,12,0,0,
        259,260,3,42,21,0,260,51,1,0,0,0,261,262,5,8,0,0,262,263,3,54,27,
        0,263,264,5,9,0,0,264,267,3,42,21,0,265,266,5,10,0,0,266,268,3,42,
        21,0,267,265,1,0,0,0,267,268,1,0,0,0,268,53,1,0,0,0,269,270,3,62,
        31,0,270,271,3,56,28,0,271,272,3,62,31,0,272,55,1,0,0,0,273,274,
        7,3,0,0,274,57,1,0,0,0,275,276,5,2,0,0,276,277,3,40,20,0,277,278,
        5,3,0,0,278,59,1,0,0,0,279,280,7,4,0,0,280,281,5,22,0,0,281,283,
        3,62,31,0,282,284,5,24,0,0,283,282,1,0,0,0,283,284,1,0,0,0,284,61,
        1,0,0,0,285,290,3,64,32,0,286,287,7,5,0,0,287,289,3,64,32,0,288,
        286,1,0,0,0,289,292,1,0,0,0,290,288,1,0,0,0,290,291,1,0,0,0,291,
        63,1,0,0,0,292,290,1,0,0,0,293,298,3,66,33,0,294,295,7,6,0,0,295,
        297,3,66,33,0,296,294,1,0,0,0,297,300,1,0,0,0,298,296,1,0,0,0,298,
        299,1,0,0,0,299,65,1,0,0,0,300,298,1,0,0,0,301,312,5,43,0,0,302,
        312,5,42,0,0,303,312,5,41,0,0,304,312,5,39,0,0,305,312,5,40,0,0,
        306,312,3,20,10,0,307,308,5,31,0,0,308,309,3,62,31,0,309,310,5,32,
        0,0,310,312,1,0,0,0,311,301,1,0,0,0,311,302,1,0,0,0,311,303,1,0,
        0,0,311,304,1,0,0,0,311,305,1,0,0,0,311,306,1,0,0,0,311,307,1,0,
        0,0,312,67,1,0,0,0,313,321,5,21,0,0,314,315,5,21,0,0,315,317,5,31,
        0,0,316,318,3,70,35,0,317,316,1,0,0,0,317,318,1,0,0,0,318,319,1,
        0,0,0,319,321,5,32,0,0,320,313,1,0,0,0,320,314,1,0,0,0,321,69,1,
        0,0,0,322,327,3,72,36,0,323,324,5,26,0,0,324,326,3,72,36,0,325,323,
        1,0,0,0,326,329,1,0,0,0,327,325,1,0,0,0,327,328,1,0,0,0,328,71,1,
        0,0,0,329,327,1,0,0,0,330,333,5,39,0,0,331,333,3,62,31,0,332,330,
        1,0,0,0,332,331,1,0,0,0,333,73,1,0,0,0,32,80,90,96,108,115,120,125,
        133,145,150,156,159,167,174,180,192,200,211,215,219,230,246,253,
        267,283,290,298,311,317,320,327,332
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
                     "<INVALID>", "<INVALID>", "':='", "':'", "';'", "'.'", 
                     "','", "'+'", "'-'", "'*'", "'/'", "'('", "')'", "'='", 
                     "'<='", "'<>'", "'<'", "'>='", "'>'" ]

    symbolicNames = [ "<INVALID>", "PROGRAM", "BEGIN_", "END", "CONST", 
                      "VAR", "DOUBLE", "INTEGER", "IF", "THEN", "ELSE", 
                      "WHILE", "DO", "REPEAT", "UNTIL", "FOR", "TO", "DOWNTO", 
                      "PROCEDURE", "FUNCTION", "RESULT", "WRITELN", "ASSIGN", 
                      "COLON", "SEMI", "DOT", "COMMA", "PLUS", "MINUS", 
                      "STAR", "SLASH", "LPAREN", "RPAREN", "EQ_OP", "LE_OP", 
                      "NE_OP", "LT_OP", "GE_OP", "GT_OP", "STRING", "IDENT", 
                      "HEXNUMBER", "FLOATNUMBER", "NUMBER", "WS", "COMMENT1", 
                      "COMMENT2", "COMMENT3" ]

    RULE_programFile = 0
    RULE_declarationPart = 1
    RULE_constSection = 2
    RULE_constDeclaration = 3
    RULE_constValue = 4
    RULE_functionDeclaration = 5
    RULE_procedureDeclaration = 6
    RULE_formalParamList = 7
    RULE_formalParam = 8
    RULE_declaration = 9
    RULE_functionCallExpr = 10
    RULE_procedureCallStatement = 11
    RULE_actualParamList = 12
    RULE_actualParam = 13
    RULE_varSection = 14
    RULE_varDeclaration = 15
    RULE_identList = 16
    RULE_typeName = 17
    RULE_block = 18
    RULE_localDeclaration = 19
    RULE_statementList = 20
    RULE_statement = 21
    RULE_forStatement = 22
    RULE_repeatStatement = 23
    RULE_argumentList = 24
    RULE_whileStatement = 25
    RULE_ifStatement = 26
    RULE_condition = 27
    RULE_compareOp = 28
    RULE_compoundStatement = 29
    RULE_assignment = 30
    RULE_expr = 31
    RULE_term = 32
    RULE_factor = 33
    RULE_writeLnStatement = 34
    RULE_writeArgList = 35
    RULE_writeArg = 36

    ruleNames =  [ "programFile", "declarationPart", "constSection", "constDeclaration", 
                   "constValue", "functionDeclaration", "procedureDeclaration", 
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
    CONST=4
    VAR=5
    DOUBLE=6
    INTEGER=7
    IF=8
    THEN=9
    ELSE=10
    WHILE=11
    DO=12
    REPEAT=13
    UNTIL=14
    FOR=15
    TO=16
    DOWNTO=17
    PROCEDURE=18
    FUNCTION=19
    RESULT=20
    WRITELN=21
    ASSIGN=22
    COLON=23
    SEMI=24
    DOT=25
    COMMA=26
    PLUS=27
    MINUS=28
    STAR=29
    SLASH=30
    LPAREN=31
    RPAREN=32
    EQ_OP=33
    LE_OP=34
    NE_OP=35
    LT_OP=36
    GE_OP=37
    GT_OP=38
    STRING=39
    IDENT=40
    HEXNUMBER=41
    FLOATNUMBER=42
    NUMBER=43
    WS=44
    COMMENT1=45
    COMMENT2=46
    COMMENT3=47

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

        def declarationPart(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.DeclarationPartContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.DeclarationPartContext,i)


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
            self.state = 74
            self.match(MiniPascalParser.PROGRAM)
            self.state = 75
            self.match(MiniPascalParser.IDENT)
            self.state = 76
            self.match(MiniPascalParser.SEMI)
            self.state = 80
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 77
                    self.declarationPart() 
                self.state = 82
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 83
            self.block()
            self.state = 84
            self.match(MiniPascalParser.DOT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationPartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def constSection(self):
            return self.getTypedRuleContext(MiniPascalParser.ConstSectionContext,0)


        def varSection(self):
            return self.getTypedRuleContext(MiniPascalParser.VarSectionContext,0)


        def procedureDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.ProcedureDeclarationContext,0)


        def functionDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.FunctionDeclarationContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_declarationPart

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclarationPart" ):
                listener.enterDeclarationPart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclarationPart" ):
                listener.exitDeclarationPart(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclarationPart" ):
                return visitor.visitDeclarationPart(self)
            else:
                return visitor.visitChildren(self)




    def declarationPart(self):

        localctx = MiniPascalParser.DeclarationPartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_declarationPart)
        try:
            self.state = 90
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 86
                self.constSection()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 87
                self.varSection()
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 3)
                self.state = 88
                self.procedureDeclaration()
                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 4)
                self.state = 89
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


    class ConstSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONST(self):
            return self.getToken(MiniPascalParser.CONST, 0)

        def constDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.ConstDeclarationContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.ConstDeclarationContext,i)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_constSection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstSection" ):
                listener.enterConstSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstSection" ):
                listener.exitConstSection(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstSection" ):
                return visitor.visitConstSection(self)
            else:
                return visitor.visitChildren(self)




    def constSection(self):

        localctx = MiniPascalParser.ConstSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_constSection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 92
            self.match(MiniPascalParser.CONST)
            self.state = 94 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 93
                self.constDeclaration()
                self.state = 96 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==40):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def EQ_OP(self):
            return self.getToken(MiniPascalParser.EQ_OP, 0)

        def constValue(self):
            return self.getTypedRuleContext(MiniPascalParser.ConstValueContext,0)


        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_constDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstDeclaration" ):
                listener.enterConstDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstDeclaration" ):
                listener.exitConstDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstDeclaration" ):
                return visitor.visitConstDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def constDeclaration(self):

        localctx = MiniPascalParser.ConstDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_constDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 98
            self.match(MiniPascalParser.IDENT)
            self.state = 99
            self.match(MiniPascalParser.EQ_OP)
            self.state = 100
            self.constValue()
            self.state = 101
            self.match(MiniPascalParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(MiniPascalParser.STRING, 0)

        def FLOATNUMBER(self):
            return self.getToken(MiniPascalParser.FLOATNUMBER, 0)

        def NUMBER(self):
            return self.getToken(MiniPascalParser.NUMBER, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_constValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstValue" ):
                listener.enterConstValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstValue" ):
                listener.exitConstValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstValue" ):
                return visitor.visitConstValue(self)
            else:
                return visitor.visitChildren(self)




    def constValue(self):

        localctx = MiniPascalParser.ConstValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_constValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 103
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 13743895347200) != 0)):
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
        self.enterRule(localctx, 10, self.RULE_functionDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            self.match(MiniPascalParser.FUNCTION)
            self.state = 106
            self.match(MiniPascalParser.IDENT)
            self.state = 108
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==31:
                self.state = 107
                self.formalParamList()


            self.state = 110
            self.match(MiniPascalParser.COLON)
            self.state = 111
            self.typeName()
            self.state = 112
            self.match(MiniPascalParser.SEMI)
            self.state = 113
            self.block()
            self.state = 115
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==24:
                self.state = 114
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
        self.enterRule(localctx, 12, self.RULE_procedureDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 117
            self.match(MiniPascalParser.PROCEDURE)
            self.state = 118
            self.match(MiniPascalParser.IDENT)
            self.state = 120
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==31:
                self.state = 119
                self.formalParamList()


            self.state = 122
            self.match(MiniPascalParser.SEMI)
            self.state = 123
            self.block()
            self.state = 125
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==24:
                self.state = 124
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
        self.enterRule(localctx, 14, self.RULE_formalParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 127
            self.match(MiniPascalParser.LPAREN)
            self.state = 128
            self.formalParam()
            self.state = 133
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==24:
                self.state = 129
                self.match(MiniPascalParser.SEMI)
                self.state = 130
                self.formalParam()
                self.state = 135
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 136
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
        self.enterRule(localctx, 16, self.RULE_formalParam)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.identList()
            self.state = 139
            self.match(MiniPascalParser.COLON)
            self.state = 140
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
        self.enterRule(localctx, 18, self.RULE_declaration)
        try:
            self.state = 145
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 142
                self.varSection()
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 2)
                self.state = 143
                self.procedureDeclaration()
                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 3)
                self.state = 144
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
        self.enterRule(localctx, 20, self.RULE_functionCallExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            self.match(MiniPascalParser.IDENT)
            self.state = 148
            self.match(MiniPascalParser.LPAREN)
            self.state = 150
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17044577714176) != 0):
                self.state = 149
                self.argumentList()


            self.state = 152
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
        self.enterRule(localctx, 22, self.RULE_procedureCallStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 154
            self.match(MiniPascalParser.IDENT)
            self.state = 156
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==31:
                self.state = 155
                self.actualParamList()


            self.state = 159
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.state = 158
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
        self.enterRule(localctx, 24, self.RULE_actualParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 161
            self.match(MiniPascalParser.LPAREN)
            self.state = 162
            self.actualParam()
            self.state = 167
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==26:
                self.state = 163
                self.match(MiniPascalParser.COMMA)
                self.state = 164
                self.actualParam()
                self.state = 169
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 170
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
        self.enterRule(localctx, 26, self.RULE_actualParam)
        try:
            self.state = 174
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 172
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 173
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
        self.enterRule(localctx, 28, self.RULE_varSection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 176
            self.match(MiniPascalParser.VAR)
            self.state = 178 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 177
                self.varDeclaration()
                self.state = 180 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==40):
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
        self.enterRule(localctx, 30, self.RULE_varDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 182
            self.identList()
            self.state = 183
            self.match(MiniPascalParser.COLON)
            self.state = 184
            self.typeName()
            self.state = 185
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
        self.enterRule(localctx, 32, self.RULE_identList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 187
            self.match(MiniPascalParser.IDENT)
            self.state = 192
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==26:
                self.state = 188
                self.match(MiniPascalParser.COMMA)
                self.state = 189
                self.match(MiniPascalParser.IDENT)
                self.state = 194
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
        self.enterRule(localctx, 34, self.RULE_typeName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 195
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1099511627968) != 0)):
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
        self.enterRule(localctx, 36, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 786480) != 0):
                self.state = 197
                self.localDeclaration()
                self.state = 202
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 203
            self.match(MiniPascalParser.BEGIN_)
            self.state = 204
            self.statementList()
            self.state = 205
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


        def constSection(self):
            return self.getTypedRuleContext(MiniPascalParser.ConstSectionContext,0)


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
        self.enterRule(localctx, 38, self.RULE_localDeclaration)
        try:
            self.state = 211
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [18]:
                self.enterOuterAlt(localctx, 1)
                self.state = 207
                self.procedureDeclaration()
                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 2)
                self.state = 208
                self.functionDeclaration()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 209
                self.varSection()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 210
                self.constSection()
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
        self.enterRule(localctx, 40, self.RULE_statementList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 219
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1099514816772) != 0):
                self.state = 213
                self.statement()
                self.state = 215
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==24:
                    self.state = 214
                    self.match(MiniPascalParser.SEMI)


                self.state = 221
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
        self.enterRule(localctx, 42, self.RULE_statement)
        try:
            self.state = 230
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 222
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 223
                self.writeLnStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 224
                self.ifStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 225
                self.whileStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 226
                self.repeatStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 227
                self.forStatement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 228
                self.procedureCallStatement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 229
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
        self.enterRule(localctx, 44, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 232
            self.match(MiniPascalParser.FOR)
            self.state = 233
            self.match(MiniPascalParser.IDENT)
            self.state = 234
            self.match(MiniPascalParser.ASSIGN)
            self.state = 235
            self.expr()
            self.state = 236
            _la = self._input.LA(1)
            if not(_la==16 or _la==17):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 237
            self.expr()
            self.state = 238
            self.match(MiniPascalParser.DO)
            self.state = 239
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
        self.enterRule(localctx, 46, self.RULE_repeatStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 241
            self.match(MiniPascalParser.REPEAT)
            self.state = 242
            self.statementList()
            self.state = 243
            self.match(MiniPascalParser.UNTIL)
            self.state = 244
            self.condition()
            self.state = 246
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.state = 245
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
        self.enterRule(localctx, 48, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 248
            self.expr()
            self.state = 253
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==26:
                self.state = 249
                self.match(MiniPascalParser.COMMA)
                self.state = 250
                self.expr()
                self.state = 255
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
        self.enterRule(localctx, 50, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 256
            self.match(MiniPascalParser.WHILE)
            self.state = 257
            self.condition()
            self.state = 258
            self.match(MiniPascalParser.DO)
            self.state = 259
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
        self.enterRule(localctx, 52, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 261
            self.match(MiniPascalParser.IF)
            self.state = 262
            self.condition()
            self.state = 263
            self.match(MiniPascalParser.THEN)
            self.state = 264
            self.statement()
            self.state = 267
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
            if la_ == 1:
                self.state = 265
                self.match(MiniPascalParser.ELSE)
                self.state = 266
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
        self.enterRule(localctx, 54, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 269
            self.expr()
            self.state = 270
            self.compareOp()
            self.state = 271
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
        self.enterRule(localctx, 56, self.RULE_compareOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 273
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 541165879296) != 0)):
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
        self.enterRule(localctx, 58, self.RULE_compoundStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 275
            self.match(MiniPascalParser.BEGIN_)
            self.state = 276
            self.statementList()
            self.state = 277
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
        self.enterRule(localctx, 60, self.RULE_assignment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 279
            _la = self._input.LA(1)
            if not(_la==20 or _la==40):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 280
            self.match(MiniPascalParser.ASSIGN)
            self.state = 281
            self.expr()
            self.state = 283
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,24,self._ctx)
            if la_ == 1:
                self.state = 282
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
        self.enterRule(localctx, 62, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 285
            self.term()
            self.state = 290
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==27 or _la==28:
                self.state = 286
                _la = self._input.LA(1)
                if not(_la==27 or _la==28):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 287
                self.term()
                self.state = 292
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
        self.enterRule(localctx, 64, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 293
            self.factor()
            self.state = 298
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==29 or _la==30:
                self.state = 294
                _la = self._input.LA(1)
                if not(_la==29 or _la==30):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 295
                self.factor()
                self.state = 300
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
        self.enterRule(localctx, 66, self.RULE_factor)
        try:
            self.state = 311
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,27,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 301
                self.match(MiniPascalParser.NUMBER)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 302
                self.match(MiniPascalParser.FLOATNUMBER)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 303
                self.match(MiniPascalParser.HEXNUMBER)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 304
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 305
                self.match(MiniPascalParser.IDENT)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 306
                self.functionCallExpr()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 307
                self.match(MiniPascalParser.LPAREN)
                self.state = 308
                self.expr()
                self.state = 309
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
        self.enterRule(localctx, 68, self.RULE_writeLnStatement)
        self._la = 0 # Token type
        try:
            self.state = 320
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,29,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 313
                self.match(MiniPascalParser.WRITELN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 314
                self.match(MiniPascalParser.WRITELN)
                self.state = 315
                self.match(MiniPascalParser.LPAREN)
                self.state = 317
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17044577714176) != 0):
                    self.state = 316
                    self.writeArgList()


                self.state = 319
                self.match(MiniPascalParser.RPAREN)
                pass


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
        self.enterRule(localctx, 70, self.RULE_writeArgList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 322
            self.writeArg()
            self.state = 327
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==26:
                self.state = 323
                self.match(MiniPascalParser.COMMA)
                self.state = 324
                self.writeArg()
                self.state = 329
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
        self.enterRule(localctx, 72, self.RULE_writeArg)
        try:
            self.state = 332
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,31,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 330
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 331
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





