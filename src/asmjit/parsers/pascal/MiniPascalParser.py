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
        4,1,71,738,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,2,46,
        7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,2,52,7,52,
        2,53,7,53,2,54,7,54,2,55,7,55,2,56,7,56,2,57,7,57,2,58,7,58,2,59,
        7,59,2,60,7,60,2,61,7,61,2,62,7,62,2,63,7,63,2,64,7,64,2,65,7,65,
        2,66,7,66,2,67,7,67,2,68,7,68,2,69,7,69,2,70,7,70,2,71,7,71,2,72,
        7,72,2,73,7,73,2,74,7,74,1,0,1,0,1,0,1,0,5,0,155,8,0,10,0,12,0,158,
        9,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,3,1,169,8,1,1,2,1,2,1,2,
        1,2,1,2,3,2,176,8,2,1,2,1,2,1,2,3,2,181,8,2,1,2,1,2,1,2,1,2,1,2,
        3,2,188,8,2,1,2,1,2,1,2,3,2,193,8,2,3,2,195,8,2,1,3,1,3,4,3,199,
        8,3,11,3,12,3,200,1,4,1,4,1,4,5,4,206,8,4,10,4,12,4,209,9,4,1,4,
        1,4,1,5,1,5,1,5,1,5,1,6,1,6,1,7,1,7,4,7,221,8,7,11,7,12,7,222,1,
        8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,3,8,234,8,8,1,9,1,9,1,9,1,9,1,
        9,1,9,1,9,1,10,5,10,244,8,10,10,10,12,10,247,9,10,1,11,1,11,1,11,
        3,11,252,8,11,1,12,1,12,1,12,1,12,1,12,1,13,1,13,1,13,3,13,262,8,
        13,1,13,1,13,1,14,1,14,1,14,3,14,269,8,14,1,14,1,14,1,15,1,15,1,
        15,1,15,3,15,277,8,15,1,15,1,15,1,16,1,16,1,16,3,16,284,8,16,1,16,
        1,16,1,17,1,17,1,17,5,17,291,8,17,10,17,12,17,294,9,17,1,17,3,17,
        297,8,17,1,18,1,18,1,18,1,18,1,18,5,18,304,8,18,10,18,12,18,307,
        9,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,3,18,316,8,18,1,19,1,19,
        1,19,1,19,1,20,1,20,1,20,3,20,325,8,20,1,21,1,21,1,22,1,22,1,22,
        1,22,1,22,1,22,1,22,1,23,1,23,1,23,5,23,339,8,23,10,23,12,23,342,
        9,23,1,24,1,24,1,24,3,24,347,8,24,1,25,1,25,1,25,1,25,5,25,353,8,
        25,10,25,12,25,356,9,25,1,25,1,25,1,25,1,26,1,26,1,26,1,26,1,26,
        1,27,1,27,1,27,3,27,369,8,27,1,27,1,27,1,27,1,27,1,27,3,27,376,8,
        27,1,28,1,28,1,28,3,28,381,8,28,1,28,1,28,1,28,3,28,386,8,28,1,29,
        1,29,1,29,1,29,5,29,392,8,29,10,29,12,29,395,9,29,1,29,1,29,1,30,
        3,30,400,8,30,1,30,1,30,1,30,1,30,1,31,1,31,1,31,3,31,409,8,31,1,
        32,1,32,1,32,3,32,414,8,32,1,32,1,32,3,32,418,8,32,1,32,1,32,1,32,
        1,32,3,32,424,8,32,1,33,1,33,1,33,3,33,429,8,33,1,33,3,33,432,8,
        33,1,33,3,33,435,8,33,1,34,1,34,1,34,1,34,5,34,441,8,34,10,34,12,
        34,444,9,34,1,34,1,34,1,35,1,35,3,35,450,8,35,1,36,1,36,4,36,454,
        8,36,11,36,12,36,455,1,37,1,37,1,37,1,37,1,37,1,38,1,38,3,38,465,
        8,38,1,39,1,39,1,39,5,39,470,8,39,10,39,12,39,473,9,39,1,40,5,40,
        476,8,40,10,40,12,40,479,9,40,1,40,1,40,1,40,1,40,1,41,1,41,1,41,
        1,41,3,41,489,8,41,1,42,1,42,3,42,493,8,42,5,42,495,8,42,10,42,12,
        42,498,9,42,1,43,1,43,1,43,1,43,1,43,1,43,1,43,1,43,1,43,1,43,1,
        43,1,43,1,43,3,43,513,8,43,1,44,1,44,1,44,1,44,5,44,519,8,44,10,
        44,12,44,522,9,44,1,44,3,44,525,8,44,1,44,1,44,1,45,1,45,1,45,1,
        45,3,45,533,8,45,1,46,1,46,1,46,5,46,538,8,46,10,46,12,46,541,9,
        46,1,47,1,47,1,48,1,48,1,48,3,48,548,8,48,1,49,1,49,1,50,1,50,1,
        51,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,51,3,51,566,
        8,51,1,52,1,52,3,52,570,8,52,1,53,1,53,1,53,1,53,1,53,1,53,1,53,
        1,53,1,53,1,54,1,54,1,54,1,54,1,54,3,54,586,8,54,1,55,1,55,1,55,
        5,55,591,8,55,10,55,12,55,594,9,55,1,56,1,56,1,56,1,56,1,56,1,57,
        1,57,1,57,1,57,1,57,1,57,3,57,607,8,57,1,58,1,58,1,58,1,58,3,58,
        613,8,58,1,59,1,59,1,60,1,60,1,60,1,60,1,61,1,61,1,61,1,61,3,61,
        625,8,61,1,62,1,62,1,62,5,62,630,8,62,10,62,12,62,633,9,62,3,62,
        635,8,62,1,63,1,63,1,63,1,63,1,63,1,63,5,63,643,8,63,10,63,12,63,
        646,9,63,1,63,1,63,1,63,3,63,651,8,63,1,64,1,64,1,65,1,65,1,65,5,
        65,658,8,65,10,65,12,65,661,9,65,1,66,1,66,1,66,5,66,666,8,66,10,
        66,12,66,669,9,66,1,67,1,67,1,67,5,67,674,8,67,10,67,12,67,677,9,
        67,1,68,1,68,1,68,1,68,3,68,683,8,68,1,69,1,69,1,69,5,69,688,8,69,
        10,69,12,69,691,9,69,1,70,1,70,1,70,5,70,696,8,70,10,70,12,70,699,
        9,70,1,71,1,71,1,71,1,71,1,71,1,71,1,71,1,71,1,71,1,71,1,71,1,71,
        1,71,1,71,3,71,715,8,71,1,72,1,72,1,72,1,72,3,72,721,8,72,1,72,3,
        72,724,8,72,1,73,1,73,1,73,5,73,729,8,73,10,73,12,73,732,9,73,1,
        74,1,74,3,74,736,8,74,1,74,0,0,75,0,2,4,6,8,10,12,14,16,18,20,22,
        24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,
        68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,
        108,110,112,114,116,118,120,122,124,126,128,130,132,134,136,138,
        140,142,144,146,148,0,7,2,0,63,63,66,67,2,0,11,12,63,64,2,0,64,64,
        67,67,1,0,28,29,1,0,57,62,1,0,47,48,1,0,49,50,767,0,150,1,0,0,0,
        2,168,1,0,0,0,4,194,1,0,0,0,6,196,1,0,0,0,8,202,1,0,0,0,10,212,1,
        0,0,0,12,216,1,0,0,0,14,218,1,0,0,0,16,233,1,0,0,0,18,235,1,0,0,
        0,20,245,1,0,0,0,22,251,1,0,0,0,24,253,1,0,0,0,26,258,1,0,0,0,28,
        265,1,0,0,0,30,272,1,0,0,0,32,280,1,0,0,0,34,287,1,0,0,0,36,315,
        1,0,0,0,38,317,1,0,0,0,40,324,1,0,0,0,42,326,1,0,0,0,44,328,1,0,
        0,0,46,335,1,0,0,0,48,343,1,0,0,0,50,348,1,0,0,0,52,360,1,0,0,0,
        54,365,1,0,0,0,56,377,1,0,0,0,58,387,1,0,0,0,60,399,1,0,0,0,62,408,
        1,0,0,0,64,423,1,0,0,0,66,425,1,0,0,0,68,436,1,0,0,0,70,449,1,0,
        0,0,72,451,1,0,0,0,74,457,1,0,0,0,76,464,1,0,0,0,78,466,1,0,0,0,
        80,477,1,0,0,0,82,488,1,0,0,0,84,496,1,0,0,0,86,512,1,0,0,0,88,514,
        1,0,0,0,90,528,1,0,0,0,92,534,1,0,0,0,94,542,1,0,0,0,96,544,1,0,
        0,0,98,549,1,0,0,0,100,551,1,0,0,0,102,565,1,0,0,0,104,567,1,0,0,
        0,106,571,1,0,0,0,108,580,1,0,0,0,110,587,1,0,0,0,112,595,1,0,0,
        0,114,600,1,0,0,0,116,608,1,0,0,0,118,614,1,0,0,0,120,616,1,0,0,
        0,122,620,1,0,0,0,124,634,1,0,0,0,126,650,1,0,0,0,128,652,1,0,0,
        0,130,654,1,0,0,0,132,662,1,0,0,0,134,670,1,0,0,0,136,678,1,0,0,
        0,138,684,1,0,0,0,140,692,1,0,0,0,142,714,1,0,0,0,144,723,1,0,0,
        0,146,725,1,0,0,0,148,735,1,0,0,0,150,151,5,1,0,0,151,152,5,64,0,
        0,152,156,5,45,0,0,153,155,3,2,1,0,154,153,1,0,0,0,155,158,1,0,0,
        0,156,154,1,0,0,0,156,157,1,0,0,0,157,159,1,0,0,0,158,156,1,0,0,
        0,159,160,3,80,40,0,160,161,5,42,0,0,161,1,1,0,0,0,162,169,3,6,3,
        0,163,169,3,14,7,0,164,169,3,72,36,0,165,169,3,56,28,0,166,169,3,
        54,27,0,167,169,3,4,2,0,168,162,1,0,0,0,168,163,1,0,0,0,168,164,
        1,0,0,0,168,165,1,0,0,0,168,166,1,0,0,0,168,167,1,0,0,0,169,3,1,
        0,0,0,170,171,5,38,0,0,171,172,5,64,0,0,172,173,5,42,0,0,173,175,
        5,64,0,0,174,176,3,58,29,0,175,174,1,0,0,0,175,176,1,0,0,0,176,177,
        1,0,0,0,177,178,5,45,0,0,178,180,3,80,40,0,179,181,5,45,0,0,180,
        179,1,0,0,0,180,181,1,0,0,0,181,195,1,0,0,0,182,183,5,39,0,0,183,
        184,5,64,0,0,184,185,5,42,0,0,185,187,5,64,0,0,186,188,3,58,29,0,
        187,186,1,0,0,0,187,188,1,0,0,0,188,189,1,0,0,0,189,190,5,45,0,0,
        190,192,3,80,40,0,191,193,5,45,0,0,192,191,1,0,0,0,192,193,1,0,0,
        0,193,195,1,0,0,0,194,170,1,0,0,0,194,182,1,0,0,0,195,5,1,0,0,0,
        196,198,5,4,0,0,197,199,3,8,4,0,198,197,1,0,0,0,199,200,1,0,0,0,
        200,198,1,0,0,0,200,201,1,0,0,0,201,7,1,0,0,0,202,207,3,10,5,0,203,
        204,5,46,0,0,204,206,3,10,5,0,205,203,1,0,0,0,206,209,1,0,0,0,207,
        205,1,0,0,0,207,208,1,0,0,0,208,210,1,0,0,0,209,207,1,0,0,0,210,
        211,5,45,0,0,211,9,1,0,0,0,212,213,5,64,0,0,213,214,5,57,0,0,214,
        215,3,12,6,0,215,11,1,0,0,0,216,217,7,0,0,0,217,13,1,0,0,0,218,220,
        5,6,0,0,219,221,3,16,8,0,220,219,1,0,0,0,221,222,1,0,0,0,222,220,
        1,0,0,0,222,223,1,0,0,0,223,15,1,0,0,0,224,225,5,64,0,0,225,226,
        5,57,0,0,226,227,3,40,20,0,227,228,5,45,0,0,228,234,1,0,0,0,229,
        234,3,44,22,0,230,234,3,50,25,0,231,234,3,30,15,0,232,234,3,18,9,
        0,233,224,1,0,0,0,233,229,1,0,0,0,233,230,1,0,0,0,233,231,1,0,0,
        0,233,232,1,0,0,0,234,17,1,0,0,0,235,236,5,64,0,0,236,237,5,57,0,
        0,237,238,5,37,0,0,238,239,3,20,10,0,239,240,5,3,0,0,240,241,5,45,
        0,0,241,19,1,0,0,0,242,244,3,22,11,0,243,242,1,0,0,0,244,247,1,0,
        0,0,245,243,1,0,0,0,245,246,1,0,0,0,246,21,1,0,0,0,247,245,1,0,0,
        0,248,252,3,24,12,0,249,252,3,26,13,0,250,252,3,28,14,0,251,248,
        1,0,0,0,251,249,1,0,0,0,251,250,1,0,0,0,252,23,1,0,0,0,253,254,3,
        78,39,0,254,255,5,44,0,0,255,256,3,40,20,0,256,257,5,45,0,0,257,
        25,1,0,0,0,258,259,5,38,0,0,259,261,5,64,0,0,260,262,3,58,29,0,261,
        260,1,0,0,0,261,262,1,0,0,0,262,263,1,0,0,0,263,264,5,45,0,0,264,
        27,1,0,0,0,265,266,5,39,0,0,266,268,5,64,0,0,267,269,3,58,29,0,268,
        267,1,0,0,0,268,269,1,0,0,0,269,270,1,0,0,0,270,271,5,45,0,0,271,
        29,1,0,0,0,272,273,5,64,0,0,273,274,5,57,0,0,274,276,3,36,18,0,275,
        277,3,32,16,0,276,275,1,0,0,0,276,277,1,0,0,0,277,278,1,0,0,0,278,
        279,5,45,0,0,279,31,1,0,0,0,280,281,5,57,0,0,281,283,5,52,0,0,282,
        284,3,34,17,0,283,282,1,0,0,0,283,284,1,0,0,0,284,285,1,0,0,0,285,
        286,5,53,0,0,286,33,1,0,0,0,287,292,3,12,6,0,288,289,5,46,0,0,289,
        291,3,12,6,0,290,288,1,0,0,0,291,294,1,0,0,0,292,290,1,0,0,0,292,
        293,1,0,0,0,293,296,1,0,0,0,294,292,1,0,0,0,295,297,5,46,0,0,296,
        295,1,0,0,0,296,297,1,0,0,0,297,35,1,0,0,0,298,299,5,8,0,0,299,300,
        5,51,0,0,300,305,3,38,19,0,301,302,5,46,0,0,302,304,3,38,19,0,303,
        301,1,0,0,0,304,307,1,0,0,0,305,303,1,0,0,0,305,306,1,0,0,0,306,
        308,1,0,0,0,307,305,1,0,0,0,308,309,5,54,0,0,309,310,5,9,0,0,310,
        311,3,40,20,0,311,316,1,0,0,0,312,313,5,8,0,0,313,314,5,9,0,0,314,
        316,3,40,20,0,315,298,1,0,0,0,315,312,1,0,0,0,316,37,1,0,0,0,317,
        318,3,128,64,0,318,319,5,41,0,0,319,320,3,128,64,0,320,39,1,0,0,
        0,321,325,3,42,21,0,322,323,5,55,0,0,323,325,3,42,21,0,324,321,1,
        0,0,0,324,322,1,0,0,0,325,41,1,0,0,0,326,327,7,1,0,0,327,43,1,0,
        0,0,328,329,5,64,0,0,329,330,5,57,0,0,330,331,5,52,0,0,331,332,3,
        46,23,0,332,333,5,53,0,0,333,334,5,45,0,0,334,45,1,0,0,0,335,340,
        3,48,24,0,336,337,5,46,0,0,337,339,3,48,24,0,338,336,1,0,0,0,339,
        342,1,0,0,0,340,338,1,0,0,0,340,341,1,0,0,0,341,47,1,0,0,0,342,340,
        1,0,0,0,343,346,5,64,0,0,344,345,5,57,0,0,345,347,5,67,0,0,346,344,
        1,0,0,0,346,347,1,0,0,0,347,49,1,0,0,0,348,349,5,64,0,0,349,350,
        5,57,0,0,350,354,5,7,0,0,351,353,3,52,26,0,352,351,1,0,0,0,353,356,
        1,0,0,0,354,352,1,0,0,0,354,355,1,0,0,0,355,357,1,0,0,0,356,354,
        1,0,0,0,357,358,5,3,0,0,358,359,5,45,0,0,359,51,1,0,0,0,360,361,
        3,78,39,0,361,362,5,44,0,0,362,363,3,40,20,0,363,364,5,45,0,0,364,
        53,1,0,0,0,365,366,5,31,0,0,366,368,5,64,0,0,367,369,3,58,29,0,368,
        367,1,0,0,0,368,369,1,0,0,0,369,370,1,0,0,0,370,371,5,44,0,0,371,
        372,3,40,20,0,372,373,5,45,0,0,373,375,3,80,40,0,374,376,5,45,0,
        0,375,374,1,0,0,0,375,376,1,0,0,0,376,55,1,0,0,0,377,378,5,30,0,
        0,378,380,5,64,0,0,379,381,3,58,29,0,380,379,1,0,0,0,380,381,1,0,
        0,0,381,382,1,0,0,0,382,383,5,45,0,0,383,385,3,80,40,0,384,386,5,
        45,0,0,385,384,1,0,0,0,385,386,1,0,0,0,386,57,1,0,0,0,387,388,5,
        52,0,0,388,393,3,60,30,0,389,390,5,45,0,0,390,392,3,60,30,0,391,
        389,1,0,0,0,392,395,1,0,0,0,393,391,1,0,0,0,393,394,1,0,0,0,394,
        396,1,0,0,0,395,393,1,0,0,0,396,397,5,53,0,0,397,59,1,0,0,0,398,
        400,5,5,0,0,399,398,1,0,0,0,399,400,1,0,0,0,400,401,1,0,0,0,401,
        402,3,78,39,0,402,403,5,44,0,0,403,404,3,40,20,0,404,61,1,0,0,0,
        405,409,3,72,36,0,406,409,3,56,28,0,407,409,3,54,27,0,408,405,1,
        0,0,0,408,406,1,0,0,0,408,407,1,0,0,0,409,63,1,0,0,0,410,413,5,64,
        0,0,411,412,5,42,0,0,412,414,5,64,0,0,413,411,1,0,0,0,413,414,1,
        0,0,0,414,415,1,0,0,0,415,417,5,52,0,0,416,418,3,110,55,0,417,416,
        1,0,0,0,417,418,1,0,0,0,418,419,1,0,0,0,419,424,5,53,0,0,420,421,
        5,64,0,0,421,422,5,42,0,0,422,424,5,64,0,0,423,410,1,0,0,0,423,420,
        1,0,0,0,424,65,1,0,0,0,425,428,5,64,0,0,426,427,5,42,0,0,427,429,
        5,64,0,0,428,426,1,0,0,0,428,429,1,0,0,0,429,431,1,0,0,0,430,432,
        3,68,34,0,431,430,1,0,0,0,431,432,1,0,0,0,432,434,1,0,0,0,433,435,
        5,45,0,0,434,433,1,0,0,0,434,435,1,0,0,0,435,67,1,0,0,0,436,437,
        5,52,0,0,437,442,3,70,35,0,438,439,5,46,0,0,439,441,3,70,35,0,440,
        438,1,0,0,0,441,444,1,0,0,0,442,440,1,0,0,0,442,443,1,0,0,0,443,
        445,1,0,0,0,444,442,1,0,0,0,445,446,5,53,0,0,446,69,1,0,0,0,447,
        450,5,63,0,0,448,450,3,128,64,0,449,447,1,0,0,0,449,448,1,0,0,0,
        450,71,1,0,0,0,451,453,5,5,0,0,452,454,3,74,37,0,453,452,1,0,0,0,
        454,455,1,0,0,0,455,453,1,0,0,0,455,456,1,0,0,0,456,73,1,0,0,0,457,
        458,3,78,39,0,458,459,5,44,0,0,459,460,3,76,38,0,460,461,5,45,0,
        0,461,75,1,0,0,0,462,465,3,40,20,0,463,465,3,36,18,0,464,462,1,0,
        0,0,464,463,1,0,0,0,465,77,1,0,0,0,466,471,5,64,0,0,467,468,5,46,
        0,0,468,470,5,64,0,0,469,467,1,0,0,0,470,473,1,0,0,0,471,469,1,0,
        0,0,471,472,1,0,0,0,472,79,1,0,0,0,473,471,1,0,0,0,474,476,3,82,
        41,0,475,474,1,0,0,0,476,479,1,0,0,0,477,475,1,0,0,0,477,478,1,0,
        0,0,478,480,1,0,0,0,479,477,1,0,0,0,480,481,5,2,0,0,481,482,3,84,
        42,0,482,483,5,3,0,0,483,81,1,0,0,0,484,489,3,56,28,0,485,489,3,
        54,27,0,486,489,3,72,36,0,487,489,3,6,3,0,488,484,1,0,0,0,488,485,
        1,0,0,0,488,486,1,0,0,0,488,487,1,0,0,0,489,83,1,0,0,0,490,492,3,
        86,43,0,491,493,5,45,0,0,492,491,1,0,0,0,492,493,1,0,0,0,493,495,
        1,0,0,0,494,490,1,0,0,0,495,498,1,0,0,0,496,494,1,0,0,0,496,497,
        1,0,0,0,497,85,1,0,0,0,498,496,1,0,0,0,499,513,3,122,61,0,500,513,
        3,144,72,0,501,513,3,102,51,0,502,513,3,114,57,0,503,513,3,112,56,
        0,504,513,3,108,54,0,505,513,3,106,53,0,506,513,3,98,49,0,507,513,
        3,100,50,0,508,513,3,88,44,0,509,513,3,66,33,0,510,513,3,104,52,
        0,511,513,3,120,60,0,512,499,1,0,0,0,512,500,1,0,0,0,512,501,1,0,
        0,0,512,502,1,0,0,0,512,503,1,0,0,0,512,504,1,0,0,0,512,505,1,0,
        0,0,512,506,1,0,0,0,512,507,1,0,0,0,512,508,1,0,0,0,512,509,1,0,
        0,0,512,510,1,0,0,0,512,511,1,0,0,0,513,87,1,0,0,0,514,515,5,13,
        0,0,515,516,3,128,64,0,516,520,5,9,0,0,517,519,3,90,45,0,518,517,
        1,0,0,0,519,522,1,0,0,0,520,518,1,0,0,0,520,521,1,0,0,0,521,524,
        1,0,0,0,522,520,1,0,0,0,523,525,3,96,48,0,524,523,1,0,0,0,524,525,
        1,0,0,0,525,526,1,0,0,0,526,527,5,3,0,0,527,89,1,0,0,0,528,529,3,
        92,46,0,529,530,5,44,0,0,530,532,3,86,43,0,531,533,5,45,0,0,532,
        531,1,0,0,0,532,533,1,0,0,0,533,91,1,0,0,0,534,539,3,94,47,0,535,
        536,5,46,0,0,536,538,3,94,47,0,537,535,1,0,0,0,538,541,1,0,0,0,539,
        537,1,0,0,0,539,540,1,0,0,0,540,93,1,0,0,0,541,539,1,0,0,0,542,543,
        7,2,0,0,543,95,1,0,0,0,544,545,5,16,0,0,545,547,3,84,42,0,546,548,
        5,45,0,0,547,546,1,0,0,0,547,548,1,0,0,0,548,97,1,0,0,0,549,550,
        5,17,0,0,550,99,1,0,0,0,551,552,5,18,0,0,552,101,1,0,0,0,553,554,
        5,34,0,0,554,555,3,84,42,0,555,556,5,35,0,0,556,557,3,84,42,0,557,
        558,5,3,0,0,558,566,1,0,0,0,559,560,5,34,0,0,560,561,3,84,42,0,561,
        562,5,36,0,0,562,563,3,84,42,0,563,564,5,3,0,0,564,566,1,0,0,0,565,
        553,1,0,0,0,565,559,1,0,0,0,566,103,1,0,0,0,567,569,5,33,0,0,568,
        570,5,45,0,0,569,568,1,0,0,0,569,570,1,0,0,0,570,105,1,0,0,0,571,
        572,5,27,0,0,572,573,5,64,0,0,573,574,5,43,0,0,574,575,3,128,64,
        0,575,576,7,3,0,0,576,577,3,128,64,0,577,578,5,24,0,0,578,579,3,
        86,43,0,579,107,1,0,0,0,580,581,5,25,0,0,581,582,3,84,42,0,582,583,
        5,26,0,0,583,585,3,116,58,0,584,586,5,45,0,0,585,584,1,0,0,0,585,
        586,1,0,0,0,586,109,1,0,0,0,587,592,3,128,64,0,588,589,5,46,0,0,
        589,591,3,128,64,0,590,588,1,0,0,0,591,594,1,0,0,0,592,590,1,0,0,
        0,592,593,1,0,0,0,593,111,1,0,0,0,594,592,1,0,0,0,595,596,5,23,0,
        0,596,597,3,116,58,0,597,598,5,24,0,0,598,599,3,86,43,0,599,113,
        1,0,0,0,600,601,5,14,0,0,601,602,3,116,58,0,602,603,5,15,0,0,603,
        606,3,86,43,0,604,605,5,16,0,0,605,607,3,86,43,0,606,604,1,0,0,0,
        606,607,1,0,0,0,607,115,1,0,0,0,608,612,3,128,64,0,609,610,3,118,
        59,0,610,611,3,128,64,0,611,613,1,0,0,0,612,609,1,0,0,0,612,613,
        1,0,0,0,613,117,1,0,0,0,614,615,7,4,0,0,615,119,1,0,0,0,616,617,
        5,2,0,0,617,618,3,84,42,0,618,619,5,3,0,0,619,121,1,0,0,0,620,621,
        3,124,62,0,621,622,5,43,0,0,622,624,3,128,64,0,623,625,5,45,0,0,
        624,623,1,0,0,0,624,625,1,0,0,0,625,123,1,0,0,0,626,635,5,32,0,0,
        627,631,5,64,0,0,628,630,3,126,63,0,629,628,1,0,0,0,630,633,1,0,
        0,0,631,629,1,0,0,0,631,632,1,0,0,0,632,635,1,0,0,0,633,631,1,0,
        0,0,634,626,1,0,0,0,634,627,1,0,0,0,635,125,1,0,0,0,636,637,5,42,
        0,0,637,651,5,64,0,0,638,639,5,51,0,0,639,644,3,128,64,0,640,641,
        5,46,0,0,641,643,3,128,64,0,642,640,1,0,0,0,643,646,1,0,0,0,644,
        642,1,0,0,0,644,645,1,0,0,0,645,647,1,0,0,0,646,644,1,0,0,0,647,
        648,5,54,0,0,648,651,1,0,0,0,649,651,5,55,0,0,650,636,1,0,0,0,650,
        638,1,0,0,0,650,649,1,0,0,0,651,127,1,0,0,0,652,653,3,130,65,0,653,
        129,1,0,0,0,654,659,3,132,66,0,655,656,5,21,0,0,656,658,3,132,66,
        0,657,655,1,0,0,0,658,661,1,0,0,0,659,657,1,0,0,0,659,660,1,0,0,
        0,660,131,1,0,0,0,661,659,1,0,0,0,662,667,3,134,67,0,663,664,5,22,
        0,0,664,666,3,134,67,0,665,663,1,0,0,0,666,669,1,0,0,0,667,665,1,
        0,0,0,667,668,1,0,0,0,668,133,1,0,0,0,669,667,1,0,0,0,670,675,3,
        136,68,0,671,672,5,20,0,0,672,674,3,136,68,0,673,671,1,0,0,0,674,
        677,1,0,0,0,675,673,1,0,0,0,675,676,1,0,0,0,676,135,1,0,0,0,677,
        675,1,0,0,0,678,682,3,138,69,0,679,680,3,118,59,0,680,681,3,138,
        69,0,681,683,1,0,0,0,682,679,1,0,0,0,682,683,1,0,0,0,683,137,1,0,
        0,0,684,689,3,140,70,0,685,686,7,5,0,0,686,688,3,140,70,0,687,685,
        1,0,0,0,688,691,1,0,0,0,689,687,1,0,0,0,689,690,1,0,0,0,690,139,
        1,0,0,0,691,689,1,0,0,0,692,697,3,142,71,0,693,694,7,6,0,0,694,696,
        3,142,71,0,695,693,1,0,0,0,696,699,1,0,0,0,697,695,1,0,0,0,697,698,
        1,0,0,0,698,141,1,0,0,0,699,697,1,0,0,0,700,701,5,19,0,0,701,715,
        3,142,71,0,702,703,5,56,0,0,703,715,3,124,62,0,704,715,3,124,62,
        0,705,715,3,64,32,0,706,715,5,10,0,0,707,715,5,67,0,0,708,715,5,
        66,0,0,709,715,5,63,0,0,710,711,5,52,0,0,711,712,3,128,64,0,712,
        713,5,53,0,0,713,715,1,0,0,0,714,700,1,0,0,0,714,702,1,0,0,0,714,
        704,1,0,0,0,714,705,1,0,0,0,714,706,1,0,0,0,714,707,1,0,0,0,714,
        708,1,0,0,0,714,709,1,0,0,0,714,710,1,0,0,0,715,143,1,0,0,0,716,
        724,5,40,0,0,717,718,5,40,0,0,718,720,5,52,0,0,719,721,3,146,73,
        0,720,719,1,0,0,0,720,721,1,0,0,0,721,722,1,0,0,0,722,724,5,53,0,
        0,723,716,1,0,0,0,723,717,1,0,0,0,724,145,1,0,0,0,725,730,3,148,
        74,0,726,727,5,46,0,0,727,729,3,148,74,0,728,726,1,0,0,0,729,732,
        1,0,0,0,730,728,1,0,0,0,730,731,1,0,0,0,731,147,1,0,0,0,732,730,
        1,0,0,0,733,736,5,63,0,0,734,736,3,128,64,0,735,733,1,0,0,0,735,
        734,1,0,0,0,736,149,1,0,0,0,75,156,168,175,180,187,192,194,200,207,
        222,233,245,251,261,268,276,283,292,296,305,315,324,340,346,354,
        368,375,380,385,393,399,408,413,417,423,428,431,434,442,449,455,
        464,471,477,488,492,496,512,520,524,532,539,547,565,569,585,592,
        606,612,624,631,634,644,650,659,667,675,682,689,697,714,720,723,
        730,735
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
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'..'", "'.'", "':='", "':'", "';'", "','", 
                     "'+'", "'-'", "'*'", "'/'", "'['", "'('", "')'", "']'", 
                     "'^'", "'@'", "'='", "'<='", "'<>'", "'<'", "'>='", 
                     "'>'" ]

    symbolicNames = [ "<INVALID>", "PROGRAM", "BEGIN_", "END", "CONST", 
                      "VAR", "TYPE", "RECORD", "ARRAY", "OF", "NIL", "DOUBLE", 
                      "INTEGER", "CASE", "IF", "THEN", "ELSE", "BREAK", 
                      "CONTINUE", "NOT", "AND", "OR", "XOR", "WHILE", "DO", 
                      "REPEAT", "UNTIL", "FOR", "TO", "DOWNTO", "PROCEDURE", 
                      "FUNCTION", "RESULT", "EXIT", "TRY", "FINALLY", "EXCEPT", 
                      "CLASS", "CONSTRUCTOR", "DESTRUCTOR", "WRITELN", "DOTDOT", 
                      "DOT", "ASSIGN", "COLON", "SEMI", "COMMA", "PLUS", 
                      "MINUS", "STAR", "SLASH", "LBRACK", "LPAREN", "RPAREN", 
                      "RBRACK", "CARET", "AT", "EQ_OP", "LE_OP", "NE_OP", 
                      "LT_OP", "GE_OP", "GT_OP", "STRING", "IDENT", "HEXNUMBER", 
                      "FLOATNUMBER", "NUMBER", "WS", "COMMENT1", "COMMENT2", 
                      "COMMENT3" ]

    RULE_programFile = 0
    RULE_declarationPart = 1
    RULE_classMethodImplementation = 2
    RULE_constSection = 3
    RULE_constDeclaration = 4
    RULE_constItem = 5
    RULE_constValue = 6
    RULE_typeSection = 7
    RULE_typeDeclaration = 8
    RULE_classDeclaration = 9
    RULE_classBody = 10
    RULE_classMember = 11
    RULE_classFieldDeclaration = 12
    RULE_constructorDeclaration = 13
    RULE_destructorDeclaration = 14
    RULE_arrayDeclaration = 15
    RULE_arrayInitializer = 16
    RULE_arrayValueList = 17
    RULE_arrayType = 18
    RULE_arrayRange = 19
    RULE_typeName = 20
    RULE_simpleType = 21
    RULE_enumDeclaration = 22
    RULE_enumValueList = 23
    RULE_enumValue = 24
    RULE_recordDeclaration = 25
    RULE_recordFieldDeclaration = 26
    RULE_functionDeclaration = 27
    RULE_procedureDeclaration = 28
    RULE_formalParamList = 29
    RULE_formalParam = 30
    RULE_declaration = 31
    RULE_functionCallExpr = 32
    RULE_procedureCallStatement = 33
    RULE_actualParamList = 34
    RULE_actualParam = 35
    RULE_varSection = 36
    RULE_varDeclaration = 37
    RULE_varType = 38
    RULE_identList = 39
    RULE_block = 40
    RULE_localDeclaration = 41
    RULE_statementList = 42
    RULE_statement = 43
    RULE_caseStatement = 44
    RULE_caseItem = 45
    RULE_caseLabelList = 46
    RULE_caseLabel = 47
    RULE_caseElse = 48
    RULE_breakStatement = 49
    RULE_continueStatement = 50
    RULE_tryStatement = 51
    RULE_exitStatement = 52
    RULE_forStatement = 53
    RULE_repeatStatement = 54
    RULE_argumentList = 55
    RULE_whileStatement = 56
    RULE_ifStatement = 57
    RULE_condition = 58
    RULE_compareOp = 59
    RULE_compoundStatement = 60
    RULE_assignment = 61
    RULE_variableRef = 62
    RULE_variableSuffix = 63
    RULE_expr = 64
    RULE_boolOrExpr = 65
    RULE_boolXorExpr = 66
    RULE_boolAndExpr = 67
    RULE_compareExpr = 68
    RULE_addExpr = 69
    RULE_term = 70
    RULE_factor = 71
    RULE_writeLnStatement = 72
    RULE_writeArgList = 73
    RULE_writeArg = 74

    ruleNames =  [ "programFile", "declarationPart", "classMethodImplementation", 
                   "constSection", "constDeclaration", "constItem", "constValue", 
                   "typeSection", "typeDeclaration", "classDeclaration", 
                   "classBody", "classMember", "classFieldDeclaration", 
                   "constructorDeclaration", "destructorDeclaration", "arrayDeclaration", 
                   "arrayInitializer", "arrayValueList", "arrayType", "arrayRange", 
                   "typeName", "simpleType", "enumDeclaration", "enumValueList", 
                   "enumValue", "recordDeclaration", "recordFieldDeclaration", 
                   "functionDeclaration", "procedureDeclaration", "formalParamList", 
                   "formalParam", "declaration", "functionCallExpr", "procedureCallStatement", 
                   "actualParamList", "actualParam", "varSection", "varDeclaration", 
                   "varType", "identList", "block", "localDeclaration", 
                   "statementList", "statement", "caseStatement", "caseItem", 
                   "caseLabelList", "caseLabel", "caseElse", "breakStatement", 
                   "continueStatement", "tryStatement", "exitStatement", 
                   "forStatement", "repeatStatement", "argumentList", "whileStatement", 
                   "ifStatement", "condition", "compareOp", "compoundStatement", 
                   "assignment", "variableRef", "variableSuffix", "expr", 
                   "boolOrExpr", "boolXorExpr", "boolAndExpr", "compareExpr", 
                   "addExpr", "term", "factor", "writeLnStatement", "writeArgList", 
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
    CASE=13
    IF=14
    THEN=15
    ELSE=16
    BREAK=17
    CONTINUE=18
    NOT=19
    AND=20
    OR=21
    XOR=22
    WHILE=23
    DO=24
    REPEAT=25
    UNTIL=26
    FOR=27
    TO=28
    DOWNTO=29
    PROCEDURE=30
    FUNCTION=31
    RESULT=32
    EXIT=33
    TRY=34
    FINALLY=35
    EXCEPT=36
    CLASS=37
    CONSTRUCTOR=38
    DESTRUCTOR=39
    WRITELN=40
    DOTDOT=41
    DOT=42
    ASSIGN=43
    COLON=44
    SEMI=45
    COMMA=46
    PLUS=47
    MINUS=48
    STAR=49
    SLASH=50
    LBRACK=51
    LPAREN=52
    RPAREN=53
    RBRACK=54
    CARET=55
    AT=56
    EQ_OP=57
    LE_OP=58
    NE_OP=59
    LT_OP=60
    GE_OP=61
    GT_OP=62
    STRING=63
    IDENT=64
    HEXNUMBER=65
    FLOATNUMBER=66
    NUMBER=67
    WS=68
    COMMENT1=69
    COMMENT2=70
    COMMENT3=71

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
            self.state = 150
            self.match(MiniPascalParser.PROGRAM)
            self.state = 151
            self.match(MiniPascalParser.IDENT)
            self.state = 152
            self.match(MiniPascalParser.SEMI)
            self.state = 156
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 153
                    self.declarationPart() 
                self.state = 158
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 159
            self.block()
            self.state = 160
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


        def classMethodImplementation(self):
            return self.getTypedRuleContext(MiniPascalParser.ClassMethodImplementationContext,0)


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
            self.state = 168
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 162
                self.constSection()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 163
                self.typeSection()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 164
                self.varSection()
                pass
            elif token in [30]:
                self.enterOuterAlt(localctx, 4)
                self.state = 165
                self.procedureDeclaration()
                pass
            elif token in [31]:
                self.enterOuterAlt(localctx, 5)
                self.state = 166
                self.functionDeclaration()
                pass
            elif token in [38, 39]:
                self.enterOuterAlt(localctx, 6)
                self.state = 167
                self.classMethodImplementation()
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


    class ClassMethodImplementationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONSTRUCTOR(self):
            return self.getToken(MiniPascalParser.CONSTRUCTOR, 0)

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.IDENT)
            else:
                return self.getToken(MiniPascalParser.IDENT, i)

        def DOT(self):
            return self.getToken(MiniPascalParser.DOT, 0)

        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.SEMI)
            else:
                return self.getToken(MiniPascalParser.SEMI, i)

        def block(self):
            return self.getTypedRuleContext(MiniPascalParser.BlockContext,0)


        def formalParamList(self):
            return self.getTypedRuleContext(MiniPascalParser.FormalParamListContext,0)


        def DESTRUCTOR(self):
            return self.getToken(MiniPascalParser.DESTRUCTOR, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_classMethodImplementation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassMethodImplementation" ):
                listener.enterClassMethodImplementation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassMethodImplementation" ):
                listener.exitClassMethodImplementation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassMethodImplementation" ):
                return visitor.visitClassMethodImplementation(self)
            else:
                return visitor.visitChildren(self)




    def classMethodImplementation(self):

        localctx = MiniPascalParser.ClassMethodImplementationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_classMethodImplementation)
        self._la = 0 # Token type
        try:
            self.state = 194
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [38]:
                self.enterOuterAlt(localctx, 1)
                self.state = 170
                self.match(MiniPascalParser.CONSTRUCTOR)
                self.state = 171
                self.match(MiniPascalParser.IDENT)
                self.state = 172
                self.match(MiniPascalParser.DOT)
                self.state = 173
                self.match(MiniPascalParser.IDENT)
                self.state = 175
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==52:
                    self.state = 174
                    self.formalParamList()


                self.state = 177
                self.match(MiniPascalParser.SEMI)
                self.state = 178
                self.block()
                self.state = 180
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==45:
                    self.state = 179
                    self.match(MiniPascalParser.SEMI)


                pass
            elif token in [39]:
                self.enterOuterAlt(localctx, 2)
                self.state = 182
                self.match(MiniPascalParser.DESTRUCTOR)
                self.state = 183
                self.match(MiniPascalParser.IDENT)
                self.state = 184
                self.match(MiniPascalParser.DOT)
                self.state = 185
                self.match(MiniPascalParser.IDENT)
                self.state = 187
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==52:
                    self.state = 186
                    self.formalParamList()


                self.state = 189
                self.match(MiniPascalParser.SEMI)
                self.state = 190
                self.block()
                self.state = 192
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==45:
                    self.state = 191
                    self.match(MiniPascalParser.SEMI)


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
        self.enterRule(localctx, 6, self.RULE_constSection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
            self.match(MiniPascalParser.CONST)
            self.state = 198 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 197
                self.constDeclaration()
                self.state = 200 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==64):
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
        self.enterRule(localctx, 8, self.RULE_constDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 202
            self.constItem()
            self.state = 207
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 203
                self.match(MiniPascalParser.COMMA)
                self.state = 204
                self.constItem()
                self.state = 209
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 210
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
        self.enterRule(localctx, 10, self.RULE_constItem)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 212
            self.match(MiniPascalParser.IDENT)
            self.state = 213
            self.match(MiniPascalParser.EQ_OP)
            self.state = 214
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
        self.enterRule(localctx, 12, self.RULE_constValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 216
            _la = self._input.LA(1)
            if not(((((_la - 63)) & ~0x3f) == 0 and ((1 << (_la - 63)) & 25) != 0)):
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
        self.enterRule(localctx, 14, self.RULE_typeSection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 218
            self.match(MiniPascalParser.TYPE)
            self.state = 220 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 219
                self.typeDeclaration()
                self.state = 222 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==64):
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


        def classDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.ClassDeclarationContext,0)


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
        self.enterRule(localctx, 16, self.RULE_typeDeclaration)
        try:
            self.state = 233
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 224
                self.match(MiniPascalParser.IDENT)
                self.state = 225
                self.match(MiniPascalParser.EQ_OP)
                self.state = 226
                self.typeName()
                self.state = 227
                self.match(MiniPascalParser.SEMI)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 229
                self.enumDeclaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 230
                self.recordDeclaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 231
                self.arrayDeclaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 232
                self.classDeclaration()
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
            return self.getToken(MiniPascalParser.IDENT, 0)

        def EQ_OP(self):
            return self.getToken(MiniPascalParser.EQ_OP, 0)

        def CLASS(self):
            return self.getToken(MiniPascalParser.CLASS, 0)

        def classBody(self):
            return self.getTypedRuleContext(MiniPascalParser.ClassBodyContext,0)


        def END(self):
            return self.getToken(MiniPascalParser.END, 0)

        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_classDeclaration

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

        localctx = MiniPascalParser.ClassDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_classDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 235
            self.match(MiniPascalParser.IDENT)
            self.state = 236
            self.match(MiniPascalParser.EQ_OP)
            self.state = 237
            self.match(MiniPascalParser.CLASS)
            self.state = 238
            self.classBody()
            self.state = 239
            self.match(MiniPascalParser.END)
            self.state = 240
            self.match(MiniPascalParser.SEMI)
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

        def classMember(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.ClassMemberContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.ClassMemberContext,i)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_classBody

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

        localctx = MiniPascalParser.ClassBodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_classBody)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 245
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 38)) & ~0x3f) == 0 and ((1 << (_la - 38)) & 67108867) != 0):
                self.state = 242
                self.classMember()
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


    class ClassMemberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def classFieldDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.ClassFieldDeclarationContext,0)


        def constructorDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.ConstructorDeclarationContext,0)


        def destructorDeclaration(self):
            return self.getTypedRuleContext(MiniPascalParser.DestructorDeclarationContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_classMember

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

        localctx = MiniPascalParser.ClassMemberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_classMember)
        try:
            self.state = 251
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [64]:
                self.enterOuterAlt(localctx, 1)
                self.state = 248
                self.classFieldDeclaration()
                pass
            elif token in [38]:
                self.enterOuterAlt(localctx, 2)
                self.state = 249
                self.constructorDeclaration()
                pass
            elif token in [39]:
                self.enterOuterAlt(localctx, 3)
                self.state = 250
                self.destructorDeclaration()
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


    class ClassFieldDeclarationContext(ParserRuleContext):
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
            return MiniPascalParser.RULE_classFieldDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassFieldDeclaration" ):
                listener.enterClassFieldDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassFieldDeclaration" ):
                listener.exitClassFieldDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassFieldDeclaration" ):
                return visitor.visitClassFieldDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def classFieldDeclaration(self):

        localctx = MiniPascalParser.ClassFieldDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_classFieldDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 253
            self.identList()
            self.state = 254
            self.match(MiniPascalParser.COLON)
            self.state = 255
            self.typeName()
            self.state = 256
            self.match(MiniPascalParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstructorDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONSTRUCTOR(self):
            return self.getToken(MiniPascalParser.CONSTRUCTOR, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def formalParamList(self):
            return self.getTypedRuleContext(MiniPascalParser.FormalParamListContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_constructorDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstructorDeclaration" ):
                listener.enterConstructorDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstructorDeclaration" ):
                listener.exitConstructorDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstructorDeclaration" ):
                return visitor.visitConstructorDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def constructorDeclaration(self):

        localctx = MiniPascalParser.ConstructorDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_constructorDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 258
            self.match(MiniPascalParser.CONSTRUCTOR)
            self.state = 259
            self.match(MiniPascalParser.IDENT)
            self.state = 261
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 260
                self.formalParamList()


            self.state = 263
            self.match(MiniPascalParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DestructorDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DESTRUCTOR(self):
            return self.getToken(MiniPascalParser.DESTRUCTOR, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def formalParamList(self):
            return self.getTypedRuleContext(MiniPascalParser.FormalParamListContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_destructorDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDestructorDeclaration" ):
                listener.enterDestructorDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDestructorDeclaration" ):
                listener.exitDestructorDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDestructorDeclaration" ):
                return visitor.visitDestructorDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def destructorDeclaration(self):

        localctx = MiniPascalParser.DestructorDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_destructorDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 265
            self.match(MiniPascalParser.DESTRUCTOR)
            self.state = 266
            self.match(MiniPascalParser.IDENT)
            self.state = 268
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 267
                self.formalParamList()


            self.state = 270
            self.match(MiniPascalParser.SEMI)
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
        self.enterRule(localctx, 30, self.RULE_arrayDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 272
            self.match(MiniPascalParser.IDENT)
            self.state = 273
            self.match(MiniPascalParser.EQ_OP)
            self.state = 274
            self.arrayType()
            self.state = 276
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==57:
                self.state = 275
                self.arrayInitializer()


            self.state = 278
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
        self.enterRule(localctx, 32, self.RULE_arrayInitializer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 280
            self.match(MiniPascalParser.EQ_OP)
            self.state = 281
            self.match(MiniPascalParser.LPAREN)
            self.state = 283
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 63)) & ~0x3f) == 0 and ((1 << (_la - 63)) & 25) != 0):
                self.state = 282
                self.arrayValueList()


            self.state = 285
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
        self.enterRule(localctx, 34, self.RULE_arrayValueList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 287
            self.constValue()
            self.state = 292
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,17,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 288
                    self.match(MiniPascalParser.COMMA)
                    self.state = 289
                    self.constValue() 
                self.state = 294
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,17,self._ctx)

            self.state = 296
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==46:
                self.state = 295
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
        self.enterRule(localctx, 36, self.RULE_arrayType)
        self._la = 0 # Token type
        try:
            self.state = 315
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 298
                self.match(MiniPascalParser.ARRAY)
                self.state = 299
                self.match(MiniPascalParser.LBRACK)
                self.state = 300
                self.arrayRange()
                self.state = 305
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==46:
                    self.state = 301
                    self.match(MiniPascalParser.COMMA)
                    self.state = 302
                    self.arrayRange()
                    self.state = 307
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 308
                self.match(MiniPascalParser.RBRACK)
                self.state = 309
                self.match(MiniPascalParser.OF)
                self.state = 310
                self.typeName()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 312
                self.match(MiniPascalParser.ARRAY)
                self.state = 313
                self.match(MiniPascalParser.OF)
                self.state = 314
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
        self.enterRule(localctx, 38, self.RULE_arrayRange)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 317
            self.expr()
            self.state = 318
            self.match(MiniPascalParser.DOTDOT)
            self.state = 319
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
        self.enterRule(localctx, 40, self.RULE_typeName)
        try:
            self.state = 324
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11, 12, 63, 64]:
                self.enterOuterAlt(localctx, 1)
                self.state = 321
                self.simpleType()
                pass
            elif token in [55]:
                self.enterOuterAlt(localctx, 2)
                self.state = 322
                self.match(MiniPascalParser.CARET)
                self.state = 323
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
        self.enterRule(localctx, 42, self.RULE_simpleType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 326
            _la = self._input.LA(1)
            if not(((((_la - 11)) & ~0x3f) == 0 and ((1 << (_la - 11)) & 13510798882111491) != 0)):
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
        self.enterRule(localctx, 44, self.RULE_enumDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 328
            self.match(MiniPascalParser.IDENT)
            self.state = 329
            self.match(MiniPascalParser.EQ_OP)
            self.state = 330
            self.match(MiniPascalParser.LPAREN)
            self.state = 331
            self.enumValueList()
            self.state = 332
            self.match(MiniPascalParser.RPAREN)
            self.state = 333
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
        self.enterRule(localctx, 46, self.RULE_enumValueList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 335
            self.enumValue()
            self.state = 340
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 336
                self.match(MiniPascalParser.COMMA)
                self.state = 337
                self.enumValue()
                self.state = 342
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
        self.enterRule(localctx, 48, self.RULE_enumValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 343
            self.match(MiniPascalParser.IDENT)
            self.state = 346
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==57:
                self.state = 344
                self.match(MiniPascalParser.EQ_OP)
                self.state = 345
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
        self.enterRule(localctx, 50, self.RULE_recordDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 348
            self.match(MiniPascalParser.IDENT)
            self.state = 349
            self.match(MiniPascalParser.EQ_OP)
            self.state = 350
            self.match(MiniPascalParser.RECORD)
            self.state = 354
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==64:
                self.state = 351
                self.recordFieldDeclaration()
                self.state = 356
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 357
            self.match(MiniPascalParser.END)
            self.state = 358
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
        self.enterRule(localctx, 52, self.RULE_recordFieldDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 360
            self.identList()
            self.state = 361
            self.match(MiniPascalParser.COLON)
            self.state = 362
            self.typeName()
            self.state = 363
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
        self.enterRule(localctx, 54, self.RULE_functionDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 365
            self.match(MiniPascalParser.FUNCTION)
            self.state = 366
            self.match(MiniPascalParser.IDENT)
            self.state = 368
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 367
                self.formalParamList()


            self.state = 370
            self.match(MiniPascalParser.COLON)
            self.state = 371
            self.typeName()
            self.state = 372
            self.match(MiniPascalParser.SEMI)
            self.state = 373
            self.block()
            self.state = 375
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 374
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
        self.enterRule(localctx, 56, self.RULE_procedureDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 377
            self.match(MiniPascalParser.PROCEDURE)
            self.state = 378
            self.match(MiniPascalParser.IDENT)
            self.state = 380
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 379
                self.formalParamList()


            self.state = 382
            self.match(MiniPascalParser.SEMI)
            self.state = 383
            self.block()
            self.state = 385
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 384
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
        self.enterRule(localctx, 58, self.RULE_formalParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 387
            self.match(MiniPascalParser.LPAREN)
            self.state = 388
            self.formalParam()
            self.state = 393
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==45:
                self.state = 389
                self.match(MiniPascalParser.SEMI)
                self.state = 390
                self.formalParam()
                self.state = 395
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 396
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
        self.enterRule(localctx, 60, self.RULE_formalParam)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 399
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 398
                self.match(MiniPascalParser.VAR)


            self.state = 401
            self.identList()
            self.state = 402
            self.match(MiniPascalParser.COLON)
            self.state = 403
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
        self.enterRule(localctx, 62, self.RULE_declaration)
        try:
            self.state = 408
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 405
                self.varSection()
                pass
            elif token in [30]:
                self.enterOuterAlt(localctx, 2)
                self.state = 406
                self.procedureDeclaration()
                pass
            elif token in [31]:
                self.enterOuterAlt(localctx, 3)
                self.state = 407
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

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.IDENT)
            else:
                return self.getToken(MiniPascalParser.IDENT, i)

        def LPAREN(self):
            return self.getToken(MiniPascalParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(MiniPascalParser.RPAREN, 0)

        def DOT(self):
            return self.getToken(MiniPascalParser.DOT, 0)

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
        self.enterRule(localctx, 64, self.RULE_functionCallExpr)
        self._la = 0 # Token type
        try:
            self.state = 423
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,34,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 410
                self.match(MiniPascalParser.IDENT)
                self.state = 413
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==42:
                    self.state = 411
                    self.match(MiniPascalParser.DOT)
                    self.state = 412
                    self.match(MiniPascalParser.IDENT)


                self.state = 415
                self.match(MiniPascalParser.LPAREN)
                self.state = 417
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 10)) & ~0x3f) == 0 and ((1 << (_la - 10)) & 243269146672890369) != 0):
                    self.state = 416
                    self.argumentList()


                self.state = 419
                self.match(MiniPascalParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 420
                self.match(MiniPascalParser.IDENT)
                self.state = 421
                self.match(MiniPascalParser.DOT)
                self.state = 422
                self.match(MiniPascalParser.IDENT)
                pass


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

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.IDENT)
            else:
                return self.getToken(MiniPascalParser.IDENT, i)

        def DOT(self):
            return self.getToken(MiniPascalParser.DOT, 0)

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
        self.enterRule(localctx, 66, self.RULE_procedureCallStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 425
            self.match(MiniPascalParser.IDENT)
            self.state = 428
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==42:
                self.state = 426
                self.match(MiniPascalParser.DOT)
                self.state = 427
                self.match(MiniPascalParser.IDENT)


            self.state = 431
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 430
                self.actualParamList()


            self.state = 434
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,37,self._ctx)
            if la_ == 1:
                self.state = 433
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
        self.enterRule(localctx, 68, self.RULE_actualParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 436
            self.match(MiniPascalParser.LPAREN)
            self.state = 437
            self.actualParam()
            self.state = 442
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 438
                self.match(MiniPascalParser.COMMA)
                self.state = 439
                self.actualParam()
                self.state = 444
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 445
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
        self.enterRule(localctx, 70, self.RULE_actualParam)
        try:
            self.state = 449
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 447
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 448
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
        self.enterRule(localctx, 72, self.RULE_varSection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 451
            self.match(MiniPascalParser.VAR)
            self.state = 453 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 452
                self.varDeclaration()
                self.state = 455 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==64):
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
        self.enterRule(localctx, 74, self.RULE_varDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 457
            self.identList()
            self.state = 458
            self.match(MiniPascalParser.COLON)
            self.state = 459
            self.varType()
            self.state = 460
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
        self.enterRule(localctx, 76, self.RULE_varType)
        try:
            self.state = 464
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11, 12, 55, 63, 64]:
                self.enterOuterAlt(localctx, 1)
                self.state = 462
                self.typeName()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 2)
                self.state = 463
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
        self.enterRule(localctx, 78, self.RULE_identList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 466
            self.match(MiniPascalParser.IDENT)
            self.state = 471
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 467
                self.match(MiniPascalParser.COMMA)
                self.state = 468
                self.match(MiniPascalParser.IDENT)
                self.state = 473
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
        self.enterRule(localctx, 80, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 477
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 3221225520) != 0):
                self.state = 474
                self.localDeclaration()
                self.state = 479
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 480
            self.match(MiniPascalParser.BEGIN_)
            self.state = 481
            self.statementList()
            self.state = 482
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
        self.enterRule(localctx, 82, self.RULE_localDeclaration)
        try:
            self.state = 488
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [30]:
                self.enterOuterAlt(localctx, 1)
                self.state = 484
                self.procedureDeclaration()
                pass
            elif token in [31]:
                self.enterOuterAlt(localctx, 2)
                self.state = 485
                self.functionDeclaration()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 486
                self.varSection()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 487
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
        self.enterRule(localctx, 84, self.RULE_statementList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 496
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 2)) & ~0x3f) == 0 and ((1 << (_la - 2)) & 4611686300865632257) != 0):
                self.state = 490
                self.statement()
                self.state = 492
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,45,self._ctx)
                if la_ == 1:
                    self.state = 491
                    self.match(MiniPascalParser.SEMI)


                self.state = 498
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


        def breakStatement(self):
            return self.getTypedRuleContext(MiniPascalParser.BreakStatementContext,0)


        def continueStatement(self):
            return self.getTypedRuleContext(MiniPascalParser.ContinueStatementContext,0)


        def caseStatement(self):
            return self.getTypedRuleContext(MiniPascalParser.CaseStatementContext,0)


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
        self.enterRule(localctx, 86, self.RULE_statement)
        try:
            self.state = 512
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,47,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 499
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 500
                self.writeLnStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 501
                self.tryStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 502
                self.ifStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 503
                self.whileStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 504
                self.repeatStatement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 505
                self.forStatement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 506
                self.breakStatement()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 507
                self.continueStatement()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 508
                self.caseStatement()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 509
                self.procedureCallStatement()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 510
                self.exitStatement()
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 511
                self.compoundStatement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CaseStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CASE(self):
            return self.getToken(MiniPascalParser.CASE, 0)

        def expr(self):
            return self.getTypedRuleContext(MiniPascalParser.ExprContext,0)


        def OF(self):
            return self.getToken(MiniPascalParser.OF, 0)

        def END(self):
            return self.getToken(MiniPascalParser.END, 0)

        def caseItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.CaseItemContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.CaseItemContext,i)


        def caseElse(self):
            return self.getTypedRuleContext(MiniPascalParser.CaseElseContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_caseStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCaseStatement" ):
                listener.enterCaseStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCaseStatement" ):
                listener.exitCaseStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCaseStatement" ):
                return visitor.visitCaseStatement(self)
            else:
                return visitor.visitChildren(self)




    def caseStatement(self):

        localctx = MiniPascalParser.CaseStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_caseStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 514
            self.match(MiniPascalParser.CASE)
            self.state = 515
            self.expr()
            self.state = 516
            self.match(MiniPascalParser.OF)
            self.state = 520
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==64 or _la==67:
                self.state = 517
                self.caseItem()
                self.state = 522
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 524
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16:
                self.state = 523
                self.caseElse()


            self.state = 526
            self.match(MiniPascalParser.END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CaseItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def caseLabelList(self):
            return self.getTypedRuleContext(MiniPascalParser.CaseLabelListContext,0)


        def COLON(self):
            return self.getToken(MiniPascalParser.COLON, 0)

        def statement(self):
            return self.getTypedRuleContext(MiniPascalParser.StatementContext,0)


        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_caseItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCaseItem" ):
                listener.enterCaseItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCaseItem" ):
                listener.exitCaseItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCaseItem" ):
                return visitor.visitCaseItem(self)
            else:
                return visitor.visitChildren(self)




    def caseItem(self):

        localctx = MiniPascalParser.CaseItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_caseItem)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 528
            self.caseLabelList()
            self.state = 529
            self.match(MiniPascalParser.COLON)
            self.state = 530
            self.statement()
            self.state = 532
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 531
                self.match(MiniPascalParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CaseLabelListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def caseLabel(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.CaseLabelContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.CaseLabelContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MiniPascalParser.COMMA)
            else:
                return self.getToken(MiniPascalParser.COMMA, i)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_caseLabelList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCaseLabelList" ):
                listener.enterCaseLabelList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCaseLabelList" ):
                listener.exitCaseLabelList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCaseLabelList" ):
                return visitor.visitCaseLabelList(self)
            else:
                return visitor.visitChildren(self)




    def caseLabelList(self):

        localctx = MiniPascalParser.CaseLabelListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_caseLabelList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 534
            self.caseLabel()
            self.state = 539
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 535
                self.match(MiniPascalParser.COMMA)
                self.state = 536
                self.caseLabel()
                self.state = 541
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CaseLabelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(MiniPascalParser.NUMBER, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_caseLabel

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCaseLabel" ):
                listener.enterCaseLabel(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCaseLabel" ):
                listener.exitCaseLabel(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCaseLabel" ):
                return visitor.visitCaseLabel(self)
            else:
                return visitor.visitChildren(self)




    def caseLabel(self):

        localctx = MiniPascalParser.CaseLabelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_caseLabel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 542
            _la = self._input.LA(1)
            if not(_la==64 or _la==67):
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


    class CaseElseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ELSE(self):
            return self.getToken(MiniPascalParser.ELSE, 0)

        def statementList(self):
            return self.getTypedRuleContext(MiniPascalParser.StatementListContext,0)


        def SEMI(self):
            return self.getToken(MiniPascalParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_caseElse

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCaseElse" ):
                listener.enterCaseElse(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCaseElse" ):
                listener.exitCaseElse(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCaseElse" ):
                return visitor.visitCaseElse(self)
            else:
                return visitor.visitChildren(self)




    def caseElse(self):

        localctx = MiniPascalParser.CaseElseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_caseElse)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 544
            self.match(MiniPascalParser.ELSE)
            self.state = 545
            self.statementList()
            self.state = 547
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 546
                self.match(MiniPascalParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BreakStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BREAK(self):
            return self.getToken(MiniPascalParser.BREAK, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_breakStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreakStatement" ):
                listener.enterBreakStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreakStatement" ):
                listener.exitBreakStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreakStatement" ):
                return visitor.visitBreakStatement(self)
            else:
                return visitor.visitChildren(self)




    def breakStatement(self):

        localctx = MiniPascalParser.BreakStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_breakStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 549
            self.match(MiniPascalParser.BREAK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContinueStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONTINUE(self):
            return self.getToken(MiniPascalParser.CONTINUE, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_continueStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContinueStatement" ):
                listener.enterContinueStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContinueStatement" ):
                listener.exitContinueStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinueStatement" ):
                return visitor.visitContinueStatement(self)
            else:
                return visitor.visitChildren(self)




    def continueStatement(self):

        localctx = MiniPascalParser.ContinueStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_continueStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 551
            self.match(MiniPascalParser.CONTINUE)
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
        self.enterRule(localctx, 102, self.RULE_tryStatement)
        try:
            self.state = 565
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,53,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 553
                self.match(MiniPascalParser.TRY)
                self.state = 554
                self.statementList()
                self.state = 555
                self.match(MiniPascalParser.FINALLY)
                self.state = 556
                self.statementList()
                self.state = 557
                self.match(MiniPascalParser.END)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 559
                self.match(MiniPascalParser.TRY)
                self.state = 560
                self.statementList()
                self.state = 561
                self.match(MiniPascalParser.EXCEPT)
                self.state = 562
                self.statementList()
                self.state = 563
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
        self.enterRule(localctx, 104, self.RULE_exitStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 567
            self.match(MiniPascalParser.EXIT)
            self.state = 569
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,54,self._ctx)
            if la_ == 1:
                self.state = 568
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
        self.enterRule(localctx, 106, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 571
            self.match(MiniPascalParser.FOR)
            self.state = 572
            self.match(MiniPascalParser.IDENT)
            self.state = 573
            self.match(MiniPascalParser.ASSIGN)
            self.state = 574
            self.expr()
            self.state = 575
            _la = self._input.LA(1)
            if not(_la==28 or _la==29):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 576
            self.expr()
            self.state = 577
            self.match(MiniPascalParser.DO)
            self.state = 578
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
        self.enterRule(localctx, 108, self.RULE_repeatStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 580
            self.match(MiniPascalParser.REPEAT)
            self.state = 581
            self.statementList()
            self.state = 582
            self.match(MiniPascalParser.UNTIL)
            self.state = 583
            self.condition()
            self.state = 585
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,55,self._ctx)
            if la_ == 1:
                self.state = 584
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
        self.enterRule(localctx, 110, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 587
            self.expr()
            self.state = 592
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 588
                self.match(MiniPascalParser.COMMA)
                self.state = 589
                self.expr()
                self.state = 594
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
        self.enterRule(localctx, 112, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 595
            self.match(MiniPascalParser.WHILE)
            self.state = 596
            self.condition()
            self.state = 597
            self.match(MiniPascalParser.DO)
            self.state = 598
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
        self.enterRule(localctx, 114, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 600
            self.match(MiniPascalParser.IF)
            self.state = 601
            self.condition()
            self.state = 602
            self.match(MiniPascalParser.THEN)
            self.state = 603
            self.statement()
            self.state = 606
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,57,self._ctx)
            if la_ == 1:
                self.state = 604
                self.match(MiniPascalParser.ELSE)
                self.state = 605
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
        self.enterRule(localctx, 116, self.RULE_condition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 608
            self.expr()
            self.state = 612
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 9079256848778919936) != 0):
                self.state = 609
                self.compareOp()
                self.state = 610
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
        self.enterRule(localctx, 118, self.RULE_compareOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 614
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 9079256848778919936) != 0)):
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
        self.enterRule(localctx, 120, self.RULE_compoundStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 616
            self.match(MiniPascalParser.BEGIN_)
            self.state = 617
            self.statementList()
            self.state = 618
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
        self.enterRule(localctx, 122, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 620
            self.variableRef()
            self.state = 621
            self.match(MiniPascalParser.ASSIGN)
            self.state = 622
            self.expr()
            self.state = 624
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,59,self._ctx)
            if la_ == 1:
                self.state = 623
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
        self.enterRule(localctx, 124, self.RULE_variableRef)
        self._la = 0 # Token type
        try:
            self.state = 634
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [32]:
                self.enterOuterAlt(localctx, 1)
                self.state = 626
                self.match(MiniPascalParser.RESULT)
                pass
            elif token in [64]:
                self.enterOuterAlt(localctx, 2)
                self.state = 627
                self.match(MiniPascalParser.IDENT)
                self.state = 631
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 38284994879160320) != 0):
                    self.state = 628
                    self.variableSuffix()
                    self.state = 633
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
        self.enterRule(localctx, 126, self.RULE_variableSuffix)
        self._la = 0 # Token type
        try:
            self.state = 650
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [42]:
                self.enterOuterAlt(localctx, 1)
                self.state = 636
                self.match(MiniPascalParser.DOT)
                self.state = 637
                self.match(MiniPascalParser.IDENT)
                pass
            elif token in [51]:
                self.enterOuterAlt(localctx, 2)
                self.state = 638
                self.match(MiniPascalParser.LBRACK)
                self.state = 639
                self.expr()
                self.state = 644
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==46:
                    self.state = 640
                    self.match(MiniPascalParser.COMMA)
                    self.state = 641
                    self.expr()
                    self.state = 646
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 647
                self.match(MiniPascalParser.RBRACK)
                pass
            elif token in [55]:
                self.enterOuterAlt(localctx, 3)
                self.state = 649
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
        self.enterRule(localctx, 128, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 652
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
        self.enterRule(localctx, 130, self.RULE_boolOrExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 654
            self.boolXorExpr()
            self.state = 659
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==21:
                self.state = 655
                self.match(MiniPascalParser.OR)
                self.state = 656
                self.boolXorExpr()
                self.state = 661
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
        self.enterRule(localctx, 132, self.RULE_boolXorExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 662
            self.boolAndExpr()
            self.state = 667
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==22:
                self.state = 663
                self.match(MiniPascalParser.XOR)
                self.state = 664
                self.boolAndExpr()
                self.state = 669
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

        def compareExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.CompareExprContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.CompareExprContext,i)


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
        self.enterRule(localctx, 134, self.RULE_boolAndExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 670
            self.compareExpr()
            self.state = 675
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==20:
                self.state = 671
                self.match(MiniPascalParser.AND)
                self.state = 672
                self.compareExpr()
                self.state = 677
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompareExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def addExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniPascalParser.AddExprContext)
            else:
                return self.getTypedRuleContext(MiniPascalParser.AddExprContext,i)


        def compareOp(self):
            return self.getTypedRuleContext(MiniPascalParser.CompareOpContext,0)


        def getRuleIndex(self):
            return MiniPascalParser.RULE_compareExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompareExpr" ):
                listener.enterCompareExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompareExpr" ):
                listener.exitCompareExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompareExpr" ):
                return visitor.visitCompareExpr(self)
            else:
                return visitor.visitChildren(self)




    def compareExpr(self):

        localctx = MiniPascalParser.CompareExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 136, self.RULE_compareExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 678
            self.addExpr()
            self.state = 682
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,67,self._ctx)
            if la_ == 1:
                self.state = 679
                self.compareOp()
                self.state = 680
                self.addExpr()


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
        self.enterRule(localctx, 138, self.RULE_addExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 684
            self.term()
            self.state = 689
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==47 or _la==48:
                self.state = 685
                _la = self._input.LA(1)
                if not(_la==47 or _la==48):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 686
                self.term()
                self.state = 691
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
        self.enterRule(localctx, 140, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 692
            self.factor()
            self.state = 697
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==49 or _la==50:
                self.state = 693
                _la = self._input.LA(1)
                if not(_la==49 or _la==50):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 694
                self.factor()
                self.state = 699
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
        self.enterRule(localctx, 142, self.RULE_factor)
        try:
            self.state = 714
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,70,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 700
                self.match(MiniPascalParser.NOT)
                self.state = 701
                self.factor()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 702
                self.match(MiniPascalParser.AT)
                self.state = 703
                self.variableRef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 704
                self.variableRef()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 705
                self.functionCallExpr()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 706
                self.match(MiniPascalParser.NIL)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 707
                self.match(MiniPascalParser.NUMBER)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 708
                self.match(MiniPascalParser.FLOATNUMBER)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 709
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 710
                self.match(MiniPascalParser.LPAREN)
                self.state = 711
                self.expr()
                self.state = 712
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
        self.enterRule(localctx, 144, self.RULE_writeLnStatement)
        self._la = 0 # Token type
        try:
            self.state = 723
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,72,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 716
                self.match(MiniPascalParser.WRITELN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 717
                self.match(MiniPascalParser.WRITELN)
                self.state = 718
                self.match(MiniPascalParser.LPAREN)
                self.state = 720
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 10)) & ~0x3f) == 0 and ((1 << (_la - 10)) & 243269146672890369) != 0):
                    self.state = 719
                    self.writeArgList()


                self.state = 722
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
        self.enterRule(localctx, 146, self.RULE_writeArgList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 725
            self.writeArg()
            self.state = 730
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 726
                self.match(MiniPascalParser.COMMA)
                self.state = 727
                self.writeArg()
                self.state = 732
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
        self.enterRule(localctx, 148, self.RULE_writeArg)
        try:
            self.state = 735
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,74,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 733
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 734
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





