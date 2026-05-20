# Generated from gramm/pascal/PasDocParser.g4 by ANTLR 4.13.2
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
        4,1,46,306,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,1,0,3,0,74,8,0,1,0,5,0,77,8,0,10,0,12,0,
        80,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,2,1,2,5,2,90,8,2,10,2,12,2,93,9,
        2,1,2,1,2,5,2,97,8,2,10,2,12,2,100,9,2,1,2,3,2,103,8,2,1,3,1,3,1,
        3,1,3,1,3,3,3,110,8,3,1,4,1,4,4,4,114,8,4,11,4,12,4,115,1,5,1,5,
        1,5,3,5,121,8,5,1,6,1,6,1,6,1,6,1,7,3,7,128,8,7,1,7,1,7,1,7,3,7,
        133,8,7,1,8,1,8,1,9,1,9,1,10,1,10,5,10,141,8,10,10,10,12,10,144,
        9,10,1,11,1,11,1,11,3,11,149,8,11,1,12,1,12,1,12,1,12,3,12,155,8,
        12,1,13,1,13,1,13,1,13,3,13,161,8,13,1,14,1,14,3,14,165,8,14,1,14,
        1,14,1,15,1,15,1,15,1,16,1,16,1,16,1,16,5,16,176,8,16,10,16,12,16,
        179,9,16,1,16,1,16,1,17,5,17,184,8,17,10,17,12,17,187,9,17,1,17,
        1,17,1,18,1,18,1,18,1,18,1,18,1,18,3,18,197,8,18,1,19,1,19,1,20,
        1,20,1,21,1,21,1,21,3,21,206,8,21,1,21,3,21,209,8,21,1,21,3,21,212,
        8,21,1,21,1,21,1,22,1,22,4,22,218,8,22,11,22,12,22,219,1,23,1,23,
        1,24,1,24,3,24,226,8,24,1,24,1,24,1,25,1,25,1,25,5,25,233,8,25,10,
        25,12,25,236,9,25,1,26,3,26,239,8,26,1,26,1,26,1,26,5,26,244,8,26,
        10,26,12,26,247,9,26,1,26,1,26,1,26,1,27,1,27,1,28,1,28,1,28,1,29,
        1,29,1,30,1,30,1,30,3,30,262,8,30,1,30,5,30,265,8,30,10,30,12,30,
        268,9,30,1,30,1,30,1,31,1,31,1,31,1,32,1,32,1,32,1,32,3,32,279,8,
        32,1,33,1,33,1,33,5,33,284,8,33,10,33,12,33,287,9,33,1,33,1,33,1,
        33,1,33,1,34,3,34,294,8,34,1,34,1,34,1,34,5,34,299,8,34,10,34,12,
        34,302,9,34,1,35,1,35,1,35,0,0,36,0,2,4,6,8,10,12,14,16,18,20,22,
        24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,
        68,70,0,5,1,0,34,35,1,0,8,11,1,0,12,15,1,0,17,22,3,0,7,7,26,28,36,
        46,311,0,73,1,0,0,0,2,83,1,0,0,0,4,102,1,0,0,0,6,109,1,0,0,0,8,111,
        1,0,0,0,10,117,1,0,0,0,12,122,1,0,0,0,14,132,1,0,0,0,16,134,1,0,
        0,0,18,136,1,0,0,0,20,138,1,0,0,0,22,148,1,0,0,0,24,150,1,0,0,0,
        26,156,1,0,0,0,28,162,1,0,0,0,30,168,1,0,0,0,32,171,1,0,0,0,34,185,
        1,0,0,0,36,196,1,0,0,0,38,198,1,0,0,0,40,200,1,0,0,0,42,202,1,0,
        0,0,44,215,1,0,0,0,46,221,1,0,0,0,48,223,1,0,0,0,50,229,1,0,0,0,
        52,238,1,0,0,0,54,251,1,0,0,0,56,253,1,0,0,0,58,256,1,0,0,0,60,258,
        1,0,0,0,62,271,1,0,0,0,64,278,1,0,0,0,66,280,1,0,0,0,68,293,1,0,
        0,0,70,303,1,0,0,0,72,74,3,2,1,0,73,72,1,0,0,0,73,74,1,0,0,0,74,
        78,1,0,0,0,75,77,3,4,2,0,76,75,1,0,0,0,77,80,1,0,0,0,78,76,1,0,0,
        0,78,79,1,0,0,0,79,81,1,0,0,0,80,78,1,0,0,0,81,82,5,0,0,1,82,1,1,
        0,0,0,83,84,5,1,0,0,84,85,5,26,0,0,85,86,5,40,0,0,86,3,1,0,0,0,87,
        91,5,2,0,0,88,90,3,6,3,0,89,88,1,0,0,0,90,93,1,0,0,0,91,89,1,0,0,
        0,91,92,1,0,0,0,92,103,1,0,0,0,93,91,1,0,0,0,94,98,5,3,0,0,95,97,
        3,6,3,0,96,95,1,0,0,0,97,100,1,0,0,0,98,96,1,0,0,0,98,99,1,0,0,0,
        99,103,1,0,0,0,100,98,1,0,0,0,101,103,3,6,3,0,102,87,1,0,0,0,102,
        94,1,0,0,0,102,101,1,0,0,0,103,5,1,0,0,0,104,110,3,18,9,0,105,110,
        3,8,4,0,106,110,3,20,10,0,107,110,3,24,12,0,108,110,3,70,35,0,109,
        104,1,0,0,0,109,105,1,0,0,0,109,106,1,0,0,0,109,107,1,0,0,0,109,
        108,1,0,0,0,110,7,1,0,0,0,111,113,5,25,0,0,112,114,3,10,5,0,113,
        112,1,0,0,0,114,115,1,0,0,0,115,113,1,0,0,0,115,116,1,0,0,0,116,
        9,1,0,0,0,117,118,3,12,6,0,118,120,5,40,0,0,119,121,3,18,9,0,120,
        119,1,0,0,0,120,121,1,0,0,0,121,11,1,0,0,0,122,123,5,26,0,0,123,
        124,5,44,0,0,124,125,3,14,7,0,125,13,1,0,0,0,126,128,3,16,8,0,127,
        126,1,0,0,0,127,128,1,0,0,0,128,129,1,0,0,0,129,133,5,28,0,0,130,
        133,5,27,0,0,131,133,5,26,0,0,132,127,1,0,0,0,132,130,1,0,0,0,132,
        131,1,0,0,0,133,15,1,0,0,0,134,135,7,0,0,0,135,17,1,0,0,0,136,137,
        5,29,0,0,137,19,1,0,0,0,138,142,5,4,0,0,139,141,3,22,11,0,140,139,
        1,0,0,0,141,144,1,0,0,0,142,140,1,0,0,0,142,143,1,0,0,0,143,21,1,
        0,0,0,144,142,1,0,0,0,145,149,3,24,12,0,146,149,3,26,13,0,147,149,
        3,70,35,0,148,145,1,0,0,0,148,146,1,0,0,0,148,147,1,0,0,0,149,23,
        1,0,0,0,150,151,5,26,0,0,151,152,5,44,0,0,152,154,3,28,14,0,153,
        155,5,40,0,0,154,153,1,0,0,0,154,155,1,0,0,0,155,25,1,0,0,0,156,
        157,5,26,0,0,157,158,5,44,0,0,158,160,3,30,15,0,159,161,5,40,0,0,
        160,159,1,0,0,0,160,161,1,0,0,0,161,27,1,0,0,0,162,164,5,5,0,0,163,
        165,3,32,16,0,164,163,1,0,0,0,164,165,1,0,0,0,165,166,1,0,0,0,166,
        167,3,34,17,0,167,29,1,0,0,0,168,169,5,6,0,0,169,170,3,34,17,0,170,
        31,1,0,0,0,171,172,5,36,0,0,172,177,3,68,34,0,173,174,5,42,0,0,174,
        176,3,68,34,0,175,173,1,0,0,0,176,179,1,0,0,0,177,175,1,0,0,0,177,
        178,1,0,0,0,178,180,1,0,0,0,179,177,1,0,0,0,180,181,5,37,0,0,181,
        33,1,0,0,0,182,184,3,36,18,0,183,182,1,0,0,0,184,187,1,0,0,0,185,
        183,1,0,0,0,185,186,1,0,0,0,186,188,1,0,0,0,187,185,1,0,0,0,188,
        189,5,7,0,0,189,35,1,0,0,0,190,197,3,18,9,0,191,197,3,38,19,0,192,
        197,3,42,21,0,193,197,3,60,30,0,194,197,3,66,33,0,195,197,3,70,35,
        0,196,190,1,0,0,0,196,191,1,0,0,0,196,192,1,0,0,0,196,193,1,0,0,
        0,196,194,1,0,0,0,196,195,1,0,0,0,197,37,1,0,0,0,198,199,3,40,20,
        0,199,39,1,0,0,0,200,201,7,1,0,0,201,41,1,0,0,0,202,203,3,46,23,
        0,203,205,5,26,0,0,204,206,3,48,24,0,205,204,1,0,0,0,205,206,1,0,
        0,0,206,208,1,0,0,0,207,209,3,56,28,0,208,207,1,0,0,0,208,209,1,
        0,0,0,209,211,1,0,0,0,210,212,3,44,22,0,211,210,1,0,0,0,211,212,
        1,0,0,0,212,213,1,0,0,0,213,214,5,40,0,0,214,43,1,0,0,0,215,217,
        5,40,0,0,216,218,3,58,29,0,217,216,1,0,0,0,218,219,1,0,0,0,219,217,
        1,0,0,0,219,220,1,0,0,0,220,45,1,0,0,0,221,222,7,2,0,0,222,47,1,
        0,0,0,223,225,5,36,0,0,224,226,3,50,25,0,225,224,1,0,0,0,225,226,
        1,0,0,0,226,227,1,0,0,0,227,228,5,37,0,0,228,49,1,0,0,0,229,234,
        3,52,26,0,230,231,5,40,0,0,231,233,3,52,26,0,232,230,1,0,0,0,233,
        236,1,0,0,0,234,232,1,0,0,0,234,235,1,0,0,0,235,51,1,0,0,0,236,234,
        1,0,0,0,237,239,3,54,27,0,238,237,1,0,0,0,238,239,1,0,0,0,239,240,
        1,0,0,0,240,245,5,26,0,0,241,242,5,42,0,0,242,244,5,26,0,0,243,241,
        1,0,0,0,244,247,1,0,0,0,245,243,1,0,0,0,245,246,1,0,0,0,246,248,
        1,0,0,0,247,245,1,0,0,0,248,249,5,41,0,0,249,250,3,68,34,0,250,53,
        1,0,0,0,251,252,5,25,0,0,252,55,1,0,0,0,253,254,5,41,0,0,254,255,
        3,68,34,0,255,57,1,0,0,0,256,257,7,3,0,0,257,59,1,0,0,0,258,259,
        5,16,0,0,259,261,5,26,0,0,260,262,3,62,31,0,261,260,1,0,0,0,261,
        262,1,0,0,0,262,266,1,0,0,0,263,265,3,64,32,0,264,263,1,0,0,0,265,
        268,1,0,0,0,266,264,1,0,0,0,266,267,1,0,0,0,267,269,1,0,0,0,268,
        266,1,0,0,0,269,270,5,40,0,0,270,61,1,0,0,0,271,272,5,41,0,0,272,
        273,3,68,34,0,273,63,1,0,0,0,274,275,5,23,0,0,275,279,5,26,0,0,276,
        277,5,24,0,0,277,279,5,26,0,0,278,274,1,0,0,0,278,276,1,0,0,0,279,
        65,1,0,0,0,280,285,5,26,0,0,281,282,5,42,0,0,282,284,5,26,0,0,283,
        281,1,0,0,0,284,287,1,0,0,0,285,283,1,0,0,0,285,286,1,0,0,0,286,
        288,1,0,0,0,287,285,1,0,0,0,288,289,5,41,0,0,289,290,3,68,34,0,290,
        291,5,40,0,0,291,67,1,0,0,0,292,294,5,45,0,0,293,292,1,0,0,0,293,
        294,1,0,0,0,294,295,1,0,0,0,295,300,5,26,0,0,296,297,5,43,0,0,297,
        299,5,26,0,0,298,296,1,0,0,0,299,302,1,0,0,0,300,298,1,0,0,0,300,
        301,1,0,0,0,301,69,1,0,0,0,302,300,1,0,0,0,303,304,7,4,0,0,304,71,
        1,0,0,0,32,73,78,91,98,102,109,115,120,127,132,142,148,154,160,164,
        177,185,196,205,208,211,219,225,234,238,245,261,266,278,285,293,
        300
    ]

