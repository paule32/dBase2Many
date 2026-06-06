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
        4,1,56,506,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,2,46,
        7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,2,52,7,52,
        1,0,1,0,1,0,1,0,5,0,111,8,0,10,0,12,0,114,9,0,1,0,1,0,1,0,1,1,1,
        1,1,1,1,1,1,1,3,1,124,8,1,1,2,1,2,4,2,128,8,2,11,2,12,2,129,1,3,
        1,3,1,3,5,3,135,8,3,10,3,12,3,138,9,3,1,3,1,3,1,4,1,4,1,4,1,4,1,
        5,1,5,1,6,1,6,4,6,150,8,6,11,6,12,6,151,1,7,1,7,1,7,1,7,1,7,1,7,
        1,7,1,7,3,7,162,8,7,1,8,1,8,1,8,1,8,3,8,168,8,8,1,8,1,8,1,9,1,9,
        1,9,3,9,175,8,9,1,9,1,9,1,10,1,10,1,10,5,10,182,8,10,10,10,12,10,
        185,9,10,1,10,3,10,188,8,10,1,11,1,11,1,11,1,11,1,11,5,11,195,8,
        11,10,11,12,11,198,9,11,1,11,1,11,1,11,1,11,1,12,1,12,1,12,1,12,
        1,13,1,13,1,13,3,13,211,8,13,1,14,1,14,1,15,1,15,1,15,1,15,1,15,
        1,15,1,15,1,16,1,16,1,16,5,16,225,8,16,10,16,12,16,228,9,16,1,17,
        1,17,1,17,3,17,233,8,17,1,18,1,18,1,18,1,18,5,18,239,8,18,10,18,
        12,18,242,9,18,1,18,1,18,1,18,1,19,1,19,1,19,1,19,1,19,1,20,1,20,
        1,20,3,20,255,8,20,1,20,1,20,1,20,1,20,1,20,3,20,262,8,20,1,21,1,
        21,1,21,3,21,267,8,21,1,21,1,21,1,21,3,21,272,8,21,1,22,1,22,1,22,
        1,22,5,22,278,8,22,10,22,12,22,281,9,22,1,22,1,22,1,23,1,23,1,23,
        1,23,1,24,1,24,1,24,3,24,292,8,24,1,25,1,25,1,25,3,25,297,8,25,1,
        25,1,25,1,26,1,26,3,26,303,8,26,1,26,3,26,306,8,26,1,27,1,27,1,27,
        1,27,5,27,312,8,27,10,27,12,27,315,9,27,1,27,1,27,1,28,1,28,3,28,
        321,8,28,1,29,1,29,4,29,325,8,29,11,29,12,29,326,1,30,1,30,1,30,
        1,30,1,30,1,31,1,31,1,31,5,31,337,8,31,10,31,12,31,340,9,31,1,32,
        5,32,343,8,32,10,32,12,32,346,9,32,1,32,1,32,1,32,1,32,1,33,1,33,
        1,33,1,33,3,33,356,8,33,1,34,1,34,3,34,360,8,34,5,34,362,8,34,10,
        34,12,34,365,9,34,1,35,1,35,1,35,1,35,1,35,1,35,1,35,1,35,3,35,375,
        8,35,1,36,1,36,1,36,1,36,1,36,1,36,1,36,1,36,1,36,1,37,1,37,1,37,
        1,37,1,37,3,37,391,8,37,1,38,1,38,1,38,5,38,396,8,38,10,38,12,38,
        399,9,38,1,39,1,39,1,39,1,39,1,39,1,40,1,40,1,40,1,40,1,40,1,40,
        3,40,412,8,40,1,41,1,41,1,41,1,41,1,42,1,42,1,43,1,43,1,43,1,43,
        1,44,1,44,1,44,1,44,3,44,428,8,44,1,45,1,45,1,45,5,45,433,8,45,10,
        45,12,45,436,9,45,3,45,438,8,45,1,46,1,46,1,46,1,46,1,46,1,46,5,
        46,446,8,46,10,46,12,46,449,9,46,1,46,1,46,1,46,3,46,454,8,46,1,
        47,1,47,1,47,5,47,459,8,47,10,47,12,47,462,9,47,1,48,1,48,1,48,5,
        48,467,8,48,10,48,12,48,470,9,48,1,49,1,49,1,49,1,49,1,49,1,49,1,
        49,1,49,1,49,1,49,1,49,3,49,483,8,49,1,50,1,50,1,50,1,50,3,50,489,
        8,50,1,50,3,50,492,8,50,1,51,1,51,1,51,5,51,497,8,51,10,51,12,51,
        500,9,51,1,52,1,52,3,52,504,8,52,1,52,0,0,53,0,2,4,6,8,10,12,14,
        16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,
        60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,
        102,104,0,6,2,0,48,48,51,52,2,0,10,11,48,49,1,0,20,21,1,0,42,47,
        1,0,32,33,1,0,34,35,520,0,106,1,0,0,0,2,123,1,0,0,0,4,125,1,0,0,
        0,6,131,1,0,0,0,8,141,1,0,0,0,10,145,1,0,0,0,12,147,1,0,0,0,14,161,
        1,0,0,0,16,163,1,0,0,0,18,171,1,0,0,0,20,178,1,0,0,0,22,189,1,0,
        0,0,24,203,1,0,0,0,26,210,1,0,0,0,28,212,1,0,0,0,30,214,1,0,0,0,
        32,221,1,0,0,0,34,229,1,0,0,0,36,234,1,0,0,0,38,246,1,0,0,0,40,251,
        1,0,0,0,42,263,1,0,0,0,44,273,1,0,0,0,46,284,1,0,0,0,48,291,1,0,
        0,0,50,293,1,0,0,0,52,300,1,0,0,0,54,307,1,0,0,0,56,320,1,0,0,0,
        58,322,1,0,0,0,60,328,1,0,0,0,62,333,1,0,0,0,64,344,1,0,0,0,66,355,
        1,0,0,0,68,363,1,0,0,0,70,374,1,0,0,0,72,376,1,0,0,0,74,385,1,0,
        0,0,76,392,1,0,0,0,78,400,1,0,0,0,80,405,1,0,0,0,82,413,1,0,0,0,
        84,417,1,0,0,0,86,419,1,0,0,0,88,423,1,0,0,0,90,437,1,0,0,0,92,453,
        1,0,0,0,94,455,1,0,0,0,96,463,1,0,0,0,98,482,1,0,0,0,100,491,1,0,
        0,0,102,493,1,0,0,0,104,503,1,0,0,0,106,107,5,1,0,0,107,108,5,49,
        0,0,108,112,5,30,0,0,109,111,3,2,1,0,110,109,1,0,0,0,111,114,1,0,
        0,0,112,110,1,0,0,0,112,113,1,0,0,0,113,115,1,0,0,0,114,112,1,0,
        0,0,115,116,3,64,32,0,116,117,5,27,0,0,117,1,1,0,0,0,118,124,3,4,
        2,0,119,124,3,12,6,0,120,124,3,58,29,0,121,124,3,42,21,0,122,124,
        3,40,20,0,123,118,1,0,0,0,123,119,1,0,0,0,123,120,1,0,0,0,123,121,
        1,0,0,0,123,122,1,0,0,0,124,3,1,0,0,0,125,127,5,4,0,0,126,128,3,
        6,3,0,127,126,1,0,0,0,128,129,1,0,0,0,129,127,1,0,0,0,129,130,1,
        0,0,0,130,5,1,0,0,0,131,136,3,8,4,0,132,133,5,31,0,0,133,135,3,8,
        4,0,134,132,1,0,0,0,135,138,1,0,0,0,136,134,1,0,0,0,136,137,1,0,
        0,0,137,139,1,0,0,0,138,136,1,0,0,0,139,140,5,30,0,0,140,7,1,0,0,
        0,141,142,5,49,0,0,142,143,5,42,0,0,143,144,3,10,5,0,144,9,1,0,0,
        0,145,146,7,0,0,0,146,11,1,0,0,0,147,149,5,6,0,0,148,150,3,14,7,
        0,149,148,1,0,0,0,150,151,1,0,0,0,151,149,1,0,0,0,151,152,1,0,0,
        0,152,13,1,0,0,0,153,154,5,49,0,0,154,155,5,42,0,0,155,156,3,26,
        13,0,156,157,5,30,0,0,157,162,1,0,0,0,158,162,3,30,15,0,159,162,
        3,36,18,0,160,162,3,16,8,0,161,153,1,0,0,0,161,158,1,0,0,0,161,159,
        1,0,0,0,161,160,1,0,0,0,162,15,1,0,0,0,163,164,5,49,0,0,164,165,
        5,42,0,0,165,167,3,22,11,0,166,168,3,18,9,0,167,166,1,0,0,0,167,
        168,1,0,0,0,168,169,1,0,0,0,169,170,5,30,0,0,170,17,1,0,0,0,171,
        172,5,42,0,0,172,174,5,37,0,0,173,175,3,20,10,0,174,173,1,0,0,0,
        174,175,1,0,0,0,175,176,1,0,0,0,176,177,5,38,0,0,177,19,1,0,0,0,
        178,183,3,10,5,0,179,180,5,31,0,0,180,182,3,10,5,0,181,179,1,0,0,
        0,182,185,1,0,0,0,183,181,1,0,0,0,183,184,1,0,0,0,184,187,1,0,0,
        0,185,183,1,0,0,0,186,188,5,31,0,0,187,186,1,0,0,0,187,188,1,0,0,
        0,188,21,1,0,0,0,189,190,5,8,0,0,190,191,5,36,0,0,191,196,3,24,12,
        0,192,193,5,31,0,0,193,195,3,24,12,0,194,192,1,0,0,0,195,198,1,0,
        0,0,196,194,1,0,0,0,196,197,1,0,0,0,197,199,1,0,0,0,198,196,1,0,
        0,0,199,200,5,39,0,0,200,201,5,9,0,0,201,202,3,26,13,0,202,23,1,
        0,0,0,203,204,3,94,47,0,204,205,5,26,0,0,205,206,3,94,47,0,206,25,
        1,0,0,0,207,211,3,28,14,0,208,209,5,40,0,0,209,211,3,28,14,0,210,
        207,1,0,0,0,210,208,1,0,0,0,211,27,1,0,0,0,212,213,7,1,0,0,213,29,
        1,0,0,0,214,215,5,49,0,0,215,216,5,42,0,0,216,217,5,37,0,0,217,218,
        3,32,16,0,218,219,5,38,0,0,219,220,5,30,0,0,220,31,1,0,0,0,221,226,
        3,34,17,0,222,223,5,31,0,0,223,225,3,34,17,0,224,222,1,0,0,0,225,
        228,1,0,0,0,226,224,1,0,0,0,226,227,1,0,0,0,227,33,1,0,0,0,228,226,
        1,0,0,0,229,232,5,49,0,0,230,231,5,42,0,0,231,233,5,52,0,0,232,230,
        1,0,0,0,232,233,1,0,0,0,233,35,1,0,0,0,234,235,5,49,0,0,235,236,
        5,42,0,0,236,240,5,7,0,0,237,239,3,38,19,0,238,237,1,0,0,0,239,242,
        1,0,0,0,240,238,1,0,0,0,240,241,1,0,0,0,241,243,1,0,0,0,242,240,
        1,0,0,0,243,244,5,3,0,0,244,245,5,30,0,0,245,37,1,0,0,0,246,247,
        3,62,31,0,247,248,5,29,0,0,248,249,3,26,13,0,249,250,5,30,0,0,250,
        39,1,0,0,0,251,252,5,23,0,0,252,254,5,49,0,0,253,255,3,44,22,0,254,
        253,1,0,0,0,254,255,1,0,0,0,255,256,1,0,0,0,256,257,5,29,0,0,257,
        258,3,26,13,0,258,259,5,30,0,0,259,261,3,64,32,0,260,262,5,30,0,
        0,261,260,1,0,0,0,261,262,1,0,0,0,262,41,1,0,0,0,263,264,5,22,0,
        0,264,266,5,49,0,0,265,267,3,44,22,0,266,265,1,0,0,0,266,267,1,0,
        0,0,267,268,1,0,0,0,268,269,5,30,0,0,269,271,3,64,32,0,270,272,5,
        30,0,0,271,270,1,0,0,0,271,272,1,0,0,0,272,43,1,0,0,0,273,274,5,
        37,0,0,274,279,3,46,23,0,275,276,5,30,0,0,276,278,3,46,23,0,277,
        275,1,0,0,0,278,281,1,0,0,0,279,277,1,0,0,0,279,280,1,0,0,0,280,
        282,1,0,0,0,281,279,1,0,0,0,282,283,5,38,0,0,283,45,1,0,0,0,284,
        285,3,62,31,0,285,286,5,29,0,0,286,287,3,26,13,0,287,47,1,0,0,0,
        288,292,3,58,29,0,289,292,3,42,21,0,290,292,3,40,20,0,291,288,1,
        0,0,0,291,289,1,0,0,0,291,290,1,0,0,0,292,49,1,0,0,0,293,294,5,49,
        0,0,294,296,5,37,0,0,295,297,3,76,38,0,296,295,1,0,0,0,296,297,1,
        0,0,0,297,298,1,0,0,0,298,299,5,38,0,0,299,51,1,0,0,0,300,302,5,
        49,0,0,301,303,3,54,27,0,302,301,1,0,0,0,302,303,1,0,0,0,303,305,
        1,0,0,0,304,306,5,30,0,0,305,304,1,0,0,0,305,306,1,0,0,0,306,53,
        1,0,0,0,307,308,5,37,0,0,308,313,3,56,28,0,309,310,5,31,0,0,310,
        312,3,56,28,0,311,309,1,0,0,0,312,315,1,0,0,0,313,311,1,0,0,0,313,
        314,1,0,0,0,314,316,1,0,0,0,315,313,1,0,0,0,316,317,5,38,0,0,317,
        55,1,0,0,0,318,321,5,48,0,0,319,321,3,94,47,0,320,318,1,0,0,0,320,
        319,1,0,0,0,321,57,1,0,0,0,322,324,5,5,0,0,323,325,3,60,30,0,324,
        323,1,0,0,0,325,326,1,0,0,0,326,324,1,0,0,0,326,327,1,0,0,0,327,
        59,1,0,0,0,328,329,3,62,31,0,329,330,5,29,0,0,330,331,3,26,13,0,
        331,332,5,30,0,0,332,61,1,0,0,0,333,338,5,49,0,0,334,335,5,31,0,
        0,335,337,5,49,0,0,336,334,1,0,0,0,337,340,1,0,0,0,338,336,1,0,0,
        0,338,339,1,0,0,0,339,63,1,0,0,0,340,338,1,0,0,0,341,343,3,66,33,
        0,342,341,1,0,0,0,343,346,1,0,0,0,344,342,1,0,0,0,344,345,1,0,0,
        0,345,347,1,0,0,0,346,344,1,0,0,0,347,348,5,2,0,0,348,349,3,68,34,
        0,349,350,5,3,0,0,350,65,1,0,0,0,351,356,3,42,21,0,352,356,3,40,
        20,0,353,356,3,58,29,0,354,356,3,4,2,0,355,351,1,0,0,0,355,352,1,
        0,0,0,355,353,1,0,0,0,355,354,1,0,0,0,356,67,1,0,0,0,357,359,3,70,
        35,0,358,360,5,30,0,0,359,358,1,0,0,0,359,360,1,0,0,0,360,362,1,
        0,0,0,361,357,1,0,0,0,362,365,1,0,0,0,363,361,1,0,0,0,363,364,1,
        0,0,0,364,69,1,0,0,0,365,363,1,0,0,0,366,375,3,88,44,0,367,375,3,
        100,50,0,368,375,3,80,40,0,369,375,3,78,39,0,370,375,3,74,37,0,371,
        375,3,72,36,0,372,375,3,52,26,0,373,375,3,86,43,0,374,366,1,0,0,
        0,374,367,1,0,0,0,374,368,1,0,0,0,374,369,1,0,0,0,374,370,1,0,0,
        0,374,371,1,0,0,0,374,372,1,0,0,0,374,373,1,0,0,0,375,71,1,0,0,0,
        376,377,5,19,0,0,377,378,5,49,0,0,378,379,5,28,0,0,379,380,3,94,
        47,0,380,381,7,2,0,0,381,382,3,94,47,0,382,383,5,16,0,0,383,384,
        3,70,35,0,384,73,1,0,0,0,385,386,5,17,0,0,386,387,3,68,34,0,387,
        388,5,18,0,0,388,390,3,82,41,0,389,391,5,30,0,0,390,389,1,0,0,0,
        390,391,1,0,0,0,391,75,1,0,0,0,392,397,3,94,47,0,393,394,5,31,0,
        0,394,396,3,94,47,0,395,393,1,0,0,0,396,399,1,0,0,0,397,395,1,0,
        0,0,397,398,1,0,0,0,398,77,1,0,0,0,399,397,1,0,0,0,400,401,5,15,
        0,0,401,402,3,82,41,0,402,403,5,16,0,0,403,404,3,70,35,0,404,79,
        1,0,0,0,405,406,5,12,0,0,406,407,3,82,41,0,407,408,5,13,0,0,408,
        411,3,70,35,0,409,410,5,14,0,0,410,412,3,70,35,0,411,409,1,0,0,0,
        411,412,1,0,0,0,412,81,1,0,0,0,413,414,3,94,47,0,414,415,3,84,42,
        0,415,416,3,94,47,0,416,83,1,0,0,0,417,418,7,3,0,0,418,85,1,0,0,
        0,419,420,5,2,0,0,420,421,3,68,34,0,421,422,5,3,0,0,422,87,1,0,0,
        0,423,424,3,90,45,0,424,425,5,28,0,0,425,427,3,94,47,0,426,428,5,
        30,0,0,427,426,1,0,0,0,427,428,1,0,0,0,428,89,1,0,0,0,429,438,5,
        24,0,0,430,434,5,49,0,0,431,433,3,92,46,0,432,431,1,0,0,0,433,436,
        1,0,0,0,434,432,1,0,0,0,434,435,1,0,0,0,435,438,1,0,0,0,436,434,
        1,0,0,0,437,429,1,0,0,0,437,430,1,0,0,0,438,91,1,0,0,0,439,440,5,
        27,0,0,440,454,5,49,0,0,441,442,5,36,0,0,442,447,3,94,47,0,443,444,
        5,31,0,0,444,446,3,94,47,0,445,443,1,0,0,0,446,449,1,0,0,0,447,445,
        1,0,0,0,447,448,1,0,0,0,448,450,1,0,0,0,449,447,1,0,0,0,450,451,
        5,39,0,0,451,454,1,0,0,0,452,454,5,40,0,0,453,439,1,0,0,0,453,441,
        1,0,0,0,453,452,1,0,0,0,454,93,1,0,0,0,455,460,3,96,48,0,456,457,
        7,4,0,0,457,459,3,96,48,0,458,456,1,0,0,0,459,462,1,0,0,0,460,458,
        1,0,0,0,460,461,1,0,0,0,461,95,1,0,0,0,462,460,1,0,0,0,463,468,3,
        98,49,0,464,465,7,5,0,0,465,467,3,98,49,0,466,464,1,0,0,0,467,470,
        1,0,0,0,468,466,1,0,0,0,468,469,1,0,0,0,469,97,1,0,0,0,470,468,1,
        0,0,0,471,472,5,41,0,0,472,483,3,90,45,0,473,483,3,90,45,0,474,483,
        3,50,25,0,475,483,5,52,0,0,476,483,5,51,0,0,477,483,5,48,0,0,478,
        479,5,37,0,0,479,480,3,94,47,0,480,481,5,38,0,0,481,483,1,0,0,0,
        482,471,1,0,0,0,482,473,1,0,0,0,482,474,1,0,0,0,482,475,1,0,0,0,
        482,476,1,0,0,0,482,477,1,0,0,0,482,478,1,0,0,0,483,99,1,0,0,0,484,
        492,5,25,0,0,485,486,5,25,0,0,486,488,5,37,0,0,487,489,3,102,51,
        0,488,487,1,0,0,0,488,489,1,0,0,0,489,490,1,0,0,0,490,492,5,38,0,
        0,491,484,1,0,0,0,491,485,1,0,0,0,492,101,1,0,0,0,493,498,3,104,
        52,0,494,495,5,31,0,0,495,497,3,104,52,0,496,494,1,0,0,0,497,500,
        1,0,0,0,498,496,1,0,0,0,498,499,1,0,0,0,499,103,1,0,0,0,500,498,
        1,0,0,0,501,504,5,48,0,0,502,504,3,94,47,0,503,501,1,0,0,0,503,502,
        1,0,0,0,504,105,1,0,0,0,48,112,123,129,136,151,161,167,174,183,187,
        196,210,226,232,240,254,261,266,271,279,291,296,302,305,313,320,
        326,338,344,355,359,363,374,390,397,411,427,434,437,447,453,460,
        468,482,488,491,498,503
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
                     "<INVALID>", "<INVALID>", "'..'", "'.'", "':='", "':'", 
                     "';'", "','", "'+'", "'-'", "'*'", "'/'", "'['", "'('", 
                     "')'", "']'", "'^'", "'@'", "'='", "'<='", "'<>'", 
                     "'<'", "'>='", "'>'" ]

    symbolicNames = [ "<INVALID>", "PROGRAM", "BEGIN_", "END", "CONST", 
                      "VAR", "TYPE", "RECORD", "ARRAY", "OF", "DOUBLE", 
                      "INTEGER", "IF", "THEN", "ELSE", "WHILE", "DO", "REPEAT", 
                      "UNTIL", "FOR", "TO", "DOWNTO", "PROCEDURE", "FUNCTION", 
                      "RESULT", "WRITELN", "DOTDOT", "DOT", "ASSIGN", "COLON", 
                      "SEMI", "COMMA", "PLUS", "MINUS", "STAR", "SLASH", 
                      "LBRACK", "LPAREN", "RPAREN", "RBRACK", "CARET", "AT", 
                      "EQ_OP", "LE_OP", "NE_OP", "LT_OP", "GE_OP", "GT_OP", 
                      "STRING", "IDENT", "HEXNUMBER", "FLOATNUMBER", "NUMBER", 
                      "WS", "COMMENT1", "COMMENT2", "COMMENT3" ]

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
    RULE_identList = 31
    RULE_block = 32
    RULE_localDeclaration = 33
    RULE_statementList = 34
    RULE_statement = 35
    RULE_forStatement = 36
    RULE_repeatStatement = 37
    RULE_argumentList = 38
    RULE_whileStatement = 39
    RULE_ifStatement = 40
    RULE_condition = 41
    RULE_compareOp = 42
    RULE_compoundStatement = 43
    RULE_assignment = 44
    RULE_variableRef = 45
    RULE_variableSuffix = 46
    RULE_expr = 47
    RULE_term = 48
    RULE_factor = 49
    RULE_writeLnStatement = 50
    RULE_writeArgList = 51
    RULE_writeArg = 52

    ruleNames =  [ "programFile", "declarationPart", "constSection", "constDeclaration", 
                   "constItem", "constValue", "typeSection", "typeDeclaration", 
                   "arrayDeclaration", "arrayInitializer", "arrayValueList", 
                   "arrayType", "arrayRange", "typeName", "simpleType", 
                   "enumDeclaration", "enumValueList", "enumValue", "recordDeclaration", 
                   "recordFieldDeclaration", "functionDeclaration", "procedureDeclaration", 
                   "formalParamList", "formalParam", "declaration", "functionCallExpr", 
                   "procedureCallStatement", "actualParamList", "actualParam", 
                   "varSection", "varDeclaration", "identList", "block", 
                   "localDeclaration", "statementList", "statement", "forStatement", 
                   "repeatStatement", "argumentList", "whileStatement", 
                   "ifStatement", "condition", "compareOp", "compoundStatement", 
                   "assignment", "variableRef", "variableSuffix", "expr", 
                   "term", "factor", "writeLnStatement", "writeArgList", 
                   "writeArg" ]

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
    DOUBLE=10
    INTEGER=11
    IF=12
    THEN=13
    ELSE=14
    WHILE=15
    DO=16
    REPEAT=17
    UNTIL=18
    FOR=19
    TO=20
    DOWNTO=21
    PROCEDURE=22
    FUNCTION=23
    RESULT=24
    WRITELN=25
    DOTDOT=26
    DOT=27
    ASSIGN=28
    COLON=29
    SEMI=30
    COMMA=31
    PLUS=32
    MINUS=33
    STAR=34
    SLASH=35
    LBRACK=36
    LPAREN=37
    RPAREN=38
    RBRACK=39
    CARET=40
    AT=41
    EQ_OP=42
    LE_OP=43
    NE_OP=44
    LT_OP=45
    GE_OP=46
    GT_OP=47
    STRING=48
    IDENT=49
    HEXNUMBER=50
    FLOATNUMBER=51
    NUMBER=52
    WS=53
    COMMENT1=54
    COMMENT2=55
    COMMENT3=56

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
            self.state = 106
            self.match(MiniPascalParser.PROGRAM)
            self.state = 107
            self.match(MiniPascalParser.IDENT)
            self.state = 108
            self.match(MiniPascalParser.SEMI)
            self.state = 112
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 109
                    self.declarationPart() 
                self.state = 114
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 115
            self.block()
            self.state = 116
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
            self.state = 123
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 118
                self.constSection()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 119
                self.typeSection()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 120
                self.varSection()
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 4)
                self.state = 121
                self.procedureDeclaration()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 5)
                self.state = 122
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
            self.state = 125
            self.match(MiniPascalParser.CONST)
            self.state = 127 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 126
                self.constDeclaration()
                self.state = 129 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==49):
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
            self.state = 131
            self.constItem()
            self.state = 136
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 132
                self.match(MiniPascalParser.COMMA)
                self.state = 133
                self.constItem()
                self.state = 138
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 139
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
            self.state = 141
            self.match(MiniPascalParser.IDENT)
            self.state = 142
            self.match(MiniPascalParser.EQ_OP)
            self.state = 143
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
            self.state = 145
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 7036874417766400) != 0)):
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
            self.state = 147
            self.match(MiniPascalParser.TYPE)
            self.state = 149 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 148
                self.typeDeclaration()
                self.state = 151 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==49):
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
            self.state = 161
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 153
                self.match(MiniPascalParser.IDENT)
                self.state = 154
                self.match(MiniPascalParser.EQ_OP)
                self.state = 155
                self.typeName()
                self.state = 156
                self.match(MiniPascalParser.SEMI)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 158
                self.enumDeclaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 159
                self.recordDeclaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 160
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
            self.state = 163
            self.match(MiniPascalParser.IDENT)
            self.state = 164
            self.match(MiniPascalParser.EQ_OP)
            self.state = 165
            self.arrayType()
            self.state = 167
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==42:
                self.state = 166
                self.arrayInitializer()


            self.state = 169
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
            self.state = 171
            self.match(MiniPascalParser.EQ_OP)
            self.state = 172
            self.match(MiniPascalParser.LPAREN)
            self.state = 174
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 7036874417766400) != 0):
                self.state = 173
                self.arrayValueList()


            self.state = 176
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
            self.state = 178
            self.constValue()
            self.state = 183
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 179
                    self.match(MiniPascalParser.COMMA)
                    self.state = 180
                    self.constValue() 
                self.state = 185
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

            self.state = 187
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==31:
                self.state = 186
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
            self.enterOuterAlt(localctx, 1)
            self.state = 189
            self.match(MiniPascalParser.ARRAY)
            self.state = 190
            self.match(MiniPascalParser.LBRACK)
            self.state = 191
            self.arrayRange()
            self.state = 196
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 192
                self.match(MiniPascalParser.COMMA)
                self.state = 193
                self.arrayRange()
                self.state = 198
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 199
            self.match(MiniPascalParser.RBRACK)
            self.state = 200
            self.match(MiniPascalParser.OF)
            self.state = 201
            self.typeName()
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
            self.state = 203
            self.expr()
            self.state = 204
            self.match(MiniPascalParser.DOTDOT)
            self.state = 205
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
            self.state = 210
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [10, 11, 48, 49]:
                self.enterOuterAlt(localctx, 1)
                self.state = 207
                self.simpleType()
                pass
            elif token in [40]:
                self.enterOuterAlt(localctx, 2)
                self.state = 208
                self.match(MiniPascalParser.CARET)
                self.state = 209
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
            self.state = 212
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 844424930135040) != 0)):
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
            self.state = 214
            self.match(MiniPascalParser.IDENT)
            self.state = 215
            self.match(MiniPascalParser.EQ_OP)
            self.state = 216
            self.match(MiniPascalParser.LPAREN)
            self.state = 217
            self.enumValueList()
            self.state = 218
            self.match(MiniPascalParser.RPAREN)
            self.state = 219
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
            self.state = 221
            self.enumValue()
            self.state = 226
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 222
                self.match(MiniPascalParser.COMMA)
                self.state = 223
                self.enumValue()
                self.state = 228
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
            self.state = 229
            self.match(MiniPascalParser.IDENT)
            self.state = 232
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==42:
                self.state = 230
                self.match(MiniPascalParser.EQ_OP)
                self.state = 231
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
            self.state = 234
            self.match(MiniPascalParser.IDENT)
            self.state = 235
            self.match(MiniPascalParser.EQ_OP)
            self.state = 236
            self.match(MiniPascalParser.RECORD)
            self.state = 240
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==49:
                self.state = 237
                self.recordFieldDeclaration()
                self.state = 242
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 243
            self.match(MiniPascalParser.END)
            self.state = 244
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
            self.state = 246
            self.identList()
            self.state = 247
            self.match(MiniPascalParser.COLON)
            self.state = 248
            self.typeName()
            self.state = 249
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
            self.state = 251
            self.match(MiniPascalParser.FUNCTION)
            self.state = 252
            self.match(MiniPascalParser.IDENT)
            self.state = 254
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==37:
                self.state = 253
                self.formalParamList()


            self.state = 256
            self.match(MiniPascalParser.COLON)
            self.state = 257
            self.typeName()
            self.state = 258
            self.match(MiniPascalParser.SEMI)
            self.state = 259
            self.block()
            self.state = 261
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==30:
                self.state = 260
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
            self.state = 263
            self.match(MiniPascalParser.PROCEDURE)
            self.state = 264
            self.match(MiniPascalParser.IDENT)
            self.state = 266
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==37:
                self.state = 265
                self.formalParamList()


            self.state = 268
            self.match(MiniPascalParser.SEMI)
            self.state = 269
            self.block()
            self.state = 271
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==30:
                self.state = 270
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
            self.state = 273
            self.match(MiniPascalParser.LPAREN)
            self.state = 274
            self.formalParam()
            self.state = 279
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==30:
                self.state = 275
                self.match(MiniPascalParser.SEMI)
                self.state = 276
                self.formalParam()
                self.state = 281
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 282
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
        self.enterRule(localctx, 46, self.RULE_formalParam)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 284
            self.identList()
            self.state = 285
            self.match(MiniPascalParser.COLON)
            self.state = 286
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
            self.state = 291
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 288
                self.varSection()
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 2)
                self.state = 289
                self.procedureDeclaration()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 3)
                self.state = 290
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
            self.state = 293
            self.match(MiniPascalParser.IDENT)
            self.state = 294
            self.match(MiniPascalParser.LPAREN)
            self.state = 296
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 7602160850173952) != 0):
                self.state = 295
                self.argumentList()


            self.state = 298
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
            self.state = 300
            self.match(MiniPascalParser.IDENT)
            self.state = 302
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==37:
                self.state = 301
                self.actualParamList()


            self.state = 305
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
            if la_ == 1:
                self.state = 304
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
            self.state = 307
            self.match(MiniPascalParser.LPAREN)
            self.state = 308
            self.actualParam()
            self.state = 313
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 309
                self.match(MiniPascalParser.COMMA)
                self.state = 310
                self.actualParam()
                self.state = 315
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 316
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
            self.state = 320
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,25,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 318
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 319
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
            self.state = 322
            self.match(MiniPascalParser.VAR)
            self.state = 324 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 323
                self.varDeclaration()
                self.state = 326 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==49):
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
        self.enterRule(localctx, 60, self.RULE_varDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 328
            self.identList()
            self.state = 329
            self.match(MiniPascalParser.COLON)
            self.state = 330
            self.typeName()
            self.state = 331
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
        self.enterRule(localctx, 62, self.RULE_identList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 333
            self.match(MiniPascalParser.IDENT)
            self.state = 338
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 334
                self.match(MiniPascalParser.COMMA)
                self.state = 335
                self.match(MiniPascalParser.IDENT)
                self.state = 340
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
        self.enterRule(localctx, 64, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 344
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 12582960) != 0):
                self.state = 341
                self.localDeclaration()
                self.state = 346
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 347
            self.match(MiniPascalParser.BEGIN_)
            self.state = 348
            self.statementList()
            self.state = 349
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
        self.enterRule(localctx, 66, self.RULE_localDeclaration)
        try:
            self.state = 355
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [22]:
                self.enterOuterAlt(localctx, 1)
                self.state = 351
                self.procedureDeclaration()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 2)
                self.state = 352
                self.functionDeclaration()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 353
                self.varSection()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 354
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
        self.enterRule(localctx, 68, self.RULE_statementList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 363
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 562950004445188) != 0):
                self.state = 357
                self.statement()
                self.state = 359
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==30:
                    self.state = 358
                    self.match(MiniPascalParser.SEMI)


                self.state = 365
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
        self.enterRule(localctx, 70, self.RULE_statement)
        try:
            self.state = 374
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,32,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 366
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 367
                self.writeLnStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 368
                self.ifStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 369
                self.whileStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 370
                self.repeatStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 371
                self.forStatement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 372
                self.procedureCallStatement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 373
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
        self.enterRule(localctx, 72, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 376
            self.match(MiniPascalParser.FOR)
            self.state = 377
            self.match(MiniPascalParser.IDENT)
            self.state = 378
            self.match(MiniPascalParser.ASSIGN)
            self.state = 379
            self.expr()
            self.state = 380
            _la = self._input.LA(1)
            if not(_la==20 or _la==21):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 381
            self.expr()
            self.state = 382
            self.match(MiniPascalParser.DO)
            self.state = 383
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
        self.enterRule(localctx, 74, self.RULE_repeatStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 385
            self.match(MiniPascalParser.REPEAT)
            self.state = 386
            self.statementList()
            self.state = 387
            self.match(MiniPascalParser.UNTIL)
            self.state = 388
            self.condition()
            self.state = 390
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,33,self._ctx)
            if la_ == 1:
                self.state = 389
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
        self.enterRule(localctx, 76, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 392
            self.expr()
            self.state = 397
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 393
                self.match(MiniPascalParser.COMMA)
                self.state = 394
                self.expr()
                self.state = 399
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
        self.enterRule(localctx, 78, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 400
            self.match(MiniPascalParser.WHILE)
            self.state = 401
            self.condition()
            self.state = 402
            self.match(MiniPascalParser.DO)
            self.state = 403
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
        self.enterRule(localctx, 80, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 405
            self.match(MiniPascalParser.IF)
            self.state = 406
            self.condition()
            self.state = 407
            self.match(MiniPascalParser.THEN)
            self.state = 408
            self.statement()
            self.state = 411
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,35,self._ctx)
            if la_ == 1:
                self.state = 409
                self.match(MiniPascalParser.ELSE)
                self.state = 410
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
        self.enterRule(localctx, 82, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 413
            self.expr()
            self.state = 414
            self.compareOp()
            self.state = 415
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
        self.enterRule(localctx, 84, self.RULE_compareOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 417
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 277076930199552) != 0)):
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
        self.enterRule(localctx, 86, self.RULE_compoundStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 419
            self.match(MiniPascalParser.BEGIN_)
            self.state = 420
            self.statementList()
            self.state = 421
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
        self.enterRule(localctx, 88, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 423
            self.variableRef()
            self.state = 424
            self.match(MiniPascalParser.ASSIGN)
            self.state = 425
            self.expr()
            self.state = 427
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,36,self._ctx)
            if la_ == 1:
                self.state = 426
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
        self.enterRule(localctx, 90, self.RULE_variableRef)
        self._la = 0 # Token type
        try:
            self.state = 437
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [24]:
                self.enterOuterAlt(localctx, 1)
                self.state = 429
                self.match(MiniPascalParser.RESULT)
                pass
            elif token in [49]:
                self.enterOuterAlt(localctx, 2)
                self.state = 430
                self.match(MiniPascalParser.IDENT)
                self.state = 434
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1168365322240) != 0):
                    self.state = 431
                    self.variableSuffix()
                    self.state = 436
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
        self.enterRule(localctx, 92, self.RULE_variableSuffix)
        self._la = 0 # Token type
        try:
            self.state = 453
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27]:
                self.enterOuterAlt(localctx, 1)
                self.state = 439
                self.match(MiniPascalParser.DOT)
                self.state = 440
                self.match(MiniPascalParser.IDENT)
                pass
            elif token in [36]:
                self.enterOuterAlt(localctx, 2)
                self.state = 441
                self.match(MiniPascalParser.LBRACK)
                self.state = 442
                self.expr()
                self.state = 447
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==31:
                    self.state = 443
                    self.match(MiniPascalParser.COMMA)
                    self.state = 444
                    self.expr()
                    self.state = 449
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 450
                self.match(MiniPascalParser.RBRACK)
                pass
            elif token in [40]:
                self.enterOuterAlt(localctx, 3)
                self.state = 452
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
        self.enterRule(localctx, 94, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 455
            self.term()
            self.state = 460
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32 or _la==33:
                self.state = 456
                _la = self._input.LA(1)
                if not(_la==32 or _la==33):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 457
                self.term()
                self.state = 462
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
        self.enterRule(localctx, 96, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 463
            self.factor()
            self.state = 468
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34 or _la==35:
                self.state = 464
                _la = self._input.LA(1)
                if not(_la==34 or _la==35):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 465
                self.factor()
                self.state = 470
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

        def AT(self):
            return self.getToken(MiniPascalParser.AT, 0)

        def variableRef(self):
            return self.getTypedRuleContext(MiniPascalParser.VariableRefContext,0)


        def functionCallExpr(self):
            return self.getTypedRuleContext(MiniPascalParser.FunctionCallExprContext,0)


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
        self.enterRule(localctx, 98, self.RULE_factor)
        try:
            self.state = 482
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,43,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 471
                self.match(MiniPascalParser.AT)
                self.state = 472
                self.variableRef()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 473
                self.variableRef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 474
                self.functionCallExpr()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 475
                self.match(MiniPascalParser.NUMBER)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 476
                self.match(MiniPascalParser.FLOATNUMBER)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 477
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 478
                self.match(MiniPascalParser.LPAREN)
                self.state = 479
                self.expr()
                self.state = 480
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
        self.enterRule(localctx, 100, self.RULE_writeLnStatement)
        self._la = 0 # Token type
        try:
            self.state = 491
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,45,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 484
                self.match(MiniPascalParser.WRITELN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 485
                self.match(MiniPascalParser.WRITELN)
                self.state = 486
                self.match(MiniPascalParser.LPAREN)
                self.state = 488
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 7602160850173952) != 0):
                    self.state = 487
                    self.writeArgList()


                self.state = 490
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
        self.enterRule(localctx, 102, self.RULE_writeArgList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 493
            self.writeArg()
            self.state = 498
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 494
                self.match(MiniPascalParser.COMMA)
                self.state = 495
                self.writeArg()
                self.state = 500
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
        self.enterRule(localctx, 104, self.RULE_writeArg)
        try:
            self.state = 503
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,47,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 501
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 502
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





