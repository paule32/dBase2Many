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
        4,1,42,257,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,1,0,3,0,60,8,0,1,0,5,0,63,8,0,10,0,12,0,66,9,
        0,1,0,1,0,1,1,1,1,1,1,1,1,1,2,1,2,5,2,76,8,2,10,2,12,2,79,9,2,1,
        2,1,2,5,2,83,8,2,10,2,12,2,86,9,2,1,2,3,2,89,8,2,1,3,1,3,1,3,3,3,
        94,8,3,1,4,1,4,5,4,98,8,4,10,4,12,4,101,9,4,1,5,1,5,1,5,3,5,106,
        8,5,1,6,1,6,1,6,1,6,3,6,112,8,6,1,7,1,7,1,7,1,7,3,7,118,8,7,1,8,
        1,8,3,8,122,8,8,1,8,1,8,1,9,1,9,1,9,1,10,1,10,1,10,1,10,5,10,133,
        8,10,10,10,12,10,136,9,10,1,10,1,10,1,11,5,11,141,8,11,10,11,12,
        11,144,9,11,1,11,1,11,1,12,1,12,1,12,1,12,1,12,3,12,153,8,12,1,13,
        1,13,1,14,1,14,1,15,1,15,1,15,3,15,162,8,15,1,15,3,15,165,8,15,1,
        15,3,15,168,8,15,1,15,1,15,1,16,1,16,4,16,174,8,16,11,16,12,16,175,
        1,17,1,17,1,18,1,18,3,18,182,8,18,1,18,1,18,1,19,1,19,1,19,5,19,
        189,8,19,10,19,12,19,192,9,19,1,20,1,20,1,20,5,20,197,8,20,10,20,
        12,20,200,9,20,1,20,1,20,1,20,1,21,1,21,1,21,1,22,1,22,1,23,1,23,
        1,23,3,23,213,8,23,1,23,5,23,216,8,23,10,23,12,23,219,9,23,1,23,
        1,23,1,24,1,24,1,24,1,25,1,25,1,25,1,25,3,25,230,8,25,1,26,1,26,
        1,26,5,26,235,8,26,10,26,12,26,238,9,26,1,26,1,26,1,26,1,26,1,27,
        3,27,245,8,27,1,27,1,27,1,27,5,27,250,8,27,10,27,12,27,253,9,27,
        1,28,1,28,1,28,0,0,29,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,
        32,34,36,38,40,42,44,46,48,50,52,54,56,0,4,1,0,8,11,1,0,12,15,1,
        0,17,22,3,0,7,7,25,27,32,42,260,0,59,1,0,0,0,2,69,1,0,0,0,4,88,1,
        0,0,0,6,93,1,0,0,0,8,95,1,0,0,0,10,105,1,0,0,0,12,107,1,0,0,0,14,
        113,1,0,0,0,16,119,1,0,0,0,18,125,1,0,0,0,20,128,1,0,0,0,22,142,
        1,0,0,0,24,152,1,0,0,0,26,154,1,0,0,0,28,156,1,0,0,0,30,158,1,0,
        0,0,32,171,1,0,0,0,34,177,1,0,0,0,36,179,1,0,0,0,38,185,1,0,0,0,
        40,193,1,0,0,0,42,204,1,0,0,0,44,207,1,0,0,0,46,209,1,0,0,0,48,222,
        1,0,0,0,50,229,1,0,0,0,52,231,1,0,0,0,54,244,1,0,0,0,56,254,1,0,
        0,0,58,60,3,2,1,0,59,58,1,0,0,0,59,60,1,0,0,0,60,64,1,0,0,0,61,63,
        3,4,2,0,62,61,1,0,0,0,63,66,1,0,0,0,64,62,1,0,0,0,64,65,1,0,0,0,
        65,67,1,0,0,0,66,64,1,0,0,0,67,68,5,0,0,1,68,1,1,0,0,0,69,70,5,1,
        0,0,70,71,5,25,0,0,71,72,5,36,0,0,72,3,1,0,0,0,73,77,5,2,0,0,74,
        76,3,6,3,0,75,74,1,0,0,0,76,79,1,0,0,0,77,75,1,0,0,0,77,78,1,0,0,
        0,78,89,1,0,0,0,79,77,1,0,0,0,80,84,5,3,0,0,81,83,3,6,3,0,82,81,
        1,0,0,0,83,86,1,0,0,0,84,82,1,0,0,0,84,85,1,0,0,0,85,89,1,0,0,0,
        86,84,1,0,0,0,87,89,3,6,3,0,88,73,1,0,0,0,88,80,1,0,0,0,88,87,1,
        0,0,0,89,5,1,0,0,0,90,94,3,8,4,0,91,94,3,12,6,0,92,94,3,56,28,0,
        93,90,1,0,0,0,93,91,1,0,0,0,93,92,1,0,0,0,94,7,1,0,0,0,95,99,5,4,
        0,0,96,98,3,10,5,0,97,96,1,0,0,0,98,101,1,0,0,0,99,97,1,0,0,0,99,
        100,1,0,0,0,100,9,1,0,0,0,101,99,1,0,0,0,102,106,3,12,6,0,103,106,
        3,14,7,0,104,106,3,56,28,0,105,102,1,0,0,0,105,103,1,0,0,0,105,104,
        1,0,0,0,106,11,1,0,0,0,107,108,5,25,0,0,108,109,5,40,0,0,109,111,
        3,16,8,0,110,112,5,36,0,0,111,110,1,0,0,0,111,112,1,0,0,0,112,13,
        1,0,0,0,113,114,5,25,0,0,114,115,5,40,0,0,115,117,3,18,9,0,116,118,
        5,36,0,0,117,116,1,0,0,0,117,118,1,0,0,0,118,15,1,0,0,0,119,121,
        5,5,0,0,120,122,3,20,10,0,121,120,1,0,0,0,121,122,1,0,0,0,122,123,
        1,0,0,0,123,124,3,22,11,0,124,17,1,0,0,0,125,126,5,6,0,0,126,127,
        3,22,11,0,127,19,1,0,0,0,128,129,5,32,0,0,129,134,3,54,27,0,130,
        131,5,38,0,0,131,133,3,54,27,0,132,130,1,0,0,0,133,136,1,0,0,0,134,
        132,1,0,0,0,134,135,1,0,0,0,135,137,1,0,0,0,136,134,1,0,0,0,137,
        138,5,33,0,0,138,21,1,0,0,0,139,141,3,24,12,0,140,139,1,0,0,0,141,
        144,1,0,0,0,142,140,1,0,0,0,142,143,1,0,0,0,143,145,1,0,0,0,144,
        142,1,0,0,0,145,146,5,7,0,0,146,23,1,0,0,0,147,153,3,26,13,0,148,
        153,3,30,15,0,149,153,3,46,23,0,150,153,3,52,26,0,151,153,3,56,28,
        0,152,147,1,0,0,0,152,148,1,0,0,0,152,149,1,0,0,0,152,150,1,0,0,
        0,152,151,1,0,0,0,153,25,1,0,0,0,154,155,3,28,14,0,155,27,1,0,0,
        0,156,157,7,0,0,0,157,29,1,0,0,0,158,159,3,34,17,0,159,161,5,25,
        0,0,160,162,3,36,18,0,161,160,1,0,0,0,161,162,1,0,0,0,162,164,1,
        0,0,0,163,165,3,42,21,0,164,163,1,0,0,0,164,165,1,0,0,0,165,167,
        1,0,0,0,166,168,3,32,16,0,167,166,1,0,0,0,167,168,1,0,0,0,168,169,
        1,0,0,0,169,170,5,36,0,0,170,31,1,0,0,0,171,173,5,36,0,0,172,174,
        3,44,22,0,173,172,1,0,0,0,174,175,1,0,0,0,175,173,1,0,0,0,175,176,
        1,0,0,0,176,33,1,0,0,0,177,178,7,1,0,0,178,35,1,0,0,0,179,181,5,
        32,0,0,180,182,3,38,19,0,181,180,1,0,0,0,181,182,1,0,0,0,182,183,
        1,0,0,0,183,184,5,33,0,0,184,37,1,0,0,0,185,190,3,40,20,0,186,187,
        5,36,0,0,187,189,3,40,20,0,188,186,1,0,0,0,189,192,1,0,0,0,190,188,
        1,0,0,0,190,191,1,0,0,0,191,39,1,0,0,0,192,190,1,0,0,0,193,198,5,
        25,0,0,194,195,5,38,0,0,195,197,5,25,0,0,196,194,1,0,0,0,197,200,
        1,0,0,0,198,196,1,0,0,0,198,199,1,0,0,0,199,201,1,0,0,0,200,198,
        1,0,0,0,201,202,5,37,0,0,202,203,3,54,27,0,203,41,1,0,0,0,204,205,
        5,37,0,0,205,206,3,54,27,0,206,43,1,0,0,0,207,208,7,2,0,0,208,45,
        1,0,0,0,209,210,5,16,0,0,210,212,5,25,0,0,211,213,3,48,24,0,212,
        211,1,0,0,0,212,213,1,0,0,0,213,217,1,0,0,0,214,216,3,50,25,0,215,
        214,1,0,0,0,216,219,1,0,0,0,217,215,1,0,0,0,217,218,1,0,0,0,218,
        220,1,0,0,0,219,217,1,0,0,0,220,221,5,36,0,0,221,47,1,0,0,0,222,
        223,5,37,0,0,223,224,3,54,27,0,224,49,1,0,0,0,225,226,5,23,0,0,226,
        230,5,25,0,0,227,228,5,24,0,0,228,230,5,25,0,0,229,225,1,0,0,0,229,
        227,1,0,0,0,230,51,1,0,0,0,231,236,5,25,0,0,232,233,5,38,0,0,233,
        235,5,25,0,0,234,232,1,0,0,0,235,238,1,0,0,0,236,234,1,0,0,0,236,
        237,1,0,0,0,237,239,1,0,0,0,238,236,1,0,0,0,239,240,5,37,0,0,240,
        241,3,54,27,0,241,242,5,36,0,0,242,53,1,0,0,0,243,245,5,41,0,0,244,
        243,1,0,0,0,244,245,1,0,0,0,245,246,1,0,0,0,246,251,5,25,0,0,247,
        248,5,39,0,0,248,250,5,25,0,0,249,247,1,0,0,0,250,253,1,0,0,0,251,
        249,1,0,0,0,251,252,1,0,0,0,252,55,1,0,0,0,253,251,1,0,0,0,254,255,
        7,3,0,0,255,57,1,0,0,0,27,59,64,77,84,88,93,99,105,111,117,121,134,
        142,152,161,164,167,175,181,190,198,212,217,229,236,244,251
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
                     "'('", "')'", "'['", "']'", "';'", "':'", "','", "'.'", 
                     "'='", "'^'" ]

    symbolicNames = [ "<INVALID>", "UNIT", "INTERFACE", "IMPLEMENTATION", 
                      "TYPE", "CLASS", "RECORD", "END", "PUBLIC", "PRIVATE", 
                      "PROTECTED", "PUBLISHED", "PROCEDURE", "FUNCTION", 
                      "CONSTRUCTOR", "DESTRUCTOR", "PROPERTY", "VIRTUAL", 
                      "OVERRIDE", "ABSTRACT", "STATIC", "OVERLOAD", "REINTRODUCE", 
                      "READ", "WRITE", "IDENT", "STRING", "NUMBER", "LINE_COMMENT", 
                      "BRACE_COMMENT", "PAREN_COMMENT", "WS", "LPAREN", 
                      "RPAREN", "LBRACK", "RBRACK", "SEMI", "COLON", "COMMA", 
                      "DOT", "EQ", "CARET", "OTHER" ]

    RULE_unitFile = 0
    RULE_unitHeader = 1
    RULE_unitSection = 2
    RULE_declaration = 3
    RULE_typeSection = 4
    RULE_typeDeclaration = 5
    RULE_classDeclaration = 6
    RULE_recordDeclaration = 7
    RULE_classType = 8
    RULE_recordType = 9
    RULE_classInheritance = 10
    RULE_classBody = 11
    RULE_classMember = 12
    RULE_visibilitySection = 13
    RULE_visibility = 14
    RULE_methodDeclaration = 15
    RULE_methodDirectiveList = 16
    RULE_methodKind = 17
    RULE_parameterList = 18
    RULE_parameterDecl = 19
    RULE_parameterItem = 20
    RULE_returnType = 21
    RULE_methodDirective = 22
    RULE_propertyDeclaration = 23
    RULE_propertyType = 24
    RULE_propertyAccessor = 25
    RULE_fieldDeclaration = 26
    RULE_typeName = 27
    RULE_otherToken = 28

    ruleNames =  [ "unitFile", "unitHeader", "unitSection", "declaration", 
                   "typeSection", "typeDeclaration", "classDeclaration", 
                   "recordDeclaration", "classType", "recordType", "classInheritance", 
                   "classBody", "classMember", "visibilitySection", "visibility", 
                   "methodDeclaration", "methodDirectiveList", "methodKind", 
                   "parameterList", "parameterDecl", "parameterItem", "returnType", 
                   "methodDirective", "propertyDeclaration", "propertyType", 
                   "propertyAccessor", "fieldDeclaration", "typeName", "otherToken" ]

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
    IDENT=25
    STRING=26
    NUMBER=27
    LINE_COMMENT=28
    BRACE_COMMENT=29
    PAREN_COMMENT=30
    WS=31
    LPAREN=32
    RPAREN=33
    LBRACK=34
    RBRACK=35
    SEMI=36
    COLON=37
    COMMA=38
    DOT=39
    EQ=40
    CARET=41
    OTHER=42

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
            self.state = 59
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 58
                self.unitHeader()


            self.state = 64
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 8792032936092) != 0):
                self.state = 61
                self.unitSection()
                self.state = 66
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 67
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
            self.state = 69
            self.match(PasDocParser.UNIT)
            self.state = 70
            self.match(PasDocParser.IDENT)
            self.state = 71
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
            self.state = 88
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 73
                self.match(PasDocParser.INTERFACE)
                self.state = 77
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 74
                        self.declaration() 
                    self.state = 79
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 80
                self.match(PasDocParser.IMPLEMENTATION)
                self.state = 84
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 81
                        self.declaration() 
                    self.state = 86
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

                pass
            elif token in [4, 7, 25, 26, 27, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]:
                self.enterOuterAlt(localctx, 3)
                self.state = 87
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
            self.state = 93
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 90
                self.typeSection()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 91
                self.classDeclaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 92
                self.otherToken()
                pass


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
        self.enterRule(localctx, 8, self.RULE_typeSection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            self.match(PasDocParser.TYPE)
            self.state = 99
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 96
                    self.typeDeclaration() 
                self.state = 101
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

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
        self.enterRule(localctx, 10, self.RULE_typeDeclaration)
        try:
            self.state = 105
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 102
                self.classDeclaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 103
                self.recordDeclaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 104
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
        self.enterRule(localctx, 12, self.RULE_classDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.match(PasDocParser.IDENT)
            self.state = 108
            self.match(PasDocParser.EQ)
            self.state = 109
            self.classType()
            self.state = 111
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.state = 110
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
        self.enterRule(localctx, 14, self.RULE_recordDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            self.match(PasDocParser.IDENT)
            self.state = 114
            self.match(PasDocParser.EQ)
            self.state = 115
            self.recordType()
            self.state = 117
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.state = 116
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
        self.enterRule(localctx, 16, self.RULE_classType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            self.match(PasDocParser.CLASS)
            self.state = 121
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.state = 120
                self.classInheritance()


            self.state = 123
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
        self.enterRule(localctx, 18, self.RULE_recordType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 125
            self.match(PasDocParser.RECORD)
            self.state = 126
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
        self.enterRule(localctx, 20, self.RULE_classInheritance)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 128
            self.match(PasDocParser.LPAREN)
            self.state = 129
            self.typeName()
            self.state = 134
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 130
                self.match(PasDocParser.COMMA)
                self.state = 131
                self.typeName()
                self.state = 136
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 137
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
        self.enterRule(localctx, 22, self.RULE_classBody)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 142
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 139
                    self.classMember() 
                self.state = 144
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

            self.state = 145
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
        self.enterRule(localctx, 24, self.RULE_classMember)
        try:
            self.state = 152
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 147
                self.visibilitySection()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 148
                self.methodDeclaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 149
                self.propertyDeclaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 150
                self.fieldDeclaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 151
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
        self.enterRule(localctx, 26, self.RULE_visibilitySection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 154
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
        self.enterRule(localctx, 28, self.RULE_visibility)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 156
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
        self.enterRule(localctx, 30, self.RULE_methodDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 158
            self.methodKind()
            self.state = 159
            self.match(PasDocParser.IDENT)
            self.state = 161
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==32:
                self.state = 160
                self.parameterList()


            self.state = 164
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==37:
                self.state = 163
                self.returnType()


            self.state = 167
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.state = 166
                self.methodDirectiveList()


            self.state = 169
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
        self.enterRule(localctx, 32, self.RULE_methodDirectiveList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 171
            self.match(PasDocParser.SEMI)
            self.state = 173 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 172
                self.methodDirective()
                self.state = 175 
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
        self.enterRule(localctx, 34, self.RULE_methodKind)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 177
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
        self.enterRule(localctx, 36, self.RULE_parameterList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 179
            self.match(PasDocParser.LPAREN)
            self.state = 181
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==25:
                self.state = 180
                self.parameterDecl()


            self.state = 183
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
        self.enterRule(localctx, 38, self.RULE_parameterDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 185
            self.parameterItem()
            self.state = 190
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==36:
                self.state = 186
                self.match(PasDocParser.SEMI)
                self.state = 187
                self.parameterItem()
                self.state = 192
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
        self.enterRule(localctx, 40, self.RULE_parameterItem)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 193
            self.match(PasDocParser.IDENT)
            self.state = 198
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 194
                self.match(PasDocParser.COMMA)
                self.state = 195
                self.match(PasDocParser.IDENT)
                self.state = 200
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 201
            self.match(PasDocParser.COLON)
            self.state = 202
            self.typeName()
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
        self.enterRule(localctx, 42, self.RULE_returnType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 204
            self.match(PasDocParser.COLON)
            self.state = 205
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
        self.enterRule(localctx, 44, self.RULE_methodDirective)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 207
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
        self.enterRule(localctx, 46, self.RULE_propertyDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 209
            self.match(PasDocParser.PROPERTY)
            self.state = 210
            self.match(PasDocParser.IDENT)
            self.state = 212
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==37:
                self.state = 211
                self.propertyType()


            self.state = 217
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==23 or _la==24:
                self.state = 214
                self.propertyAccessor()
                self.state = 219
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 220
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
        self.enterRule(localctx, 48, self.RULE_propertyType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 222
            self.match(PasDocParser.COLON)
            self.state = 223
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
        self.enterRule(localctx, 50, self.RULE_propertyAccessor)
        try:
            self.state = 229
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.enterOuterAlt(localctx, 1)
                self.state = 225
                self.match(PasDocParser.READ)
                self.state = 226
                self.match(PasDocParser.IDENT)
                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 2)
                self.state = 227
                self.match(PasDocParser.WRITE)
                self.state = 228
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
        self.enterRule(localctx, 52, self.RULE_fieldDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 231
            self.match(PasDocParser.IDENT)
            self.state = 236
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 232
                self.match(PasDocParser.COMMA)
                self.state = 233
                self.match(PasDocParser.IDENT)
                self.state = 238
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 239
            self.match(PasDocParser.COLON)
            self.state = 240
            self.typeName()
            self.state = 241
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
        self.enterRule(localctx, 54, self.RULE_typeName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 244
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==41:
                self.state = 243
                self.match(PasDocParser.CARET)


            self.state = 246
            self.match(PasDocParser.IDENT)
            self.state = 251
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==39:
                self.state = 247
                self.match(PasDocParser.DOT)
                self.state = 248
                self.match(PasDocParser.IDENT)
                self.state = 253
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
        self.enterRule(localctx, 56, self.RULE_otherToken)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 254
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8792032936064) != 0)):
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





