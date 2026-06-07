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
        4,1,58,528,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,2,46,
        7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,2,52,7,52,
        2,53,7,53,2,54,7,54,1,0,1,0,1,0,1,0,5,0,115,8,0,10,0,12,0,118,9,
        0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,3,1,128,8,1,1,2,1,2,4,2,132,8,
        2,11,2,12,2,133,1,3,1,3,1,3,5,3,139,8,3,10,3,12,3,142,9,3,1,3,1,
        3,1,4,1,4,1,4,1,4,1,5,1,5,1,6,1,6,4,6,154,8,6,11,6,12,6,155,1,7,
        1,7,1,7,1,7,1,7,1,7,1,7,1,7,3,7,166,8,7,1,8,1,8,1,8,1,8,3,8,172,
        8,8,1,8,1,8,1,9,1,9,1,9,3,9,179,8,9,1,9,1,9,1,10,1,10,1,10,5,10,
        186,8,10,10,10,12,10,189,9,10,1,10,3,10,192,8,10,1,11,1,11,1,11,
        1,11,1,11,5,11,199,8,11,10,11,12,11,202,9,11,1,11,1,11,1,11,1,11,
        1,11,1,11,1,11,3,11,211,8,11,1,12,1,12,1,12,1,12,1,13,1,13,1,13,
        3,13,220,8,13,1,14,1,14,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,16,
        1,16,1,16,5,16,234,8,16,10,16,12,16,237,9,16,1,17,1,17,1,17,3,17,
        242,8,17,1,18,1,18,1,18,1,18,5,18,248,8,18,10,18,12,18,251,9,18,
        1,18,1,18,1,18,1,19,1,19,1,19,1,19,1,19,1,20,1,20,1,20,3,20,264,
        8,20,1,20,1,20,1,20,1,20,1,20,3,20,271,8,20,1,21,1,21,1,21,3,21,
        276,8,21,1,21,1,21,1,21,3,21,281,8,21,1,22,1,22,1,22,1,22,5,22,287,
        8,22,10,22,12,22,290,9,22,1,22,1,22,1,23,3,23,295,8,23,1,23,1,23,
        1,23,1,23,1,24,1,24,1,24,3,24,304,8,24,1,25,1,25,1,25,3,25,309,8,
        25,1,25,1,25,1,26,1,26,3,26,315,8,26,1,26,3,26,318,8,26,1,27,1,27,
        1,27,1,27,5,27,324,8,27,10,27,12,27,327,9,27,1,27,1,27,1,28,1,28,
        3,28,333,8,28,1,29,1,29,4,29,337,8,29,11,29,12,29,338,1,30,1,30,
        1,30,1,30,1,30,1,31,1,31,3,31,348,8,31,1,32,1,32,1,32,5,32,353,8,
        32,10,32,12,32,356,9,32,1,33,5,33,359,8,33,10,33,12,33,362,9,33,
        1,33,1,33,1,33,1,33,1,34,1,34,1,34,1,34,3,34,372,8,34,1,35,1,35,
        3,35,376,8,35,5,35,378,8,35,10,35,12,35,381,9,35,1,36,1,36,1,36,
        1,36,1,36,1,36,1,36,1,36,1,36,3,36,392,8,36,1,37,1,37,3,37,396,8,
        37,1,38,1,38,1,38,1,38,1,38,1,38,1,38,1,38,1,38,1,39,1,39,1,39,1,
        39,1,39,3,39,412,8,39,1,40,1,40,1,40,5,40,417,8,40,10,40,12,40,420,
        9,40,1,41,1,41,1,41,1,41,1,41,1,42,1,42,1,42,1,42,1,42,1,42,3,42,
        433,8,42,1,43,1,43,1,43,1,43,1,44,1,44,1,45,1,45,1,45,1,45,1,46,
        1,46,1,46,1,46,3,46,449,8,46,1,47,1,47,1,47,5,47,454,8,47,10,47,
        12,47,457,9,47,3,47,459,8,47,1,48,1,48,1,48,1,48,1,48,1,48,5,48,
        467,8,48,10,48,12,48,470,9,48,1,48,1,48,1,48,3,48,475,8,48,1,49,
        1,49,1,49,5,49,480,8,49,10,49,12,49,483,9,49,1,50,1,50,1,50,5,50,
        488,8,50,10,50,12,50,491,9,50,1,51,1,51,1,51,1,51,1,51,1,51,1,51,
        1,51,1,51,1,51,1,51,1,51,3,51,505,8,51,1,52,1,52,1,52,1,52,3,52,
        511,8,52,1,52,3,52,514,8,52,1,53,1,53,1,53,5,53,519,8,53,10,53,12,
        53,522,9,53,1,54,1,54,3,54,526,8,54,1,54,0,0,55,0,2,4,6,8,10,12,
        14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,
        58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,
        102,104,106,108,0,6,2,0,50,50,53,54,2,0,11,12,50,51,1,0,21,22,1,
        0,44,49,1,0,34,35,1,0,36,37,546,0,110,1,0,0,0,2,127,1,0,0,0,4,129,
        1,0,0,0,6,135,1,0,0,0,8,145,1,0,0,0,10,149,1,0,0,0,12,151,1,0,0,
        0,14,165,1,0,0,0,16,167,1,0,0,0,18,175,1,0,0,0,20,182,1,0,0,0,22,
        210,1,0,0,0,24,212,1,0,0,0,26,219,1,0,0,0,28,221,1,0,0,0,30,223,
        1,0,0,0,32,230,1,0,0,0,34,238,1,0,0,0,36,243,1,0,0,0,38,255,1,0,
        0,0,40,260,1,0,0,0,42,272,1,0,0,0,44,282,1,0,0,0,46,294,1,0,0,0,
        48,303,1,0,0,0,50,305,1,0,0,0,52,312,1,0,0,0,54,319,1,0,0,0,56,332,
        1,0,0,0,58,334,1,0,0,0,60,340,1,0,0,0,62,347,1,0,0,0,64,349,1,0,
        0,0,66,360,1,0,0,0,68,371,1,0,0,0,70,379,1,0,0,0,72,391,1,0,0,0,
        74,393,1,0,0,0,76,397,1,0,0,0,78,406,1,0,0,0,80,413,1,0,0,0,82,421,
        1,0,0,0,84,426,1,0,0,0,86,434,1,0,0,0,88,438,1,0,0,0,90,440,1,0,
        0,0,92,444,1,0,0,0,94,458,1,0,0,0,96,474,1,0,0,0,98,476,1,0,0,0,
        100,484,1,0,0,0,102,504,1,0,0,0,104,513,1,0,0,0,106,515,1,0,0,0,
        108,525,1,0,0,0,110,111,5,1,0,0,111,112,5,51,0,0,112,116,5,32,0,
        0,113,115,3,2,1,0,114,113,1,0,0,0,115,118,1,0,0,0,116,114,1,0,0,
        0,116,117,1,0,0,0,117,119,1,0,0,0,118,116,1,0,0,0,119,120,3,66,33,
        0,120,121,5,29,0,0,121,1,1,0,0,0,122,128,3,4,2,0,123,128,3,12,6,
        0,124,128,3,58,29,0,125,128,3,42,21,0,126,128,3,40,20,0,127,122,
        1,0,0,0,127,123,1,0,0,0,127,124,1,0,0,0,127,125,1,0,0,0,127,126,
        1,0,0,0,128,3,1,0,0,0,129,131,5,4,0,0,130,132,3,6,3,0,131,130,1,
        0,0,0,132,133,1,0,0,0,133,131,1,0,0,0,133,134,1,0,0,0,134,5,1,0,
        0,0,135,140,3,8,4,0,136,137,5,33,0,0,137,139,3,8,4,0,138,136,1,0,
        0,0,139,142,1,0,0,0,140,138,1,0,0,0,140,141,1,0,0,0,141,143,1,0,
        0,0,142,140,1,0,0,0,143,144,5,32,0,0,144,7,1,0,0,0,145,146,5,51,
        0,0,146,147,5,44,0,0,147,148,3,10,5,0,148,9,1,0,0,0,149,150,7,0,
        0,0,150,11,1,0,0,0,151,153,5,6,0,0,152,154,3,14,7,0,153,152,1,0,
        0,0,154,155,1,0,0,0,155,153,1,0,0,0,155,156,1,0,0,0,156,13,1,0,0,
        0,157,158,5,51,0,0,158,159,5,44,0,0,159,160,3,26,13,0,160,161,5,
        32,0,0,161,166,1,0,0,0,162,166,3,30,15,0,163,166,3,36,18,0,164,166,
        3,16,8,0,165,157,1,0,0,0,165,162,1,0,0,0,165,163,1,0,0,0,165,164,
        1,0,0,0,166,15,1,0,0,0,167,168,5,51,0,0,168,169,5,44,0,0,169,171,
        3,22,11,0,170,172,3,18,9,0,171,170,1,0,0,0,171,172,1,0,0,0,172,173,
        1,0,0,0,173,174,5,32,0,0,174,17,1,0,0,0,175,176,5,44,0,0,176,178,
        5,39,0,0,177,179,3,20,10,0,178,177,1,0,0,0,178,179,1,0,0,0,179,180,
        1,0,0,0,180,181,5,40,0,0,181,19,1,0,0,0,182,187,3,10,5,0,183,184,
        5,33,0,0,184,186,3,10,5,0,185,183,1,0,0,0,186,189,1,0,0,0,187,185,
        1,0,0,0,187,188,1,0,0,0,188,191,1,0,0,0,189,187,1,0,0,0,190,192,
        5,33,0,0,191,190,1,0,0,0,191,192,1,0,0,0,192,21,1,0,0,0,193,194,
        5,8,0,0,194,195,5,38,0,0,195,200,3,24,12,0,196,197,5,33,0,0,197,
        199,3,24,12,0,198,196,1,0,0,0,199,202,1,0,0,0,200,198,1,0,0,0,200,
        201,1,0,0,0,201,203,1,0,0,0,202,200,1,0,0,0,203,204,5,41,0,0,204,
        205,5,9,0,0,205,206,3,26,13,0,206,211,1,0,0,0,207,208,5,8,0,0,208,
        209,5,9,0,0,209,211,3,26,13,0,210,193,1,0,0,0,210,207,1,0,0,0,211,
        23,1,0,0,0,212,213,3,98,49,0,213,214,5,28,0,0,214,215,3,98,49,0,
        215,25,1,0,0,0,216,220,3,28,14,0,217,218,5,42,0,0,218,220,3,28,14,
        0,219,216,1,0,0,0,219,217,1,0,0,0,220,27,1,0,0,0,221,222,7,1,0,0,
        222,29,1,0,0,0,223,224,5,51,0,0,224,225,5,44,0,0,225,226,5,39,0,
        0,226,227,3,32,16,0,227,228,5,40,0,0,228,229,5,32,0,0,229,31,1,0,
        0,0,230,235,3,34,17,0,231,232,5,33,0,0,232,234,3,34,17,0,233,231,
        1,0,0,0,234,237,1,0,0,0,235,233,1,0,0,0,235,236,1,0,0,0,236,33,1,
        0,0,0,237,235,1,0,0,0,238,241,5,51,0,0,239,240,5,44,0,0,240,242,
        5,54,0,0,241,239,1,0,0,0,241,242,1,0,0,0,242,35,1,0,0,0,243,244,
        5,51,0,0,244,245,5,44,0,0,245,249,5,7,0,0,246,248,3,38,19,0,247,
        246,1,0,0,0,248,251,1,0,0,0,249,247,1,0,0,0,249,250,1,0,0,0,250,
        252,1,0,0,0,251,249,1,0,0,0,252,253,5,3,0,0,253,254,5,32,0,0,254,
        37,1,0,0,0,255,256,3,64,32,0,256,257,5,31,0,0,257,258,3,26,13,0,
        258,259,5,32,0,0,259,39,1,0,0,0,260,261,5,24,0,0,261,263,5,51,0,
        0,262,264,3,44,22,0,263,262,1,0,0,0,263,264,1,0,0,0,264,265,1,0,
        0,0,265,266,5,31,0,0,266,267,3,26,13,0,267,268,5,32,0,0,268,270,
        3,66,33,0,269,271,5,32,0,0,270,269,1,0,0,0,270,271,1,0,0,0,271,41,
        1,0,0,0,272,273,5,23,0,0,273,275,5,51,0,0,274,276,3,44,22,0,275,
        274,1,0,0,0,275,276,1,0,0,0,276,277,1,0,0,0,277,278,5,32,0,0,278,
        280,3,66,33,0,279,281,5,32,0,0,280,279,1,0,0,0,280,281,1,0,0,0,281,
        43,1,0,0,0,282,283,5,39,0,0,283,288,3,46,23,0,284,285,5,32,0,0,285,
        287,3,46,23,0,286,284,1,0,0,0,287,290,1,0,0,0,288,286,1,0,0,0,288,
        289,1,0,0,0,289,291,1,0,0,0,290,288,1,0,0,0,291,292,5,40,0,0,292,
        45,1,0,0,0,293,295,5,5,0,0,294,293,1,0,0,0,294,295,1,0,0,0,295,296,
        1,0,0,0,296,297,3,64,32,0,297,298,5,31,0,0,298,299,3,26,13,0,299,
        47,1,0,0,0,300,304,3,58,29,0,301,304,3,42,21,0,302,304,3,40,20,0,
        303,300,1,0,0,0,303,301,1,0,0,0,303,302,1,0,0,0,304,49,1,0,0,0,305,
        306,5,51,0,0,306,308,5,39,0,0,307,309,3,80,40,0,308,307,1,0,0,0,
        308,309,1,0,0,0,309,310,1,0,0,0,310,311,5,40,0,0,311,51,1,0,0,0,
        312,314,5,51,0,0,313,315,3,54,27,0,314,313,1,0,0,0,314,315,1,0,0,
        0,315,317,1,0,0,0,316,318,5,32,0,0,317,316,1,0,0,0,317,318,1,0,0,
        0,318,53,1,0,0,0,319,320,5,39,0,0,320,325,3,56,28,0,321,322,5,33,
        0,0,322,324,3,56,28,0,323,321,1,0,0,0,324,327,1,0,0,0,325,323,1,
        0,0,0,325,326,1,0,0,0,326,328,1,0,0,0,327,325,1,0,0,0,328,329,5,
        40,0,0,329,55,1,0,0,0,330,333,5,50,0,0,331,333,3,98,49,0,332,330,
        1,0,0,0,332,331,1,0,0,0,333,57,1,0,0,0,334,336,5,5,0,0,335,337,3,
        60,30,0,336,335,1,0,0,0,337,338,1,0,0,0,338,336,1,0,0,0,338,339,
        1,0,0,0,339,59,1,0,0,0,340,341,3,64,32,0,341,342,5,31,0,0,342,343,
        3,62,31,0,343,344,5,32,0,0,344,61,1,0,0,0,345,348,3,26,13,0,346,
        348,3,22,11,0,347,345,1,0,0,0,347,346,1,0,0,0,348,63,1,0,0,0,349,
        354,5,51,0,0,350,351,5,33,0,0,351,353,5,51,0,0,352,350,1,0,0,0,353,
        356,1,0,0,0,354,352,1,0,0,0,354,355,1,0,0,0,355,65,1,0,0,0,356,354,
        1,0,0,0,357,359,3,68,34,0,358,357,1,0,0,0,359,362,1,0,0,0,360,358,
        1,0,0,0,360,361,1,0,0,0,361,363,1,0,0,0,362,360,1,0,0,0,363,364,
        5,2,0,0,364,365,3,70,35,0,365,366,5,3,0,0,366,67,1,0,0,0,367,372,
        3,42,21,0,368,372,3,40,20,0,369,372,3,58,29,0,370,372,3,4,2,0,371,
        367,1,0,0,0,371,368,1,0,0,0,371,369,1,0,0,0,371,370,1,0,0,0,372,
        69,1,0,0,0,373,375,3,72,36,0,374,376,5,32,0,0,375,374,1,0,0,0,375,
        376,1,0,0,0,376,378,1,0,0,0,377,373,1,0,0,0,378,381,1,0,0,0,379,
        377,1,0,0,0,379,380,1,0,0,0,380,71,1,0,0,0,381,379,1,0,0,0,382,392,
        3,92,46,0,383,392,3,104,52,0,384,392,3,84,42,0,385,392,3,82,41,0,
        386,392,3,78,39,0,387,392,3,76,38,0,388,392,3,52,26,0,389,392,3,
        74,37,0,390,392,3,90,45,0,391,382,1,0,0,0,391,383,1,0,0,0,391,384,
        1,0,0,0,391,385,1,0,0,0,391,386,1,0,0,0,391,387,1,0,0,0,391,388,
        1,0,0,0,391,389,1,0,0,0,391,390,1,0,0,0,392,73,1,0,0,0,393,395,5,
        26,0,0,394,396,5,32,0,0,395,394,1,0,0,0,395,396,1,0,0,0,396,75,1,
        0,0,0,397,398,5,20,0,0,398,399,5,51,0,0,399,400,5,30,0,0,400,401,
        3,98,49,0,401,402,7,2,0,0,402,403,3,98,49,0,403,404,5,17,0,0,404,
        405,3,72,36,0,405,77,1,0,0,0,406,407,5,18,0,0,407,408,3,70,35,0,
        408,409,5,19,0,0,409,411,3,86,43,0,410,412,5,32,0,0,411,410,1,0,
        0,0,411,412,1,0,0,0,412,79,1,0,0,0,413,418,3,98,49,0,414,415,5,33,
        0,0,415,417,3,98,49,0,416,414,1,0,0,0,417,420,1,0,0,0,418,416,1,
        0,0,0,418,419,1,0,0,0,419,81,1,0,0,0,420,418,1,0,0,0,421,422,5,16,
        0,0,422,423,3,86,43,0,423,424,5,17,0,0,424,425,3,72,36,0,425,83,
        1,0,0,0,426,427,5,13,0,0,427,428,3,86,43,0,428,429,5,14,0,0,429,
        432,3,72,36,0,430,431,5,15,0,0,431,433,3,72,36,0,432,430,1,0,0,0,
        432,433,1,0,0,0,433,85,1,0,0,0,434,435,3,98,49,0,435,436,3,88,44,
        0,436,437,3,98,49,0,437,87,1,0,0,0,438,439,7,3,0,0,439,89,1,0,0,
        0,440,441,5,2,0,0,441,442,3,70,35,0,442,443,5,3,0,0,443,91,1,0,0,
        0,444,445,3,94,47,0,445,446,5,30,0,0,446,448,3,98,49,0,447,449,5,
        32,0,0,448,447,1,0,0,0,448,449,1,0,0,0,449,93,1,0,0,0,450,459,5,
        25,0,0,451,455,5,51,0,0,452,454,3,96,48,0,453,452,1,0,0,0,454,457,
        1,0,0,0,455,453,1,0,0,0,455,456,1,0,0,0,456,459,1,0,0,0,457,455,
        1,0,0,0,458,450,1,0,0,0,458,451,1,0,0,0,459,95,1,0,0,0,460,461,5,
        29,0,0,461,475,5,51,0,0,462,463,5,38,0,0,463,468,3,98,49,0,464,465,
        5,33,0,0,465,467,3,98,49,0,466,464,1,0,0,0,467,470,1,0,0,0,468,466,
        1,0,0,0,468,469,1,0,0,0,469,471,1,0,0,0,470,468,1,0,0,0,471,472,
        5,41,0,0,472,475,1,0,0,0,473,475,5,42,0,0,474,460,1,0,0,0,474,462,
        1,0,0,0,474,473,1,0,0,0,475,97,1,0,0,0,476,481,3,100,50,0,477,478,
        7,4,0,0,478,480,3,100,50,0,479,477,1,0,0,0,480,483,1,0,0,0,481,479,
        1,0,0,0,481,482,1,0,0,0,482,99,1,0,0,0,483,481,1,0,0,0,484,489,3,
        102,51,0,485,486,7,5,0,0,486,488,3,102,51,0,487,485,1,0,0,0,488,
        491,1,0,0,0,489,487,1,0,0,0,489,490,1,0,0,0,490,101,1,0,0,0,491,
        489,1,0,0,0,492,493,5,43,0,0,493,505,3,94,47,0,494,505,3,94,47,0,
        495,505,3,50,25,0,496,505,5,10,0,0,497,505,5,54,0,0,498,505,5,53,
        0,0,499,505,5,50,0,0,500,501,5,39,0,0,501,502,3,98,49,0,502,503,
        5,40,0,0,503,505,1,0,0,0,504,492,1,0,0,0,504,494,1,0,0,0,504,495,
        1,0,0,0,504,496,1,0,0,0,504,497,1,0,0,0,504,498,1,0,0,0,504,499,
        1,0,0,0,504,500,1,0,0,0,505,103,1,0,0,0,506,514,5,27,0,0,507,508,
        5,27,0,0,508,510,5,39,0,0,509,511,3,106,53,0,510,509,1,0,0,0,510,
        511,1,0,0,0,511,512,1,0,0,0,512,514,5,40,0,0,513,506,1,0,0,0,513,
        507,1,0,0,0,514,105,1,0,0,0,515,520,3,108,54,0,516,517,5,33,0,0,
        517,519,3,108,54,0,518,516,1,0,0,0,519,522,1,0,0,0,520,518,1,0,0,
        0,520,521,1,0,0,0,521,107,1,0,0,0,522,520,1,0,0,0,523,526,5,50,0,
        0,524,526,3,98,49,0,525,523,1,0,0,0,525,524,1,0,0,0,526,109,1,0,
        0,0,52,116,127,133,140,155,165,171,178,187,191,200,210,219,235,241,
        249,263,270,275,280,288,294,303,308,314,317,325,332,338,347,354,
        360,371,375,379,391,395,411,418,432,448,455,458,468,474,481,489,
        504,510,513,520,525
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
                     "'..'", "'.'", "':='", "':'", "';'", "','", "'+'", 
                     "'-'", "'*'", "'/'", "'['", "'('", "')'", "']'", "'^'", 
                     "'@'", "'='", "'<='", "'<>'", "'<'", "'>='", "'>'" ]

    symbolicNames = [ "<INVALID>", "PROGRAM", "BEGIN_", "END", "CONST", 
                      "VAR", "TYPE", "RECORD", "ARRAY", "OF", "NIL", "DOUBLE", 
                      "INTEGER", "IF", "THEN", "ELSE", "WHILE", "DO", "REPEAT", 
                      "UNTIL", "FOR", "TO", "DOWNTO", "PROCEDURE", "FUNCTION", 
                      "RESULT", "EXIT", "WRITELN", "DOTDOT", "DOT", "ASSIGN", 
                      "COLON", "SEMI", "COMMA", "PLUS", "MINUS", "STAR", 
                      "SLASH", "LBRACK", "LPAREN", "RPAREN", "RBRACK", "CARET", 
                      "AT", "EQ_OP", "LE_OP", "NE_OP", "LT_OP", "GE_OP", 
                      "GT_OP", "STRING", "IDENT", "HEXNUMBER", "FLOATNUMBER", 
                      "NUMBER", "WS", "COMMENT1", "COMMENT2", "COMMENT3" ]

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
    RULE_exitStatement = 37
    RULE_forStatement = 38
    RULE_repeatStatement = 39
    RULE_argumentList = 40
    RULE_whileStatement = 41
    RULE_ifStatement = 42
    RULE_condition = 43
    RULE_compareOp = 44
    RULE_compoundStatement = 45
    RULE_assignment = 46
    RULE_variableRef = 47
    RULE_variableSuffix = 48
    RULE_expr = 49
    RULE_term = 50
    RULE_factor = 51
    RULE_writeLnStatement = 52
    RULE_writeArgList = 53
    RULE_writeArg = 54

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
                   "exitStatement", "forStatement", "repeatStatement", "argumentList", 
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
    NIL=10
    DOUBLE=11
    INTEGER=12
    IF=13
    THEN=14
    ELSE=15
    WHILE=16
    DO=17
    REPEAT=18
    UNTIL=19
    FOR=20
    TO=21
    DOWNTO=22
    PROCEDURE=23
    FUNCTION=24
    RESULT=25
    EXIT=26
    WRITELN=27
    DOTDOT=28
    DOT=29
    ASSIGN=30
    COLON=31
    SEMI=32
    COMMA=33
    PLUS=34
    MINUS=35
    STAR=36
    SLASH=37
    LBRACK=38
    LPAREN=39
    RPAREN=40
    RBRACK=41
    CARET=42
    AT=43
    EQ_OP=44
    LE_OP=45
    NE_OP=46
    LT_OP=47
    GE_OP=48
    GT_OP=49
    STRING=50
    IDENT=51
    HEXNUMBER=52
    FLOATNUMBER=53
    NUMBER=54
    WS=55
    COMMENT1=56
    COMMENT2=57
    COMMENT3=58

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
            self.state = 110
            self.match(MiniPascalParser.PROGRAM)
            self.state = 111
            self.match(MiniPascalParser.IDENT)
            self.state = 112
            self.match(MiniPascalParser.SEMI)
            self.state = 116
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 113
                    self.declarationPart() 
                self.state = 118
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 119
            self.block()
            self.state = 120
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
            self.state = 127
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 122
                self.constSection()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 123
                self.typeSection()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 124
                self.varSection()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 4)
                self.state = 125
                self.procedureDeclaration()
                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 5)
                self.state = 126
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
            self.state = 129
            self.match(MiniPascalParser.CONST)
            self.state = 131 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 130
                self.constDeclaration()
                self.state = 133 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==51):
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
            self.state = 135
            self.constItem()
            self.state = 140
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33:
                self.state = 136
                self.match(MiniPascalParser.COMMA)
                self.state = 137
                self.constItem()
                self.state = 142
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 143
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
            self.state = 145
            self.match(MiniPascalParser.IDENT)
            self.state = 146
            self.match(MiniPascalParser.EQ_OP)
            self.state = 147
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
            self.state = 149
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 28147497671065600) != 0)):
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
            self.state = 151
            self.match(MiniPascalParser.TYPE)
            self.state = 153 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 152
                self.typeDeclaration()
                self.state = 155 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==51):
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
            self.state = 165
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 157
                self.match(MiniPascalParser.IDENT)
                self.state = 158
                self.match(MiniPascalParser.EQ_OP)
                self.state = 159
                self.typeName()
                self.state = 160
                self.match(MiniPascalParser.SEMI)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 162
                self.enumDeclaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 163
                self.recordDeclaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 164
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
            self.state = 167
            self.match(MiniPascalParser.IDENT)
            self.state = 168
            self.match(MiniPascalParser.EQ_OP)
            self.state = 169
            self.arrayType()
            self.state = 171
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==44:
                self.state = 170
                self.arrayInitializer()


            self.state = 173
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
            self.state = 175
            self.match(MiniPascalParser.EQ_OP)
            self.state = 176
            self.match(MiniPascalParser.LPAREN)
            self.state = 178
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 28147497671065600) != 0):
                self.state = 177
                self.arrayValueList()


            self.state = 180
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
            self.state = 182
            self.constValue()
            self.state = 187
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 183
                    self.match(MiniPascalParser.COMMA)
                    self.state = 184
                    self.constValue() 
                self.state = 189
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

            self.state = 191
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==33:
                self.state = 190
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
            self.state = 210
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 193
                self.match(MiniPascalParser.ARRAY)
                self.state = 194
                self.match(MiniPascalParser.LBRACK)
                self.state = 195
                self.arrayRange()
                self.state = 200
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==33:
                    self.state = 196
                    self.match(MiniPascalParser.COMMA)
                    self.state = 197
                    self.arrayRange()
                    self.state = 202
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 203
                self.match(MiniPascalParser.RBRACK)
                self.state = 204
                self.match(MiniPascalParser.OF)
                self.state = 205
                self.typeName()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 207
                self.match(MiniPascalParser.ARRAY)
                self.state = 208
                self.match(MiniPascalParser.OF)
                self.state = 209
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
            self.state = 212
            self.expr()
            self.state = 213
            self.match(MiniPascalParser.DOTDOT)
            self.state = 214
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
            self.state = 219
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11, 12, 50, 51]:
                self.enterOuterAlt(localctx, 1)
                self.state = 216
                self.simpleType()
                pass
            elif token in [42]:
                self.enterOuterAlt(localctx, 2)
                self.state = 217
                self.match(MiniPascalParser.CARET)
                self.state = 218
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
            self.state = 221
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3377699720534016) != 0)):
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
            self.state = 223
            self.match(MiniPascalParser.IDENT)
            self.state = 224
            self.match(MiniPascalParser.EQ_OP)
            self.state = 225
            self.match(MiniPascalParser.LPAREN)
            self.state = 226
            self.enumValueList()
            self.state = 227
            self.match(MiniPascalParser.RPAREN)
            self.state = 228
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
            self.state = 230
            self.enumValue()
            self.state = 235
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33:
                self.state = 231
                self.match(MiniPascalParser.COMMA)
                self.state = 232
                self.enumValue()
                self.state = 237
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
            self.state = 238
            self.match(MiniPascalParser.IDENT)
            self.state = 241
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==44:
                self.state = 239
                self.match(MiniPascalParser.EQ_OP)
                self.state = 240
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
            self.state = 243
            self.match(MiniPascalParser.IDENT)
            self.state = 244
            self.match(MiniPascalParser.EQ_OP)
            self.state = 245
            self.match(MiniPascalParser.RECORD)
            self.state = 249
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==51:
                self.state = 246
                self.recordFieldDeclaration()
                self.state = 251
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 252
            self.match(MiniPascalParser.END)
            self.state = 253
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
            self.state = 255
            self.identList()
            self.state = 256
            self.match(MiniPascalParser.COLON)
            self.state = 257
            self.typeName()
            self.state = 258
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
            self.state = 260
            self.match(MiniPascalParser.FUNCTION)
            self.state = 261
            self.match(MiniPascalParser.IDENT)
            self.state = 263
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 262
                self.formalParamList()


            self.state = 265
            self.match(MiniPascalParser.COLON)
            self.state = 266
            self.typeName()
            self.state = 267
            self.match(MiniPascalParser.SEMI)
            self.state = 268
            self.block()
            self.state = 270
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==32:
                self.state = 269
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
            self.state = 272
            self.match(MiniPascalParser.PROCEDURE)
            self.state = 273
            self.match(MiniPascalParser.IDENT)
            self.state = 275
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 274
                self.formalParamList()


            self.state = 277
            self.match(MiniPascalParser.SEMI)
            self.state = 278
            self.block()
            self.state = 280
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==32:
                self.state = 279
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
            self.state = 282
            self.match(MiniPascalParser.LPAREN)
            self.state = 283
            self.formalParam()
            self.state = 288
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 284
                self.match(MiniPascalParser.SEMI)
                self.state = 285
                self.formalParam()
                self.state = 290
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 291
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
            self.state = 294
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 293
                self.match(MiniPascalParser.VAR)


            self.state = 296
            self.identList()
            self.state = 297
            self.match(MiniPascalParser.COLON)
            self.state = 298
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
            self.state = 303
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 300
                self.varSection()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 2)
                self.state = 301
                self.procedureDeclaration()
                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 3)
                self.state = 302
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
            self.state = 305
            self.match(MiniPascalParser.IDENT)
            self.state = 306
            self.match(MiniPascalParser.LPAREN)
            self.state = 308
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 30408643367142400) != 0):
                self.state = 307
                self.argumentList()


            self.state = 310
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
            self.state = 312
            self.match(MiniPascalParser.IDENT)
            self.state = 314
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 313
                self.actualParamList()


            self.state = 317
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,25,self._ctx)
            if la_ == 1:
                self.state = 316
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
            self.state = 319
            self.match(MiniPascalParser.LPAREN)
            self.state = 320
            self.actualParam()
            self.state = 325
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33:
                self.state = 321
                self.match(MiniPascalParser.COMMA)
                self.state = 322
                self.actualParam()
                self.state = 327
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 328
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
            self.state = 332
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,27,self._ctx)
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
            self.state = 334
            self.match(MiniPascalParser.VAR)
            self.state = 336 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 335
                self.varDeclaration()
                self.state = 338 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==51):
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
            self.state = 340
            self.identList()
            self.state = 341
            self.match(MiniPascalParser.COLON)
            self.state = 342
            self.varType()
            self.state = 343
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
            self.state = 347
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11, 12, 42, 50, 51]:
                self.enterOuterAlt(localctx, 1)
                self.state = 345
                self.typeName()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 2)
                self.state = 346
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
            self.state = 349
            self.match(MiniPascalParser.IDENT)
            self.state = 354
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33:
                self.state = 350
                self.match(MiniPascalParser.COMMA)
                self.state = 351
                self.match(MiniPascalParser.IDENT)
                self.state = 356
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
            self.state = 360
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 25165872) != 0):
                self.state = 357
                self.localDeclaration()
                self.state = 362
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 363
            self.match(MiniPascalParser.BEGIN_)
            self.state = 364
            self.statementList()
            self.state = 365
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
            self.state = 371
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.enterOuterAlt(localctx, 1)
                self.state = 367
                self.procedureDeclaration()
                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 2)
                self.state = 368
                self.functionDeclaration()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 369
                self.varSection()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 370
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
            self.state = 379
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2251800049950724) != 0):
                self.state = 373
                self.statement()
                self.state = 375
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==32:
                    self.state = 374
                    self.match(MiniPascalParser.SEMI)


                self.state = 381
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
            self.state = 391
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,35,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 382
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 383
                self.writeLnStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 384
                self.ifStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 385
                self.whileStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 386
                self.repeatStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 387
                self.forStatement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 388
                self.procedureCallStatement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 389
                self.exitStatement()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 390
                self.compoundStatement()
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
        self.enterRule(localctx, 74, self.RULE_exitStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 393
            self.match(MiniPascalParser.EXIT)
            self.state = 395
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,36,self._ctx)
            if la_ == 1:
                self.state = 394
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
        self.enterRule(localctx, 76, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 397
            self.match(MiniPascalParser.FOR)
            self.state = 398
            self.match(MiniPascalParser.IDENT)
            self.state = 399
            self.match(MiniPascalParser.ASSIGN)
            self.state = 400
            self.expr()
            self.state = 401
            _la = self._input.LA(1)
            if not(_la==21 or _la==22):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 402
            self.expr()
            self.state = 403
            self.match(MiniPascalParser.DO)
            self.state = 404
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
        self.enterRule(localctx, 78, self.RULE_repeatStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 406
            self.match(MiniPascalParser.REPEAT)
            self.state = 407
            self.statementList()
            self.state = 408
            self.match(MiniPascalParser.UNTIL)
            self.state = 409
            self.condition()
            self.state = 411
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,37,self._ctx)
            if la_ == 1:
                self.state = 410
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
        self.enterRule(localctx, 80, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 413
            self.expr()
            self.state = 418
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33:
                self.state = 414
                self.match(MiniPascalParser.COMMA)
                self.state = 415
                self.expr()
                self.state = 420
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
        self.enterRule(localctx, 82, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 421
            self.match(MiniPascalParser.WHILE)
            self.state = 422
            self.condition()
            self.state = 423
            self.match(MiniPascalParser.DO)
            self.state = 424
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
        self.enterRule(localctx, 84, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 426
            self.match(MiniPascalParser.IF)
            self.state = 427
            self.condition()
            self.state = 428
            self.match(MiniPascalParser.THEN)
            self.state = 429
            self.statement()
            self.state = 432
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
            if la_ == 1:
                self.state = 430
                self.match(MiniPascalParser.ELSE)
                self.state = 431
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
        self.enterRule(localctx, 86, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 434
            self.expr()
            self.state = 435
            self.compareOp()
            self.state = 436
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
        self.enterRule(localctx, 88, self.RULE_compareOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 438
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1108307720798208) != 0)):
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
        self.enterRule(localctx, 90, self.RULE_compoundStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 440
            self.match(MiniPascalParser.BEGIN_)
            self.state = 441
            self.statementList()
            self.state = 442
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
        self.enterRule(localctx, 92, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 444
            self.variableRef()
            self.state = 445
            self.match(MiniPascalParser.ASSIGN)
            self.state = 446
            self.expr()
            self.state = 448
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,40,self._ctx)
            if la_ == 1:
                self.state = 447
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
        self.enterRule(localctx, 94, self.RULE_variableRef)
        self._la = 0 # Token type
        try:
            self.state = 458
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [25]:
                self.enterOuterAlt(localctx, 1)
                self.state = 450
                self.match(MiniPascalParser.RESULT)
                pass
            elif token in [51]:
                self.enterOuterAlt(localctx, 2)
                self.state = 451
                self.match(MiniPascalParser.IDENT)
                self.state = 455
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 4673461288960) != 0):
                    self.state = 452
                    self.variableSuffix()
                    self.state = 457
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
        self.enterRule(localctx, 96, self.RULE_variableSuffix)
        self._la = 0 # Token type
        try:
            self.state = 474
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [29]:
                self.enterOuterAlt(localctx, 1)
                self.state = 460
                self.match(MiniPascalParser.DOT)
                self.state = 461
                self.match(MiniPascalParser.IDENT)
                pass
            elif token in [38]:
                self.enterOuterAlt(localctx, 2)
                self.state = 462
                self.match(MiniPascalParser.LBRACK)
                self.state = 463
                self.expr()
                self.state = 468
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==33:
                    self.state = 464
                    self.match(MiniPascalParser.COMMA)
                    self.state = 465
                    self.expr()
                    self.state = 470
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 471
                self.match(MiniPascalParser.RBRACK)
                pass
            elif token in [42]:
                self.enterOuterAlt(localctx, 3)
                self.state = 473
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
        self.enterRule(localctx, 98, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 476
            self.term()
            self.state = 481
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34 or _la==35:
                self.state = 477
                _la = self._input.LA(1)
                if not(_la==34 or _la==35):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 478
                self.term()
                self.state = 483
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
        self.enterRule(localctx, 100, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 484
            self.factor()
            self.state = 489
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==36 or _la==37:
                self.state = 485
                _la = self._input.LA(1)
                if not(_la==36 or _la==37):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 486
                self.factor()
                self.state = 491
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
        self.enterRule(localctx, 102, self.RULE_factor)
        try:
            self.state = 504
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,47,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 492
                self.match(MiniPascalParser.AT)
                self.state = 493
                self.variableRef()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 494
                self.variableRef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 495
                self.functionCallExpr()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 496
                self.match(MiniPascalParser.NIL)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 497
                self.match(MiniPascalParser.NUMBER)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 498
                self.match(MiniPascalParser.FLOATNUMBER)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 499
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 500
                self.match(MiniPascalParser.LPAREN)
                self.state = 501
                self.expr()
                self.state = 502
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
        self.enterRule(localctx, 104, self.RULE_writeLnStatement)
        self._la = 0 # Token type
        try:
            self.state = 513
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,49,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 506
                self.match(MiniPascalParser.WRITELN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 507
                self.match(MiniPascalParser.WRITELN)
                self.state = 508
                self.match(MiniPascalParser.LPAREN)
                self.state = 510
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 30408643367142400) != 0):
                    self.state = 509
                    self.writeArgList()


                self.state = 512
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
        self.enterRule(localctx, 106, self.RULE_writeArgList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 515
            self.writeArg()
            self.state = 520
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33:
                self.state = 516
                self.match(MiniPascalParser.COMMA)
                self.state = 517
                self.writeArg()
                self.state = 522
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
        self.enterRule(localctx, 108, self.RULE_writeArg)
        try:
            self.state = 525
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,51,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 523
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 524
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