class PasDocParser ( Parser ):

    grammarFileName = "PasDocParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'-'", "'+'", "'('", "')'", 
                     "'['", "']'", "';'", "':'", "','", "'.'", "'='", "'^'" ]

    symbolicNames = [ "<INVALID>", "UNIT", "INTERFACE", "IMPLEMENTATION", 
                      "TYPE", "CLASS", "RECORD", "END", "PUBLIC", "PRIVATE", 
                      "PROTECTED", "PUBLISHED", "PROCEDURE", "FUNCTION", 
                      "CONSTRUCTOR", "DESTRUCTOR", "PROPERTY", "VIRTUAL", 
                      "OVERRIDE", "ABSTRACT", "STATIC", "OVERLOAD", "REINTRODUCE", 
                      "READ", "WRITE", "CONST", "IDENT", "STRING", "NUMBER", 
                      "DOC_COMMENT", "LINE_COMMENT", "BRACE_COMMENT", "PAREN_COMMENT", 
                      "WS", "MINUS", "PLUS", "LPAREN", "RPAREN", "LBRACK", 
                      "RBRACK", "SEMI", "COLON", "COMMA", "DOT", "EQ", "CARET", 
                      "OTHER" ]

    RULE_unitFile = 0
    RULE_unitHeader = 1
    RULE_unitSection = 2
    RULE_declaration = 3
    RULE_constSection = 4
    RULE_constDeclaration = 5
    RULE_constItem = 6
    RULE_constValue = 7
    RULE_sign = 8
    RULE_docComment = 9
    RULE_typeSection = 10
    RULE_typeDeclaration = 11
    RULE_classDeclaration = 12
    RULE_recordDeclaration = 13
    RULE_classType = 14
    RULE_recordType = 15
    RULE_classInheritance = 16
    RULE_classBody = 17
    RULE_classMember = 18
    RULE_visibilitySection = 19
    RULE_visibility = 20
    RULE_methodDeclaration = 21
    RULE_methodDirectiveList = 22
    RULE_methodKind = 23
    RULE_parameterList = 24
    RULE_parameterDecl = 25
    RULE_parameterItem = 26
    RULE_parameterModifier = 27
    RULE_returnType = 28
    RULE_methodDirective = 29
    RULE_propertyDeclaration = 30
    RULE_propertyType = 31
    RULE_propertyAccessor = 32
    RULE_fieldDeclaration = 33
    RULE_typeName = 34
    RULE_otherToken = 35

    ruleNames =  [ "unitFile", "unitHeader", "unitSection", "declaration", 
                   "constSection", "constDeclaration", "constItem", "constValue", 
                   "sign", "docComment", "typeSection", "typeDeclaration", 
                   "classDeclaration", "recordDeclaration", "classType", 
                   "recordType", "classInheritance", "classBody", "classMember", 
                   "visibilitySection", "visibility", "methodDeclaration", 
                   "methodDirectiveList", "methodKind", "parameterList", 
                   "parameterDecl", "parameterItem", "parameterModifier", 
                   "returnType", "methodDirective", "propertyDeclaration", 
                   "propertyType", "propertyAccessor", "fieldDeclaration", 
                   "typeName", "otherToken" ]

    EOF = Token.EOF
    UNIT=1
    INTERFACE=2
    IMPLEMENTATION=3
    TYPE=4
    CLASS=5
    RECORD=6
    END=7
    PUBLIC=8
    PRIVATE=9
    PROTECTED=10
    PUBLISHED=11
    PROCEDURE=12
    FUNCTION=13
    CONSTRUCTOR=14
    DESTRUCTOR=15
    PROPERTY=16
    VIRTUAL=17
    OVERRIDE=18
    ABSTRACT=19
    STATIC=20
    OVERLOAD=21
    REINTRODUCE=22
    READ=23
    WRITE=24
    CONST=25
    IDENT=26
    STRING=27
    NUMBER=28
    DOC_COMMENT=29
    LINE_COMMENT=30
    BRACE_COMMENT=31
    PAREN_COMMENT=32
    WS=33
    MINUS=34
    PLUS=35
    LPAREN=36
    RPAREN=37
    LBRACK=38
    RBRACK=39
    SEMI=40
    COLON=41
    COMMA=42
    DOT=43
    EQ=44
    CARET=45
    OTHER=46

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class UnitFileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(PasDocParser.EOF, 0)

        def unitHeader(self):
            return self.getTypedRuleContext(PasDocParser.UnitHeaderContext,0)


        def unitSection(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PasDocParser.UnitSectionContext)
            else:
                return self.getTypedRuleContext(PasDocParser.UnitSectionContext,i)


        def getRuleIndex(self):
            return PasDocParser.RULE_unitFile

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnitFile" ):
                listener.enterUnitFile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnitFile" ):
                listener.exitUnitFile(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnitFile" ):
                return visitor.visitUnitFile(self)
            else:
                return visitor.visitChildren(self)




    def unitFile(self):

        localctx = PasDocParser.UnitFileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_unitFile)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 72
                self.unitHeader()


            self.state = 78
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 140669809066140) != 0):
                self.state = 75
                self.unitSection()
                self.state = 80
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 81
            self.match(PasDocParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnitHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def UNIT(self):
            return self.getToken(PasDocParser.UNIT, 0)

        def IDENT(self):
            return self.getToken(PasDocParser.IDENT, 0)

        def SEMI(self):
            return self.getToken(PasDocParser.SEMI, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_unitHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnitHeader" ):
                listener.enterUnitHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnitHeader" ):
                listener.exitUnitHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnitHeader" ):
                return visitor.visitUnitHeader(self)
            else:
                return visitor.visitChildren(self)




    def unitHeader(self):

        localctx = PasDocParser.UnitHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_unitHeader)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            self.match(PasDocParser.UNIT)
            self.state = 84
            self.match(PasDocParser.IDENT)
            self.state = 85
            self.match(PasDocParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnitSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTERFACE(self):
            return self.getToken(PasDocParser.INTERFACE, 0)

        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PasDocParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(PasDocParser.DeclarationContext,i)


        def IMPLEMENTATION(self):
            return self.getToken(PasDocParser.IMPLEMENTATION, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_unitSection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnitSection" ):
                listener.enterUnitSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnitSection" ):
                listener.exitUnitSection(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnitSection" ):
                return visitor.visitUnitSection(self)
            else:
                return visitor.visitChildren(self)




    def unitSection(self):

        localctx = PasDocParser.UnitSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_unitSection)
        try:
            self.state = 102
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 87
                self.match(PasDocParser.INTERFACE)
                self.state = 91
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 88
                        self.declaration() 
                    self.state = 93
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 94
                self.match(PasDocParser.IMPLEMENTATION)
                self.state = 98
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 95
                        self.declaration() 
                    self.state = 100
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

                pass
            elif token in [4, 7, 25, 26, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]:
                self.enterOuterAlt(localctx, 3)
                self.state = 101
                self.declaration()
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


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def docComment(self):
            return self.getTypedRuleContext(PasDocParser.DocCommentContext,0)


        def constSection(self):
            return self.getTypedRuleContext(PasDocParser.ConstSectionContext,0)


        def typeSection(self):
            return self.getTypedRuleContext(PasDocParser.TypeSectionContext,0)


        def classDeclaration(self):
            return self.getTypedRuleContext(PasDocParser.ClassDeclarationContext,0)


        def otherToken(self):
            return self.getTypedRuleContext(PasDocParser.OtherTokenContext,0)


        def getRuleIndex(self):
            return PasDocParser.RULE_declaration

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

        localctx = PasDocParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_declaration)
        try:
            self.state = 109
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 104
                self.docComment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 105
                self.constSection()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 106
                self.typeSection()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 107
                self.classDeclaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 108
                self.otherToken()
                pass


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
            return self.getToken(PasDocParser.CONST, 0)

        def constDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PasDocParser.ConstDeclarationContext)
            else:
                return self.getTypedRuleContext(PasDocParser.ConstDeclarationContext,i)


        def getRuleIndex(self):
            return PasDocParser.RULE_constSection

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

        localctx = PasDocParser.ConstSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_constSection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 111
            self.match(PasDocParser.CONST)
            self.state = 113 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 112
                    self.constDeclaration()

                else:
                    raise NoViableAltException(self)
                self.state = 115 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

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

        def constItem(self):
            return self.getTypedRuleContext(PasDocParser.ConstItemContext,0)


        def SEMI(self):
            return self.getToken(PasDocParser.SEMI, 0)

        def docComment(self):
            return self.getTypedRuleContext(PasDocParser.DocCommentContext,0)


        def getRuleIndex(self):
            return PasDocParser.RULE_constDeclaration

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

        localctx = PasDocParser.ConstDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_constDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 117
            self.constItem()
            self.state = 118
            self.match(PasDocParser.SEMI)
            self.state = 120
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.state = 119
                self.docComment()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(PasDocParser.IDENT, 0)

        def EQ(self):
            return self.getToken(PasDocParser.EQ, 0)

        def constValue(self):
            return self.getTypedRuleContext(PasDocParser.ConstValueContext,0)


        def getRuleIndex(self):
            return PasDocParser.RULE_constItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstItem" ):
                listener.enterConstItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstItem" ):
                listener.exitConstItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstItem" ):
                return visitor.visitConstItem(self)
            else:
                return visitor.visitChildren(self)




    def constItem(self):

        localctx = PasDocParser.ConstItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_constItem)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 122
            self.match(PasDocParser.IDENT)
            self.state = 123
            self.match(PasDocParser.EQ)
            self.state = 124
            self.constValue()
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

        def NUMBER(self):
            return self.getToken(PasDocParser.NUMBER, 0)

        def sign(self):
            return self.getTypedRuleContext(PasDocParser.SignContext,0)


        def STRING(self):
            return self.getToken(PasDocParser.STRING, 0)

        def IDENT(self):
            return self.getToken(PasDocParser.IDENT, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_constValue

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

        localctx = PasDocParser.ConstValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_constValue)
        self._la = 0 # Token type
        try:
            self.state = 132
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [28, 34, 35]:
                self.enterOuterAlt(localctx, 1)
                self.state = 127
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==34 or _la==35:
                    self.state = 126
                    self.sign()


                self.state = 129
                self.match(PasDocParser.NUMBER)
                pass
            elif token in [27]:
                self.enterOuterAlt(localctx, 2)
                self.state = 130
                self.match(PasDocParser.STRING)
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 3)
                self.state = 131
                self.match(PasDocParser.IDENT)
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


    class SignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self):
            return self.getToken(PasDocParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(PasDocParser.MINUS, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_sign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSign" ):
                listener.enterSign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSign" ):
                listener.exitSign(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSign" ):
                return visitor.visitSign(self)
            else:
                return visitor.visitChildren(self)




    def sign(self):

        localctx = PasDocParser.SignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_sign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 134
            _la = self._input.LA(1)
            if not(_la==34 or _la==35):
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


    class DocCommentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOC_COMMENT(self):
            return self.getToken(PasDocParser.DOC_COMMENT, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_docComment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDocComment" ):
                listener.enterDocComment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDocComment" ):
                listener.exitDocComment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDocComment" ):
                return visitor.visitDocComment(self)
            else:
                return visitor.visitChildren(self)




    def docComment(self):

        localctx = PasDocParser.DocCommentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_docComment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136
            self.match(PasDocParser.DOC_COMMENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TYPE(self):
            return self.getToken(PasDocParser.TYPE, 0)

        def typeDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PasDocParser.TypeDeclarationContext)
            else:
                return self.getTypedRuleContext(PasDocParser.TypeDeclarationContext,i)


        def getRuleIndex(self):
            return PasDocParser.RULE_typeSection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeSection" ):
                listener.enterTypeSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeSection" ):
                listener.exitTypeSection(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeSection" ):
                return visitor.visitTypeSection(self)
            else:
                return visitor.visitChildren(self)




    def typeSection(self):

        localctx = PasDocParser.TypeSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_typeSection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.match(PasDocParser.TYPE)
            self.state = 142
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 139
                    self.typeDeclaration() 
                self.state = 144
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def classDeclaration(self):
            return self.getTypedRuleContext(PasDocParser.ClassDeclarationContext,0)


        def recordDeclaration(self):
            return self.getTypedRuleContext(PasDocParser.RecordDeclarationContext,0)


        def otherToken(self):
            return self.getTypedRuleContext(PasDocParser.OtherTokenContext,0)


        def getRuleIndex(self):
            return PasDocParser.RULE_typeDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeDeclaration" ):
                listener.enterTypeDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeDeclaration" ):
                listener.exitTypeDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeDeclaration" ):
                return visitor.visitTypeDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def typeDeclaration(self):

        localctx = PasDocParser.TypeDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_typeDeclaration)
        try:
            self.state = 148
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 145
                self.classDeclaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 146
                self.recordDeclaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 147
                self.otherToken()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(PasDocParser.IDENT, 0)

        def EQ(self):
            return self.getToken(PasDocParser.EQ, 0)

        def classType(self):
            return self.getTypedRuleContext(PasDocParser.ClassTypeContext,0)


        def SEMI(self):
            return self.getToken(PasDocParser.SEMI, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_classDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassDeclaration" ):
                listener.enterClassDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassDeclaration" ):
                listener.exitClassDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassDeclaration" ):
                return visitor.visitClassDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def classDeclaration(self):

        localctx = PasDocParser.ClassDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_classDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 150
            self.match(PasDocParser.IDENT)
            self.state = 151
            self.match(PasDocParser.EQ)
            self.state = 152
            self.classType()
            self.state = 154
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                self.state = 153
                self.match(PasDocParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RecordDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(PasDocParser.IDENT, 0)

        def EQ(self):
            return self.getToken(PasDocParser.EQ, 0)

        def recordType(self):
            return self.getTypedRuleContext(PasDocParser.RecordTypeContext,0)


        def SEMI(self):
            return self.getToken(PasDocParser.SEMI, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_recordDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRecordDeclaration" ):
                listener.enterRecordDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRecordDeclaration" ):
                listener.exitRecordDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRecordDeclaration" ):
                return visitor.visitRecordDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def recordDeclaration(self):

        localctx = PasDocParser.RecordDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_recordDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 156
            self.match(PasDocParser.IDENT)
            self.state = 157
            self.match(PasDocParser.EQ)
            self.state = 158
            self.recordType()
            self.state = 160
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.state = 159
                self.match(PasDocParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CLASS(self):
            return self.getToken(PasDocParser.CLASS, 0)

        def classBody(self):
            return self.getTypedRuleContext(PasDocParser.ClassBodyContext,0)


        def classInheritance(self):
            return self.getTypedRuleContext(PasDocParser.ClassInheritanceContext,0)


        def getRuleIndex(self):
            return PasDocParser.RULE_classType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassType" ):
                listener.enterClassType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassType" ):
                listener.exitClassType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassType" ):
                return visitor.visitClassType(self)
            else:
                return visitor.visitChildren(self)




    def classType(self):

        localctx = PasDocParser.ClassTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_classType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 162
            self.match(PasDocParser.CLASS)
            self.state = 164
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.state = 163
                self.classInheritance()


            self.state = 166
            self.classBody()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RecordTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RECORD(self):
            return self.getToken(PasDocParser.RECORD, 0)

        def classBody(self):
            return self.getTypedRuleContext(PasDocParser.ClassBodyContext,0)


        def getRuleIndex(self):
            return PasDocParser.RULE_recordType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRecordType" ):
                listener.enterRecordType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRecordType" ):
                listener.exitRecordType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRecordType" ):
                return visitor.visitRecordType(self)
            else:
                return visitor.visitChildren(self)




    def recordType(self):

        localctx = PasDocParser.RecordTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_recordType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 168
            self.match(PasDocParser.RECORD)
            self.state = 169
            self.classBody()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassInheritanceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(PasDocParser.LPAREN, 0)

        def typeName(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PasDocParser.TypeNameContext)
            else:
                return self.getTypedRuleContext(PasDocParser.TypeNameContext,i)


        def RPAREN(self):
            return self.getToken(PasDocParser.RPAREN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(PasDocParser.COMMA)
            else:
                return self.getToken(PasDocParser.COMMA, i)

        def getRuleIndex(self):
            return PasDocParser.RULE_classInheritance

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassInheritance" ):
                listener.enterClassInheritance(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassInheritance" ):
                listener.exitClassInheritance(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassInheritance" ):
                return visitor.visitClassInheritance(self)
            else:
                return visitor.visitChildren(self)




    def classInheritance(self):

        localctx = PasDocParser.ClassInheritanceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_classInheritance)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 171
            self.match(PasDocParser.LPAREN)
            self.state = 172
            self.typeName()
            self.state = 177
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==42:
                self.state = 173
                self.match(PasDocParser.COMMA)
                self.state = 174
                self.typeName()
                self.state = 179
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 180
            self.match(PasDocParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassBodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def END(self):
            return self.getToken(PasDocParser.END, 0)

        def classMember(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PasDocParser.ClassMemberContext)
            else:
                return self.getTypedRuleContext(PasDocParser.ClassMemberContext,i)


        def getRuleIndex(self):
            return PasDocParser.RULE_classBody

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassBody" ):
                listener.enterClassBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassBody" ):
                listener.exitClassBody(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassBody" ):
                return visitor.visitClassBody(self)
            else:
                return visitor.visitChildren(self)




    def classBody(self):

        localctx = PasDocParser.ClassBodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_classBody)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 185
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,16,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 182
                    self.classMember() 
                self.state = 187
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,16,self._ctx)

            self.state = 188
            self.match(PasDocParser.END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassMemberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def docComment(self):
            return self.getTypedRuleContext(PasDocParser.DocCommentContext,0)


        def visibilitySection(self):
            return self.getTypedRuleContext(PasDocParser.VisibilitySectionContext,0)


        def methodDeclaration(self):
            return self.getTypedRuleContext(PasDocParser.MethodDeclarationContext,0)


        def propertyDeclaration(self):
            return self.getTypedRuleContext(PasDocParser.PropertyDeclarationContext,0)


        def fieldDeclaration(self):
            return self.getTypedRuleContext(PasDocParser.FieldDeclarationContext,0)


        def otherToken(self):
            return self.getTypedRuleContext(PasDocParser.OtherTokenContext,0)


        def getRuleIndex(self):
            return PasDocParser.RULE_classMember

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassMember" ):
                listener.enterClassMember(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassMember" ):
                listener.exitClassMember(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassMember" ):
                return visitor.visitClassMember(self)
            else:
                return visitor.visitChildren(self)




    def classMember(self):

        localctx = PasDocParser.ClassMemberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_classMember)
        try:
            self.state = 196
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 190
                self.docComment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 191
                self.visibilitySection()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 192
                self.methodDeclaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 193
                self.propertyDeclaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 194
                self.fieldDeclaration()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 195
                self.otherToken()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VisibilitySectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def visibility(self):
            return self.getTypedRuleContext(PasDocParser.VisibilityContext,0)


        def getRuleIndex(self):
            return PasDocParser.RULE_visibilitySection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVisibilitySection" ):
                listener.enterVisibilitySection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVisibilitySection" ):
                listener.exitVisibilitySection(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVisibilitySection" ):
                return visitor.visitVisibilitySection(self)
            else:
                return visitor.visitChildren(self)




    def visibilitySection(self):

        localctx = PasDocParser.VisibilitySectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_visibilitySection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 198
            self.visibility()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VisibilityContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PUBLIC(self):
            return self.getToken(PasDocParser.PUBLIC, 0)

        def PRIVATE(self):
            return self.getToken(PasDocParser.PRIVATE, 0)

        def PROTECTED(self):
            return self.getToken(PasDocParser.PROTECTED, 0)

        def PUBLISHED(self):
            return self.getToken(PasDocParser.PUBLISHED, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_visibility

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVisibility" ):
                listener.enterVisibility(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVisibility" ):
                listener.exitVisibility(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVisibility" ):
                return visitor.visitVisibility(self)
            else:
                return visitor.visitChildren(self)




    def visibility(self):

        localctx = PasDocParser.VisibilityContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_visibility)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3840) != 0)):
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


    class MethodDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def methodKind(self):
            return self.getTypedRuleContext(PasDocParser.MethodKindContext,0)


        def IDENT(self):
            return self.getToken(PasDocParser.IDENT, 0)

        def SEMI(self):
            return self.getToken(PasDocParser.SEMI, 0)

        def parameterList(self):
            return self.getTypedRuleContext(PasDocParser.ParameterListContext,0)


        def returnType(self):
            return self.getTypedRuleContext(PasDocParser.ReturnTypeContext,0)


        def methodDirectiveList(self):
            return self.getTypedRuleContext(PasDocParser.MethodDirectiveListContext,0)


        def getRuleIndex(self):
            return PasDocParser.RULE_methodDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMethodDeclaration" ):
                listener.enterMethodDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMethodDeclaration" ):
                listener.exitMethodDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMethodDeclaration" ):
                return visitor.visitMethodDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def methodDeclaration(self):

        localctx = PasDocParser.MethodDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_methodDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 202
            self.methodKind()
            self.state = 203
            self.match(PasDocParser.IDENT)
            self.state = 205
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==36:
                self.state = 204
                self.parameterList()


            self.state = 208
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==41:
                self.state = 207
                self.returnType()


            self.state = 211
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.state = 210
                self.methodDirectiveList()


            self.state = 213
            self.match(PasDocParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MethodDirectiveListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SEMI(self):
            return self.getToken(PasDocParser.SEMI, 0)

        def methodDirective(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PasDocParser.MethodDirectiveContext)
            else:
                return self.getTypedRuleContext(PasDocParser.MethodDirectiveContext,i)


        def getRuleIndex(self):
            return PasDocParser.RULE_methodDirectiveList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMethodDirectiveList" ):
                listener.enterMethodDirectiveList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMethodDirectiveList" ):
                listener.exitMethodDirectiveList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMethodDirectiveList" ):
                return visitor.visitMethodDirectiveList(self)
            else:
                return visitor.visitChildren(self)




    def methodDirectiveList(self):

        localctx = PasDocParser.MethodDirectiveListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_methodDirectiveList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 215
            self.match(PasDocParser.SEMI)
            self.state = 217 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 216
                self.methodDirective()
                self.state = 219 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 8257536) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MethodKindContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROCEDURE(self):
            return self.getToken(PasDocParser.PROCEDURE, 0)

        def FUNCTION(self):
            return self.getToken(PasDocParser.FUNCTION, 0)

        def CONSTRUCTOR(self):
            return self.getToken(PasDocParser.CONSTRUCTOR, 0)

        def DESTRUCTOR(self):
            return self.getToken(PasDocParser.DESTRUCTOR, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_methodKind

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMethodKind" ):
                listener.enterMethodKind(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMethodKind" ):
                listener.exitMethodKind(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMethodKind" ):
                return visitor.visitMethodKind(self)
            else:
                return visitor.visitChildren(self)




    def methodKind(self):

        localctx = PasDocParser.MethodKindContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_methodKind)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 221
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 61440) != 0)):
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


    class ParameterListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(PasDocParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(PasDocParser.RPAREN, 0)

        def parameterDecl(self):
            return self.getTypedRuleContext(PasDocParser.ParameterDeclContext,0)


        def getRuleIndex(self):
            return PasDocParser.RULE_parameterList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameterList" ):
                listener.enterParameterList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameterList" ):
                listener.exitParameterList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameterList" ):
                return visitor.visitParameterList(self)
            else:
                return visitor.visitChildren(self)




    def parameterList(self):

        localctx = PasDocParser.ParameterListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_parameterList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 223
            self.match(PasDocParser.LPAREN)
            self.state = 225
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==25 or _la==26:
                self.state = 224
                self.parameterDecl()


            self.state = 227
            self.match(PasDocParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParameterDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parameterItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PasDocParser.ParameterItemContext)
            else:
                return self.getTypedRuleContext(PasDocParser.ParameterItemContext,i)


        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(PasDocParser.SEMI)
            else:
                return self.getToken(PasDocParser.SEMI, i)

        def getRuleIndex(self):
            return PasDocParser.RULE_parameterDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameterDecl" ):
                listener.enterParameterDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameterDecl" ):
                listener.exitParameterDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameterDecl" ):
                return visitor.visitParameterDecl(self)
            else:
                return visitor.visitChildren(self)




    def parameterDecl(self):

        localctx = PasDocParser.ParameterDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_parameterDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 229
            self.parameterItem()
            self.state = 234
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 230
                self.match(PasDocParser.SEMI)
                self.state = 231
                self.parameterItem()
                self.state = 236
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParameterItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(PasDocParser.IDENT)
            else:
                return self.getToken(PasDocParser.IDENT, i)

        def COLON(self):
            return self.getToken(PasDocParser.COLON, 0)

        def typeName(self):
            return self.getTypedRuleContext(PasDocParser.TypeNameContext,0)


        def parameterModifier(self):
            return self.getTypedRuleContext(PasDocParser.ParameterModifierContext,0)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(PasDocParser.COMMA)
            else:
                return self.getToken(PasDocParser.COMMA, i)

        def getRuleIndex(self):
            return PasDocParser.RULE_parameterItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameterItem" ):
                listener.enterParameterItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameterItem" ):
                listener.exitParameterItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameterItem" ):
                return visitor.visitParameterItem(self)
            else:
                return visitor.visitChildren(self)




    def parameterItem(self):

        localctx = PasDocParser.ParameterItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_parameterItem)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 238
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==25:
                self.state = 237
                self.parameterModifier()


            self.state = 240
            self.match(PasDocParser.IDENT)
            self.state = 245
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==42:
                self.state = 241
                self.match(PasDocParser.COMMA)
                self.state = 242
                self.match(PasDocParser.IDENT)
                self.state = 247
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 248
            self.match(PasDocParser.COLON)
            self.state = 249
            self.typeName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParameterModifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONST(self):
            return self.getToken(PasDocParser.CONST, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_parameterModifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameterModifier" ):
                listener.enterParameterModifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameterModifier" ):
                listener.exitParameterModifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameterModifier" ):
                return visitor.visitParameterModifier(self)
            else:
                return visitor.visitChildren(self)




    def parameterModifier(self):

        localctx = PasDocParser.ParameterModifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_parameterModifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 251
            self.match(PasDocParser.CONST)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COLON(self):
            return self.getToken(PasDocParser.COLON, 0)

        def typeName(self):
            return self.getTypedRuleContext(PasDocParser.TypeNameContext,0)


        def getRuleIndex(self):
            return PasDocParser.RULE_returnType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnType" ):
                listener.enterReturnType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnType" ):
                listener.exitReturnType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnType" ):
                return visitor.visitReturnType(self)
            else:
                return visitor.visitChildren(self)




    def returnType(self):

        localctx = PasDocParser.ReturnTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_returnType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 253
            self.match(PasDocParser.COLON)
            self.state = 254
            self.typeName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MethodDirectiveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VIRTUAL(self):
            return self.getToken(PasDocParser.VIRTUAL, 0)

        def OVERRIDE(self):
            return self.getToken(PasDocParser.OVERRIDE, 0)

        def ABSTRACT(self):
            return self.getToken(PasDocParser.ABSTRACT, 0)

        def STATIC(self):
            return self.getToken(PasDocParser.STATIC, 0)

        def OVERLOAD(self):
            return self.getToken(PasDocParser.OVERLOAD, 0)

        def REINTRODUCE(self):
            return self.getToken(PasDocParser.REINTRODUCE, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_methodDirective

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMethodDirective" ):
                listener.enterMethodDirective(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMethodDirective" ):
                listener.exitMethodDirective(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMethodDirective" ):
                return visitor.visitMethodDirective(self)
            else:
                return visitor.visitChildren(self)




    def methodDirective(self):

        localctx = PasDocParser.MethodDirectiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_methodDirective)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 256
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8257536) != 0)):
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


    class PropertyDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROPERTY(self):
            return self.getToken(PasDocParser.PROPERTY, 0)

        def IDENT(self):
            return self.getToken(PasDocParser.IDENT, 0)

        def SEMI(self):
            return self.getToken(PasDocParser.SEMI, 0)

        def propertyType(self):
            return self.getTypedRuleContext(PasDocParser.PropertyTypeContext,0)


        def propertyAccessor(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PasDocParser.PropertyAccessorContext)
            else:
                return self.getTypedRuleContext(PasDocParser.PropertyAccessorContext,i)


        def getRuleIndex(self):
            return PasDocParser.RULE_propertyDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropertyDeclaration" ):
                listener.enterPropertyDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropertyDeclaration" ):
                listener.exitPropertyDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropertyDeclaration" ):
                return visitor.visitPropertyDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def propertyDeclaration(self):

        localctx = PasDocParser.PropertyDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_propertyDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 258
            self.match(PasDocParser.PROPERTY)
            self.state = 259
            self.match(PasDocParser.IDENT)
            self.state = 261
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==41:
                self.state = 260
                self.propertyType()


            self.state = 266
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==23 or _la==24:
                self.state = 263
                self.propertyAccessor()
                self.state = 268
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 269
            self.match(PasDocParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropertyTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COLON(self):
            return self.getToken(PasDocParser.COLON, 0)

        def typeName(self):
            return self.getTypedRuleContext(PasDocParser.TypeNameContext,0)


        def getRuleIndex(self):
            return PasDocParser.RULE_propertyType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropertyType" ):
                listener.enterPropertyType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropertyType" ):
                listener.exitPropertyType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropertyType" ):
                return visitor.visitPropertyType(self)
            else:
                return visitor.visitChildren(self)




    def propertyType(self):

        localctx = PasDocParser.PropertyTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_propertyType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 271
            self.match(PasDocParser.COLON)
            self.state = 272
            self.typeName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropertyAccessorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def READ(self):
            return self.getToken(PasDocParser.READ, 0)

        def IDENT(self):
            return self.getToken(PasDocParser.IDENT, 0)

        def WRITE(self):
            return self.getToken(PasDocParser.WRITE, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_propertyAccessor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropertyAccessor" ):
                listener.enterPropertyAccessor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropertyAccessor" ):
                listener.exitPropertyAccessor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropertyAccessor" ):
                return visitor.visitPropertyAccessor(self)
            else:
                return visitor.visitChildren(self)




    def propertyAccessor(self):

        localctx = PasDocParser.PropertyAccessorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_propertyAccessor)
        try:
            self.state = 278
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.enterOuterAlt(localctx, 1)
                self.state = 274
                self.match(PasDocParser.READ)
                self.state = 275
                self.match(PasDocParser.IDENT)
                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 2)
                self.state = 276
                self.match(PasDocParser.WRITE)
                self.state = 277
                self.match(PasDocParser.IDENT)
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


    class FieldDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(PasDocParser.IDENT)
            else:
                return self.getToken(PasDocParser.IDENT, i)

        def COLON(self):
            return self.getToken(PasDocParser.COLON, 0)

        def typeName(self):
            return self.getTypedRuleContext(PasDocParser.TypeNameContext,0)


        def SEMI(self):
            return self.getToken(PasDocParser.SEMI, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(PasDocParser.COMMA)
            else:
                return self.getToken(PasDocParser.COMMA, i)

        def getRuleIndex(self):
            return PasDocParser.RULE_fieldDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFieldDeclaration" ):
                listener.enterFieldDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFieldDeclaration" ):
                listener.exitFieldDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFieldDeclaration" ):
                return visitor.visitFieldDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def fieldDeclaration(self):

        localctx = PasDocParser.FieldDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_fieldDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 280
            self.match(PasDocParser.IDENT)
            self.state = 285
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==42:
                self.state = 281
                self.match(PasDocParser.COMMA)
                self.state = 282
                self.match(PasDocParser.IDENT)
                self.state = 287
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 288
            self.match(PasDocParser.COLON)
            self.state = 289
            self.typeName()
            self.state = 290
            self.match(PasDocParser.SEMI)
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

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(PasDocParser.IDENT)
            else:
                return self.getToken(PasDocParser.IDENT, i)

        def CARET(self):
            return self.getToken(PasDocParser.CARET, 0)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(PasDocParser.DOT)
            else:
                return self.getToken(PasDocParser.DOT, i)

        def getRuleIndex(self):
            return PasDocParser.RULE_typeName

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

        localctx = PasDocParser.TypeNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_typeName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 293
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 292
                self.match(PasDocParser.CARET)


            self.state = 295
            self.match(PasDocParser.IDENT)
            self.state = 300
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==43:
                self.state = 296
                self.match(PasDocParser.DOT)
                self.state = 297
                self.match(PasDocParser.IDENT)
                self.state = 302
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OtherTokenContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(PasDocParser.IDENT, 0)

        def STRING(self):
            return self.getToken(PasDocParser.STRING, 0)

        def NUMBER(self):
            return self.getToken(PasDocParser.NUMBER, 0)

        def LPAREN(self):
            return self.getToken(PasDocParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(PasDocParser.RPAREN, 0)

        def LBRACK(self):
            return self.getToken(PasDocParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(PasDocParser.RBRACK, 0)

        def SEMI(self):
            return self.getToken(PasDocParser.SEMI, 0)

        def COLON(self):
            return self.getToken(PasDocParser.COLON, 0)

        def COMMA(self):
            return self.getToken(PasDocParser.COMMA, 0)

        def DOT(self):
            return self.getToken(PasDocParser.DOT, 0)

        def EQ(self):
            return self.getToken(PasDocParser.EQ, 0)

        def CARET(self):
            return self.getToken(PasDocParser.CARET, 0)

        def END(self):
            return self.getToken(PasDocParser.END, 0)

        def OTHER(self):
            return self.getToken(PasDocParser.OTHER, 0)

        def getRuleIndex(self):
            return PasDocParser.RULE_otherToken

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOtherToken" ):
                listener.enterOtherToken(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOtherToken" ):
                listener.exitOtherToken(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOtherToken" ):
                return visitor.visitOtherToken(self)
            else:
                return visitor.visitChildren(self)




    def otherToken(self):

        localctx = PasDocParser.OtherTokenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_otherToken)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 303
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 140669238640768) != 0)):
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





