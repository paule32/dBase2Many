# Generated from compiler/grammar/BasicParser.g4 by ANTLR 4.13.2
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
        4,1,73,531,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,2,46,
        7,46,2,47,7,47,2,48,7,48,1,0,5,0,100,8,0,10,0,12,0,103,9,0,1,0,3,
        0,106,8,0,1,0,4,0,109,8,0,11,0,12,0,110,1,0,1,0,5,0,115,8,0,10,0,
        12,0,118,9,0,1,0,5,0,121,8,0,10,0,12,0,124,9,0,1,0,1,0,1,1,1,1,1,
        1,3,1,131,8,1,1,2,4,2,134,8,2,11,2,12,2,135,1,3,1,3,1,4,1,4,1,4,
        3,4,143,8,4,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,3,5,153,8,5,1,5,1,5,
        3,5,157,8,5,1,5,1,5,1,5,1,5,1,5,1,6,1,6,3,6,166,8,6,1,6,1,6,1,7,
        1,7,1,7,5,7,173,8,7,10,7,12,7,176,9,7,1,8,3,8,179,8,8,1,8,1,8,1,
        8,3,8,184,8,8,1,9,3,9,187,8,9,1,9,1,9,1,10,1,10,1,11,1,11,1,11,1,
        11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,3,
        11,209,8,11,1,12,1,12,4,12,213,8,12,11,12,12,12,214,5,12,217,8,12,
        10,12,12,12,220,9,12,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,
        1,13,1,13,3,13,233,8,13,1,14,3,14,236,8,14,1,14,1,14,1,14,1,14,1,
        15,1,15,1,15,1,15,3,15,246,8,15,1,15,1,15,1,15,1,16,1,16,1,16,1,
        16,5,16,255,8,16,10,16,12,16,258,9,16,1,17,1,17,3,17,262,8,17,1,
        17,1,17,3,17,266,8,17,1,17,1,17,3,17,270,8,17,1,18,1,18,1,18,1,18,
        5,18,276,8,18,10,18,12,18,279,9,18,1,18,1,18,1,19,1,19,1,19,1,19,
        1,19,3,19,288,8,19,1,20,1,20,3,20,292,8,20,1,21,1,21,1,21,5,21,297,
        8,21,10,21,12,21,300,9,21,1,21,3,21,303,8,21,1,22,1,22,1,22,3,22,
        308,8,22,1,22,1,22,1,22,5,22,313,8,22,10,22,12,22,316,9,22,1,23,
        1,23,1,23,1,23,1,23,1,23,3,23,324,8,23,1,23,1,23,1,23,1,23,1,23,
        1,23,1,23,1,23,1,23,1,23,1,23,5,23,337,8,23,10,23,12,23,340,9,23,
        1,23,1,23,1,23,1,23,3,23,346,8,23,1,23,1,23,1,23,3,23,351,8,23,1,
        24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,3,24,361,8,24,1,24,1,24,1,
        24,1,24,3,24,367,8,24,1,25,1,25,1,25,1,25,1,25,1,25,1,25,3,25,376,
        8,25,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,
        1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,
        1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,3,26,411,8,26,1,27,1,27,
        1,27,1,28,1,28,1,28,1,29,1,29,1,30,1,30,3,30,423,8,30,1,31,1,31,
        1,31,1,31,3,31,429,8,31,1,31,3,31,432,8,31,1,32,1,32,3,32,436,8,
        32,1,33,1,33,1,33,1,34,1,34,1,35,1,35,1,36,1,36,1,37,1,37,1,37,5,
        37,450,8,37,10,37,12,37,453,9,37,1,38,1,38,1,38,5,38,458,8,38,10,
        38,12,38,461,9,38,1,39,1,39,1,39,5,39,466,8,39,10,39,12,39,469,9,
        39,1,40,1,40,1,40,3,40,474,8,40,1,41,1,41,1,41,3,41,479,8,41,1,42,
        1,42,1,42,5,42,484,8,42,10,42,12,42,487,9,42,1,43,1,43,1,43,5,43,
        492,8,43,10,43,12,43,495,9,43,1,44,1,44,1,44,3,44,500,8,44,1,45,
        1,45,1,45,3,45,505,8,45,1,46,1,46,1,46,1,46,3,46,511,8,46,1,46,1,
        46,1,46,1,46,1,46,1,46,3,46,519,8,46,1,47,1,47,1,47,5,47,524,8,47,
        10,47,12,47,527,9,47,1,48,1,48,1,48,0,0,49,0,2,4,6,8,10,12,14,16,
        18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,
        62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,0,12,2,0,70,
        70,72,72,1,0,6,7,1,0,68,69,2,0,13,13,42,42,2,0,51,51,71,71,4,0,11,
        11,19,20,40,40,46,46,7,0,5,5,12,12,25,25,28,28,36,36,39,39,71,71,
        1,0,53,58,2,0,59,60,65,65,2,0,30,30,61,63,1,0,59,60,3,0,18,18,43,
        43,48,52,566,0,101,1,0,0,0,2,130,1,0,0,0,4,133,1,0,0,0,6,137,1,0,
        0,0,8,139,1,0,0,0,10,149,1,0,0,0,12,163,1,0,0,0,14,169,1,0,0,0,16,
        178,1,0,0,0,18,186,1,0,0,0,20,190,1,0,0,0,22,208,1,0,0,0,24,218,
        1,0,0,0,26,232,1,0,0,0,28,235,1,0,0,0,30,241,1,0,0,0,32,250,1,0,
        0,0,34,259,1,0,0,0,36,271,1,0,0,0,38,282,1,0,0,0,40,289,1,0,0,0,
        42,293,1,0,0,0,44,304,1,0,0,0,46,350,1,0,0,0,48,352,1,0,0,0,50,368,
        1,0,0,0,52,410,1,0,0,0,54,412,1,0,0,0,56,415,1,0,0,0,58,418,1,0,
        0,0,60,420,1,0,0,0,62,424,1,0,0,0,64,433,1,0,0,0,66,437,1,0,0,0,
        68,440,1,0,0,0,70,442,1,0,0,0,72,444,1,0,0,0,74,446,1,0,0,0,76,454,
        1,0,0,0,78,462,1,0,0,0,80,473,1,0,0,0,82,475,1,0,0,0,84,480,1,0,
        0,0,86,488,1,0,0,0,88,496,1,0,0,0,90,504,1,0,0,0,92,518,1,0,0,0,
        94,520,1,0,0,0,96,528,1,0,0,0,98,100,3,4,2,0,99,98,1,0,0,0,100,103,
        1,0,0,0,101,99,1,0,0,0,101,102,1,0,0,0,102,105,1,0,0,0,103,101,1,
        0,0,0,104,106,3,2,1,0,105,104,1,0,0,0,105,106,1,0,0,0,106,116,1,
        0,0,0,107,109,3,4,2,0,108,107,1,0,0,0,109,110,1,0,0,0,110,108,1,
        0,0,0,110,111,1,0,0,0,111,112,1,0,0,0,112,113,3,2,1,0,113,115,1,
        0,0,0,114,108,1,0,0,0,115,118,1,0,0,0,116,114,1,0,0,0,116,117,1,
        0,0,0,117,122,1,0,0,0,118,116,1,0,0,0,119,121,3,4,2,0,120,119,1,
        0,0,0,121,124,1,0,0,0,122,120,1,0,0,0,122,123,1,0,0,0,123,125,1,
        0,0,0,124,122,1,0,0,0,125,126,5,0,0,1,126,1,1,0,0,0,127,131,3,8,
        4,0,128,131,3,10,5,0,129,131,3,18,9,0,130,127,1,0,0,0,130,128,1,
        0,0,0,130,129,1,0,0,0,131,3,1,0,0,0,132,134,3,6,3,0,133,132,1,0,
        0,0,134,135,1,0,0,0,135,133,1,0,0,0,135,136,1,0,0,0,136,5,1,0,0,
        0,137,138,7,0,0,0,138,7,1,0,0,0,139,140,5,40,0,0,140,142,5,71,0,
        0,141,143,3,12,6,0,142,141,1,0,0,0,142,143,1,0,0,0,143,144,1,0,0,
        0,144,145,3,4,2,0,145,146,3,24,12,0,146,147,5,16,0,0,147,148,5,40,
        0,0,148,9,1,0,0,0,149,150,5,20,0,0,150,152,5,71,0,0,151,153,3,12,
        6,0,152,151,1,0,0,0,152,153,1,0,0,0,153,156,1,0,0,0,154,155,5,4,
        0,0,155,157,3,70,35,0,156,154,1,0,0,0,156,157,1,0,0,0,157,158,1,
        0,0,0,158,159,3,4,2,0,159,160,3,24,12,0,160,161,5,16,0,0,161,162,
        5,20,0,0,162,11,1,0,0,0,163,165,5,66,0,0,164,166,3,14,7,0,165,164,
        1,0,0,0,165,166,1,0,0,0,166,167,1,0,0,0,167,168,5,67,0,0,168,13,
        1,0,0,0,169,174,3,16,8,0,170,171,5,68,0,0,171,173,3,16,8,0,172,170,
        1,0,0,0,173,176,1,0,0,0,174,172,1,0,0,0,174,175,1,0,0,0,175,15,1,
        0,0,0,176,174,1,0,0,0,177,179,7,1,0,0,178,177,1,0,0,0,178,179,1,
        0,0,0,179,180,1,0,0,0,180,183,5,71,0,0,181,182,5,4,0,0,182,184,3,
        70,35,0,183,181,1,0,0,0,183,184,1,0,0,0,184,17,1,0,0,0,185,187,3,
        20,10,0,186,185,1,0,0,0,186,187,1,0,0,0,187,188,1,0,0,0,188,189,
        3,22,11,0,189,19,1,0,0,0,190,191,5,51,0,0,191,21,1,0,0,0,192,209,
        3,28,14,0,193,209,3,30,15,0,194,209,3,40,20,0,195,209,3,44,22,0,
        196,209,3,32,16,0,197,209,3,46,23,0,198,209,3,48,24,0,199,209,3,
        50,25,0,200,209,3,52,26,0,201,209,3,54,27,0,202,209,3,56,28,0,203,
        209,3,60,30,0,204,209,3,62,31,0,205,209,3,64,32,0,206,209,3,66,33,
        0,207,209,3,68,34,0,208,192,1,0,0,0,208,193,1,0,0,0,208,194,1,0,
        0,0,208,195,1,0,0,0,208,196,1,0,0,0,208,197,1,0,0,0,208,198,1,0,
        0,0,208,199,1,0,0,0,208,200,1,0,0,0,208,201,1,0,0,0,208,202,1,0,
        0,0,208,203,1,0,0,0,208,204,1,0,0,0,208,205,1,0,0,0,208,206,1,0,
        0,0,208,207,1,0,0,0,209,23,1,0,0,0,210,212,3,18,9,0,211,213,3,4,
        2,0,212,211,1,0,0,0,213,214,1,0,0,0,214,212,1,0,0,0,214,215,1,0,
        0,0,215,217,1,0,0,0,216,210,1,0,0,0,217,220,1,0,0,0,218,216,1,0,
        0,0,218,219,1,0,0,0,219,25,1,0,0,0,220,218,1,0,0,0,221,233,3,28,
        14,0,222,233,3,30,15,0,223,233,3,40,20,0,224,233,3,44,22,0,225,233,
        3,32,16,0,226,233,3,54,27,0,227,233,3,56,28,0,228,233,3,60,30,0,
        229,233,3,62,31,0,230,233,3,64,32,0,231,233,3,68,34,0,232,221,1,
        0,0,0,232,222,1,0,0,0,232,223,1,0,0,0,232,224,1,0,0,0,232,225,1,
        0,0,0,232,226,1,0,0,0,232,227,1,0,0,0,232,228,1,0,0,0,232,229,1,
        0,0,0,232,230,1,0,0,0,232,231,1,0,0,0,233,27,1,0,0,0,234,236,5,27,
        0,0,235,234,1,0,0,0,235,236,1,0,0,0,236,237,1,0,0,0,237,238,3,38,
        19,0,238,239,5,56,0,0,239,240,3,72,36,0,240,29,1,0,0,0,241,242,5,
        9,0,0,242,245,5,71,0,0,243,244,5,4,0,0,244,246,3,70,35,0,245,243,
        1,0,0,0,245,246,1,0,0,0,246,247,1,0,0,0,247,248,5,56,0,0,248,249,
        3,72,36,0,249,31,1,0,0,0,250,251,5,10,0,0,251,256,3,34,17,0,252,
        253,5,68,0,0,253,255,3,34,17,0,254,252,1,0,0,0,255,258,1,0,0,0,256,
        254,1,0,0,0,256,257,1,0,0,0,257,33,1,0,0,0,258,256,1,0,0,0,259,261,
        5,71,0,0,260,262,3,36,18,0,261,260,1,0,0,0,261,262,1,0,0,0,262,265,
        1,0,0,0,263,264,5,4,0,0,264,266,3,70,35,0,265,263,1,0,0,0,265,266,
        1,0,0,0,266,269,1,0,0,0,267,268,5,56,0,0,268,270,3,72,36,0,269,267,
        1,0,0,0,269,270,1,0,0,0,270,35,1,0,0,0,271,272,5,66,0,0,272,277,
        3,72,36,0,273,274,5,68,0,0,274,276,3,72,36,0,275,273,1,0,0,0,276,
        279,1,0,0,0,277,275,1,0,0,0,277,278,1,0,0,0,278,280,1,0,0,0,279,
        277,1,0,0,0,280,281,5,67,0,0,281,37,1,0,0,0,282,287,5,71,0,0,283,
        284,5,66,0,0,284,285,3,94,47,0,285,286,5,67,0,0,286,288,1,0,0,0,
        287,283,1,0,0,0,287,288,1,0,0,0,288,39,1,0,0,0,289,291,5,34,0,0,
        290,292,3,42,21,0,291,290,1,0,0,0,291,292,1,0,0,0,292,41,1,0,0,0,
        293,298,3,72,36,0,294,295,7,2,0,0,295,297,3,72,36,0,296,294,1,0,
        0,0,297,300,1,0,0,0,298,296,1,0,0,0,298,299,1,0,0,0,299,302,1,0,
        0,0,300,298,1,0,0,0,301,303,7,2,0,0,302,301,1,0,0,0,302,303,1,0,
        0,0,303,43,1,0,0,0,304,307,5,24,0,0,305,306,5,52,0,0,306,308,5,68,
        0,0,307,305,1,0,0,0,307,308,1,0,0,0,308,309,1,0,0,0,309,314,3,38,
        19,0,310,311,5,68,0,0,311,313,3,38,19,0,312,310,1,0,0,0,313,316,
        1,0,0,0,314,312,1,0,0,0,314,315,1,0,0,0,315,45,1,0,0,0,316,314,1,
        0,0,0,317,318,5,23,0,0,318,319,3,72,36,0,319,320,5,41,0,0,320,323,
        3,26,13,0,321,322,5,14,0,0,322,324,3,26,13,0,323,321,1,0,0,0,323,
        324,1,0,0,0,324,351,1,0,0,0,325,326,5,23,0,0,326,327,3,72,36,0,327,
        328,5,41,0,0,328,329,3,4,2,0,329,338,3,24,12,0,330,331,5,15,0,0,
        331,332,3,72,36,0,332,333,5,41,0,0,333,334,3,4,2,0,334,335,3,24,
        12,0,335,337,1,0,0,0,336,330,1,0,0,0,337,340,1,0,0,0,338,336,1,0,
        0,0,338,339,1,0,0,0,339,345,1,0,0,0,340,338,1,0,0,0,341,342,5,14,
        0,0,342,343,3,4,2,0,343,344,3,24,12,0,344,346,1,0,0,0,345,341,1,
        0,0,0,345,346,1,0,0,0,346,347,1,0,0,0,347,348,5,16,0,0,348,349,5,
        23,0,0,349,351,1,0,0,0,350,317,1,0,0,0,350,325,1,0,0,0,351,47,1,
        0,0,0,352,353,5,19,0,0,353,354,3,38,19,0,354,355,5,56,0,0,355,356,
        3,72,36,0,356,357,7,3,0,0,357,360,3,72,36,0,358,359,5,37,0,0,359,
        361,3,72,36,0,360,358,1,0,0,0,360,361,1,0,0,0,361,362,1,0,0,0,362,
        363,3,4,2,0,363,364,3,24,12,0,364,366,5,31,0,0,365,367,5,71,0,0,
        366,365,1,0,0,0,366,367,1,0,0,0,367,49,1,0,0,0,368,369,5,46,0,0,
        369,370,3,72,36,0,370,371,3,4,2,0,371,375,3,24,12,0,372,376,5,45,
        0,0,373,374,5,16,0,0,374,376,5,46,0,0,375,372,1,0,0,0,375,373,1,
        0,0,0,376,51,1,0,0,0,377,378,5,11,0,0,378,379,5,46,0,0,379,380,3,
        72,36,0,380,381,3,4,2,0,381,382,3,24,12,0,382,383,5,29,0,0,383,411,
        1,0,0,0,384,385,5,11,0,0,385,386,5,44,0,0,386,387,3,72,36,0,387,
        388,3,4,2,0,388,389,3,24,12,0,389,390,5,29,0,0,390,411,1,0,0,0,391,
        392,5,11,0,0,392,393,3,4,2,0,393,394,3,24,12,0,394,395,5,29,0,0,
        395,396,5,46,0,0,396,397,3,72,36,0,397,411,1,0,0,0,398,399,5,11,
        0,0,399,400,3,4,2,0,400,401,3,24,12,0,401,402,5,29,0,0,402,403,5,
        44,0,0,403,404,3,72,36,0,404,411,1,0,0,0,405,406,5,11,0,0,406,407,
        3,4,2,0,407,408,3,24,12,0,408,409,5,29,0,0,409,411,1,0,0,0,410,377,
        1,0,0,0,410,384,1,0,0,0,410,391,1,0,0,0,410,398,1,0,0,0,410,405,
        1,0,0,0,411,53,1,0,0,0,412,413,5,22,0,0,413,414,3,58,29,0,414,55,
        1,0,0,0,415,416,5,21,0,0,416,417,3,58,29,0,417,57,1,0,0,0,418,419,
        7,4,0,0,419,59,1,0,0,0,420,422,5,35,0,0,421,423,3,72,36,0,422,421,
        1,0,0,0,422,423,1,0,0,0,423,61,1,0,0,0,424,425,5,8,0,0,425,431,5,
        71,0,0,426,428,5,66,0,0,427,429,3,94,47,0,428,427,1,0,0,0,428,429,
        1,0,0,0,429,430,1,0,0,0,430,432,5,67,0,0,431,426,1,0,0,0,431,432,
        1,0,0,0,432,63,1,0,0,0,433,435,5,17,0,0,434,436,7,5,0,0,435,434,
        1,0,0,0,435,436,1,0,0,0,436,65,1,0,0,0,437,438,5,26,0,0,438,439,
        5,71,0,0,439,67,1,0,0,0,440,441,5,38,0,0,441,69,1,0,0,0,442,443,
        7,6,0,0,443,71,1,0,0,0,444,445,3,74,37,0,445,73,1,0,0,0,446,451,
        3,76,38,0,447,448,5,33,0,0,448,450,3,76,38,0,449,447,1,0,0,0,450,
        453,1,0,0,0,451,449,1,0,0,0,451,452,1,0,0,0,452,75,1,0,0,0,453,451,
        1,0,0,0,454,459,3,78,39,0,455,456,5,47,0,0,456,458,3,78,39,0,457,
        455,1,0,0,0,458,461,1,0,0,0,459,457,1,0,0,0,459,460,1,0,0,0,460,
        77,1,0,0,0,461,459,1,0,0,0,462,467,3,80,40,0,463,464,5,3,0,0,464,
        466,3,80,40,0,465,463,1,0,0,0,466,469,1,0,0,0,467,465,1,0,0,0,467,
        468,1,0,0,0,468,79,1,0,0,0,469,467,1,0,0,0,470,471,5,32,0,0,471,
        474,3,80,40,0,472,474,3,82,41,0,473,470,1,0,0,0,473,472,1,0,0,0,
        474,81,1,0,0,0,475,478,3,84,42,0,476,477,7,7,0,0,477,479,3,84,42,
        0,478,476,1,0,0,0,478,479,1,0,0,0,479,83,1,0,0,0,480,485,3,86,43,
        0,481,482,7,8,0,0,482,484,3,86,43,0,483,481,1,0,0,0,484,487,1,0,
        0,0,485,483,1,0,0,0,485,486,1,0,0,0,486,85,1,0,0,0,487,485,1,0,0,
        0,488,493,3,88,44,0,489,490,7,9,0,0,490,492,3,88,44,0,491,489,1,
        0,0,0,492,495,1,0,0,0,493,491,1,0,0,0,493,494,1,0,0,0,494,87,1,0,
        0,0,495,493,1,0,0,0,496,499,3,90,45,0,497,498,5,64,0,0,498,500,3,
        88,44,0,499,497,1,0,0,0,499,500,1,0,0,0,500,89,1,0,0,0,501,502,7,
        10,0,0,502,505,3,90,45,0,503,505,3,92,46,0,504,501,1,0,0,0,504,503,
        1,0,0,0,505,91,1,0,0,0,506,519,3,96,48,0,507,508,5,71,0,0,508,510,
        5,66,0,0,509,511,3,94,47,0,510,509,1,0,0,0,510,511,1,0,0,0,511,512,
        1,0,0,0,512,519,5,67,0,0,513,519,5,71,0,0,514,515,5,66,0,0,515,516,
        3,72,36,0,516,517,5,67,0,0,517,519,1,0,0,0,518,506,1,0,0,0,518,507,
        1,0,0,0,518,513,1,0,0,0,518,514,1,0,0,0,519,93,1,0,0,0,520,525,3,
        72,36,0,521,522,5,68,0,0,522,524,3,72,36,0,523,521,1,0,0,0,524,527,
        1,0,0,0,525,523,1,0,0,0,525,526,1,0,0,0,526,95,1,0,0,0,527,525,1,
        0,0,0,528,529,7,11,0,0,529,97,1,0,0,0,56,101,105,110,116,122,130,
        135,142,152,156,165,174,178,183,186,208,214,218,232,235,245,256,
        261,265,269,277,287,291,298,302,307,314,323,338,345,350,360,366,
        375,410,422,428,431,435,451,459,467,473,478,485,493,499,504,510,
        518,525
    ]

