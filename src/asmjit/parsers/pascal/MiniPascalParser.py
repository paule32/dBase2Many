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
        4,1,54,474,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,2,46,
        7,46,2,47,7,47,2,48,7,48,2,49,7,49,1,0,1,0,1,0,1,0,5,0,105,8,0,10,
        0,12,0,108,9,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,3,1,118,8,1,1,2,1,
        2,4,2,122,8,2,11,2,12,2,123,1,3,1,3,1,3,5,3,129,8,3,10,3,12,3,132,
        9,3,1,3,1,3,1,4,1,4,1,4,1,4,1,5,1,5,1,6,1,6,4,6,144,8,6,11,6,12,
        6,145,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,3,7,156,8,7,1,8,1,8,1,8,1,
        8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,3,8,169,8,8,1,8,1,8,1,9,1,9,1,9,3,
        9,176,8,9,1,9,1,9,1,10,1,10,1,10,5,10,183,8,10,10,10,12,10,186,9,
        10,1,10,3,10,189,8,10,1,11,1,11,1,12,1,12,1,12,1,12,1,12,1,12,1,
        12,1,13,1,13,1,13,5,13,203,8,13,10,13,12,13,206,9,13,1,14,1,14,1,
        14,3,14,211,8,14,1,15,1,15,1,15,1,15,5,15,217,8,15,10,15,12,15,220,
        9,15,1,15,1,15,1,15,1,16,1,16,1,16,1,16,1,16,1,17,1,17,1,17,3,17,
        233,8,17,1,17,1,17,1,17,1,17,1,17,3,17,240,8,17,1,18,1,18,1,18,3,
        18,245,8,18,1,18,1,18,1,18,3,18,250,8,18,1,19,1,19,1,19,1,19,5,19,
        256,8,19,10,19,12,19,259,9,19,1,19,1,19,1,20,1,20,1,20,1,20,1,21,
        1,21,1,21,3,21,270,8,21,1,22,1,22,1,22,3,22,275,8,22,1,22,1,22,1,
        23,1,23,3,23,281,8,23,1,23,3,23,284,8,23,1,24,1,24,1,24,1,24,5,24,
        290,8,24,10,24,12,24,293,9,24,1,24,1,24,1,25,1,25,3,25,299,8,25,
        1,26,1,26,4,26,303,8,26,11,26,12,26,304,1,27,1,27,1,27,1,27,1,27,
        1,28,1,28,1,28,5,28,315,8,28,10,28,12,28,318,9,28,1,29,5,29,321,
        8,29,10,29,12,29,324,9,29,1,29,1,29,1,29,1,29,1,30,1,30,1,30,1,30,
        3,30,334,8,30,1,31,1,31,3,31,338,8,31,5,31,340,8,31,10,31,12,31,
        343,9,31,1,32,1,32,1,32,1,32,1,32,1,32,1,32,1,32,3,32,353,8,32,1,
        33,1,33,1,33,1,33,1,33,1,33,1,33,1,33,1,33,1,34,1,34,1,34,1,34,1,
        34,3,34,369,8,34,1,35,1,35,1,35,5,35,374,8,35,10,35,12,35,377,9,
        35,1,36,1,36,1,36,1,36,1,36,1,37,1,37,1,37,1,37,1,37,1,37,3,37,390,
        8,37,1,38,1,38,1,38,1,38,1,39,1,39,1,40,1,40,1,40,1,40,1,41,1,41,
        1,41,1,41,3,41,406,8,41,1,42,1,42,1,42,5,42,411,8,42,10,42,12,42,
        414,9,42,3,42,416,8,42,1,43,1,43,1,43,1,43,1,43,1,43,3,43,424,8,
        43,1,44,1,44,1,44,5,44,429,8,44,10,44,12,44,432,9,44,1,45,1,45,1,
        45,5,45,437,8,45,10,45,12,45,440,9,45,1,46,1,46,1,46,1,46,1,46,1,
        46,1,46,1,46,1,46,3,46,451,8,46,1,47,1,47,1,47,1,47,3,47,457,8,47,
        1,47,3,47,460,8,47,1,48,1,48,1,48,5,48,465,8,48,10,48,12,48,468,
        9,48,1,49,1,49,3,49,472,8,49,1,49,0,0,50,0,2,4,6,8,10,12,14,16,18,
        20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,
        64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,0,6,2,0,46,
        46,49,50,2,0,10,11,47,47,1,0,20,21,1,0,40,45,1,0,32,33,1,0,34,35,
        486,0,100,1,0,0,0,2,117,1,0,0,0,4,119,1,0,0,0,6,125,1,0,0,0,8,135,
        1,0,0,0,10,139,1,0,0,0,12,141,1,0,0,0,14,155,1,0,0,0,16,157,1,0,
        0,0,18,172,1,0,0,0,20,179,1,0,0,0,22,190,1,0,0,0,24,192,1,0,0,0,
        26,199,1,0,0,0,28,207,1,0,0,0,30,212,1,0,0,0,32,224,1,0,0,0,34,229,
        1,0,0,0,36,241,1,0,0,0,38,251,1,0,0,0,40,262,1,0,0,0,42,269,1,0,
        0,0,44,271,1,0,0,0,46,278,1,0,0,0,48,285,1,0,0,0,50,298,1,0,0,0,
        52,300,1,0,0,0,54,306,1,0,0,0,56,311,1,0,0,0,58,322,1,0,0,0,60,333,
        1,0,0,0,62,341,1,0,0,0,64,352,1,0,0,0,66,354,1,0,0,0,68,363,1,0,
        0,0,70,370,1,0,0,0,72,378,1,0,0,0,74,383,1,0,0,0,76,391,1,0,0,0,
        78,395,1,0,0,0,80,397,1,0,0,0,82,401,1,0,0,0,84,415,1,0,0,0,86,423,
        1,0,0,0,88,425,1,0,0,0,90,433,1,0,0,0,92,450,1,0,0,0,94,459,1,0,
        0,0,96,461,1,0,0,0,98,471,1,0,0,0,100,101,5,1,0,0,101,102,5,47,0,
        0,102,106,5,30,0,0,103,105,3,2,1,0,104,103,1,0,0,0,105,108,1,0,0,
        0,106,104,1,0,0,0,106,107,1,0,0,0,107,109,1,0,0,0,108,106,1,0,0,
        0,109,110,3,58,29,0,110,111,5,27,0,0,111,1,1,0,0,0,112,118,3,4,2,
        0,113,118,3,12,6,0,114,118,3,52,26,0,115,118,3,36,18,0,116,118,3,
        34,17,0,117,112,1,0,0,0,117,113,1,0,0,0,117,114,1,0,0,0,117,115,
        1,0,0,0,117,116,1,0,0,0,118,3,1,0,0,0,119,121,5,4,0,0,120,122,3,
        6,3,0,121,120,1,0,0,0,122,123,1,0,0,0,123,121,1,0,0,0,123,124,1,
        0,0,0,124,5,1,0,0,0,125,130,3,8,4,0,126,127,5,31,0,0,127,129,3,8,
        4,0,128,126,1,0,0,0,129,132,1,0,0,0,130,128,1,0,0,0,130,131,1,0,
        0,0,131,133,1,0,0,0,132,130,1,0,0,0,133,134,5,30,0,0,134,7,1,0,0,
        0,135,136,5,47,0,0,136,137,5,40,0,0,137,138,3,10,5,0,138,9,1,0,0,
        0,139,140,7,0,0,0,140,11,1,0,0,0,141,143,5,6,0,0,142,144,3,14,7,
        0,143,142,1,0,0,0,144,145,1,0,0,0,145,143,1,0,0,0,145,146,1,0,0,
        0,146,13,1,0,0,0,147,148,5,47,0,0,148,149,5,40,0,0,149,150,3,22,
        11,0,150,151,5,30,0,0,151,156,1,0,0,0,152,156,3,24,12,0,153,156,
        3,30,15,0,154,156,3,16,8,0,155,147,1,0,0,0,155,152,1,0,0,0,155,153,
        1,0,0,0,155,154,1,0,0,0,156,15,1,0,0,0,157,158,5,47,0,0,158,159,
        5,40,0,0,159,160,5,8,0,0,160,161,5,36,0,0,161,162,5,50,0,0,162,163,
        5,26,0,0,163,164,5,50,0,0,164,165,5,39,0,0,165,166,5,9,0,0,166,168,
        3,22,11,0,167,169,3,18,9,0,168,167,1,0,0,0,168,169,1,0,0,0,169,170,
        1,0,0,0,170,171,5,30,0,0,171,17,1,0,0,0,172,173,5,40,0,0,173,175,
        5,37,0,0,174,176,3,20,10,0,175,174,1,0,0,0,175,176,1,0,0,0,176,177,
        1,0,0,0,177,178,5,38,0,0,178,19,1,0,0,0,179,184,3,10,5,0,180,181,
        5,31,0,0,181,183,3,10,5,0,182,180,1,0,0,0,183,186,1,0,0,0,184,182,
        1,0,0,0,184,185,1,0,0,0,185,188,1,0,0,0,186,184,1,0,0,0,187,189,
        5,31,0,0,188,187,1,0,0,0,188,189,1,0,0,0,189,21,1,0,0,0,190,191,
        7,1,0,0,191,23,1,0,0,0,192,193,5,47,0,0,193,194,5,40,0,0,194,195,
        5,37,0,0,195,196,3,26,13,0,196,197,5,38,0,0,197,198,5,30,0,0,198,
        25,1,0,0,0,199,204,3,28,14,0,200,201,5,31,0,0,201,203,3,28,14,0,
        202,200,1,0,0,0,203,206,1,0,0,0,204,202,1,0,0,0,204,205,1,0,0,0,
        205,27,1,0,0,0,206,204,1,0,0,0,207,210,5,47,0,0,208,209,5,40,0,0,
        209,211,5,50,0,0,210,208,1,0,0,0,210,211,1,0,0,0,211,29,1,0,0,0,
        212,213,5,47,0,0,213,214,5,40,0,0,214,218,5,7,0,0,215,217,3,32,16,
        0,216,215,1,0,0,0,217,220,1,0,0,0,218,216,1,0,0,0,218,219,1,0,0,
        0,219,221,1,0,0,0,220,218,1,0,0,0,221,222,5,3,0,0,222,223,5,30,0,
        0,223,31,1,0,0,0,224,225,3,56,28,0,225,226,5,29,0,0,226,227,3,22,
        11,0,227,228,5,30,0,0,228,33,1,0,0,0,229,230,5,23,0,0,230,232,5,
        47,0,0,231,233,3,38,19,0,232,231,1,0,0,0,232,233,1,0,0,0,233,234,
        1,0,0,0,234,235,5,29,0,0,235,236,3,22,11,0,236,237,5,30,0,0,237,
        239,3,58,29,0,238,240,5,30,0,0,239,238,1,0,0,0,239,240,1,0,0,0,240,
        35,1,0,0,0,241,242,5,22,0,0,242,244,5,47,0,0,243,245,3,38,19,0,244,
        243,1,0,0,0,244,245,1,0,0,0,245,246,1,0,0,0,246,247,5,30,0,0,247,
        249,3,58,29,0,248,250,5,30,0,0,249,248,1,0,0,0,249,250,1,0,0,0,250,
        37,1,0,0,0,251,252,5,37,0,0,252,257,3,40,20,0,253,254,5,30,0,0,254,
        256,3,40,20,0,255,253,1,0,0,0,256,259,1,0,0,0,257,255,1,0,0,0,257,
        258,1,0,0,0,258,260,1,0,0,0,259,257,1,0,0,0,260,261,5,38,0,0,261,
        39,1,0,0,0,262,263,3,56,28,0,263,264,5,29,0,0,264,265,3,22,11,0,
        265,41,1,0,0,0,266,270,3,52,26,0,267,270,3,36,18,0,268,270,3,34,
        17,0,269,266,1,0,0,0,269,267,1,0,0,0,269,268,1,0,0,0,270,43,1,0,
        0,0,271,272,5,47,0,0,272,274,5,37,0,0,273,275,3,70,35,0,274,273,
        1,0,0,0,274,275,1,0,0,0,275,276,1,0,0,0,276,277,5,38,0,0,277,45,
        1,0,0,0,278,280,5,47,0,0,279,281,3,48,24,0,280,279,1,0,0,0,280,281,
        1,0,0,0,281,283,1,0,0,0,282,284,5,30,0,0,283,282,1,0,0,0,283,284,
        1,0,0,0,284,47,1,0,0,0,285,286,5,37,0,0,286,291,3,50,25,0,287,288,
        5,31,0,0,288,290,3,50,25,0,289,287,1,0,0,0,290,293,1,0,0,0,291,289,
        1,0,0,0,291,292,1,0,0,0,292,294,1,0,0,0,293,291,1,0,0,0,294,295,
        5,38,0,0,295,49,1,0,0,0,296,299,5,46,0,0,297,299,3,88,44,0,298,296,
        1,0,0,0,298,297,1,0,0,0,299,51,1,0,0,0,300,302,5,5,0,0,301,303,3,
        54,27,0,302,301,1,0,0,0,303,304,1,0,0,0,304,302,1,0,0,0,304,305,
        1,0,0,0,305,53,1,0,0,0,306,307,3,56,28,0,307,308,5,29,0,0,308,309,
        3,22,11,0,309,310,5,30,0,0,310,55,1,0,0,0,311,316,5,47,0,0,312,313,
        5,31,0,0,313,315,5,47,0,0,314,312,1,0,0,0,315,318,1,0,0,0,316,314,
        1,0,0,0,316,317,1,0,0,0,317,57,1,0,0,0,318,316,1,0,0,0,319,321,3,
        60,30,0,320,319,1,0,0,0,321,324,1,0,0,0,322,320,1,0,0,0,322,323,
        1,0,0,0,323,325,1,0,0,0,324,322,1,0,0,0,325,326,5,2,0,0,326,327,
        3,62,31,0,327,328,5,3,0,0,328,59,1,0,0,0,329,334,3,36,18,0,330,334,
        3,34,17,0,331,334,3,52,26,0,332,334,3,4,2,0,333,329,1,0,0,0,333,
        330,1,0,0,0,333,331,1,0,0,0,333,332,1,0,0,0,334,61,1,0,0,0,335,337,
        3,64,32,0,336,338,5,30,0,0,337,336,1,0,0,0,337,338,1,0,0,0,338,340,
        1,0,0,0,339,335,1,0,0,0,340,343,1,0,0,0,341,339,1,0,0,0,341,342,
        1,0,0,0,342,63,1,0,0,0,343,341,1,0,0,0,344,353,3,82,41,0,345,353,
        3,94,47,0,346,353,3,74,37,0,347,353,3,72,36,0,348,353,3,68,34,0,
        349,353,3,66,33,0,350,353,3,46,23,0,351,353,3,80,40,0,352,344,1,
        0,0,0,352,345,1,0,0,0,352,346,1,0,0,0,352,347,1,0,0,0,352,348,1,
        0,0,0,352,349,1,0,0,0,352,350,1,0,0,0,352,351,1,0,0,0,353,65,1,0,
        0,0,354,355,5,19,0,0,355,356,5,47,0,0,356,357,5,28,0,0,357,358,3,
        88,44,0,358,359,7,2,0,0,359,360,3,88,44,0,360,361,5,16,0,0,361,362,
        3,64,32,0,362,67,1,0,0,0,363,364,5,17,0,0,364,365,3,62,31,0,365,
        366,5,18,0,0,366,368,3,76,38,0,367,369,5,30,0,0,368,367,1,0,0,0,
        368,369,1,0,0,0,369,69,1,0,0,0,370,375,3,88,44,0,371,372,5,31,0,
        0,372,374,3,88,44,0,373,371,1,0,0,0,374,377,1,0,0,0,375,373,1,0,
        0,0,375,376,1,0,0,0,376,71,1,0,0,0,377,375,1,0,0,0,378,379,5,15,
        0,0,379,380,3,76,38,0,380,381,5,16,0,0,381,382,3,64,32,0,382,73,
        1,0,0,0,383,384,5,12,0,0,384,385,3,76,38,0,385,386,5,13,0,0,386,
        389,3,64,32,0,387,388,5,14,0,0,388,390,3,64,32,0,389,387,1,0,0,0,
        389,390,1,0,0,0,390,75,1,0,0,0,391,392,3,88,44,0,392,393,3,78,39,
        0,393,394,3,88,44,0,394,77,1,0,0,0,395,396,7,3,0,0,396,79,1,0,0,
        0,397,398,5,2,0,0,398,399,3,62,31,0,399,400,5,3,0,0,400,81,1,0,0,
        0,401,402,3,84,42,0,402,403,5,28,0,0,403,405,3,88,44,0,404,406,5,
        30,0,0,405,404,1,0,0,0,405,406,1,0,0,0,406,83,1,0,0,0,407,416,5,
        24,0,0,408,412,5,47,0,0,409,411,3,86,43,0,410,409,1,0,0,0,411,414,
        1,0,0,0,412,410,1,0,0,0,412,413,1,0,0,0,413,416,1,0,0,0,414,412,
        1,0,0,0,415,407,1,0,0,0,415,408,1,0,0,0,416,85,1,0,0,0,417,418,5,
        27,0,0,418,424,5,47,0,0,419,420,5,36,0,0,420,421,3,88,44,0,421,422,
        5,39,0,0,422,424,1,0,0,0,423,417,1,0,0,0,423,419,1,0,0,0,424,87,
        1,0,0,0,425,430,3,90,45,0,426,427,7,4,0,0,427,429,3,90,45,0,428,
        426,1,0,0,0,429,432,1,0,0,0,430,428,1,0,0,0,430,431,1,0,0,0,431,
        89,1,0,0,0,432,430,1,0,0,0,433,438,3,92,46,0,434,435,7,5,0,0,435,
        437,3,92,46,0,436,434,1,0,0,0,437,440,1,0,0,0,438,436,1,0,0,0,438,
        439,1,0,0,0,439,91,1,0,0,0,440,438,1,0,0,0,441,451,3,84,42,0,442,
        451,3,44,22,0,443,451,5,50,0,0,444,451,5,49,0,0,445,451,5,46,0,0,
        446,447,5,37,0,0,447,448,3,88,44,0,448,449,5,38,0,0,449,451,1,0,
        0,0,450,441,1,0,0,0,450,442,1,0,0,0,450,443,1,0,0,0,450,444,1,0,
        0,0,450,445,1,0,0,0,450,446,1,0,0,0,451,93,1,0,0,0,452,460,5,25,
        0,0,453,454,5,25,0,0,454,456,5,37,0,0,455,457,3,96,48,0,456,455,
        1,0,0,0,456,457,1,0,0,0,457,458,1,0,0,0,458,460,5,38,0,0,459,452,
        1,0,0,0,459,453,1,0,0,0,460,95,1,0,0,0,461,466,3,98,49,0,462,463,
        5,31,0,0,463,465,3,98,49,0,464,462,1,0,0,0,465,468,1,0,0,0,466,464,
        1,0,0,0,466,467,1,0,0,0,467,97,1,0,0,0,468,466,1,0,0,0,469,472,5,
        46,0,0,470,472,3,88,44,0,471,469,1,0,0,0,471,470,1,0,0,0,472,99,
        1,0,0,0,45,106,117,123,130,145,155,168,175,184,188,204,210,218,232,
        239,244,249,257,269,274,280,283,291,298,304,316,322,333,337,341,
        352,368,375,389,405,412,415,423,430,438,450,456,459,466,471
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
                     "')'", "']'", "'='", "'<='", "'<>'", "'<'", "'>='", 
                     "'>'" ]

    symbolicNames = [ "<INVALID>", "PROGRAM", "BEGIN_", "END", "CONST", 
                      "VAR", "TYPE", "RECORD", "ARRAY", "OF", "DOUBLE", 
                      "INTEGER", "IF", "THEN", "ELSE", "WHILE", "DO", "REPEAT", 
                      "UNTIL", "FOR", "TO", "DOWNTO", "PROCEDURE", "FUNCTION", 
                      "RESULT", "WRITELN", "DOTDOT", "DOT", "ASSIGN", "COLON", 
                      "SEMI", "COMMA", "PLUS", "MINUS", "STAR", "SLASH", 
                      "LBRACK", "LPAREN", "RPAREN", "RBRACK", "EQ_OP", "LE_OP", 
                      "NE_OP", "LT_OP", "GE_OP", "GT_OP", "STRING", "IDENT", 
                      "HEXNUMBER", "FLOATNUMBER", "NUMBER", "WS", "COMMENT1", 
                      "COMMENT2", "COMMENT3" ]

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
    RULE_typeName = 11
    RULE_enumDeclaration = 12
    RULE_enumValueList = 13
    RULE_enumValue = 14
    RULE_recordDeclaration = 15
    RULE_recordFieldDeclaration = 16
    RULE_functionDeclaration = 17
    RULE_procedureDeclaration = 18
    RULE_formalParamList = 19
    RULE_formalParam = 20
    RULE_declaration = 21
    RULE_functionCallExpr = 22
    RULE_procedureCallStatement = 23
    RULE_actualParamList = 24
    RULE_actualParam = 25
    RULE_varSection = 26
    RULE_varDeclaration = 27
    RULE_identList = 28
    RULE_block = 29
    RULE_localDeclaration = 30
    RULE_statementList = 31
    RULE_statement = 32
    RULE_forStatement = 33
    RULE_repeatStatement = 34
    RULE_argumentList = 35
    RULE_whileStatement = 36
    RULE_ifStatement = 37
    RULE_condition = 38
    RULE_compareOp = 39
    RULE_compoundStatement = 40
    RULE_assignment = 41
    RULE_variableRef = 42
    RULE_variableSuffix = 43
    RULE_expr = 44
    RULE_term = 45
    RULE_factor = 46
    RULE_writeLnStatement = 47
    RULE_writeArgList = 48
    RULE_writeArg = 49

    ruleNames =  [ "programFile", "declarationPart", "constSection", "constDeclaration", 
                   "constItem", "constValue", "typeSection", "typeDeclaration", 
                   "arrayDeclaration", "arrayInitializer", "arrayValueList", 
                   "typeName", "enumDeclaration", "enumValueList", "enumValue", 
                   "recordDeclaration", "recordFieldDeclaration", "functionDeclaration", 
                   "procedureDeclaration", "formalParamList", "formalParam", 
                   "declaration", "functionCallExpr", "procedureCallStatement", 
                   "actualParamList", "actualParam", "varSection", "varDeclaration", 
                   "identList", "block", "localDeclaration", "statementList", 
                   "statement", "forStatement", "repeatStatement", "argumentList", 
                   "whileStatement", "ifStatement", "condition", "compareOp", 
                   "compoundStatement", "assignment", "variableRef", "variableSuffix", 
                   "expr", "term", "factor", "writeLnStatement", "writeArgList", 
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
    EQ_OP=40
    LE_OP=41
    NE_OP=42
    LT_OP=43
    GE_OP=44
    GT_OP=45
    STRING=46
    IDENT=47
    HEXNUMBER=48
    FLOATNUMBER=49
    NUMBER=50
    WS=51
    COMMENT1=52
    COMMENT2=53
    COMMENT3=54

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
            self.state = 100
            self.match(MiniPascalParser.PROGRAM)
            self.state = 101
            self.match(MiniPascalParser.IDENT)
            self.state = 102
            self.match(MiniPascalParser.SEMI)
            self.state = 106
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 103
                    self.declarationPart() 
                self.state = 108
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 109
            self.block()
            self.state = 110
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
            self.state = 117
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 112
                self.constSection()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 113
                self.typeSection()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 114
                self.varSection()
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 4)
                self.state = 115
                self.procedureDeclaration()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 5)
                self.state = 116
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
            self.state = 119
            self.match(MiniPascalParser.CONST)
            self.state = 121 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 120
                self.constDeclaration()
                self.state = 123 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==47):
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
            self.state = 125
            self.constItem()
            self.state = 130
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 126
                self.match(MiniPascalParser.COMMA)
                self.state = 127
                self.constItem()
                self.state = 132
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 133
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
            self.state = 135
            self.match(MiniPascalParser.IDENT)
            self.state = 136
            self.match(MiniPascalParser.EQ_OP)
            self.state = 137
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
            self.state = 139
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1759218604441600) != 0)):
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
            self.state = 141
            self.match(MiniPascalParser.TYPE)
            self.state = 143 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 142
                self.typeDeclaration()
                self.state = 145 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==47):
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
            self.state = 155
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 147
                self.match(MiniPascalParser.IDENT)
                self.state = 148
                self.match(MiniPascalParser.EQ_OP)
                self.state = 149
                self.typeName()
                self.state = 150
                self.match(MiniPascalParser.SEMI)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 152
                self.enumDeclaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 153
                self.recordDeclaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 154
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

        def ARRAY(self):
            return self.getToken(MiniPascalParser.ARRAY, 0)

        def LBRACK(self):
            return self.getToken(MiniPascalParser.LBRACK, 0)

        def NUMBER(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.NUMBER)
            else:
                return self.getToken(MiniPascalParser.NUMBER, i)

        def DOTDOT(self):
            return self.getToken(MiniPascalParser.DOTDOT, 0)

        def RBRACK(self):
            return self.getToken(MiniPascalParser.RBRACK, 0)

        def OF(self):
            return self.getToken(MiniPascalParser.OF, 0)

        def typeName(self):
            return self.getTypedRuleContext(MiniPascalParser.TypeNameContext,0)


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
            self.state = 157
            self.match(MiniPascalParser.IDENT)
            self.state = 158
            self.match(MiniPascalParser.EQ_OP)
            self.state = 159
            self.match(MiniPascalParser.ARRAY)
            self.state = 160
            self.match(MiniPascalParser.LBRACK)
            self.state = 161
            self.match(MiniPascalParser.NUMBER)
            self.state = 162
            self.match(MiniPascalParser.DOTDOT)
            self.state = 163
            self.match(MiniPascalParser.NUMBER)
            self.state = 164
            self.match(MiniPascalParser.RBRACK)
            self.state = 165
            self.match(MiniPascalParser.OF)
            self.state = 166
            self.typeName()
            self.state = 168
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==40:
                self.state = 167
                self.arrayInitializer()


            self.state = 170
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
            self.state = 172
            self.match(MiniPascalParser.EQ_OP)
            self.state = 173
            self.match(MiniPascalParser.LPAREN)
            self.state = 175
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1759218604441600) != 0):
                self.state = 174
                self.arrayValueList()


            self.state = 177
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
            self.state = 179
            self.constValue()
            self.state = 184
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 180
                    self.match(MiniPascalParser.COMMA)
                    self.state = 181
                    self.constValue() 
                self.state = 186
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

            self.state = 188
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==31:
                self.state = 187
                self.match(MiniPascalParser.COMMA)


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
        self.enterRule(localctx, 22, self.RULE_typeName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 140737488358400) != 0)):
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
        self.enterRule(localctx, 24, self.RULE_enumDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
            self.match(MiniPascalParser.IDENT)
            self.state = 193
            self.match(MiniPascalParser.EQ_OP)
            self.state = 194
            self.match(MiniPascalParser.LPAREN)
            self.state = 195
            self.enumValueList()
            self.state = 196
            self.match(MiniPascalParser.RPAREN)
            self.state = 197
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
        self.enterRule(localctx, 26, self.RULE_enumValueList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 199
            self.enumValue()
            self.state = 204
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 200
                self.match(MiniPascalParser.COMMA)
                self.state = 201
                self.enumValue()
                self.state = 206
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
        self.enterRule(localctx, 28, self.RULE_enumValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 207
            self.match(MiniPascalParser.IDENT)
            self.state = 210
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==40:
                self.state = 208
                self.match(MiniPascalParser.EQ_OP)
                self.state = 209
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
        self.enterRule(localctx, 30, self.RULE_recordDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 212
            self.match(MiniPascalParser.IDENT)
            self.state = 213
            self.match(MiniPascalParser.EQ_OP)
            self.state = 214
            self.match(MiniPascalParser.RECORD)
            self.state = 218
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==47:
                self.state = 215
                self.recordFieldDeclaration()
                self.state = 220
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 221
            self.match(MiniPascalParser.END)
            self.state = 222
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
        self.enterRule(localctx, 32, self.RULE_recordFieldDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 224
            self.identList()
            self.state = 225
            self.match(MiniPascalParser.COLON)
            self.state = 226
            self.typeName()
            self.state = 227
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
        self.enterRule(localctx, 34, self.RULE_functionDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 229
            self.match(MiniPascalParser.FUNCTION)
            self.state = 230
            self.match(MiniPascalParser.IDENT)
            self.state = 232
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==37:
                self.state = 231
                self.formalParamList()


            self.state = 234
            self.match(MiniPascalParser.COLON)
            self.state = 235
            self.typeName()
            self.state = 236
            self.match(MiniPascalParser.SEMI)
            self.state = 237
            self.block()
            self.state = 239
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==30:
                self.state = 238
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
        self.enterRule(localctx, 36, self.RULE_procedureDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 241
            self.match(MiniPascalParser.PROCEDURE)
            self.state = 242
            self.match(MiniPascalParser.IDENT)
            self.state = 244
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==37:
                self.state = 243
                self.formalParamList()


            self.state = 246
            self.match(MiniPascalParser.SEMI)
            self.state = 247
            self.block()
            self.state = 249
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==30:
                self.state = 248
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
        self.enterRule(localctx, 38, self.RULE_formalParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 251
            self.match(MiniPascalParser.LPAREN)
            self.state = 252
            self.formalParam()
            self.state = 257
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==30:
                self.state = 253
                self.match(MiniPascalParser.SEMI)
                self.state = 254
                self.formalParam()
                self.state = 259
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 260
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
        self.enterRule(localctx, 40, self.RULE_formalParam)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 262
            self.identList()
            self.state = 263
            self.match(MiniPascalParser.COLON)
            self.state = 264
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
        self.enterRule(localctx, 42, self.RULE_declaration)
        try:
            self.state = 269
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 266
                self.varSection()
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 2)
                self.state = 267
                self.procedureDeclaration()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 3)
                self.state = 268
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
        self.enterRule(localctx, 44, self.RULE_functionCallExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 271
            self.match(MiniPascalParser.IDENT)
            self.state = 272
            self.match(MiniPascalParser.LPAREN)
            self.state = 274
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1900093548527616) != 0):
                self.state = 273
                self.argumentList()


            self.state = 276
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
        self.enterRule(localctx, 46, self.RULE_procedureCallStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 278
            self.match(MiniPascalParser.IDENT)
            self.state = 280
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==37:
                self.state = 279
                self.actualParamList()


            self.state = 283
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
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
        self.enterRule(localctx, 48, self.RULE_actualParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 285
            self.match(MiniPascalParser.LPAREN)
            self.state = 286
            self.actualParam()
            self.state = 291
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 287
                self.match(MiniPascalParser.COMMA)
                self.state = 288
                self.actualParam()
                self.state = 293
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 294
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
        self.enterRule(localctx, 50, self.RULE_actualParam)
        try:
            self.state = 298
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 296
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 297
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
        self.enterRule(localctx, 52, self.RULE_varSection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 300
            self.match(MiniPascalParser.VAR)
            self.state = 302 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 301
                self.varDeclaration()
                self.state = 304 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==47):
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
        self.enterRule(localctx, 54, self.RULE_varDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 306
            self.identList()
            self.state = 307
            self.match(MiniPascalParser.COLON)
            self.state = 308
            self.typeName()
            self.state = 309
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
        self.enterRule(localctx, 56, self.RULE_identList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 311
            self.match(MiniPascalParser.IDENT)
            self.state = 316
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 312
                self.match(MiniPascalParser.COMMA)
                self.state = 313
                self.match(MiniPascalParser.IDENT)
                self.state = 318
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
        self.enterRule(localctx, 58, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 322
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 12582960) != 0):
                self.state = 319
                self.localDeclaration()
                self.state = 324
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 325
            self.match(MiniPascalParser.BEGIN_)
            self.state = 326
            self.statementList()
            self.state = 327
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
        self.enterRule(localctx, 60, self.RULE_localDeclaration)
        try:
            self.state = 333
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [22]:
                self.enterOuterAlt(localctx, 1)
                self.state = 329
                self.procedureDeclaration()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 2)
                self.state = 330
                self.functionDeclaration()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 331
                self.varSection()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 332
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
        self.enterRule(localctx, 62, self.RULE_statementList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 341
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 140737539379204) != 0):
                self.state = 335
                self.statement()
                self.state = 337
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==30:
                    self.state = 336
                    self.match(MiniPascalParser.SEMI)


                self.state = 343
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
        self.enterRule(localctx, 64, self.RULE_statement)
        try:
            self.state = 352
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 344
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 345
                self.writeLnStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 346
                self.ifStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 347
                self.whileStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 348
                self.repeatStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 349
                self.forStatement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 350
                self.procedureCallStatement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 351
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
        self.enterRule(localctx, 66, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 354
            self.match(MiniPascalParser.FOR)
            self.state = 355
            self.match(MiniPascalParser.IDENT)
            self.state = 356
            self.match(MiniPascalParser.ASSIGN)
            self.state = 357
            self.expr()
            self.state = 358
            _la = self._input.LA(1)
            if not(_la==20 or _la==21):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 359
            self.expr()
            self.state = 360
            self.match(MiniPascalParser.DO)
            self.state = 361
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
        self.enterRule(localctx, 68, self.RULE_repeatStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 363
            self.match(MiniPascalParser.REPEAT)
            self.state = 364
            self.statementList()
            self.state = 365
            self.match(MiniPascalParser.UNTIL)
            self.state = 366
            self.condition()
            self.state = 368
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,31,self._ctx)
            if la_ == 1:
                self.state = 367
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
        self.enterRule(localctx, 70, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 370
            self.expr()
            self.state = 375
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 371
                self.match(MiniPascalParser.COMMA)
                self.state = 372
                self.expr()
                self.state = 377
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
        self.enterRule(localctx, 72, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 378
            self.match(MiniPascalParser.WHILE)
            self.state = 379
            self.condition()
            self.state = 380
            self.match(MiniPascalParser.DO)
            self.state = 381
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
        self.enterRule(localctx, 74, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 383
            self.match(MiniPascalParser.IF)
            self.state = 384
            self.condition()
            self.state = 385
            self.match(MiniPascalParser.THEN)
            self.state = 386
            self.statement()
            self.state = 389
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,33,self._ctx)
            if la_ == 1:
                self.state = 387
                self.match(MiniPascalParser.ELSE)
                self.state = 388
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
        self.enterRule(localctx, 76, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 391
            self.expr()
            self.state = 392
            self.compareOp()
            self.state = 393
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
        self.enterRule(localctx, 78, self.RULE_compareOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 395
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 69269232549888) != 0)):
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
        self.enterRule(localctx, 80, self.RULE_compoundStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 397
            self.match(MiniPascalParser.BEGIN_)
            self.state = 398
            self.statementList()
            self.state = 399
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
        self.enterRule(localctx, 82, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 401
            self.variableRef()
            self.state = 402
            self.match(MiniPascalParser.ASSIGN)
            self.state = 403
            self.expr()
            self.state = 405
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,34,self._ctx)
            if la_ == 1:
                self.state = 404
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
        self.enterRule(localctx, 84, self.RULE_variableRef)
        self._la = 0 # Token type
        try:
            self.state = 415
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [24]:
                self.enterOuterAlt(localctx, 1)
                self.state = 407
                self.match(MiniPascalParser.RESULT)
                pass
            elif token in [47]:
                self.enterOuterAlt(localctx, 2)
                self.state = 408
                self.match(MiniPascalParser.IDENT)
                self.state = 412
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==27 or _la==36:
                    self.state = 409
                    self.variableSuffix()
                    self.state = 414
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

        def expr(self):
            return self.getTypedRuleContext(MiniPascalParser.ExprContext,0)


        def RBRACK(self):
            return self.getToken(MiniPascalParser.RBRACK, 0)

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
        self.enterRule(localctx, 86, self.RULE_variableSuffix)
        try:
            self.state = 423
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27]:
                self.enterOuterAlt(localctx, 1)
                self.state = 417
                self.match(MiniPascalParser.DOT)
                self.state = 418
                self.match(MiniPascalParser.IDENT)
                pass
            elif token in [36]:
                self.enterOuterAlt(localctx, 2)
                self.state = 419
                self.match(MiniPascalParser.LBRACK)
                self.state = 420
                self.expr()
                self.state = 421
                self.match(MiniPascalParser.RBRACK)
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
        self.enterRule(localctx, 88, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 425
            self.term()
            self.state = 430
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32 or _la==33:
                self.state = 426
                _la = self._input.LA(1)
                if not(_la==32 or _la==33):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 427
                self.term()
                self.state = 432
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
        self.enterRule(localctx, 90, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 433
            self.factor()
            self.state = 438
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34 or _la==35:
                self.state = 434
                _la = self._input.LA(1)
                if not(_la==34 or _la==35):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 435
                self.factor()
                self.state = 440
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
        self.enterRule(localctx, 92, self.RULE_factor)
        try:
            self.state = 450
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,40,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 441
                self.variableRef()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 442
                self.functionCallExpr()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 443
                self.match(MiniPascalParser.NUMBER)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 444
                self.match(MiniPascalParser.FLOATNUMBER)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 445
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 446
                self.match(MiniPascalParser.LPAREN)
                self.state = 447
                self.expr()
                self.state = 448
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
        self.enterRule(localctx, 94, self.RULE_writeLnStatement)
        self._la = 0 # Token type
        try:
            self.state = 459
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,42,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 452
                self.match(MiniPascalParser.WRITELN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 453
                self.match(MiniPascalParser.WRITELN)
                self.state = 454
                self.match(MiniPascalParser.LPAREN)
                self.state = 456
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1900093548527616) != 0):
                    self.state = 455
                    self.writeArgList()


                self.state = 458
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
        self.enterRule(localctx, 96, self.RULE_writeArgList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 461
            self.writeArg()
            self.state = 466
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31:
                self.state = 462
                self.match(MiniPascalParser.COMMA)
                self.state = 463
                self.writeArg()
                self.state = 468
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
        self.enterRule(localctx, 98, self.RULE_writeArg)
        try:
            self.state = 471
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,44,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 469
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 470
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





