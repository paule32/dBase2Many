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
        4,1,65,583,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,2,46,
        7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,2,52,7,52,
        2,53,7,53,2,54,7,54,2,55,7,55,2,56,7,56,2,57,7,57,2,58,7,58,2,59,
        7,59,1,0,1,0,1,0,1,0,5,0,125,8,0,10,0,12,0,128,9,0,1,0,1,0,1,0,1,
        1,1,1,1,1,1,1,1,1,3,1,138,8,1,1,2,1,2,4,2,142,8,2,11,2,12,2,143,
        1,3,1,3,1,3,5,3,149,8,3,10,3,12,3,152,9,3,1,3,1,3,1,4,1,4,1,4,1,
        4,1,5,1,5,1,6,1,6,4,6,164,8,6,11,6,12,6,165,1,7,1,7,1,7,1,7,1,7,
        1,7,1,7,1,7,3,7,176,8,7,1,8,1,8,1,8,1,8,3,8,182,8,8,1,8,1,8,1,9,
        1,9,1,9,3,9,189,8,9,1,9,1,9,1,10,1,10,1,10,5,10,196,8,10,10,10,12,
        10,199,9,10,1,10,3,10,202,8,10,1,11,1,11,1,11,1,11,1,11,5,11,209,
        8,11,10,11,12,11,212,9,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,3,11,
        221,8,11,1,12,1,12,1,12,1,12,1,13,1,13,1,13,3,13,230,8,13,1,14,1,
        14,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,16,1,16,1,16,5,16,244,8,
        16,10,16,12,16,247,9,16,1,17,1,17,1,17,3,17,252,8,17,1,18,1,18,1,
        18,1,18,5,18,258,8,18,10,18,12,18,261,9,18,1,18,1,18,1,18,1,19,1,
        19,1,19,1,19,1,19,1,20,1,20,1,20,3,20,274,8,20,1,20,1,20,1,20,1,
        20,1,20,3,20,281,8,20,1,21,1,21,1,21,3,21,286,8,21,1,21,1,21,1,21,
        3,21,291,8,21,1,22,1,22,1,22,1,22,5,22,297,8,22,10,22,12,22,300,
        9,22,1,22,1,22,1,23,3,23,305,8,23,1,23,1,23,1,23,1,23,1,24,1,24,
        1,24,3,24,314,8,24,1,25,1,25,1,25,3,25,319,8,25,1,25,1,25,1,26,1,
        26,3,26,325,8,26,1,26,3,26,328,8,26,1,27,1,27,1,27,1,27,5,27,334,
        8,27,10,27,12,27,337,9,27,1,27,1,27,1,28,1,28,3,28,343,8,28,1,29,
        1,29,4,29,347,8,29,11,29,12,29,348,1,30,1,30,1,30,1,30,1,30,1,31,
        1,31,3,31,358,8,31,1,32,1,32,1,32,5,32,363,8,32,10,32,12,32,366,
        9,32,1,33,5,33,369,8,33,10,33,12,33,372,9,33,1,33,1,33,1,33,1,33,
        1,34,1,34,1,34,1,34,3,34,382,8,34,1,35,1,35,3,35,386,8,35,5,35,388,
        8,35,10,35,12,35,391,9,35,1,36,1,36,1,36,1,36,1,36,1,36,1,36,1,36,
        1,36,1,36,3,36,403,8,36,1,37,1,37,1,37,1,37,1,37,1,37,1,37,1,37,
        1,37,1,37,1,37,1,37,3,37,417,8,37,1,38,1,38,3,38,421,8,38,1,39,1,
        39,1,39,1,39,1,39,1,39,1,39,1,39,1,39,1,40,1,40,1,40,1,40,1,40,3,
        40,437,8,40,1,41,1,41,1,41,5,41,442,8,41,10,41,12,41,445,9,41,1,
        42,1,42,1,42,1,42,1,42,1,43,1,43,1,43,1,43,1,43,1,43,3,43,458,8,
        43,1,44,1,44,1,44,1,44,3,44,464,8,44,1,45,1,45,1,46,1,46,1,46,1,
        46,1,47,1,47,1,47,1,47,3,47,476,8,47,1,48,1,48,1,48,5,48,481,8,48,
        10,48,12,48,484,9,48,3,48,486,8,48,1,49,1,49,1,49,1,49,1,49,1,49,
        5,49,494,8,49,10,49,12,49,497,9,49,1,49,1,49,1,49,3,49,502,8,49,
        1,50,1,50,1,51,1,51,1,51,5,51,509,8,51,10,51,12,51,512,9,51,1,52,
        1,52,1,52,5,52,517,8,52,10,52,12,52,520,9,52,1,53,1,53,1,53,5,53,
        525,8,53,10,53,12,53,528,9,53,1,54,1,54,1,54,5,54,533,8,54,10,54,
        12,54,536,9,54,1,55,1,55,1,55,5,55,541,8,55,10,55,12,55,544,9,55,
        1,56,1,56,1,56,1,56,1,56,1,56,1,56,1,56,1,56,1,56,1,56,1,56,1,56,
        1,56,3,56,560,8,56,1,57,1,57,1,57,1,57,3,57,566,8,57,1,57,3,57,569,
        8,57,1,58,1,58,1,58,5,58,574,8,58,10,58,12,58,577,9,58,1,59,1,59,
        3,59,581,8,59,1,59,0,0,60,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,
        30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,
        74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,
        114,116,118,0,6,2,0,57,57,60,61,2,0,11,12,57,58,1,0,25,26,1,0,51,
        56,1,0,41,42,1,0,43,44,603,0,120,1,0,0,0,2,137,1,0,0,0,4,139,1,0,
        0,0,6,145,1,0,0,0,8,155,1,0,0,0,10,159,1,0,0,0,12,161,1,0,0,0,14,
        175,1,0,0,0,16,177,1,0,0,0,18,185,1,0,0,0,20,192,1,0,0,0,22,220,
        1,0,0,0,24,222,1,0,0,0,26,229,1,0,0,0,28,231,1,0,0,0,30,233,1,0,
        0,0,32,240,1,0,0,0,34,248,1,0,0,0,36,253,1,0,0,0,38,265,1,0,0,0,
        40,270,1,0,0,0,42,282,1,0,0,0,44,292,1,0,0,0,46,304,1,0,0,0,48,313,
        1,0,0,0,50,315,1,0,0,0,52,322,1,0,0,0,54,329,1,0,0,0,56,342,1,0,
        0,0,58,344,1,0,0,0,60,350,1,0,0,0,62,357,1,0,0,0,64,359,1,0,0,0,
        66,370,1,0,0,0,68,381,1,0,0,0,70,389,1,0,0,0,72,402,1,0,0,0,74,416,
        1,0,0,0,76,418,1,0,0,0,78,422,1,0,0,0,80,431,1,0,0,0,82,438,1,0,
        0,0,84,446,1,0,0,0,86,451,1,0,0,0,88,459,1,0,0,0,90,465,1,0,0,0,
        92,467,1,0,0,0,94,471,1,0,0,0,96,485,1,0,0,0,98,501,1,0,0,0,100,
        503,1,0,0,0,102,505,1,0,0,0,104,513,1,0,0,0,106,521,1,0,0,0,108,
        529,1,0,0,0,110,537,1,0,0,0,112,559,1,0,0,0,114,568,1,0,0,0,116,
        570,1,0,0,0,118,580,1,0,0,0,120,121,5,1,0,0,121,122,5,58,0,0,122,
        126,5,39,0,0,123,125,3,2,1,0,124,123,1,0,0,0,125,128,1,0,0,0,126,
        124,1,0,0,0,126,127,1,0,0,0,127,129,1,0,0,0,128,126,1,0,0,0,129,
        130,3,66,33,0,130,131,5,36,0,0,131,1,1,0,0,0,132,138,3,4,2,0,133,
        138,3,12,6,0,134,138,3,58,29,0,135,138,3,42,21,0,136,138,3,40,20,
        0,137,132,1,0,0,0,137,133,1,0,0,0,137,134,1,0,0,0,137,135,1,0,0,
        0,137,136,1,0,0,0,138,3,1,0,0,0,139,141,5,4,0,0,140,142,3,6,3,0,
        141,140,1,0,0,0,142,143,1,0,0,0,143,141,1,0,0,0,143,144,1,0,0,0,
        144,5,1,0,0,0,145,150,3,8,4,0,146,147,5,40,0,0,147,149,3,8,4,0,148,
        146,1,0,0,0,149,152,1,0,0,0,150,148,1,0,0,0,150,151,1,0,0,0,151,
        153,1,0,0,0,152,150,1,0,0,0,153,154,5,39,0,0,154,7,1,0,0,0,155,156,
        5,58,0,0,156,157,5,51,0,0,157,158,3,10,5,0,158,9,1,0,0,0,159,160,
        7,0,0,0,160,11,1,0,0,0,161,163,5,6,0,0,162,164,3,14,7,0,163,162,
        1,0,0,0,164,165,1,0,0,0,165,163,1,0,0,0,165,166,1,0,0,0,166,13,1,
        0,0,0,167,168,5,58,0,0,168,169,5,51,0,0,169,170,3,26,13,0,170,171,
        5,39,0,0,171,176,1,0,0,0,172,176,3,30,15,0,173,176,3,36,18,0,174,
        176,3,16,8,0,175,167,1,0,0,0,175,172,1,0,0,0,175,173,1,0,0,0,175,
        174,1,0,0,0,176,15,1,0,0,0,177,178,5,58,0,0,178,179,5,51,0,0,179,
        181,3,22,11,0,180,182,3,18,9,0,181,180,1,0,0,0,181,182,1,0,0,0,182,
        183,1,0,0,0,183,184,5,39,0,0,184,17,1,0,0,0,185,186,5,51,0,0,186,
        188,5,46,0,0,187,189,3,20,10,0,188,187,1,0,0,0,188,189,1,0,0,0,189,
        190,1,0,0,0,190,191,5,47,0,0,191,19,1,0,0,0,192,197,3,10,5,0,193,
        194,5,40,0,0,194,196,3,10,5,0,195,193,1,0,0,0,196,199,1,0,0,0,197,
        195,1,0,0,0,197,198,1,0,0,0,198,201,1,0,0,0,199,197,1,0,0,0,200,
        202,5,40,0,0,201,200,1,0,0,0,201,202,1,0,0,0,202,21,1,0,0,0,203,
        204,5,8,0,0,204,205,5,45,0,0,205,210,3,24,12,0,206,207,5,40,0,0,
        207,209,3,24,12,0,208,206,1,0,0,0,209,212,1,0,0,0,210,208,1,0,0,
        0,210,211,1,0,0,0,211,213,1,0,0,0,212,210,1,0,0,0,213,214,5,48,0,
        0,214,215,5,9,0,0,215,216,3,26,13,0,216,221,1,0,0,0,217,218,5,8,
        0,0,218,219,5,9,0,0,219,221,3,26,13,0,220,203,1,0,0,0,220,217,1,
        0,0,0,221,23,1,0,0,0,222,223,3,100,50,0,223,224,5,35,0,0,224,225,
        3,100,50,0,225,25,1,0,0,0,226,230,3,28,14,0,227,228,5,49,0,0,228,
        230,3,28,14,0,229,226,1,0,0,0,229,227,1,0,0,0,230,27,1,0,0,0,231,
        232,7,1,0,0,232,29,1,0,0,0,233,234,5,58,0,0,234,235,5,51,0,0,235,
        236,5,46,0,0,236,237,3,32,16,0,237,238,5,47,0,0,238,239,5,39,0,0,
        239,31,1,0,0,0,240,245,3,34,17,0,241,242,5,40,0,0,242,244,3,34,17,
        0,243,241,1,0,0,0,244,247,1,0,0,0,245,243,1,0,0,0,245,246,1,0,0,
        0,246,33,1,0,0,0,247,245,1,0,0,0,248,251,5,58,0,0,249,250,5,51,0,
        0,250,252,5,61,0,0,251,249,1,0,0,0,251,252,1,0,0,0,252,35,1,0,0,
        0,253,254,5,58,0,0,254,255,5,51,0,0,255,259,5,7,0,0,256,258,3,38,
        19,0,257,256,1,0,0,0,258,261,1,0,0,0,259,257,1,0,0,0,259,260,1,0,
        0,0,260,262,1,0,0,0,261,259,1,0,0,0,262,263,5,3,0,0,263,264,5,39,
        0,0,264,37,1,0,0,0,265,266,3,64,32,0,266,267,5,38,0,0,267,268,3,
        26,13,0,268,269,5,39,0,0,269,39,1,0,0,0,270,271,5,28,0,0,271,273,
        5,58,0,0,272,274,3,44,22,0,273,272,1,0,0,0,273,274,1,0,0,0,274,275,
        1,0,0,0,275,276,5,38,0,0,276,277,3,26,13,0,277,278,5,39,0,0,278,
        280,3,66,33,0,279,281,5,39,0,0,280,279,1,0,0,0,280,281,1,0,0,0,281,
        41,1,0,0,0,282,283,5,27,0,0,283,285,5,58,0,0,284,286,3,44,22,0,285,
        284,1,0,0,0,285,286,1,0,0,0,286,287,1,0,0,0,287,288,5,39,0,0,288,
        290,3,66,33,0,289,291,5,39,0,0,290,289,1,0,0,0,290,291,1,0,0,0,291,
        43,1,0,0,0,292,293,5,46,0,0,293,298,3,46,23,0,294,295,5,39,0,0,295,
        297,3,46,23,0,296,294,1,0,0,0,297,300,1,0,0,0,298,296,1,0,0,0,298,
        299,1,0,0,0,299,301,1,0,0,0,300,298,1,0,0,0,301,302,5,47,0,0,302,
        45,1,0,0,0,303,305,5,5,0,0,304,303,1,0,0,0,304,305,1,0,0,0,305,306,
        1,0,0,0,306,307,3,64,32,0,307,308,5,38,0,0,308,309,3,26,13,0,309,
        47,1,0,0,0,310,314,3,58,29,0,311,314,3,42,21,0,312,314,3,40,20,0,
        313,310,1,0,0,0,313,311,1,0,0,0,313,312,1,0,0,0,314,49,1,0,0,0,315,
        316,5,58,0,0,316,318,5,46,0,0,317,319,3,82,41,0,318,317,1,0,0,0,
        318,319,1,0,0,0,319,320,1,0,0,0,320,321,5,47,0,0,321,51,1,0,0,0,
        322,324,5,58,0,0,323,325,3,54,27,0,324,323,1,0,0,0,324,325,1,0,0,
        0,325,327,1,0,0,0,326,328,5,39,0,0,327,326,1,0,0,0,327,328,1,0,0,
        0,328,53,1,0,0,0,329,330,5,46,0,0,330,335,3,56,28,0,331,332,5,40,
        0,0,332,334,3,56,28,0,333,331,1,0,0,0,334,337,1,0,0,0,335,333,1,
        0,0,0,335,336,1,0,0,0,336,338,1,0,0,0,337,335,1,0,0,0,338,339,5,
        47,0,0,339,55,1,0,0,0,340,343,5,57,0,0,341,343,3,100,50,0,342,340,
        1,0,0,0,342,341,1,0,0,0,343,57,1,0,0,0,344,346,5,5,0,0,345,347,3,
        60,30,0,346,345,1,0,0,0,347,348,1,0,0,0,348,346,1,0,0,0,348,349,
        1,0,0,0,349,59,1,0,0,0,350,351,3,64,32,0,351,352,5,38,0,0,352,353,
        3,62,31,0,353,354,5,39,0,0,354,61,1,0,0,0,355,358,3,26,13,0,356,
        358,3,22,11,0,357,355,1,0,0,0,357,356,1,0,0,0,358,63,1,0,0,0,359,
        364,5,58,0,0,360,361,5,40,0,0,361,363,5,58,0,0,362,360,1,0,0,0,363,
        366,1,0,0,0,364,362,1,0,0,0,364,365,1,0,0,0,365,65,1,0,0,0,366,364,
        1,0,0,0,367,369,3,68,34,0,368,367,1,0,0,0,369,372,1,0,0,0,370,368,
        1,0,0,0,370,371,1,0,0,0,371,373,1,0,0,0,372,370,1,0,0,0,373,374,
        5,2,0,0,374,375,3,70,35,0,375,376,5,3,0,0,376,67,1,0,0,0,377,382,
        3,42,21,0,378,382,3,40,20,0,379,382,3,58,29,0,380,382,3,4,2,0,381,
        377,1,0,0,0,381,378,1,0,0,0,381,379,1,0,0,0,381,380,1,0,0,0,382,
        69,1,0,0,0,383,385,3,72,36,0,384,386,5,39,0,0,385,384,1,0,0,0,385,
        386,1,0,0,0,386,388,1,0,0,0,387,383,1,0,0,0,388,391,1,0,0,0,389,
        387,1,0,0,0,389,390,1,0,0,0,390,71,1,0,0,0,391,389,1,0,0,0,392,403,
        3,94,47,0,393,403,3,114,57,0,394,403,3,74,37,0,395,403,3,86,43,0,
        396,403,3,84,42,0,397,403,3,80,40,0,398,403,3,78,39,0,399,403,3,
        52,26,0,400,403,3,76,38,0,401,403,3,92,46,0,402,392,1,0,0,0,402,
        393,1,0,0,0,402,394,1,0,0,0,402,395,1,0,0,0,402,396,1,0,0,0,402,
        397,1,0,0,0,402,398,1,0,0,0,402,399,1,0,0,0,402,400,1,0,0,0,402,
        401,1,0,0,0,403,73,1,0,0,0,404,405,5,31,0,0,405,406,3,70,35,0,406,
        407,5,32,0,0,407,408,3,70,35,0,408,409,5,3,0,0,409,417,1,0,0,0,410,
        411,5,31,0,0,411,412,3,70,35,0,412,413,5,33,0,0,413,414,3,70,35,
        0,414,415,5,3,0,0,415,417,1,0,0,0,416,404,1,0,0,0,416,410,1,0,0,
        0,417,75,1,0,0,0,418,420,5,30,0,0,419,421,5,39,0,0,420,419,1,0,0,
        0,420,421,1,0,0,0,421,77,1,0,0,0,422,423,5,24,0,0,423,424,5,58,0,
        0,424,425,5,37,0,0,425,426,3,100,50,0,426,427,7,2,0,0,427,428,3,
        100,50,0,428,429,5,21,0,0,429,430,3,72,36,0,430,79,1,0,0,0,431,432,
        5,22,0,0,432,433,3,70,35,0,433,434,5,23,0,0,434,436,3,88,44,0,435,
        437,5,39,0,0,436,435,1,0,0,0,436,437,1,0,0,0,437,81,1,0,0,0,438,
        443,3,100,50,0,439,440,5,40,0,0,440,442,3,100,50,0,441,439,1,0,0,
        0,442,445,1,0,0,0,443,441,1,0,0,0,443,444,1,0,0,0,444,83,1,0,0,0,
        445,443,1,0,0,0,446,447,5,20,0,0,447,448,3,88,44,0,448,449,5,21,
        0,0,449,450,3,72,36,0,450,85,1,0,0,0,451,452,5,13,0,0,452,453,3,
        88,44,0,453,454,5,14,0,0,454,457,3,72,36,0,455,456,5,15,0,0,456,
        458,3,72,36,0,457,455,1,0,0,0,457,458,1,0,0,0,458,87,1,0,0,0,459,
        463,3,100,50,0,460,461,3,90,45,0,461,462,3,100,50,0,462,464,1,0,
        0,0,463,460,1,0,0,0,463,464,1,0,0,0,464,89,1,0,0,0,465,466,7,3,0,
        0,466,91,1,0,0,0,467,468,5,2,0,0,468,469,3,70,35,0,469,470,5,3,0,
        0,470,93,1,0,0,0,471,472,3,96,48,0,472,473,5,37,0,0,473,475,3,100,
        50,0,474,476,5,39,0,0,475,474,1,0,0,0,475,476,1,0,0,0,476,95,1,0,
        0,0,477,486,5,29,0,0,478,482,5,58,0,0,479,481,3,98,49,0,480,479,
        1,0,0,0,481,484,1,0,0,0,482,480,1,0,0,0,482,483,1,0,0,0,483,486,
        1,0,0,0,484,482,1,0,0,0,485,477,1,0,0,0,485,478,1,0,0,0,486,97,1,
        0,0,0,487,488,5,36,0,0,488,502,5,58,0,0,489,490,5,45,0,0,490,495,
        3,100,50,0,491,492,5,40,0,0,492,494,3,100,50,0,493,491,1,0,0,0,494,
        497,1,0,0,0,495,493,1,0,0,0,495,496,1,0,0,0,496,498,1,0,0,0,497,
        495,1,0,0,0,498,499,5,48,0,0,499,502,1,0,0,0,500,502,5,49,0,0,501,
        487,1,0,0,0,501,489,1,0,0,0,501,500,1,0,0,0,502,99,1,0,0,0,503,504,
        3,102,51,0,504,101,1,0,0,0,505,510,3,104,52,0,506,507,5,18,0,0,507,
        509,3,104,52,0,508,506,1,0,0,0,509,512,1,0,0,0,510,508,1,0,0,0,510,
        511,1,0,0,0,511,103,1,0,0,0,512,510,1,0,0,0,513,518,3,106,53,0,514,
        515,5,19,0,0,515,517,3,106,53,0,516,514,1,0,0,0,517,520,1,0,0,0,
        518,516,1,0,0,0,518,519,1,0,0,0,519,105,1,0,0,0,520,518,1,0,0,0,
        521,526,3,108,54,0,522,523,5,17,0,0,523,525,3,108,54,0,524,522,1,
        0,0,0,525,528,1,0,0,0,526,524,1,0,0,0,526,527,1,0,0,0,527,107,1,
        0,0,0,528,526,1,0,0,0,529,534,3,110,55,0,530,531,7,4,0,0,531,533,
        3,110,55,0,532,530,1,0,0,0,533,536,1,0,0,0,534,532,1,0,0,0,534,535,
        1,0,0,0,535,109,1,0,0,0,536,534,1,0,0,0,537,542,3,112,56,0,538,539,
        7,5,0,0,539,541,3,112,56,0,540,538,1,0,0,0,541,544,1,0,0,0,542,540,
        1,0,0,0,542,543,1,0,0,0,543,111,1,0,0,0,544,542,1,0,0,0,545,546,
        5,16,0,0,546,560,3,112,56,0,547,548,5,50,0,0,548,560,3,96,48,0,549,
        560,3,96,48,0,550,560,3,50,25,0,551,560,5,10,0,0,552,560,5,61,0,
        0,553,560,5,60,0,0,554,560,5,57,0,0,555,556,5,46,0,0,556,557,3,100,
        50,0,557,558,5,47,0,0,558,560,1,0,0,0,559,545,1,0,0,0,559,547,1,
        0,0,0,559,549,1,0,0,0,559,550,1,0,0,0,559,551,1,0,0,0,559,552,1,
        0,0,0,559,553,1,0,0,0,559,554,1,0,0,0,559,555,1,0,0,0,560,113,1,
        0,0,0,561,569,5,34,0,0,562,563,5,34,0,0,563,565,5,46,0,0,564,566,
        3,116,58,0,565,564,1,0,0,0,565,566,1,0,0,0,566,567,1,0,0,0,567,569,
        5,47,0,0,568,561,1,0,0,0,568,562,1,0,0,0,569,115,1,0,0,0,570,575,
        3,118,59,0,571,572,5,40,0,0,572,574,3,118,59,0,573,571,1,0,0,0,574,
        577,1,0,0,0,575,573,1,0,0,0,575,576,1,0,0,0,576,117,1,0,0,0,577,
        575,1,0,0,0,578,581,5,57,0,0,579,581,3,100,50,0,580,578,1,0,0,0,
        580,579,1,0,0,0,581,119,1,0,0,0,57,126,137,143,150,165,175,181,188,
        197,201,210,220,229,245,251,259,273,280,285,290,298,304,313,318,
        324,327,335,342,348,357,364,370,381,385,389,402,416,420,436,443,
        457,463,475,482,485,495,501,510,518,526,534,542,559,565,568,575,
        580
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
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'..'", "'.'", 
                     "':='", "':'", "';'", "','", "'+'", "'-'", "'*'", "'/'", 
                     "'['", "'('", "')'", "']'", "'^'", "'@'", "'='", "'<='", 
                     "'<>'", "'<'", "'>='", "'>'" ]

    symbolicNames = [ "<INVALID>", "PROGRAM", "BEGIN_", "END", "CONST", 
                      "VAR", "TYPE", "RECORD", "ARRAY", "OF", "NIL", "DOUBLE", 
                      "INTEGER", "IF", "THEN", "ELSE", "NOT", "AND", "OR", 
                      "XOR", "WHILE", "DO", "REPEAT", "UNTIL", "FOR", "TO", 
                      "DOWNTO", "PROCEDURE", "FUNCTION", "RESULT", "EXIT", 
                      "TRY", "FINALLY", "EXCEPT", "WRITELN", "DOTDOT", "DOT", 
                      "ASSIGN", "COLON", "SEMI", "COMMA", "PLUS", "MINUS", 
                      "STAR", "SLASH", "LBRACK", "LPAREN", "RPAREN", "RBRACK", 
                      "CARET", "AT", "EQ_OP", "LE_OP", "NE_OP", "LT_OP", 
                      "GE_OP", "GT_OP", "STRING", "IDENT", "HEXNUMBER", 
                      "FLOATNUMBER", "NUMBER", "WS", "COMMENT1", "COMMENT2", 
                      "COMMENT3" ]

    RULE_programFile = 0
    RULE_declarationPart = 1
    RULE_constSection = 2
    RULE_constDeclaration = 3
    RULE_constItem = 4
    RULE_constValue = 5
    RULE_typeSection = 6
    RULE_typeDeclaration = 7
    RULE_arrayDeclaration = 8
    RULE_arrayInitializer = 9
    RULE_arrayValueList = 10
    RULE_arrayType = 11
    RULE_arrayRange = 12
    RULE_typeName = 13
    RULE_simpleType = 14
    RULE_enumDeclaration = 15
    RULE_enumValueList = 16
    RULE_enumValue = 17
    RULE_recordDeclaration = 18
    RULE_recordFieldDeclaration = 19
    RULE_functionDeclaration = 20
    RULE_procedureDeclaration = 21
    RULE_formalParamList = 22
    RULE_formalParam = 23
    RULE_declaration = 24
    RULE_functionCallExpr = 25
    RULE_procedureCallStatement = 26
    RULE_actualParamList = 27
    RULE_actualParam = 28
    RULE_varSection = 29
    RULE_varDeclaration = 30
    RULE_varType = 31
    RULE_identList = 32
    RULE_block = 33
    RULE_localDeclaration = 34
    RULE_statementList = 35
    RULE_statement = 36
    RULE_tryStatement = 37
    RULE_exitStatement = 38
    RULE_forStatement = 39
    RULE_repeatStatement = 40
    RULE_argumentList = 41
    RULE_whileStatement = 42
    RULE_ifStatement = 43
    RULE_condition = 44
    RULE_compareOp = 45
    RULE_compoundStatement = 46
    RULE_assignment = 47
    RULE_variableRef = 48
    RULE_variableSuffix = 49
    RULE_expr = 50
    RULE_boolOrExpr = 51
    RULE_boolXorExpr = 52
    RULE_boolAndExpr = 53
    RULE_addExpr = 54
    RULE_term = 55
    RULE_factor = 56
    RULE_writeLnStatement = 57
    RULE_writeArgList = 58
    RULE_writeArg = 59

    ruleNames =  [ "programFile", "declarationPart", "constSection", "constDeclaration", 
                   "constItem", "constValue", "typeSection", "typeDeclaration", 
                   "arrayDeclaration", "arrayInitializer", "arrayValueList", 
                   "arrayType", "arrayRange", "typeName", "simpleType", 
                   "enumDeclaration", "enumValueList", "enumValue", "recordDeclaration", 
                   "recordFieldDeclaration", "functionDeclaration", "procedureDeclaration", 
                   "formalParamList", "formalParam", "declaration", "functionCallExpr", 
                   "procedureCallStatement", "actualParamList", "actualParam", 
                   "varSection", "varDeclaration", "varType", "identList", 
                   "block", "localDeclaration", "statementList", "statement", 
                   "tryStatement", "exitStatement", "forStatement", "repeatStatement", 
                   "argumentList", "whileStatement", "ifStatement", "condition", 
                   "compareOp", "compoundStatement", "assignment", "variableRef", 
                   "variableSuffix", "expr", "boolOrExpr", "boolXorExpr", 
                   "boolAndExpr", "addExpr", "term", "factor", "writeLnStatement", 
                   "writeArgList", "writeArg" ]

    EOF = Token.EOF
    PROGRAM=1
    BEGIN_=2
    END=3
    CONST=4
    VAR=5
    TYPE=6
    RECORD=7
    ARRAY=8
    OF=9
    NIL=10
    DOUBLE=11
    INTEGER=12
    IF=13
    THEN=14
    ELSE=15
    NOT=16
    AND=17
    OR=18
    XOR=19
    WHILE=20
    DO=21
    REPEAT=22
    UNTIL=23
    FOR=24
    TO=25
    DOWNTO=26
    PROCEDURE=27
    FUNCTION=28
    RESULT=29
    EXIT=30
    TRY=31
    FINALLY=32
    EXCEPT=33
    WRITELN=34
    DOTDOT=35
    DOT=36
    ASSIGN=37
    COLON=38
    SEMI=39
    COMMA=40
    PLUS=41
    MINUS=42
    STAR=43
    SLASH=44
    LBRACK=45
    LPAREN=46
    RPAREN=47
    RBRACK=48
    CARET=49
    AT=50
    EQ_OP=51
    LE_OP=52
    NE_OP=53
    LT_OP=54
    GE_OP=55
    GT_OP=56
    STRING=57
    IDENT=58
    HEXNUMBER=59
    FLOATNUMBER=60
    NUMBER=61
    WS=62
    COMMENT1=63
    COMMENT2=64
    COMMENT3=65

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
            self.state = 120
            self.match(MiniPascalParser.PROGRAM)
            self.state = 121
            self.match(MiniPascalParser.IDENT)
            self.state = 122
            self.match(MiniPascalParser.SEMI)
            self.state = 126
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 123
                    self.declarationPart() 
                self.state = 128
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 129
            self.block()
            self.state = 130
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


        def typeSection(self):
            return self.getTypedRuleContext(MiniPascalParser.TypeSectionContext,0)


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
            self.state = 137
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 132
                self.constSection()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 133
                self.typeSection()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 134
                self.varSection()
                pass
            elif token in [27]:
                self.enterOuterAlt(localctx, 4)
                self.state = 135
                self.procedureDeclaration()
                pass
            elif token in [28]:
                self.enterOuterAlt(localctx, 5)
                self.state = 136
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
            self.state = 139
            self.match(MiniPascalParser.CONST)
            self.state = 141 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 140
                self.constDeclaration()
                self.state = 143 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==58):
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

        def constItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.ConstItemContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.ConstItemContext,i)


        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.COMMA)
            else:
                return self.getToken(MiniPascalParser.COMMA, i)

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
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 145
            self.constItem()
            self.state = 150
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 146
                self.match(MiniPascalParser.COMMA)
                self.state = 147
                self.constItem()
                self.state = 152
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 153
            self.match(MiniPascalParser.SEMI)
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
            return self.getToken(MiniPascalParser.IDENT, 0)

        def EQ_OP(self):
            return self.getToken(MiniPascalParser.EQ_OP, 0)

        def constValue(self):
            return self.getTypedRuleContext(MiniPascalParser.ConstValueContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_constItem

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

        localctx = MiniPascalParser.ConstItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_constItem)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 155
            self.match(MiniPascalParser.IDENT)
            self.state = 156
            self.match(MiniPascalParser.EQ_OP)
            self.state = 157
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
        self.enterRule(localctx, 10, self.RULE_constValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 159
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3602879701896396800) != 0)):
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


    class TypeSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TYPE(self):
            return self.getToken(MiniPascalParser.TYPE, 0)

        def typeDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.TypeDeclarationContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.TypeDeclarationContext,i)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_typeSection

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

        localctx = MiniPascalParser.TypeSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_typeSection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 161
            self.match(MiniPascalParser.TYPE)
            self.state = 163 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 162
                self.typeDeclaration()
                self.state = 165 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==58):
                    break

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

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def EQ_OP(self):
            return self.getToken(MiniPascalParser.EQ_OP, 0)

        def typeName(self):
            return self.getTypedRuleContext(MiniPascalParser.TypeNameContext,0)


        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def enumDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.EnumDeclarationContext,0)


        def recordDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.RecordDeclarationContext,0)


        def arrayDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.ArrayDeclarationContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_typeDeclaration

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

        localctx = MiniPascalParser.TypeDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_typeDeclaration)
        try:
            self.state = 175
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 167
                self.match(MiniPascalParser.IDENT)
                self.state = 168
                self.match(MiniPascalParser.EQ_OP)
                self.state = 169
                self.typeName()
                self.state = 170
                self.match(MiniPascalParser.SEMI)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 172
                self.enumDeclaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 173
                self.recordDeclaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 174
                self.arrayDeclaration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def EQ_OP(self):
            return self.getToken(MiniPascalParser.EQ_OP, 0)

        def arrayType(self):
            return self.getTypedRuleContext(MiniPascalParser.ArrayTypeContext,0)


        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def arrayInitializer(self):
            return self.getTypedRuleContext(MiniPascalParser.ArrayInitializerContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_arrayDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayDeclaration" ):
                listener.enterArrayDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayDeclaration" ):
                listener.exitArrayDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayDeclaration" ):
                return visitor.visitArrayDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def arrayDeclaration(self):

        localctx = MiniPascalParser.ArrayDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_arrayDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 177
            self.match(MiniPascalParser.IDENT)
            self.state = 178
            self.match(MiniPascalParser.EQ_OP)
            self.state = 179
            self.arrayType()
            self.state = 181
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==51:
                self.state = 180
                self.arrayInitializer()


            self.state = 183
            self.match(MiniPascalParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayInitializerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ_OP(self):
            return self.getToken(MiniPascalParser.EQ_OP, 0)

        def LPAREN(self):
            return self.getToken(MiniPascalParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(MiniPascalParser.RPAREN, 0)

        def arrayValueList(self):
            return self.getTypedRuleContext(MiniPascalParser.ArrayValueListContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_arrayInitializer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayInitializer" ):
                listener.enterArrayInitializer(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayInitializer" ):
                listener.exitArrayInitializer(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayInitializer" ):
                return visitor.visitArrayInitializer(self)
            else:
                return visitor.visitChildren(self)




    def arrayInitializer(self):

        localctx = MiniPascalParser.ArrayInitializerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_arrayInitializer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 185
            self.match(MiniPascalParser.EQ_OP)
            self.state = 186
            self.match(MiniPascalParser.LPAREN)
            self.state = 188
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3602879701896396800) != 0):
                self.state = 187
                self.arrayValueList()


            self.state = 190
            self.match(MiniPascalParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayValueListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def constValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.ConstValueContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.ConstValueContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.COMMA)
            else:
                return self.getToken(MiniPascalParser.COMMA, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_arrayValueList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayValueList" ):
                listener.enterArrayValueList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayValueList" ):
                listener.exitArrayValueList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayValueList" ):
                return visitor.visitArrayValueList(self)
            else:
                return visitor.visitChildren(self)




    def arrayValueList(self):

        localctx = MiniPascalParser.ArrayValueListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_arrayValueList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
            self.constValue()
            self.state = 197
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 193
                    self.match(MiniPascalParser.COMMA)
                    self.state = 194
                    self.constValue() 
                self.state = 199
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

            self.state = 201
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==40:
                self.state = 200
                self.match(MiniPascalParser.COMMA)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ARRAY(self):
            return self.getToken(MiniPascalParser.ARRAY, 0)

        def LBRACK(self):
            return self.getToken(MiniPascalParser.LBRACK, 0)

        def arrayRange(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.ArrayRangeContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.ArrayRangeContext,i)


        def RBRACK(self):
            return self.getToken(MiniPascalParser.RBRACK, 0)

        def OF(self):
            return self.getToken(MiniPascalParser.OF, 0)

        def typeName(self):
            return self.getTypedRuleContext(MiniPascalParser.TypeNameContext,0)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.COMMA)
            else:
                return self.getToken(MiniPascalParser.COMMA, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_arrayType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayType" ):
                listener.enterArrayType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayType" ):
                listener.exitArrayType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayType" ):
                return visitor.visitArrayType(self)
            else:
                return visitor.visitChildren(self)




    def arrayType(self):

        localctx = MiniPascalParser.ArrayTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_arrayType)
        self._la = 0 # Token type
        try:
            self.state = 220
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 203
                self.match(MiniPascalParser.ARRAY)
                self.state = 204
                self.match(MiniPascalParser.LBRACK)
                self.state = 205
                self.arrayRange()
                self.state = 210
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==40:
                    self.state = 206
                    self.match(MiniPascalParser.COMMA)
                    self.state = 207
                    self.arrayRange()
                    self.state = 212
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 213
                self.match(MiniPascalParser.RBRACK)
                self.state = 214
                self.match(MiniPascalParser.OF)
                self.state = 215
                self.typeName()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 217
                self.match(MiniPascalParser.ARRAY)
                self.state = 218
                self.match(MiniPascalParser.OF)
                self.state = 219
                self.typeName()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayRangeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.ExprContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.ExprContext,i)


        def DOTDOT(self):
            return self.getToken(MiniPascalParser.DOTDOT, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_arrayRange

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayRange" ):
                listener.enterArrayRange(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayRange" ):
                listener.exitArrayRange(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayRange" ):
                return visitor.visitArrayRange(self)
            else:
                return visitor.visitChildren(self)




    def arrayRange(self):

        localctx = MiniPascalParser.ArrayRangeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_arrayRange)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 222
            self.expr()
            self.state = 223
            self.match(MiniPascalParser.DOTDOT)
            self.state = 224
            self.expr()
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

        def simpleType(self):
            return self.getTypedRuleContext(MiniPascalParser.SimpleTypeContext,0)


        def CARET(self):
            return self.getToken(MiniPascalParser.CARET, 0)

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
        try:
            self.state = 229
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11, 12, 57, 58]:
                self.enterOuterAlt(localctx, 1)
                self.state = 226
                self.simpleType()
                pass
            elif token in [49]:
                self.enterOuterAlt(localctx, 2)
                self.state = 227
                self.match(MiniPascalParser.CARET)
                self.state = 228
                self.simpleType()
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


    class SimpleTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def INTEGER(self):
            return self.getToken(MiniPascalParser.INTEGER, 0)

        def DOUBLE(self):
            return self.getToken(MiniPascalParser.DOUBLE, 0)

        def STRING(self):
            return self.getToken(MiniPascalParser.STRING, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_simpleType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleType" ):
                listener.enterSimpleType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleType" ):
                listener.exitSimpleType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleType" ):
                return visitor.visitSimpleType(self)
            else:
                return visitor.visitChildren(self)




    def simpleType(self):

        localctx = MiniPascalParser.SimpleTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_simpleType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 231
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 432345564227573760) != 0)):
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


    class EnumDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def EQ_OP(self):
            return self.getToken(MiniPascalParser.EQ_OP, 0)

        def LPAREN(self):
            return self.getToken(MiniPascalParser.LPAREN, 0)

        def enumValueList(self):
            return self.getTypedRuleContext(MiniPascalParser.EnumValueListContext,0)


        def RPAREN(self):
            return self.getToken(MiniPascalParser.RPAREN, 0)

        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_enumDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnumDeclaration" ):
                listener.enterEnumDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnumDeclaration" ):
                listener.exitEnumDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnumDeclaration" ):
                return visitor.visitEnumDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def enumDeclaration(self):

        localctx = MiniPascalParser.EnumDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_enumDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 233
            self.match(MiniPascalParser.IDENT)
            self.state = 234
            self.match(MiniPascalParser.EQ_OP)
            self.state = 235
            self.match(MiniPascalParser.LPAREN)
            self.state = 236
            self.enumValueList()
            self.state = 237
            self.match(MiniPascalParser.RPAREN)
            self.state = 238
            self.match(MiniPascalParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnumValueListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def enumValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.EnumValueContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.EnumValueContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.COMMA)
            else:
                return self.getToken(MiniPascalParser.COMMA, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_enumValueList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnumValueList" ):
                listener.enterEnumValueList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnumValueList" ):
                listener.exitEnumValueList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnumValueList" ):
                return visitor.visitEnumValueList(self)
            else:
                return visitor.visitChildren(self)




    def enumValueList(self):

        localctx = MiniPascalParser.EnumValueListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_enumValueList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 240
            self.enumValue()
            self.state = 245
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 241
                self.match(MiniPascalParser.COMMA)
                self.state = 242
                self.enumValue()
                self.state = 247
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnumValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def EQ_OP(self):
            return self.getToken(MiniPascalParser.EQ_OP, 0)

        def NUMBER(self):
            return self.getToken(MiniPascalParser.NUMBER, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_enumValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnumValue" ):
                listener.enterEnumValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnumValue" ):
                listener.exitEnumValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnumValue" ):
                return visitor.visitEnumValue(self)
            else:
                return visitor.visitChildren(self)




    def enumValue(self):

        localctx = MiniPascalParser.EnumValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_enumValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 248
            self.match(MiniPascalParser.IDENT)
            self.state = 251
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==51:
                self.state = 249
                self.match(MiniPascalParser.EQ_OP)
                self.state = 250
                self.match(MiniPascalParser.NUMBER)


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
            return self.getToken(MiniPascalParser.IDENT, 0)

        def EQ_OP(self):
            return self.getToken(MiniPascalParser.EQ_OP, 0)

        def RECORD(self):
            return self.getToken(MiniPascalParser.RECORD, 0)

        def END(self):
            return self.getToken(MiniPascalParser.END, 0)

        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def recordFieldDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.RecordFieldDeclarationContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.RecordFieldDeclarationContext,i)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_recordDeclaration

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

        localctx = MiniPascalParser.RecordDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_recordDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 253
            self.match(MiniPascalParser.IDENT)
            self.state = 254
            self.match(MiniPascalParser.EQ_OP)
            self.state = 255
            self.match(MiniPascalParser.RECORD)
            self.state = 259
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==58:
                self.state = 256
                self.recordFieldDeclaration()
                self.state = 261
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 262
            self.match(MiniPascalParser.END)
            self.state = 263
            self.match(MiniPascalParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RecordFieldDeclarationContext(ParserRuleContext):
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
            return MiniPascalParser.RULE_recordFieldDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRecordFieldDeclaration" ):
                listener.enterRecordFieldDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRecordFieldDeclaration" ):
                listener.exitRecordFieldDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRecordFieldDeclaration" ):
                return visitor.visitRecordFieldDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def recordFieldDeclaration(self):

        localctx = MiniPascalParser.RecordFieldDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_recordFieldDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 265
            self.identList()
            self.state = 266
            self.match(MiniPascalParser.COLON)
            self.state = 267
            self.typeName()
            self.state = 268
            self.match(MiniPascalParser.SEMI)
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
        self.enterRule(localctx, 40, self.RULE_functionDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 270
            self.match(MiniPascalParser.FUNCTION)
            self.state = 271
            self.match(MiniPascalParser.IDENT)
            self.state = 273
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==46:
                self.state = 272
                self.formalParamList()


            self.state = 275
            self.match(MiniPascalParser.COLON)
            self.state = 276
            self.typeName()
            self.state = 277
            self.match(MiniPascalParser.SEMI)
            self.state = 278
            self.block()
            self.state = 280
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 279
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
        self.enterRule(localctx, 42, self.RULE_procedureDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 282
            self.match(MiniPascalParser.PROCEDURE)
            self.state = 283
            self.match(MiniPascalParser.IDENT)
            self.state = 285
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==46:
                self.state = 284
                self.formalParamList()


            self.state = 287
            self.match(MiniPascalParser.SEMI)
            self.state = 288
            self.block()
            self.state = 290
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 289
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
        self.enterRule(localctx, 44, self.RULE_formalParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 292
            self.match(MiniPascalParser.LPAREN)
            self.state = 293
            self.formalParam()
            self.state = 298
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==39:
                self.state = 294
                self.match(MiniPascalParser.SEMI)
                self.state = 295
                self.formalParam()
                self.state = 300
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 301
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


        def VAR(self):
            return self.getToken(MiniPascalParser.VAR, 0)

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
        self.enterRule(localctx, 46, self.RULE_formalParam)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 304
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 303
                self.match(MiniPascalParser.VAR)


            self.state = 306
            self.identList()
            self.state = 307
            self.match(MiniPascalParser.COLON)
            self.state = 308
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
        self.enterRule(localctx, 48, self.RULE_declaration)
        try:
            self.state = 313
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 310
                self.varSection()
                pass
            elif token in [27]:
                self.enterOuterAlt(localctx, 2)
                self.state = 311
                self.procedureDeclaration()
                pass
            elif token in [28]:
                self.enterOuterAlt(localctx, 3)
                self.state = 312
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
        self.enterRule(localctx, 50, self.RULE_functionCallExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 315
            self.match(MiniPascalParser.IDENT)
            self.state = 316
            self.match(MiniPascalParser.LPAREN)
            self.state = 318
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3892306347236066304) != 0):
                self.state = 317
                self.argumentList()


            self.state = 320
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
        self.enterRule(localctx, 52, self.RULE_procedureCallStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 322
            self.match(MiniPascalParser.IDENT)
            self.state = 324
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==46:
                self.state = 323
                self.actualParamList()


            self.state = 327
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,25,self._ctx)
            if la_ == 1:
                self.state = 326
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
        self.enterRule(localctx, 54, self.RULE_actualParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 329
            self.match(MiniPascalParser.LPAREN)
            self.state = 330
            self.actualParam()
            self.state = 335
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 331
                self.match(MiniPascalParser.COMMA)
                self.state = 332
                self.actualParam()
                self.state = 337
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 338
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
        self.enterRule(localctx, 56, self.RULE_actualParam)
        try:
            self.state = 342
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,27,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 340
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 341
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
        self.enterRule(localctx, 58, self.RULE_varSection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 344
            self.match(MiniPascalParser.VAR)
            self.state = 346 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 345
                self.varDeclaration()
                self.state = 348 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==58):
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

        def varType(self):
            return self.getTypedRuleContext(MiniPascalParser.VarTypeContext,0)


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
        self.enterRule(localctx, 60, self.RULE_varDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 350
            self.identList()
            self.state = 351
            self.match(MiniPascalParser.COLON)
            self.state = 352
            self.varType()
            self.state = 353
            self.match(MiniPascalParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeName(self):
            return self.getTypedRuleContext(MiniPascalParser.TypeNameContext,0)


        def arrayType(self):
            return self.getTypedRuleContext(MiniPascalParser.ArrayTypeContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_varType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarType" ):
                listener.enterVarType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarType" ):
                listener.exitVarType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarType" ):
                return visitor.visitVarType(self)
            else:
                return visitor.visitChildren(self)




    def varType(self):

        localctx = MiniPascalParser.VarTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_varType)
        try:
            self.state = 357
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11, 12, 49, 57, 58]:
                self.enterOuterAlt(localctx, 1)
                self.state = 355
                self.typeName()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 2)
                self.state = 356
                self.arrayType()
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
        self.enterRule(localctx, 64, self.RULE_identList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 359
            self.match(MiniPascalParser.IDENT)
            self.state = 364
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 360
                self.match(MiniPascalParser.COMMA)
                self.state = 361
                self.match(MiniPascalParser.IDENT)
                self.state = 366
                self._errHandler.sync(self)
                _la = self._input.LA(1)

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
        self.enterRule(localctx, 66, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 370
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 402653232) != 0):
                self.state = 367
                self.localDeclaration()
                self.state = 372
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 373
            self.match(MiniPascalParser.BEGIN_)
            self.state = 374
            self.statementList()
            self.state = 375
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
        self.enterRule(localctx, 68, self.RULE_localDeclaration)
        try:
            self.state = 381
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27]:
                self.enterOuterAlt(localctx, 1)
                self.state = 377
                self.procedureDeclaration()
                pass
            elif token in [28]:
                self.enterOuterAlt(localctx, 2)
                self.state = 378
                self.functionDeclaration()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 379
                self.varSection()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 380
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
        self.enterRule(localctx, 70, self.RULE_statementList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 389
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 288230397111705604) != 0):
                self.state = 383
                self.statement()
                self.state = 385
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==39:
                    self.state = 384
                    self.match(MiniPascalParser.SEMI)


                self.state = 391
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


        def tryStatement(self):
            return self.getTypedRuleContext(MiniPascalParser.TryStatementContext,0)


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


        def exitStatement(self):
            return self.getTypedRuleContext(MiniPascalParser.ExitStatementContext,0)


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
        self.enterRule(localctx, 72, self.RULE_statement)
        try:
            self.state = 402
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,35,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 392
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 393
                self.writeLnStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 394
                self.tryStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 395
                self.ifStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 396
                self.whileStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 397
                self.repeatStatement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 398
                self.forStatement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 399
                self.procedureCallStatement()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 400
                self.exitStatement()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 401
                self.compoundStatement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TryStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRY(self):
            return self.getToken(MiniPascalParser.TRY, 0)

        def statementList(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.StatementListContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.StatementListContext,i)


        def FINALLY(self):
            return self.getToken(MiniPascalParser.FINALLY, 0)

        def END(self):
            return self.getToken(MiniPascalParser.END, 0)

        def EXCEPT(self):
            return self.getToken(MiniPascalParser.EXCEPT, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_tryStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTryStatement" ):
                listener.enterTryStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTryStatement" ):
                listener.exitTryStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTryStatement" ):
                return visitor.visitTryStatement(self)
            else:
                return visitor.visitChildren(self)




    def tryStatement(self):

        localctx = MiniPascalParser.TryStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_tryStatement)
        try:
            self.state = 416
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,36,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 404
                self.match(MiniPascalParser.TRY)
                self.state = 405
                self.statementList()
                self.state = 406
                self.match(MiniPascalParser.FINALLY)
                self.state = 407
                self.statementList()
                self.state = 408
                self.match(MiniPascalParser.END)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 410
                self.match(MiniPascalParser.TRY)
                self.state = 411
                self.statementList()
                self.state = 412
                self.match(MiniPascalParser.EXCEPT)
                self.state = 413
                self.statementList()
                self.state = 414
                self.match(MiniPascalParser.END)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExitStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXIT(self):
            return self.getToken(MiniPascalParser.EXIT, 0)

        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_exitStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExitStatement" ):
                listener.enterExitStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExitStatement" ):
                listener.exitExitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExitStatement" ):
                return visitor.visitExitStatement(self)
            else:
                return visitor.visitChildren(self)




    def exitStatement(self):

        localctx = MiniPascalParser.ExitStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_exitStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 418
            self.match(MiniPascalParser.EXIT)
            self.state = 420
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,37,self._ctx)
            if la_ == 1:
                self.state = 419
                self.match(MiniPascalParser.SEMI)


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
        self.enterRule(localctx, 78, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 422
            self.match(MiniPascalParser.FOR)
            self.state = 423
            self.match(MiniPascalParser.IDENT)
            self.state = 424
            self.match(MiniPascalParser.ASSIGN)
            self.state = 425
            self.expr()
            self.state = 426
            _la = self._input.LA(1)
            if not(_la==25 or _la==26):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 427
            self.expr()
            self.state = 428
            self.match(MiniPascalParser.DO)
            self.state = 429
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
        self.enterRule(localctx, 80, self.RULE_repeatStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 431
            self.match(MiniPascalParser.REPEAT)
            self.state = 432
            self.statementList()
            self.state = 433
            self.match(MiniPascalParser.UNTIL)
            self.state = 434
            self.condition()
            self.state = 436
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,38,self._ctx)
            if la_ == 1:
                self.state = 435
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
        self.enterRule(localctx, 82, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 438
            self.expr()
            self.state = 443
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 439
                self.match(MiniPascalParser.COMMA)
                self.state = 440
                self.expr()
                self.state = 445
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
        self.enterRule(localctx, 84, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 446
            self.match(MiniPascalParser.WHILE)
            self.state = 447
            self.condition()
            self.state = 448
            self.match(MiniPascalParser.DO)
            self.state = 449
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
        self.enterRule(localctx, 86, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 451
            self.match(MiniPascalParser.IF)
            self.state = 452
            self.condition()
            self.state = 453
            self.match(MiniPascalParser.THEN)
            self.state = 454
            self.statement()
            self.state = 457
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,40,self._ctx)
            if la_ == 1:
                self.state = 455
                self.match(MiniPascalParser.ELSE)
                self.state = 456
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
        self.enterRule(localctx, 88, self.RULE_condition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 459
            self.expr()
            self.state = 463
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 141863388262170624) != 0):
                self.state = 460
                self.compareOp()
                self.state = 461
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
        self.enterRule(localctx, 90, self.RULE_compareOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 465
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 141863388262170624) != 0)):
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
        self.enterRule(localctx, 92, self.RULE_compoundStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 467
            self.match(MiniPascalParser.BEGIN_)
            self.state = 468
            self.statementList()
            self.state = 469
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

        def variableRef(self):
            return self.getTypedRuleContext(MiniPascalParser.VariableRefContext,0)


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
        self.enterRule(localctx, 94, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 471
            self.variableRef()
            self.state = 472
            self.match(MiniPascalParser.ASSIGN)
            self.state = 473
            self.expr()
            self.state = 475
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,42,self._ctx)
            if la_ == 1:
                self.state = 474
                self.match(MiniPascalParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RESULT(self):
            return self.getToken(MiniPascalParser.RESULT, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def variableSuffix(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.VariableSuffixContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.VariableSuffixContext,i)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_variableRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariableRef" ):
                listener.enterVariableRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariableRef" ):
                listener.exitVariableRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableRef" ):
                return visitor.visitVariableRef(self)
            else:
                return visitor.visitChildren(self)




    def variableRef(self):

        localctx = MiniPascalParser.VariableRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_variableRef)
        self._la = 0 # Token type
        try:
            self.state = 485
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [29]:
                self.enterOuterAlt(localctx, 1)
                self.state = 477
                self.match(MiniPascalParser.RESULT)
                pass
            elif token in [58]:
                self.enterOuterAlt(localctx, 2)
                self.state = 478
                self.match(MiniPascalParser.IDENT)
                self.state = 482
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 598203044986880) != 0):
                    self.state = 479
                    self.variableSuffix()
                    self.state = 484
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

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


    class VariableSuffixContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOT(self):
            return self.getToken(MiniPascalParser.DOT, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def LBRACK(self):
            return self.getToken(MiniPascalParser.LBRACK, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.ExprContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.ExprContext,i)


        def RBRACK(self):
            return self.getToken(MiniPascalParser.RBRACK, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.COMMA)
            else:
                return self.getToken(MiniPascalParser.COMMA, i)

        def CARET(self):
            return self.getToken(MiniPascalParser.CARET, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_variableSuffix

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariableSuffix" ):
                listener.enterVariableSuffix(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariableSuffix" ):
                listener.exitVariableSuffix(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableSuffix" ):
                return visitor.visitVariableSuffix(self)
            else:
                return visitor.visitChildren(self)




    def variableSuffix(self):

        localctx = MiniPascalParser.VariableSuffixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_variableSuffix)
        self._la = 0 # Token type
        try:
            self.state = 501
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [36]:
                self.enterOuterAlt(localctx, 1)
                self.state = 487
                self.match(MiniPascalParser.DOT)
                self.state = 488
                self.match(MiniPascalParser.IDENT)
                pass
            elif token in [45]:
                self.enterOuterAlt(localctx, 2)
                self.state = 489
                self.match(MiniPascalParser.LBRACK)
                self.state = 490
                self.expr()
                self.state = 495
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==40:
                    self.state = 491
                    self.match(MiniPascalParser.COMMA)
                    self.state = 492
                    self.expr()
                    self.state = 497
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 498
                self.match(MiniPascalParser.RBRACK)
                pass
            elif token in [49]:
                self.enterOuterAlt(localctx, 3)
                self.state = 500
                self.match(MiniPascalParser.CARET)
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


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def boolOrExpr(self):
            return self.getTypedRuleContext(MiniPascalParser.BoolOrExprContext,0)


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
        self.enterRule(localctx, 100, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 503
            self.boolOrExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BoolOrExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def boolXorExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.BoolXorExprContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.BoolXorExprContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.OR)
            else:
                return self.getToken(MiniPascalParser.OR, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_boolOrExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolOrExpr" ):
                listener.enterBoolOrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolOrExpr" ):
                listener.exitBoolOrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolOrExpr" ):
                return visitor.visitBoolOrExpr(self)
            else:
                return visitor.visitChildren(self)




    def boolOrExpr(self):

        localctx = MiniPascalParser.BoolOrExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_boolOrExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 505
            self.boolXorExpr()
            self.state = 510
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==18:
                self.state = 506
                self.match(MiniPascalParser.OR)
                self.state = 507
                self.boolXorExpr()
                self.state = 512
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BoolXorExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def boolAndExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.BoolAndExprContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.BoolAndExprContext,i)


        def XOR(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.XOR)
            else:
                return self.getToken(MiniPascalParser.XOR, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_boolXorExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolXorExpr" ):
                listener.enterBoolXorExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolXorExpr" ):
                listener.exitBoolXorExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolXorExpr" ):
                return visitor.visitBoolXorExpr(self)
            else:
                return visitor.visitChildren(self)




    def boolXorExpr(self):

        localctx = MiniPascalParser.BoolXorExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 104, self.RULE_boolXorExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 513
            self.boolAndExpr()
            self.state = 518
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==19:
                self.state = 514
                self.match(MiniPascalParser.XOR)
                self.state = 515
                self.boolAndExpr()
                self.state = 520
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BoolAndExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def addExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.AddExprContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.AddExprContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.AND)
            else:
                return self.getToken(MiniPascalParser.AND, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_boolAndExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolAndExpr" ):
                listener.enterBoolAndExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolAndExpr" ):
                listener.exitBoolAndExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolAndExpr" ):
                return visitor.visitBoolAndExpr(self)
            else:
                return visitor.visitChildren(self)




    def boolAndExpr(self):

        localctx = MiniPascalParser.BoolAndExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 106, self.RULE_boolAndExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 521
            self.addExpr()
            self.state = 526
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==17:
                self.state = 522
                self.match(MiniPascalParser.AND)
                self.state = 523
                self.addExpr()
                self.state = 528
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddExprContext(ParserRuleContext):
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
            return MiniPascalParser.RULE_addExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddExpr" ):
                listener.enterAddExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddExpr" ):
                listener.exitAddExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddExpr" ):
                return visitor.visitAddExpr(self)
            else:
                return visitor.visitChildren(self)




    def addExpr(self):

        localctx = MiniPascalParser.AddExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 108, self.RULE_addExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 529
            self.term()
            self.state = 534
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==41 or _la==42:
                self.state = 530
                _la = self._input.LA(1)
                if not(_la==41 or _la==42):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 531
                self.term()
                self.state = 536
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
        self.enterRule(localctx, 110, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 537
            self.factor()
            self.state = 542
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==43 or _la==44:
                self.state = 538
                _la = self._input.LA(1)
                if not(_la==43 or _la==44):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 539
                self.factor()
                self.state = 544
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

        def NOT(self):
            return self.getToken(MiniPascalParser.NOT, 0)

        def factor(self):
            return self.getTypedRuleContext(MiniPascalParser.FactorContext,0)


        def AT(self):
            return self.getToken(MiniPascalParser.AT, 0)

        def variableRef(self):
            return self.getTypedRuleContext(MiniPascalParser.VariableRefContext,0)


        def functionCallExpr(self):
            return self.getTypedRuleContext(MiniPascalParser.FunctionCallExprContext,0)


        def NIL(self):
            return self.getToken(MiniPascalParser.NIL, 0)

        def NUMBER(self):
            return self.getToken(MiniPascalParser.NUMBER, 0)

        def FLOATNUMBER(self):
            return self.getToken(MiniPascalParser.FLOATNUMBER, 0)

        def STRING(self):
            return self.getToken(MiniPascalParser.STRING, 0)

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
        self.enterRule(localctx, 112, self.RULE_factor)
        try:
            self.state = 559
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,52,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 545
                self.match(MiniPascalParser.NOT)
                self.state = 546
                self.factor()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 547
                self.match(MiniPascalParser.AT)
                self.state = 548
                self.variableRef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 549
                self.variableRef()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 550
                self.functionCallExpr()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 551
                self.match(MiniPascalParser.NIL)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 552
                self.match(MiniPascalParser.NUMBER)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 553
                self.match(MiniPascalParser.FLOATNUMBER)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 554
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 555
                self.match(MiniPascalParser.LPAREN)
                self.state = 556
                self.expr()
                self.state = 557
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
        self.enterRule(localctx, 114, self.RULE_writeLnStatement)
        self._la = 0 # Token type
        try:
            self.state = 568
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,54,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 561
                self.match(MiniPascalParser.WRITELN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 562
                self.match(MiniPascalParser.WRITELN)
                self.state = 563
                self.match(MiniPascalParser.LPAREN)
                self.state = 565
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3892306347236066304) != 0):
                    self.state = 564
                    self.writeArgList()


                self.state = 567
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
        self.enterRule(localctx, 116, self.RULE_writeArgList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 570
            self.writeArg()
            self.state = 575
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 571
                self.match(MiniPascalParser.COMMA)
                self.state = 572
                self.writeArg()
                self.state = 577
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
        self.enterRule(localctx, 118, self.RULE_writeArg)
        try:
            self.state = 580
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,56,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 578
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 579
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