class BasicParser ( Parser ):

    grammarFileName = "BasicParser.g4"

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
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'<='", "'>='", "<INVALID>", "'='", "'<'", 
                     "'>'", "'+'", "'-'", "'*'", "'/'", "'\\'", "'^'", "'&'", 
                     "'('", "')'", "','", "';'", "':'" ]

    symbolicNames = [ "<INVALID>", "REM_COMMENT", "APOSTROPHE_COMMENT", 
                      "AND", "AS", "BOOLEAN", "BYREF", "BYVAL", "CALL", 
                      "CONST", "DIM", "DO", "DOUBLE", "DOWNTO", "ELSE", 
                      "ELSEIF", "END", "EXIT", "FALSE", "FOR", "FUNCTION", 
                      "GOSUB", "GOTO", "IF", "INPUT", "INTEGER_KW", "LABEL", 
                      "LET", "LONG", "LOOP", "MOD", "NEXT", "NOT", "OR", 
                      "PRINT", "RETURN", "SINGLE", "STEP", "STOP", "STRING_KW", 
                      "SUB", "THEN", "TO", "TRUE", "UNTIL", "WEND", "WHILE", 
                      "XOR", "HEX_LITERAL", "BINARY_LITERAL", "FLOAT_LITERAL", 
                      "INTEGER_LITERAL", "STRING_LITERAL", "LE", "GE", "NE", 
                      "EQ", "LT", "GT", "PLUS", "MINUS", "STAR", "SLASH", 
                      "INTDIV", "CARET", "AMP", "LPAREN", "RPAREN", "COMMA", 
                      "SEMI", "COLON", "IDENT", "NEWLINE", "WS" ]

    RULE_program = 0
    RULE_topLevelItem = 1
    RULE_separators = 2
    RULE_separator = 3
    RULE_subDeclaration = 4
    RULE_functionDeclaration = 5
    RULE_parameterList = 6
    RULE_parameterDeclList = 7
    RULE_parameterDecl = 8
    RULE_statement = 9
    RULE_lineNumber = 10
    RULE_statementCore = 11
    RULE_statementBlock = 12
    RULE_inlineStatement = 13
    RULE_assignmentStatement = 14
    RULE_constStatement = 15
    RULE_dimStatement = 16
    RULE_variableDecl = 17
    RULE_arrayBounds = 18
    RULE_lvalue = 19
    RULE_printStatement = 20
    RULE_printList = 21
    RULE_inputStatement = 22
    RULE_ifStatement = 23
    RULE_forStatement = 24
    RULE_whileStatement = 25
    RULE_doLoopStatement = 26
    RULE_gotoStatement = 27
    RULE_gosubStatement = 28
    RULE_jumpTarget = 29
    RULE_returnStatement = 30
    RULE_callStatement = 31
    RULE_exitStatement = 32
    RULE_labelStatement = 33
    RULE_stopStatement = 34
    RULE_typeName = 35
    RULE_expression = 36
    RULE_orExpression = 37
    RULE_xorExpression = 38
    RULE_andExpression = 39
    RULE_notExpression = 40
    RULE_comparisonExpression = 41
    RULE_additiveExpression = 42
    RULE_multiplicativeExpression = 43
    RULE_powerExpression = 44
    RULE_unaryExpression = 45
    RULE_primaryExpression = 46
    RULE_argumentList = 47
    RULE_literal = 48

    ruleNames =  [ "program", "topLevelItem", "separators", "separator", 
                   "subDeclaration", "functionDeclaration", "parameterList", 
                   "parameterDeclList", "parameterDecl", "statement", "lineNumber", 
                   "statementCore", "statementBlock", "inlineStatement", 
                   "assignmentStatement", "constStatement", "dimStatement", 
                   "variableDecl", "arrayBounds", "lvalue", "printStatement", 
                   "printList", "inputStatement", "ifStatement", "forStatement", 
                   "whileStatement", "doLoopStatement", "gotoStatement", 
                   "gosubStatement", "jumpTarget", "returnStatement", "callStatement", 
                   "exitStatement", "labelStatement", "stopStatement", "typeName", 
                   "expression", "orExpression", "xorExpression", "andExpression", 
                   "notExpression", "comparisonExpression", "additiveExpression", 
                   "multiplicativeExpression", "powerExpression", "unaryExpression", 
                   "primaryExpression", "argumentList", "literal" ]

    EOF = Token.EOF
    REM_COMMENT=1
    APOSTROPHE_COMMENT=2
    AND=3
    AS=4
    BOOLEAN=5
    BYREF=6
    BYVAL=7
    CALL=8
    CONST=9
    DIM=10
    DO=11
    DOUBLE=12
    DOWNTO=13
    ELSE=14
    ELSEIF=15
    END=16
    EXIT=17
    FALSE=18
    FOR=19
    FUNCTION=20
    GOSUB=21
    GOTO=22
    IF=23
    INPUT=24
    INTEGER_KW=25
    LABEL=26
    LET=27
    LONG=28
    LOOP=29
    MOD=30
    NEXT=31
    NOT=32
    OR=33
    PRINT=34
    RETURN=35
    SINGLE=36
    STEP=37
    STOP=38
    STRING_KW=39
    SUB=40
    THEN=41
    TO=42
    TRUE=43
    UNTIL=44
    WEND=45
    WHILE=46
    XOR=47
    HEX_LITERAL=48
    BINARY_LITERAL=49
    FLOAT_LITERAL=50
    INTEGER_LITERAL=51
    STRING_LITERAL=52
    LE=53
    GE=54
    NE=55
    EQ=56
    LT=57
    GT=58
    PLUS=59
    MINUS=60
    STAR=61
    SLASH=62
    INTDIV=63
    CARET=64
    AMP=65
    LPAREN=66
    RPAREN=67
    COMMA=68
    SEMI=69
    COLON=70
    IDENT=71
    NEWLINE=72
    WS=73

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(BasicParser.EOF, 0)

        def separators(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.SeparatorsContext)
            else:
                return self.getTypedRuleContext(BasicParser.SeparatorsContext,i)


        def topLevelItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.TopLevelItemContext)
            else:
                return self.getTypedRuleContext(BasicParser.TopLevelItemContext,i)


        def getRuleIndex(self):
            return BasicParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = BasicParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 98
                    self.separators() 
                self.state = 103
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 105
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 8)) & ~0x3f) == 0 and ((1 << (_la - 8)) & -9223362960312894961) != 0):
                self.state = 104
                self.topLevelItem()


            self.state = 116
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 108 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while True:
                        self.state = 107
                        self.separators()
                        self.state = 110 
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if not (_la==70 or _la==72):
                            break

                    self.state = 112
                    self.topLevelItem() 
                self.state = 118
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

            self.state = 122
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==70 or _la==72:
                self.state = 119
                self.separators()
                self.state = 124
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 125
            self.match(BasicParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TopLevelItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subDeclaration(self):
            return self.getTypedRuleContext(BasicParser.SubDeclarationContext,0)


        def functionDeclaration(self):
            return self.getTypedRuleContext(BasicParser.FunctionDeclarationContext,0)


        def statement(self):
            return self.getTypedRuleContext(BasicParser.StatementContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_topLevelItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTopLevelItem" ):
                listener.enterTopLevelItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTopLevelItem" ):
                listener.exitTopLevelItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTopLevelItem" ):
                return visitor.visitTopLevelItem(self)
            else:
                return visitor.visitChildren(self)




    def topLevelItem(self):

        localctx = BasicParser.TopLevelItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_topLevelItem)
        try:
            self.state = 130
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [40]:
                self.enterOuterAlt(localctx, 1)
                self.state = 127
                self.subDeclaration()
                pass
            elif token in [20]:
                self.enterOuterAlt(localctx, 2)
                self.state = 128
                self.functionDeclaration()
                pass
            elif token in [8, 9, 10, 11, 17, 19, 21, 22, 23, 24, 26, 27, 34, 35, 38, 46, 51, 71]:
                self.enterOuterAlt(localctx, 3)
                self.state = 129
                self.statement()
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


    class SeparatorsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def separator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.SeparatorContext)
            else:
                return self.getTypedRuleContext(BasicParser.SeparatorContext,i)


        def getRuleIndex(self):
            return BasicParser.RULE_separators

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSeparators" ):
                listener.enterSeparators(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSeparators" ):
                listener.exitSeparators(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSeparators" ):
                return visitor.visitSeparators(self)
            else:
                return visitor.visitChildren(self)




    def separators(self):

        localctx = BasicParser.SeparatorsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_separators)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 133 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 132
                    self.separator()

                else:
                    raise NoViableAltException(self)
                self.state = 135 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SeparatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NEWLINE(self):
            return self.getToken(BasicParser.NEWLINE, 0)

        def COLON(self):
            return self.getToken(BasicParser.COLON, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_separator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSeparator" ):
                listener.enterSeparator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSeparator" ):
                listener.exitSeparator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSeparator" ):
                return visitor.visitSeparator(self)
            else:
                return visitor.visitChildren(self)




    def separator(self):

        localctx = BasicParser.SeparatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_separator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            _la = self._input.LA(1)
            if not(_la==70 or _la==72):
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


    class SubDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SUB(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.SUB)
            else:
                return self.getToken(BasicParser.SUB, i)

        def IDENT(self):
            return self.getToken(BasicParser.IDENT, 0)

        def separators(self):
            return self.getTypedRuleContext(BasicParser.SeparatorsContext,0)


        def statementBlock(self):
            return self.getTypedRuleContext(BasicParser.StatementBlockContext,0)


        def END(self):
            return self.getToken(BasicParser.END, 0)

        def parameterList(self):
            return self.getTypedRuleContext(BasicParser.ParameterListContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_subDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubDeclaration" ):
                listener.enterSubDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubDeclaration" ):
                listener.exitSubDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubDeclaration" ):
                return visitor.visitSubDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def subDeclaration(self):

        localctx = BasicParser.SubDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_subDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            self.match(BasicParser.SUB)
            self.state = 140
            self.match(BasicParser.IDENT)
            self.state = 142
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==66:
                self.state = 141
                self.parameterList()


            self.state = 144
            self.separators()
            self.state = 145
            self.statementBlock()
            self.state = 146
            self.match(BasicParser.END)
            self.state = 147
            self.match(BasicParser.SUB)
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

        def FUNCTION(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.FUNCTION)
            else:
                return self.getToken(BasicParser.FUNCTION, i)

        def IDENT(self):
            return self.getToken(BasicParser.IDENT, 0)

        def separators(self):
            return self.getTypedRuleContext(BasicParser.SeparatorsContext,0)


        def statementBlock(self):
            return self.getTypedRuleContext(BasicParser.StatementBlockContext,0)


        def END(self):
            return self.getToken(BasicParser.END, 0)

        def parameterList(self):
            return self.getTypedRuleContext(BasicParser.ParameterListContext,0)


        def AS(self):
            return self.getToken(BasicParser.AS, 0)

        def typeName(self):
            return self.getTypedRuleContext(BasicParser.TypeNameContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_functionDeclaration

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

        localctx = BasicParser.FunctionDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_functionDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 149
            self.match(BasicParser.FUNCTION)
            self.state = 150
            self.match(BasicParser.IDENT)
            self.state = 152
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==66:
                self.state = 151
                self.parameterList()


            self.state = 156
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 154
                self.match(BasicParser.AS)
                self.state = 155
                self.typeName()


            self.state = 158
            self.separators()
            self.state = 159
            self.statementBlock()
            self.state = 160
            self.match(BasicParser.END)
            self.state = 161
            self.match(BasicParser.FUNCTION)
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
            return self.getToken(BasicParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(BasicParser.RPAREN, 0)

        def parameterDeclList(self):
            return self.getTypedRuleContext(BasicParser.ParameterDeclListContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_parameterList

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

        localctx = BasicParser.ParameterListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_parameterList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 163
            self.match(BasicParser.LPAREN)
            self.state = 165
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6 or _la==7 or _la==71:
                self.state = 164
                self.parameterDeclList()


            self.state = 167
            self.match(BasicParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParameterDeclListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parameterDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.ParameterDeclContext)
            else:
                return self.getTypedRuleContext(BasicParser.ParameterDeclContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.COMMA)
            else:
                return self.getToken(BasicParser.COMMA, i)

        def getRuleIndex(self):
            return BasicParser.RULE_parameterDeclList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameterDeclList" ):
                listener.enterParameterDeclList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameterDeclList" ):
                listener.exitParameterDeclList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameterDeclList" ):
                return visitor.visitParameterDeclList(self)
            else:
                return visitor.visitChildren(self)




    def parameterDeclList(self):

        localctx = BasicParser.ParameterDeclListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_parameterDeclList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 169
            self.parameterDecl()
            self.state = 174
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==68:
                self.state = 170
                self.match(BasicParser.COMMA)
                self.state = 171
                self.parameterDecl()
                self.state = 176
                self._errHandler.sync(self)
                _la = self._input.LA(1)

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

        def IDENT(self):
            return self.getToken(BasicParser.IDENT, 0)

        def AS(self):
            return self.getToken(BasicParser.AS, 0)

        def typeName(self):
            return self.getTypedRuleContext(BasicParser.TypeNameContext,0)


        def BYVAL(self):
            return self.getToken(BasicParser.BYVAL, 0)

        def BYREF(self):
            return self.getToken(BasicParser.BYREF, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_parameterDecl

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

        localctx = BasicParser.ParameterDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_parameterDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6 or _la==7:
                self.state = 177
                _la = self._input.LA(1)
                if not(_la==6 or _la==7):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 180
            self.match(BasicParser.IDENT)
            self.state = 183
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 181
                self.match(BasicParser.AS)
                self.state = 182
                self.typeName()


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

        def statementCore(self):
            return self.getTypedRuleContext(BasicParser.StatementCoreContext,0)


        def lineNumber(self):
            return self.getTypedRuleContext(BasicParser.LineNumberContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_statement

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

        localctx = BasicParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==51:
                self.state = 185
                self.lineNumber()


            self.state = 188
            self.statementCore()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LineNumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER_LITERAL(self):
            return self.getToken(BasicParser.INTEGER_LITERAL, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_lineNumber

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLineNumber" ):
                listener.enterLineNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLineNumber" ):
                listener.exitLineNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLineNumber" ):
                return visitor.visitLineNumber(self)
            else:
                return visitor.visitChildren(self)




    def lineNumber(self):

        localctx = BasicParser.LineNumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_lineNumber)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
            self.match(BasicParser.INTEGER_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementCoreContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignmentStatement(self):
            return self.getTypedRuleContext(BasicParser.AssignmentStatementContext,0)


        def constStatement(self):
            return self.getTypedRuleContext(BasicParser.ConstStatementContext,0)


        def printStatement(self):
            return self.getTypedRuleContext(BasicParser.PrintStatementContext,0)


        def inputStatement(self):
            return self.getTypedRuleContext(BasicParser.InputStatementContext,0)


        def dimStatement(self):
            return self.getTypedRuleContext(BasicParser.DimStatementContext,0)


        def ifStatement(self):
            return self.getTypedRuleContext(BasicParser.IfStatementContext,0)


        def forStatement(self):
            return self.getTypedRuleContext(BasicParser.ForStatementContext,0)


        def whileStatement(self):
            return self.getTypedRuleContext(BasicParser.WhileStatementContext,0)


        def doLoopStatement(self):
            return self.getTypedRuleContext(BasicParser.DoLoopStatementContext,0)


        def gotoStatement(self):
            return self.getTypedRuleContext(BasicParser.GotoStatementContext,0)


        def gosubStatement(self):
            return self.getTypedRuleContext(BasicParser.GosubStatementContext,0)


        def returnStatement(self):
            return self.getTypedRuleContext(BasicParser.ReturnStatementContext,0)


        def callStatement(self):
            return self.getTypedRuleContext(BasicParser.CallStatementContext,0)


        def exitStatement(self):
            return self.getTypedRuleContext(BasicParser.ExitStatementContext,0)


        def labelStatement(self):
            return self.getTypedRuleContext(BasicParser.LabelStatementContext,0)


        def stopStatement(self):
            return self.getTypedRuleContext(BasicParser.StopStatementContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_statementCore

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatementCore" ):
                listener.enterStatementCore(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatementCore" ):
                listener.exitStatementCore(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatementCore" ):
                return visitor.visitStatementCore(self)
            else:
                return visitor.visitChildren(self)




    def statementCore(self):

        localctx = BasicParser.StatementCoreContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_statementCore)
        try:
            self.state = 208
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27, 71]:
                self.enterOuterAlt(localctx, 1)
                self.state = 192
                self.assignmentStatement()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 2)
                self.state = 193
                self.constStatement()
                pass
            elif token in [34]:
                self.enterOuterAlt(localctx, 3)
                self.state = 194
                self.printStatement()
                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 4)
                self.state = 195
                self.inputStatement()
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 5)
                self.state = 196
                self.dimStatement()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 6)
                self.state = 197
                self.ifStatement()
                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 7)
                self.state = 198
                self.forStatement()
                pass
            elif token in [46]:
                self.enterOuterAlt(localctx, 8)
                self.state = 199
                self.whileStatement()
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 9)
                self.state = 200
                self.doLoopStatement()
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 10)
                self.state = 201
                self.gotoStatement()
                pass
            elif token in [21]:
                self.enterOuterAlt(localctx, 11)
                self.state = 202
                self.gosubStatement()
                pass
            elif token in [35]:
                self.enterOuterAlt(localctx, 12)
                self.state = 203
                self.returnStatement()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 13)
                self.state = 204
                self.callStatement()
                pass
            elif token in [17]:
                self.enterOuterAlt(localctx, 14)
                self.state = 205
                self.exitStatement()
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 15)
                self.state = 206
                self.labelStatement()
                pass
            elif token in [38]:
                self.enterOuterAlt(localctx, 16)
                self.state = 207
                self.stopStatement()
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


    class StatementBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.StatementContext)
            else:
                return self.getTypedRuleContext(BasicParser.StatementContext,i)


        def separators(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.SeparatorsContext)
            else:
                return self.getTypedRuleContext(BasicParser.SeparatorsContext,i)


        def getRuleIndex(self):
            return BasicParser.RULE_statementBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatementBlock" ):
                listener.enterStatementBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatementBlock" ):
                listener.exitStatementBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatementBlock" ):
                return visitor.visitStatementBlock(self)
            else:
                return visitor.visitChildren(self)




    def statementBlock(self):

        localctx = BasicParser.StatementBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_statementBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 218
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 8)) & ~0x3f) == 0 and ((1 << (_la - 8)) & -9223362964607866353) != 0):
                self.state = 210
                self.statement()
                self.state = 212 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 211
                    self.separators()
                    self.state = 214 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==70 or _la==72):
                        break

                self.state = 220
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InlineStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignmentStatement(self):
            return self.getTypedRuleContext(BasicParser.AssignmentStatementContext,0)


        def constStatement(self):
            return self.getTypedRuleContext(BasicParser.ConstStatementContext,0)


        def printStatement(self):
            return self.getTypedRuleContext(BasicParser.PrintStatementContext,0)


        def inputStatement(self):
            return self.getTypedRuleContext(BasicParser.InputStatementContext,0)


        def dimStatement(self):
            return self.getTypedRuleContext(BasicParser.DimStatementContext,0)


        def gotoStatement(self):
            return self.getTypedRuleContext(BasicParser.GotoStatementContext,0)


        def gosubStatement(self):
            return self.getTypedRuleContext(BasicParser.GosubStatementContext,0)


        def returnStatement(self):
            return self.getTypedRuleContext(BasicParser.ReturnStatementContext,0)


        def callStatement(self):
            return self.getTypedRuleContext(BasicParser.CallStatementContext,0)


        def exitStatement(self):
            return self.getTypedRuleContext(BasicParser.ExitStatementContext,0)


        def stopStatement(self):
            return self.getTypedRuleContext(BasicParser.StopStatementContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_inlineStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInlineStatement" ):
                listener.enterInlineStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInlineStatement" ):
                listener.exitInlineStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInlineStatement" ):
                return visitor.visitInlineStatement(self)
            else:
                return visitor.visitChildren(self)




    def inlineStatement(self):

        localctx = BasicParser.InlineStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_inlineStatement)
        try:
            self.state = 232
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27, 71]:
                self.enterOuterAlt(localctx, 1)
                self.state = 221
                self.assignmentStatement()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 2)
                self.state = 222
                self.constStatement()
                pass
            elif token in [34]:
                self.enterOuterAlt(localctx, 3)
                self.state = 223
                self.printStatement()
                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 4)
                self.state = 224
                self.inputStatement()
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 5)
                self.state = 225
                self.dimStatement()
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 6)
                self.state = 226
                self.gotoStatement()
                pass
            elif token in [21]:
                self.enterOuterAlt(localctx, 7)
                self.state = 227
                self.gosubStatement()
                pass
            elif token in [35]:
                self.enterOuterAlt(localctx, 8)
                self.state = 228
                self.returnStatement()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 9)
                self.state = 229
                self.callStatement()
                pass
            elif token in [17]:
                self.enterOuterAlt(localctx, 10)
                self.state = 230
                self.exitStatement()
                pass
            elif token in [38]:
                self.enterOuterAlt(localctx, 11)
                self.state = 231
                self.stopStatement()
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


    class AssignmentStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lvalue(self):
            return self.getTypedRuleContext(BasicParser.LvalueContext,0)


        def EQ(self):
            return self.getToken(BasicParser.EQ, 0)

        def expression(self):
            return self.getTypedRuleContext(BasicParser.ExpressionContext,0)


        def LET(self):
            return self.getToken(BasicParser.LET, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_assignmentStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignmentStatement" ):
                listener.enterAssignmentStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignmentStatement" ):
                listener.exitAssignmentStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignmentStatement" ):
                return visitor.visitAssignmentStatement(self)
            else:
                return visitor.visitChildren(self)




    def assignmentStatement(self):

        localctx = BasicParser.AssignmentStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_assignmentStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 235
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==27:
                self.state = 234
                self.match(BasicParser.LET)


            self.state = 237
            self.lvalue()
            self.state = 238
            self.match(BasicParser.EQ)
            self.state = 239
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONST(self):
            return self.getToken(BasicParser.CONST, 0)

        def IDENT(self):
            return self.getToken(BasicParser.IDENT, 0)

        def EQ(self):
            return self.getToken(BasicParser.EQ, 0)

        def expression(self):
            return self.getTypedRuleContext(BasicParser.ExpressionContext,0)


        def AS(self):
            return self.getToken(BasicParser.AS, 0)

        def typeName(self):
            return self.getTypedRuleContext(BasicParser.TypeNameContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_constStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstStatement" ):
                listener.enterConstStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstStatement" ):
                listener.exitConstStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstStatement" ):
                return visitor.visitConstStatement(self)
            else:
                return visitor.visitChildren(self)




    def constStatement(self):

        localctx = BasicParser.ConstStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_constStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 241
            self.match(BasicParser.CONST)
            self.state = 242
            self.match(BasicParser.IDENT)
            self.state = 245
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 243
                self.match(BasicParser.AS)
                self.state = 244
                self.typeName()


            self.state = 247
            self.match(BasicParser.EQ)
            self.state = 248
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DimStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DIM(self):
            return self.getToken(BasicParser.DIM, 0)

        def variableDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.VariableDeclContext)
            else:
                return self.getTypedRuleContext(BasicParser.VariableDeclContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.COMMA)
            else:
                return self.getToken(BasicParser.COMMA, i)

        def getRuleIndex(self):
            return BasicParser.RULE_dimStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDimStatement" ):
                listener.enterDimStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDimStatement" ):
                listener.exitDimStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDimStatement" ):
                return visitor.visitDimStatement(self)
            else:
                return visitor.visitChildren(self)




    def dimStatement(self):

        localctx = BasicParser.DimStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_dimStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 250
            self.match(BasicParser.DIM)
            self.state = 251
            self.variableDecl()
            self.state = 256
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==68:
                self.state = 252
                self.match(BasicParser.COMMA)
                self.state = 253
                self.variableDecl()
                self.state = 258
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(BasicParser.IDENT, 0)

        def arrayBounds(self):
            return self.getTypedRuleContext(BasicParser.ArrayBoundsContext,0)


        def AS(self):
            return self.getToken(BasicParser.AS, 0)

        def typeName(self):
            return self.getTypedRuleContext(BasicParser.TypeNameContext,0)


        def EQ(self):
            return self.getToken(BasicParser.EQ, 0)

        def expression(self):
            return self.getTypedRuleContext(BasicParser.ExpressionContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_variableDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariableDecl" ):
                listener.enterVariableDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariableDecl" ):
                listener.exitVariableDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableDecl" ):
                return visitor.visitVariableDecl(self)
            else:
                return visitor.visitChildren(self)




    def variableDecl(self):

        localctx = BasicParser.VariableDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_variableDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 259
            self.match(BasicParser.IDENT)
            self.state = 261
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==66:
                self.state = 260
                self.arrayBounds()


            self.state = 265
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 263
                self.match(BasicParser.AS)
                self.state = 264
                self.typeName()


            self.state = 269
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==56:
                self.state = 267
                self.match(BasicParser.EQ)
                self.state = 268
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayBoundsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(BasicParser.LPAREN, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(BasicParser.ExpressionContext,i)


        def RPAREN(self):
            return self.getToken(BasicParser.RPAREN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.COMMA)
            else:
                return self.getToken(BasicParser.COMMA, i)

        def getRuleIndex(self):
            return BasicParser.RULE_arrayBounds

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayBounds" ):
                listener.enterArrayBounds(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayBounds" ):
                listener.exitArrayBounds(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayBounds" ):
                return visitor.visitArrayBounds(self)
            else:
                return visitor.visitChildren(self)




    def arrayBounds(self):

        localctx = BasicParser.ArrayBoundsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_arrayBounds)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 271
            self.match(BasicParser.LPAREN)
            self.state = 272
            self.expression()
            self.state = 277
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==68:
                self.state = 273
                self.match(BasicParser.COMMA)
                self.state = 274
                self.expression()
                self.state = 279
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 280
            self.match(BasicParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LvalueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(BasicParser.IDENT, 0)

        def LPAREN(self):
            return self.getToken(BasicParser.LPAREN, 0)

        def argumentList(self):
            return self.getTypedRuleContext(BasicParser.ArgumentListContext,0)


        def RPAREN(self):
            return self.getToken(BasicParser.RPAREN, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_lvalue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLvalue" ):
                listener.enterLvalue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLvalue" ):
                listener.exitLvalue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLvalue" ):
                return visitor.visitLvalue(self)
            else:
                return visitor.visitChildren(self)




    def lvalue(self):

        localctx = BasicParser.LvalueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_lvalue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 282
            self.match(BasicParser.IDENT)
            self.state = 287
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==66:
                self.state = 283
                self.match(BasicParser.LPAREN)
                self.state = 284
                self.argumentList()
                self.state = 285
                self.match(BasicParser.RPAREN)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PRINT(self):
            return self.getToken(BasicParser.PRINT, 0)

        def printList(self):
            return self.getTypedRuleContext(BasicParser.PrintListContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_printStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrintStatement" ):
                listener.enterPrintStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrintStatement" ):
                listener.exitPrintStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintStatement" ):
                return visitor.visitPrintStatement(self)
            else:
                return visitor.visitChildren(self)




    def printStatement(self):

        localctx = BasicParser.PrintStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_printStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 289
            self.match(BasicParser.PRINT)
            self.state = 291
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 18)) & ~0x3f) == 0 and ((1 << (_la - 18)) & 9295304620785665) != 0):
                self.state = 290
                self.printList()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(BasicParser.ExpressionContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.COMMA)
            else:
                return self.getToken(BasicParser.COMMA, i)

        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.SEMI)
            else:
                return self.getToken(BasicParser.SEMI, i)

        def getRuleIndex(self):
            return BasicParser.RULE_printList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrintList" ):
                listener.enterPrintList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrintList" ):
                listener.exitPrintList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintList" ):
                return visitor.visitPrintList(self)
            else:
                return visitor.visitChildren(self)




    def printList(self):

        localctx = BasicParser.PrintListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_printList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 293
            self.expression()
            self.state = 298
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,28,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 294
                    _la = self._input.LA(1)
                    if not(_la==68 or _la==69):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 295
                    self.expression() 
                self.state = 300
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,28,self._ctx)

            self.state = 302
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==68 or _la==69:
                self.state = 301
                _la = self._input.LA(1)
                if not(_la==68 or _la==69):
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


    class InputStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INPUT(self):
            return self.getToken(BasicParser.INPUT, 0)

        def lvalue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.LvalueContext)
            else:
                return self.getTypedRuleContext(BasicParser.LvalueContext,i)


        def STRING_LITERAL(self):
            return self.getToken(BasicParser.STRING_LITERAL, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.COMMA)
            else:
                return self.getToken(BasicParser.COMMA, i)

        def getRuleIndex(self):
            return BasicParser.RULE_inputStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInputStatement" ):
                listener.enterInputStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInputStatement" ):
                listener.exitInputStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInputStatement" ):
                return visitor.visitInputStatement(self)
            else:
                return visitor.visitChildren(self)




    def inputStatement(self):

        localctx = BasicParser.InputStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_inputStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 304
            self.match(BasicParser.INPUT)
            self.state = 307
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 305
                self.match(BasicParser.STRING_LITERAL)
                self.state = 306
                self.match(BasicParser.COMMA)


            self.state = 309
            self.lvalue()
            self.state = 314
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==68:
                self.state = 310
                self.match(BasicParser.COMMA)
                self.state = 311
                self.lvalue()
                self.state = 316
                self._errHandler.sync(self)
                _la = self._input.LA(1)

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


        def getRuleIndex(self):
            return BasicParser.RULE_ifStatement

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class BlockIfContext(IfStatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BasicParser.IfStatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IF(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.IF)
            else:
                return self.getToken(BasicParser.IF, i)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(BasicParser.ExpressionContext,i)

        def THEN(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.THEN)
            else:
                return self.getToken(BasicParser.THEN, i)
        def separators(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.SeparatorsContext)
            else:
                return self.getTypedRuleContext(BasicParser.SeparatorsContext,i)

        def statementBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.StatementBlockContext)
            else:
                return self.getTypedRuleContext(BasicParser.StatementBlockContext,i)

        def END(self):
            return self.getToken(BasicParser.END, 0)
        def ELSEIF(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.ELSEIF)
            else:
                return self.getToken(BasicParser.ELSEIF, i)
        def ELSE(self):
            return self.getToken(BasicParser.ELSE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlockIf" ):
                listener.enterBlockIf(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlockIf" ):
                listener.exitBlockIf(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlockIf" ):
                return visitor.visitBlockIf(self)
            else:
                return visitor.visitChildren(self)


    class InlineIfContext(IfStatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BasicParser.IfStatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IF(self):
            return self.getToken(BasicParser.IF, 0)
        def expression(self):
            return self.getTypedRuleContext(BasicParser.ExpressionContext,0)

        def THEN(self):
            return self.getToken(BasicParser.THEN, 0)
        def inlineStatement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.InlineStatementContext)
            else:
                return self.getTypedRuleContext(BasicParser.InlineStatementContext,i)

        def ELSE(self):
            return self.getToken(BasicParser.ELSE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInlineIf" ):
                listener.enterInlineIf(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInlineIf" ):
                listener.exitInlineIf(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInlineIf" ):
                return visitor.visitInlineIf(self)
            else:
                return visitor.visitChildren(self)



    def ifStatement(self):

        localctx = BasicParser.IfStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_ifStatement)
        self._la = 0 # Token type
        try:
            self.state = 350
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,35,self._ctx)
            if la_ == 1:
                localctx = BasicParser.InlineIfContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 317
                self.match(BasicParser.IF)
                self.state = 318
                self.expression()
                self.state = 319
                self.match(BasicParser.THEN)
                self.state = 320
                self.inlineStatement()
                self.state = 323
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==14:
                    self.state = 321
                    self.match(BasicParser.ELSE)
                    self.state = 322
                    self.inlineStatement()


                pass

            elif la_ == 2:
                localctx = BasicParser.BlockIfContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 325
                self.match(BasicParser.IF)
                self.state = 326
                self.expression()
                self.state = 327
                self.match(BasicParser.THEN)
                self.state = 328
                self.separators()
                self.state = 329
                self.statementBlock()
                self.state = 338
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==15:
                    self.state = 330
                    self.match(BasicParser.ELSEIF)
                    self.state = 331
                    self.expression()
                    self.state = 332
                    self.match(BasicParser.THEN)
                    self.state = 333
                    self.separators()
                    self.state = 334
                    self.statementBlock()
                    self.state = 340
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 345
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==14:
                    self.state = 341
                    self.match(BasicParser.ELSE)
                    self.state = 342
                    self.separators()
                    self.state = 343
                    self.statementBlock()


                self.state = 347
                self.match(BasicParser.END)
                self.state = 348
                self.match(BasicParser.IF)
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
            return self.getToken(BasicParser.FOR, 0)

        def lvalue(self):
            return self.getTypedRuleContext(BasicParser.LvalueContext,0)


        def EQ(self):
            return self.getToken(BasicParser.EQ, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(BasicParser.ExpressionContext,i)


        def separators(self):
            return self.getTypedRuleContext(BasicParser.SeparatorsContext,0)


        def statementBlock(self):
            return self.getTypedRuleContext(BasicParser.StatementBlockContext,0)


        def NEXT(self):
            return self.getToken(BasicParser.NEXT, 0)

        def TO(self):
            return self.getToken(BasicParser.TO, 0)

        def DOWNTO(self):
            return self.getToken(BasicParser.DOWNTO, 0)

        def STEP(self):
            return self.getToken(BasicParser.STEP, 0)

        def IDENT(self):
            return self.getToken(BasicParser.IDENT, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_forStatement

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

        localctx = BasicParser.ForStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 352
            self.match(BasicParser.FOR)
            self.state = 353
            self.lvalue()
            self.state = 354
            self.match(BasicParser.EQ)
            self.state = 355
            self.expression()
            self.state = 356
            _la = self._input.LA(1)
            if not(_la==13 or _la==42):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 357
            self.expression()
            self.state = 360
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==37:
                self.state = 358
                self.match(BasicParser.STEP)
                self.state = 359
                self.expression()


            self.state = 362
            self.separators()
            self.state = 363
            self.statementBlock()
            self.state = 364
            self.match(BasicParser.NEXT)
            self.state = 366
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==71:
                self.state = 365
                self.match(BasicParser.IDENT)


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

        def WHILE(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.WHILE)
            else:
                return self.getToken(BasicParser.WHILE, i)

        def expression(self):
            return self.getTypedRuleContext(BasicParser.ExpressionContext,0)


        def separators(self):
            return self.getTypedRuleContext(BasicParser.SeparatorsContext,0)


        def statementBlock(self):
            return self.getTypedRuleContext(BasicParser.StatementBlockContext,0)


        def WEND(self):
            return self.getToken(BasicParser.WEND, 0)

        def END(self):
            return self.getToken(BasicParser.END, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_whileStatement

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

        localctx = BasicParser.WhileStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 368
            self.match(BasicParser.WHILE)
            self.state = 369
            self.expression()
            self.state = 370
            self.separators()
            self.state = 371
            self.statementBlock()
            self.state = 375
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [45]:
                self.state = 372
                self.match(BasicParser.WEND)
                pass
            elif token in [16]:
                self.state = 373
                self.match(BasicParser.END)
                self.state = 374
                self.match(BasicParser.WHILE)
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


    class DoLoopStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return BasicParser.RULE_doLoopStatement

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class DoWhilePreContext(DoLoopStatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BasicParser.DoLoopStatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DO(self):
            return self.getToken(BasicParser.DO, 0)
        def WHILE(self):
            return self.getToken(BasicParser.WHILE, 0)
        def expression(self):
            return self.getTypedRuleContext(BasicParser.ExpressionContext,0)

        def separators(self):
            return self.getTypedRuleContext(BasicParser.SeparatorsContext,0)

        def statementBlock(self):
            return self.getTypedRuleContext(BasicParser.StatementBlockContext,0)

        def LOOP(self):
            return self.getToken(BasicParser.LOOP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoWhilePre" ):
                listener.enterDoWhilePre(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoWhilePre" ):
                listener.exitDoWhilePre(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoWhilePre" ):
                return visitor.visitDoWhilePre(self)
            else:
                return visitor.visitChildren(self)


    class DoUntilPreContext(DoLoopStatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BasicParser.DoLoopStatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DO(self):
            return self.getToken(BasicParser.DO, 0)
        def UNTIL(self):
            return self.getToken(BasicParser.UNTIL, 0)
        def expression(self):
            return self.getTypedRuleContext(BasicParser.ExpressionContext,0)

        def separators(self):
            return self.getTypedRuleContext(BasicParser.SeparatorsContext,0)

        def statementBlock(self):
            return self.getTypedRuleContext(BasicParser.StatementBlockContext,0)

        def LOOP(self):
            return self.getToken(BasicParser.LOOP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoUntilPre" ):
                listener.enterDoUntilPre(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoUntilPre" ):
                listener.exitDoUntilPre(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoUntilPre" ):
                return visitor.visitDoUntilPre(self)
            else:
                return visitor.visitChildren(self)


    class DoUntilPostContext(DoLoopStatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BasicParser.DoLoopStatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DO(self):
            return self.getToken(BasicParser.DO, 0)
        def separators(self):
            return self.getTypedRuleContext(BasicParser.SeparatorsContext,0)

        def statementBlock(self):
            return self.getTypedRuleContext(BasicParser.StatementBlockContext,0)

        def LOOP(self):
            return self.getToken(BasicParser.LOOP, 0)
        def UNTIL(self):
            return self.getToken(BasicParser.UNTIL, 0)
        def expression(self):
            return self.getTypedRuleContext(BasicParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoUntilPost" ):
                listener.enterDoUntilPost(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoUntilPost" ):
                listener.exitDoUntilPost(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoUntilPost" ):
                return visitor.visitDoUntilPost(self)
            else:
                return visitor.visitChildren(self)


    class DoWhilePostContext(DoLoopStatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BasicParser.DoLoopStatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DO(self):
            return self.getToken(BasicParser.DO, 0)
        def separators(self):
            return self.getTypedRuleContext(BasicParser.SeparatorsContext,0)

        def statementBlock(self):
            return self.getTypedRuleContext(BasicParser.StatementBlockContext,0)

        def LOOP(self):
            return self.getToken(BasicParser.LOOP, 0)
        def WHILE(self):
            return self.getToken(BasicParser.WHILE, 0)
        def expression(self):
            return self.getTypedRuleContext(BasicParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoWhilePost" ):
                listener.enterDoWhilePost(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoWhilePost" ):
                listener.exitDoWhilePost(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoWhilePost" ):
                return visitor.visitDoWhilePost(self)
            else:
                return visitor.visitChildren(self)


    class DoForeverContext(DoLoopStatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BasicParser.DoLoopStatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DO(self):
            return self.getToken(BasicParser.DO, 0)
        def separators(self):
            return self.getTypedRuleContext(BasicParser.SeparatorsContext,0)

        def statementBlock(self):
            return self.getTypedRuleContext(BasicParser.StatementBlockContext,0)

        def LOOP(self):
            return self.getToken(BasicParser.LOOP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoForever" ):
                listener.enterDoForever(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoForever" ):
                listener.exitDoForever(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoForever" ):
                return visitor.visitDoForever(self)
            else:
                return visitor.visitChildren(self)



    def doLoopStatement(self):

        localctx = BasicParser.DoLoopStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_doLoopStatement)
        try:
            self.state = 410
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
            if la_ == 1:
                localctx = BasicParser.DoWhilePreContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 377
                self.match(BasicParser.DO)
                self.state = 378
                self.match(BasicParser.WHILE)
                self.state = 379
                self.expression()
                self.state = 380
                self.separators()
                self.state = 381
                self.statementBlock()
                self.state = 382
                self.match(BasicParser.LOOP)
                pass

            elif la_ == 2:
                localctx = BasicParser.DoUntilPreContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 384
                self.match(BasicParser.DO)
                self.state = 385
                self.match(BasicParser.UNTIL)
                self.state = 386
                self.expression()
                self.state = 387
                self.separators()
                self.state = 388
                self.statementBlock()
                self.state = 389
                self.match(BasicParser.LOOP)
                pass

            elif la_ == 3:
                localctx = BasicParser.DoWhilePostContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 391
                self.match(BasicParser.DO)
                self.state = 392
                self.separators()
                self.state = 393
                self.statementBlock()
                self.state = 394
                self.match(BasicParser.LOOP)
                self.state = 395
                self.match(BasicParser.WHILE)
                self.state = 396
                self.expression()
                pass

            elif la_ == 4:
                localctx = BasicParser.DoUntilPostContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 398
                self.match(BasicParser.DO)
                self.state = 399
                self.separators()
                self.state = 400
                self.statementBlock()
                self.state = 401
                self.match(BasicParser.LOOP)
                self.state = 402
                self.match(BasicParser.UNTIL)
                self.state = 403
                self.expression()
                pass

            elif la_ == 5:
                localctx = BasicParser.DoForeverContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 405
                self.match(BasicParser.DO)
                self.state = 406
                self.separators()
                self.state = 407
                self.statementBlock()
                self.state = 408
                self.match(BasicParser.LOOP)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GotoStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GOTO(self):
            return self.getToken(BasicParser.GOTO, 0)

        def jumpTarget(self):
            return self.getTypedRuleContext(BasicParser.JumpTargetContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_gotoStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGotoStatement" ):
                listener.enterGotoStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGotoStatement" ):
                listener.exitGotoStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGotoStatement" ):
                return visitor.visitGotoStatement(self)
            else:
                return visitor.visitChildren(self)




    def gotoStatement(self):

        localctx = BasicParser.GotoStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_gotoStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 412
            self.match(BasicParser.GOTO)
            self.state = 413
            self.jumpTarget()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GosubStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GOSUB(self):
            return self.getToken(BasicParser.GOSUB, 0)

        def jumpTarget(self):
            return self.getTypedRuleContext(BasicParser.JumpTargetContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_gosubStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGosubStatement" ):
                listener.enterGosubStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGosubStatement" ):
                listener.exitGosubStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGosubStatement" ):
                return visitor.visitGosubStatement(self)
            else:
                return visitor.visitChildren(self)




    def gosubStatement(self):

        localctx = BasicParser.GosubStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_gosubStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 415
            self.match(BasicParser.GOSUB)
            self.state = 416
            self.jumpTarget()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JumpTargetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER_LITERAL(self):
            return self.getToken(BasicParser.INTEGER_LITERAL, 0)

        def IDENT(self):
            return self.getToken(BasicParser.IDENT, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_jumpTarget

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJumpTarget" ):
                listener.enterJumpTarget(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJumpTarget" ):
                listener.exitJumpTarget(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJumpTarget" ):
                return visitor.visitJumpTarget(self)
            else:
                return visitor.visitChildren(self)




    def jumpTarget(self):

        localctx = BasicParser.JumpTargetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_jumpTarget)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 418
            _la = self._input.LA(1)
            if not(_la==51 or _la==71):
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


    class ReturnStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(BasicParser.RETURN, 0)

        def expression(self):
            return self.getTypedRuleContext(BasicParser.ExpressionContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_returnStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStatement" ):
                listener.enterReturnStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStatement" ):
                listener.exitReturnStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStatement" ):
                return visitor.visitReturnStatement(self)
            else:
                return visitor.visitChildren(self)




    def returnStatement(self):

        localctx = BasicParser.ReturnStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_returnStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 420
            self.match(BasicParser.RETURN)
            self.state = 422
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 18)) & ~0x3f) == 0 and ((1 << (_la - 18)) & 9295304620785665) != 0):
                self.state = 421
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CallStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CALL(self):
            return self.getToken(BasicParser.CALL, 0)

        def IDENT(self):
            return self.getToken(BasicParser.IDENT, 0)

        def LPAREN(self):
            return self.getToken(BasicParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(BasicParser.RPAREN, 0)

        def argumentList(self):
            return self.getTypedRuleContext(BasicParser.ArgumentListContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_callStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCallStatement" ):
                listener.enterCallStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCallStatement" ):
                listener.exitCallStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCallStatement" ):
                return visitor.visitCallStatement(self)
            else:
                return visitor.visitChildren(self)




    def callStatement(self):

        localctx = BasicParser.CallStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_callStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 424
            self.match(BasicParser.CALL)
            self.state = 425
            self.match(BasicParser.IDENT)
            self.state = 431
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==66:
                self.state = 426
                self.match(BasicParser.LPAREN)
                self.state = 428
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 18)) & ~0x3f) == 0 and ((1 << (_la - 18)) & 9295304620785665) != 0):
                    self.state = 427
                    self.argumentList()


                self.state = 430
                self.match(BasicParser.RPAREN)


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
            return self.getToken(BasicParser.EXIT, 0)

        def FOR(self):
            return self.getToken(BasicParser.FOR, 0)

        def DO(self):
            return self.getToken(BasicParser.DO, 0)

        def WHILE(self):
            return self.getToken(BasicParser.WHILE, 0)

        def SUB(self):
            return self.getToken(BasicParser.SUB, 0)

        def FUNCTION(self):
            return self.getToken(BasicParser.FUNCTION, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_exitStatement

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

        localctx = BasicParser.ExitStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_exitStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 433
            self.match(BasicParser.EXIT)
            self.state = 435
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 71468257380352) != 0):
                self.state = 434
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 71468257380352) != 0)):
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


    class LabelStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LABEL(self):
            return self.getToken(BasicParser.LABEL, 0)

        def IDENT(self):
            return self.getToken(BasicParser.IDENT, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_labelStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLabelStatement" ):
                listener.enterLabelStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLabelStatement" ):
                listener.exitLabelStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLabelStatement" ):
                return visitor.visitLabelStatement(self)
            else:
                return visitor.visitChildren(self)




    def labelStatement(self):

        localctx = BasicParser.LabelStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_labelStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 437
            self.match(BasicParser.LABEL)
            self.state = 438
            self.match(BasicParser.IDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StopStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STOP(self):
            return self.getToken(BasicParser.STOP, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_stopStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStopStatement" ):
                listener.enterStopStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStopStatement" ):
                listener.exitStopStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStopStatement" ):
                return visitor.visitStopStatement(self)
            else:
                return visitor.visitChildren(self)




    def stopStatement(self):

        localctx = BasicParser.StopStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_stopStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 440
            self.match(BasicParser.STOP)
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

        def BOOLEAN(self):
            return self.getToken(BasicParser.BOOLEAN, 0)

        def INTEGER_KW(self):
            return self.getToken(BasicParser.INTEGER_KW, 0)

        def LONG(self):
            return self.getToken(BasicParser.LONG, 0)

        def SINGLE(self):
            return self.getToken(BasicParser.SINGLE, 0)

        def DOUBLE(self):
            return self.getToken(BasicParser.DOUBLE, 0)

        def STRING_KW(self):
            return self.getToken(BasicParser.STRING_KW, 0)

        def IDENT(self):
            return self.getToken(BasicParser.IDENT, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_typeName

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

        localctx = BasicParser.TypeNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_typeName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 442
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 618777284640) != 0) or _la==71):
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


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def orExpression(self):
            return self.getTypedRuleContext(BasicParser.OrExpressionContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = BasicParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 444
            self.orExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def xorExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.XorExpressionContext)
            else:
                return self.getTypedRuleContext(BasicParser.XorExpressionContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.OR)
            else:
                return self.getToken(BasicParser.OR, i)

        def getRuleIndex(self):
            return BasicParser.RULE_orExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrExpression" ):
                listener.enterOrExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrExpression" ):
                listener.exitOrExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpression" ):
                return visitor.visitOrExpression(self)
            else:
                return visitor.visitChildren(self)




    def orExpression(self):

        localctx = BasicParser.OrExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_orExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 446
            self.xorExpression()
            self.state = 451
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33:
                self.state = 447
                self.match(BasicParser.OR)
                self.state = 448
                self.xorExpression()
                self.state = 453
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class XorExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def andExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.AndExpressionContext)
            else:
                return self.getTypedRuleContext(BasicParser.AndExpressionContext,i)


        def XOR(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.XOR)
            else:
                return self.getToken(BasicParser.XOR, i)

        def getRuleIndex(self):
            return BasicParser.RULE_xorExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterXorExpression" ):
                listener.enterXorExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitXorExpression" ):
                listener.exitXorExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitXorExpression" ):
                return visitor.visitXorExpression(self)
            else:
                return visitor.visitChildren(self)




    def xorExpression(self):

        localctx = BasicParser.XorExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_xorExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 454
            self.andExpression()
            self.state = 459
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==47:
                self.state = 455
                self.match(BasicParser.XOR)
                self.state = 456
                self.andExpression()
                self.state = 461
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AndExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def notExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.NotExpressionContext)
            else:
                return self.getTypedRuleContext(BasicParser.NotExpressionContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.AND)
            else:
                return self.getToken(BasicParser.AND, i)

        def getRuleIndex(self):
            return BasicParser.RULE_andExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndExpression" ):
                listener.enterAndExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndExpression" ):
                listener.exitAndExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpression" ):
                return visitor.visitAndExpression(self)
            else:
                return visitor.visitChildren(self)




    def andExpression(self):

        localctx = BasicParser.AndExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_andExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 462
            self.notExpression()
            self.state = 467
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3:
                self.state = 463
                self.match(BasicParser.AND)
                self.state = 464
                self.notExpression()
                self.state = 469
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NotExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NOT(self):
            return self.getToken(BasicParser.NOT, 0)

        def notExpression(self):
            return self.getTypedRuleContext(BasicParser.NotExpressionContext,0)


        def comparisonExpression(self):
            return self.getTypedRuleContext(BasicParser.ComparisonExpressionContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_notExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNotExpression" ):
                listener.enterNotExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNotExpression" ):
                listener.exitNotExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNotExpression" ):
                return visitor.visitNotExpression(self)
            else:
                return visitor.visitChildren(self)




    def notExpression(self):

        localctx = BasicParser.NotExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_notExpression)
        try:
            self.state = 473
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [32]:
                self.enterOuterAlt(localctx, 1)
                self.state = 470
                self.match(BasicParser.NOT)
                self.state = 471
                self.notExpression()
                pass
            elif token in [18, 43, 48, 49, 50, 51, 52, 59, 60, 66, 71]:
                self.enterOuterAlt(localctx, 2)
                self.state = 472
                self.comparisonExpression()
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


    class ComparisonExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def additiveExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.AdditiveExpressionContext)
            else:
                return self.getTypedRuleContext(BasicParser.AdditiveExpressionContext,i)


        def EQ(self):
            return self.getToken(BasicParser.EQ, 0)

        def NE(self):
            return self.getToken(BasicParser.NE, 0)

        def LT(self):
            return self.getToken(BasicParser.LT, 0)

        def LE(self):
            return self.getToken(BasicParser.LE, 0)

        def GT(self):
            return self.getToken(BasicParser.GT, 0)

        def GE(self):
            return self.getToken(BasicParser.GE, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_comparisonExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonExpression" ):
                listener.enterComparisonExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonExpression" ):
                listener.exitComparisonExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonExpression" ):
                return visitor.visitComparisonExpression(self)
            else:
                return visitor.visitChildren(self)




    def comparisonExpression(self):

        localctx = BasicParser.ComparisonExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_comparisonExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 475
            self.additiveExpression()
            self.state = 478
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 567453553048682496) != 0):
                self.state = 476
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 567453553048682496) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 477
                self.additiveExpression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multiplicativeExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.MultiplicativeExpressionContext)
            else:
                return self.getTypedRuleContext(BasicParser.MultiplicativeExpressionContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.PLUS)
            else:
                return self.getToken(BasicParser.PLUS, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.MINUS)
            else:
                return self.getToken(BasicParser.MINUS, i)

        def AMP(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.AMP)
            else:
                return self.getToken(BasicParser.AMP, i)

        def getRuleIndex(self):
            return BasicParser.RULE_additiveExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveExpression" ):
                listener.enterAdditiveExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveExpression" ):
                listener.exitAdditiveExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveExpression" ):
                return visitor.visitAdditiveExpression(self)
            else:
                return visitor.visitChildren(self)




    def additiveExpression(self):

        localctx = BasicParser.AdditiveExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_additiveExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 480
            self.multiplicativeExpression()
            self.state = 485
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 59)) & ~0x3f) == 0 and ((1 << (_la - 59)) & 67) != 0):
                self.state = 481
                _la = self._input.LA(1)
                if not(((((_la - 59)) & ~0x3f) == 0 and ((1 << (_la - 59)) & 67) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 482
                self.multiplicativeExpression()
                self.state = 487
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicativeExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def powerExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.PowerExpressionContext)
            else:
                return self.getTypedRuleContext(BasicParser.PowerExpressionContext,i)


        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.STAR)
            else:
                return self.getToken(BasicParser.STAR, i)

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.SLASH)
            else:
                return self.getToken(BasicParser.SLASH, i)

        def INTDIV(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.INTDIV)
            else:
                return self.getToken(BasicParser.INTDIV, i)

        def MOD(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.MOD)
            else:
                return self.getToken(BasicParser.MOD, i)

        def getRuleIndex(self):
            return BasicParser.RULE_multiplicativeExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeExpression" ):
                listener.enterMultiplicativeExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeExpression" ):
                listener.exitMultiplicativeExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeExpression" ):
                return visitor.visitMultiplicativeExpression(self)
            else:
                return visitor.visitChildren(self)




    def multiplicativeExpression(self):

        localctx = BasicParser.MultiplicativeExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_multiplicativeExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 488
            self.powerExpression()
            self.state = 493
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & -2305843008139952128) != 0):
                self.state = 489
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & -2305843008139952128) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 490
                self.powerExpression()
                self.state = 495
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PowerExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpression(self):
            return self.getTypedRuleContext(BasicParser.UnaryExpressionContext,0)


        def CARET(self):
            return self.getToken(BasicParser.CARET, 0)

        def powerExpression(self):
            return self.getTypedRuleContext(BasicParser.PowerExpressionContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_powerExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPowerExpression" ):
                listener.enterPowerExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPowerExpression" ):
                listener.exitPowerExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPowerExpression" ):
                return visitor.visitPowerExpression(self)
            else:
                return visitor.visitChildren(self)




    def powerExpression(self):

        localctx = BasicParser.PowerExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_powerExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 496
            self.unaryExpression()
            self.state = 499
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==64:
                self.state = 497
                self.match(BasicParser.CARET)
                self.state = 498
                self.powerExpression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpression(self):
            return self.getTypedRuleContext(BasicParser.UnaryExpressionContext,0)


        def PLUS(self):
            return self.getToken(BasicParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(BasicParser.MINUS, 0)

        def primaryExpression(self):
            return self.getTypedRuleContext(BasicParser.PrimaryExpressionContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_unaryExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryExpression" ):
                listener.enterUnaryExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryExpression" ):
                listener.exitUnaryExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryExpression" ):
                return visitor.visitUnaryExpression(self)
            else:
                return visitor.visitChildren(self)




    def unaryExpression(self):

        localctx = BasicParser.UnaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_unaryExpression)
        self._la = 0 # Token type
        try:
            self.state = 504
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [59, 60]:
                self.enterOuterAlt(localctx, 1)
                self.state = 501
                _la = self._input.LA(1)
                if not(_la==59 or _la==60):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 502
                self.unaryExpression()
                pass
            elif token in [18, 43, 48, 49, 50, 51, 52, 66, 71]:
                self.enterOuterAlt(localctx, 2)
                self.state = 503
                self.primaryExpression()
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


    class PrimaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literal(self):
            return self.getTypedRuleContext(BasicParser.LiteralContext,0)


        def IDENT(self):
            return self.getToken(BasicParser.IDENT, 0)

        def LPAREN(self):
            return self.getToken(BasicParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(BasicParser.RPAREN, 0)

        def argumentList(self):
            return self.getTypedRuleContext(BasicParser.ArgumentListContext,0)


        def expression(self):
            return self.getTypedRuleContext(BasicParser.ExpressionContext,0)


        def getRuleIndex(self):
            return BasicParser.RULE_primaryExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimaryExpression" ):
                listener.enterPrimaryExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimaryExpression" ):
                listener.exitPrimaryExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimaryExpression" ):
                return visitor.visitPrimaryExpression(self)
            else:
                return visitor.visitChildren(self)




    def primaryExpression(self):

        localctx = BasicParser.PrimaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_primaryExpression)
        self._la = 0 # Token type
        try:
            self.state = 518
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,54,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 506
                self.literal()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 507
                self.match(BasicParser.IDENT)
                self.state = 508
                self.match(BasicParser.LPAREN)
                self.state = 510
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 18)) & ~0x3f) == 0 and ((1 << (_la - 18)) & 9295304620785665) != 0):
                    self.state = 509
                    self.argumentList()


                self.state = 512
                self.match(BasicParser.RPAREN)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 513
                self.match(BasicParser.IDENT)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 514
                self.match(BasicParser.LPAREN)
                self.state = 515
                self.expression()
                self.state = 516
                self.match(BasicParser.RPAREN)
                pass


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

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BasicParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(BasicParser.ExpressionContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(BasicParser.COMMA)
            else:
                return self.getToken(BasicParser.COMMA, i)

        def getRuleIndex(self):
            return BasicParser.RULE_argumentList

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

        localctx = BasicParser.ArgumentListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 520
            self.expression()
            self.state = 525
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==68:
                self.state = 521
                self.match(BasicParser.COMMA)
                self.state = 522
                self.expression()
                self.state = 527
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER_LITERAL(self):
            return self.getToken(BasicParser.INTEGER_LITERAL, 0)

        def FLOAT_LITERAL(self):
            return self.getToken(BasicParser.FLOAT_LITERAL, 0)

        def HEX_LITERAL(self):
            return self.getToken(BasicParser.HEX_LITERAL, 0)

        def BINARY_LITERAL(self):
            return self.getToken(BasicParser.BINARY_LITERAL, 0)

        def STRING_LITERAL(self):
            return self.getToken(BasicParser.STRING_LITERAL, 0)

        def TRUE(self):
            return self.getToken(BasicParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(BasicParser.FALSE, 0)

        def getRuleIndex(self):
            return BasicParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)




    def literal(self):

        localctx = BasicParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_literal)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 528
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8734520371314688) != 0)):
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





