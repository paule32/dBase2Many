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
        4,1,71,747,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
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
        7,72,2,73,7,73,2,74,7,74,2,75,7,75,1,0,1,0,1,0,1,0,5,0,157,8,0,10,
        0,12,0,160,9,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,3,1,171,8,1,1,
        2,1,2,1,2,1,2,1,2,3,2,178,8,2,1,2,1,2,1,2,3,2,183,8,2,1,2,1,2,1,
        2,1,2,1,2,3,2,190,8,2,1,2,1,2,1,2,3,2,195,8,2,3,2,197,8,2,1,3,1,
        3,4,3,201,8,3,11,3,12,3,202,1,4,1,4,1,4,5,4,208,8,4,10,4,12,4,211,
        9,4,1,4,1,4,1,5,1,5,1,5,1,5,1,6,1,6,1,7,1,7,4,7,223,8,7,11,7,12,
        7,224,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,3,8,236,8,8,1,9,1,9,1,
        9,1,9,3,9,242,8,9,1,9,1,9,1,9,1,9,1,10,1,10,1,10,1,10,1,11,5,11,
        253,8,11,10,11,12,11,256,9,11,1,12,1,12,1,12,3,12,261,8,12,1,13,
        1,13,1,13,1,13,1,13,1,14,1,14,1,14,3,14,271,8,14,1,14,1,14,1,15,
        1,15,1,15,3,15,278,8,15,1,15,1,15,1,16,1,16,1,16,1,16,3,16,286,8,
        16,1,16,1,16,1,17,1,17,1,17,3,17,293,8,17,1,17,1,17,1,18,1,18,1,
        18,5,18,300,8,18,10,18,12,18,303,9,18,1,18,3,18,306,8,18,1,19,1,
        19,1,19,1,19,1,19,5,19,313,8,19,10,19,12,19,316,9,19,1,19,1,19,1,
        19,1,19,1,19,1,19,1,19,3,19,325,8,19,1,20,1,20,1,20,1,20,1,21,1,
        21,1,21,3,21,334,8,21,1,22,1,22,1,23,1,23,1,23,1,23,1,23,1,23,1,
        23,1,24,1,24,1,24,5,24,348,8,24,10,24,12,24,351,9,24,1,25,1,25,1,
        25,3,25,356,8,25,1,26,1,26,1,26,1,26,5,26,362,8,26,10,26,12,26,365,
        9,26,1,26,1,26,1,26,1,27,1,27,1,27,1,27,1,27,1,28,1,28,1,28,3,28,
        378,8,28,1,28,1,28,1,28,1,28,1,28,3,28,385,8,28,1,29,1,29,1,29,3,
        29,390,8,29,1,29,1,29,1,29,3,29,395,8,29,1,30,1,30,1,30,1,30,5,30,
        401,8,30,10,30,12,30,404,9,30,1,30,1,30,1,31,3,31,409,8,31,1,31,
        1,31,1,31,1,31,1,32,1,32,1,32,3,32,418,8,32,1,33,1,33,1,33,3,33,
        423,8,33,1,33,1,33,3,33,427,8,33,1,33,1,33,1,33,1,33,3,33,433,8,
        33,1,34,1,34,1,34,3,34,438,8,34,1,34,3,34,441,8,34,1,34,3,34,444,
        8,34,1,35,1,35,1,35,1,35,5,35,450,8,35,10,35,12,35,453,9,35,1,35,
        1,35,1,36,1,36,3,36,459,8,36,1,37,1,37,4,37,463,8,37,11,37,12,37,
        464,1,38,1,38,1,38,1,38,1,38,1,39,1,39,3,39,474,8,39,1,40,1,40,1,
        40,5,40,479,8,40,10,40,12,40,482,9,40,1,41,5,41,485,8,41,10,41,12,
        41,488,9,41,1,41,1,41,1,41,1,41,1,42,1,42,1,42,1,42,3,42,498,8,42,
        1,43,1,43,3,43,502,8,43,5,43,504,8,43,10,43,12,43,507,9,43,1,44,
        1,44,1,44,1,44,1,44,1,44,1,44,1,44,1,44,1,44,1,44,1,44,1,44,3,44,
        522,8,44,1,45,1,45,1,45,1,45,5,45,528,8,45,10,45,12,45,531,9,45,
        1,45,3,45,534,8,45,1,45,1,45,1,46,1,46,1,46,1,46,3,46,542,8,46,1,
        47,1,47,1,47,5,47,547,8,47,10,47,12,47,550,9,47,1,48,1,48,1,49,1,
        49,1,49,3,49,557,8,49,1,50,1,50,1,51,1,51,1,52,1,52,1,52,1,52,1,
        52,1,52,1,52,1,52,1,52,1,52,1,52,1,52,3,52,575,8,52,1,53,1,53,3,
        53,579,8,53,1,54,1,54,1,54,1,54,1,54,1,54,1,54,1,54,1,54,1,55,1,
        55,1,55,1,55,1,55,3,55,595,8,55,1,56,1,56,1,56,5,56,600,8,56,10,
        56,12,56,603,9,56,1,57,1,57,1,57,1,57,1,57,1,58,1,58,1,58,1,58,1,
        58,1,58,3,58,616,8,58,1,59,1,59,1,59,1,59,3,59,622,8,59,1,60,1,60,
        1,61,1,61,1,61,1,61,1,62,1,62,1,62,1,62,3,62,634,8,62,1,63,1,63,
        1,63,5,63,639,8,63,10,63,12,63,642,9,63,3,63,644,8,63,1,64,1,64,
        1,64,1,64,1,64,1,64,5,64,652,8,64,10,64,12,64,655,9,64,1,64,1,64,
        1,64,3,64,660,8,64,1,65,1,65,1,66,1,66,1,66,5,66,667,8,66,10,66,
        12,66,670,9,66,1,67,1,67,1,67,5,67,675,8,67,10,67,12,67,678,9,67,
        1,68,1,68,1,68,5,68,683,8,68,10,68,12,68,686,9,68,1,69,1,69,1,69,
        1,69,3,69,692,8,69,1,70,1,70,1,70,5,70,697,8,70,10,70,12,70,700,
        9,70,1,71,1,71,1,71,5,71,705,8,71,10,71,12,71,708,9,71,1,72,1,72,
        1,72,1,72,1,72,1,72,1,72,1,72,1,72,1,72,1,72,1,72,1,72,1,72,3,72,
        724,8,72,1,73,1,73,1,73,1,73,3,73,730,8,73,1,73,3,73,733,8,73,1,
        74,1,74,1,74,5,74,738,8,74,10,74,12,74,741,9,74,1,75,1,75,3,75,745,
        8,75,1,75,0,0,76,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,
        36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,
        80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,114,116,
        118,120,122,124,126,128,130,132,134,136,138,140,142,144,146,148,
        150,0,7,2,0,63,63,66,67,2,0,11,12,63,64,2,0,64,64,67,67,1,0,28,29,
        1,0,57,62,1,0,47,48,1,0,49,50,776,0,152,1,0,0,0,2,170,1,0,0,0,4,
        196,1,0,0,0,6,198,1,0,0,0,8,204,1,0,0,0,10,214,1,0,0,0,12,218,1,
        0,0,0,14,220,1,0,0,0,16,235,1,0,0,0,18,237,1,0,0,0,20,247,1,0,0,
        0,22,254,1,0,0,0,24,260,1,0,0,0,26,262,1,0,0,0,28,267,1,0,0,0,30,
        274,1,0,0,0,32,281,1,0,0,0,34,289,1,0,0,0,36,296,1,0,0,0,38,324,
        1,0,0,0,40,326,1,0,0,0,42,333,1,0,0,0,44,335,1,0,0,0,46,337,1,0,
        0,0,48,344,1,0,0,0,50,352,1,0,0,0,52,357,1,0,0,0,54,369,1,0,0,0,
        56,374,1,0,0,0,58,386,1,0,0,0,60,396,1,0,0,0,62,408,1,0,0,0,64,417,
        1,0,0,0,66,432,1,0,0,0,68,434,1,0,0,0,70,445,1,0,0,0,72,458,1,0,
        0,0,74,460,1,0,0,0,76,466,1,0,0,0,78,473,1,0,0,0,80,475,1,0,0,0,
        82,486,1,0,0,0,84,497,1,0,0,0,86,505,1,0,0,0,88,521,1,0,0,0,90,523,
        1,0,0,0,92,537,1,0,0,0,94,543,1,0,0,0,96,551,1,0,0,0,98,553,1,0,
        0,0,100,558,1,0,0,0,102,560,1,0,0,0,104,574,1,0,0,0,106,576,1,0,
        0,0,108,580,1,0,0,0,110,589,1,0,0,0,112,596,1,0,0,0,114,604,1,0,
        0,0,116,609,1,0,0,0,118,617,1,0,0,0,120,623,1,0,0,0,122,625,1,0,
        0,0,124,629,1,0,0,0,126,643,1,0,0,0,128,659,1,0,0,0,130,661,1,0,
        0,0,132,663,1,0,0,0,134,671,1,0,0,0,136,679,1,0,0,0,138,687,1,0,
        0,0,140,693,1,0,0,0,142,701,1,0,0,0,144,723,1,0,0,0,146,732,1,0,
        0,0,148,734,1,0,0,0,150,744,1,0,0,0,152,153,5,1,0,0,153,154,5,64,
        0,0,154,158,5,45,0,0,155,157,3,2,1,0,156,155,1,0,0,0,157,160,1,0,
        0,0,158,156,1,0,0,0,158,159,1,0,0,0,159,161,1,0,0,0,160,158,1,0,
        0,0,161,162,3,82,41,0,162,163,5,42,0,0,163,1,1,0,0,0,164,171,3,6,
        3,0,165,171,3,14,7,0,166,171,3,74,37,0,167,171,3,58,29,0,168,171,
        3,56,28,0,169,171,3,4,2,0,170,164,1,0,0,0,170,165,1,0,0,0,170,166,
        1,0,0,0,170,167,1,0,0,0,170,168,1,0,0,0,170,169,1,0,0,0,171,3,1,
        0,0,0,172,173,5,38,0,0,173,174,5,64,0,0,174,175,5,42,0,0,175,177,
        5,64,0,0,176,178,3,60,30,0,177,176,1,0,0,0,177,178,1,0,0,0,178,179,
        1,0,0,0,179,180,5,45,0,0,180,182,3,82,41,0,181,183,5,45,0,0,182,
        181,1,0,0,0,182,183,1,0,0,0,183,197,1,0,0,0,184,185,5,39,0,0,185,
        186,5,64,0,0,186,187,5,42,0,0,187,189,5,64,0,0,188,190,3,60,30,0,
        189,188,1,0,0,0,189,190,1,0,0,0,190,191,1,0,0,0,191,192,5,45,0,0,
        192,194,3,82,41,0,193,195,5,45,0,0,194,193,1,0,0,0,194,195,1,0,0,
        0,195,197,1,0,0,0,196,172,1,0,0,0,196,184,1,0,0,0,197,5,1,0,0,0,
        198,200,5,4,0,0,199,201,3,8,4,0,200,199,1,0,0,0,201,202,1,0,0,0,
        202,200,1,0,0,0,202,203,1,0,0,0,203,7,1,0,0,0,204,209,3,10,5,0,205,
        206,5,46,0,0,206,208,3,10,5,0,207,205,1,0,0,0,208,211,1,0,0,0,209,
        207,1,0,0,0,209,210,1,0,0,0,210,212,1,0,0,0,211,209,1,0,0,0,212,
        213,5,45,0,0,213,9,1,0,0,0,214,215,5,64,0,0,215,216,5,57,0,0,216,
        217,3,12,6,0,217,11,1,0,0,0,218,219,7,0,0,0,219,13,1,0,0,0,220,222,
        5,6,0,0,221,223,3,16,8,0,222,221,1,0,0,0,223,224,1,0,0,0,224,222,
        1,0,0,0,224,225,1,0,0,0,225,15,1,0,0,0,226,227,5,64,0,0,227,228,
        5,57,0,0,228,229,3,42,21,0,229,230,5,45,0,0,230,236,1,0,0,0,231,
        236,3,46,23,0,232,236,3,52,26,0,233,236,3,32,16,0,234,236,3,18,9,
        0,235,226,1,0,0,0,235,231,1,0,0,0,235,232,1,0,0,0,235,233,1,0,0,
        0,235,234,1,0,0,0,236,17,1,0,0,0,237,238,5,64,0,0,238,239,5,57,0,
        0,239,241,5,37,0,0,240,242,3,20,10,0,241,240,1,0,0,0,241,242,1,0,
        0,0,242,243,1,0,0,0,243,244,3,22,11,0,244,245,5,3,0,0,245,246,5,
        45,0,0,246,19,1,0,0,0,247,248,5,52,0,0,248,249,5,64,0,0,249,250,
        5,53,0,0,250,21,1,0,0,0,251,253,3,24,12,0,252,251,1,0,0,0,253,256,
        1,0,0,0,254,252,1,0,0,0,254,255,1,0,0,0,255,23,1,0,0,0,256,254,1,
        0,0,0,257,261,3,26,13,0,258,261,3,28,14,0,259,261,3,30,15,0,260,
        257,1,0,0,0,260,258,1,0,0,0,260,259,1,0,0,0,261,25,1,0,0,0,262,263,
        3,80,40,0,263,264,5,44,0,0,264,265,3,42,21,0,265,266,5,45,0,0,266,
        27,1,0,0,0,267,268,5,38,0,0,268,270,5,64,0,0,269,271,3,60,30,0,270,
        269,1,0,0,0,270,271,1,0,0,0,271,272,1,0,0,0,272,273,5,45,0,0,273,
        29,1,0,0,0,274,275,5,39,0,0,275,277,5,64,0,0,276,278,3,60,30,0,277,
        276,1,0,0,0,277,278,1,0,0,0,278,279,1,0,0,0,279,280,5,45,0,0,280,
        31,1,0,0,0,281,282,5,64,0,0,282,283,5,57,0,0,283,285,3,38,19,0,284,
        286,3,34,17,0,285,284,1,0,0,0,285,286,1,0,0,0,286,287,1,0,0,0,287,
        288,5,45,0,0,288,33,1,0,0,0,289,290,5,57,0,0,290,292,5,52,0,0,291,
        293,3,36,18,0,292,291,1,0,0,0,292,293,1,0,0,0,293,294,1,0,0,0,294,
        295,5,53,0,0,295,35,1,0,0,0,296,301,3,12,6,0,297,298,5,46,0,0,298,
        300,3,12,6,0,299,297,1,0,0,0,300,303,1,0,0,0,301,299,1,0,0,0,301,
        302,1,0,0,0,302,305,1,0,0,0,303,301,1,0,0,0,304,306,5,46,0,0,305,
        304,1,0,0,0,305,306,1,0,0,0,306,37,1,0,0,0,307,308,5,8,0,0,308,309,
        5,51,0,0,309,314,3,40,20,0,310,311,5,46,0,0,311,313,3,40,20,0,312,
        310,1,0,0,0,313,316,1,0,0,0,314,312,1,0,0,0,314,315,1,0,0,0,315,
        317,1,0,0,0,316,314,1,0,0,0,317,318,5,54,0,0,318,319,5,9,0,0,319,
        320,3,42,21,0,320,325,1,0,0,0,321,322,5,8,0,0,322,323,5,9,0,0,323,
        325,3,42,21,0,324,307,1,0,0,0,324,321,1,0,0,0,325,39,1,0,0,0,326,
        327,3,130,65,0,327,328,5,41,0,0,328,329,3,130,65,0,329,41,1,0,0,
        0,330,334,3,44,22,0,331,332,5,55,0,0,332,334,3,44,22,0,333,330,1,
        0,0,0,333,331,1,0,0,0,334,43,1,0,0,0,335,336,7,1,0,0,336,45,1,0,
        0,0,337,338,5,64,0,0,338,339,5,57,0,0,339,340,5,52,0,0,340,341,3,
        48,24,0,341,342,5,53,0,0,342,343,5,45,0,0,343,47,1,0,0,0,344,349,
        3,50,25,0,345,346,5,46,0,0,346,348,3,50,25,0,347,345,1,0,0,0,348,
        351,1,0,0,0,349,347,1,0,0,0,349,350,1,0,0,0,350,49,1,0,0,0,351,349,
        1,0,0,0,352,355,5,64,0,0,353,354,5,57,0,0,354,356,5,67,0,0,355,353,
        1,0,0,0,355,356,1,0,0,0,356,51,1,0,0,0,357,358,5,64,0,0,358,359,
        5,57,0,0,359,363,5,7,0,0,360,362,3,54,27,0,361,360,1,0,0,0,362,365,
        1,0,0,0,363,361,1,0,0,0,363,364,1,0,0,0,364,366,1,0,0,0,365,363,
        1,0,0,0,366,367,5,3,0,0,367,368,5,45,0,0,368,53,1,0,0,0,369,370,
        3,80,40,0,370,371,5,44,0,0,371,372,3,42,21,0,372,373,5,45,0,0,373,
        55,1,0,0,0,374,375,5,31,0,0,375,377,5,64,0,0,376,378,3,60,30,0,377,
        376,1,0,0,0,377,378,1,0,0,0,378,379,1,0,0,0,379,380,5,44,0,0,380,
        381,3,42,21,0,381,382,5,45,0,0,382,384,3,82,41,0,383,385,5,45,0,
        0,384,383,1,0,0,0,384,385,1,0,0,0,385,57,1,0,0,0,386,387,5,30,0,
        0,387,389,5,64,0,0,388,390,3,60,30,0,389,388,1,0,0,0,389,390,1,0,
        0,0,390,391,1,0,0,0,391,392,5,45,0,0,392,394,3,82,41,0,393,395,5,
        45,0,0,394,393,1,0,0,0,394,395,1,0,0,0,395,59,1,0,0,0,396,397,5,
        52,0,0,397,402,3,62,31,0,398,399,5,45,0,0,399,401,3,62,31,0,400,
        398,1,0,0,0,401,404,1,0,0,0,402,400,1,0,0,0,402,403,1,0,0,0,403,
        405,1,0,0,0,404,402,1,0,0,0,405,406,5,53,0,0,406,61,1,0,0,0,407,
        409,5,5,0,0,408,407,1,0,0,0,408,409,1,0,0,0,409,410,1,0,0,0,410,
        411,3,80,40,0,411,412,5,44,0,0,412,413,3,42,21,0,413,63,1,0,0,0,
        414,418,3,74,37,0,415,418,3,58,29,0,416,418,3,56,28,0,417,414,1,
        0,0,0,417,415,1,0,0,0,417,416,1,0,0,0,418,65,1,0,0,0,419,422,5,64,
        0,0,420,421,5,42,0,0,421,423,5,64,0,0,422,420,1,0,0,0,422,423,1,
        0,0,0,423,424,1,0,0,0,424,426,5,52,0,0,425,427,3,112,56,0,426,425,
        1,0,0,0,426,427,1,0,0,0,427,428,1,0,0,0,428,433,5,53,0,0,429,430,
        5,64,0,0,430,431,5,42,0,0,431,433,5,64,0,0,432,419,1,0,0,0,432,429,
        1,0,0,0,433,67,1,0,0,0,434,437,5,64,0,0,435,436,5,42,0,0,436,438,
        5,64,0,0,437,435,1,0,0,0,437,438,1,0,0,0,438,440,1,0,0,0,439,441,
        3,70,35,0,440,439,1,0,0,0,440,441,1,0,0,0,441,443,1,0,0,0,442,444,
        5,45,0,0,443,442,1,0,0,0,443,444,1,0,0,0,444,69,1,0,0,0,445,446,
        5,52,0,0,446,451,3,72,36,0,447,448,5,46,0,0,448,450,3,72,36,0,449,
        447,1,0,0,0,450,453,1,0,0,0,451,449,1,0,0,0,451,452,1,0,0,0,452,
        454,1,0,0,0,453,451,1,0,0,0,454,455,5,53,0,0,455,71,1,0,0,0,456,
        459,5,63,0,0,457,459,3,130,65,0,458,456,1,0,0,0,458,457,1,0,0,0,
        459,73,1,0,0,0,460,462,5,5,0,0,461,463,3,76,38,0,462,461,1,0,0,0,
        463,464,1,0,0,0,464,462,1,0,0,0,464,465,1,0,0,0,465,75,1,0,0,0,466,
        467,3,80,40,0,467,468,5,44,0,0,468,469,3,78,39,0,469,470,5,45,0,
        0,470,77,1,0,0,0,471,474,3,42,21,0,472,474,3,38,19,0,473,471,1,0,
        0,0,473,472,1,0,0,0,474,79,1,0,0,0,475,480,5,64,0,0,476,477,5,46,
        0,0,477,479,5,64,0,0,478,476,1,0,0,0,479,482,1,0,0,0,480,478,1,0,
        0,0,480,481,1,0,0,0,481,81,1,0,0,0,482,480,1,0,0,0,483,485,3,84,
        42,0,484,483,1,0,0,0,485,488,1,0,0,0,486,484,1,0,0,0,486,487,1,0,
        0,0,487,489,1,0,0,0,488,486,1,0,0,0,489,490,5,2,0,0,490,491,3,86,
        43,0,491,492,5,3,0,0,492,83,1,0,0,0,493,498,3,58,29,0,494,498,3,
        56,28,0,495,498,3,74,37,0,496,498,3,6,3,0,497,493,1,0,0,0,497,494,
        1,0,0,0,497,495,1,0,0,0,497,496,1,0,0,0,498,85,1,0,0,0,499,501,3,
        88,44,0,500,502,5,45,0,0,501,500,1,0,0,0,501,502,1,0,0,0,502,504,
        1,0,0,0,503,499,1,0,0,0,504,507,1,0,0,0,505,503,1,0,0,0,505,506,
        1,0,0,0,506,87,1,0,0,0,507,505,1,0,0,0,508,522,3,124,62,0,509,522,
        3,146,73,0,510,522,3,104,52,0,511,522,3,116,58,0,512,522,3,114,57,
        0,513,522,3,110,55,0,514,522,3,108,54,0,515,522,3,100,50,0,516,522,
        3,102,51,0,517,522,3,90,45,0,518,522,3,68,34,0,519,522,3,106,53,
        0,520,522,3,122,61,0,521,508,1,0,0,0,521,509,1,0,0,0,521,510,1,0,
        0,0,521,511,1,0,0,0,521,512,1,0,0,0,521,513,1,0,0,0,521,514,1,0,
        0,0,521,515,1,0,0,0,521,516,1,0,0,0,521,517,1,0,0,0,521,518,1,0,
        0,0,521,519,1,0,0,0,521,520,1,0,0,0,522,89,1,0,0,0,523,524,5,13,
        0,0,524,525,3,130,65,0,525,529,5,9,0,0,526,528,3,92,46,0,527,526,
        1,0,0,0,528,531,1,0,0,0,529,527,1,0,0,0,529,530,1,0,0,0,530,533,
        1,0,0,0,531,529,1,0,0,0,532,534,3,98,49,0,533,532,1,0,0,0,533,534,
        1,0,0,0,534,535,1,0,0,0,535,536,5,3,0,0,536,91,1,0,0,0,537,538,3,
        94,47,0,538,539,5,44,0,0,539,541,3,88,44,0,540,542,5,45,0,0,541,
        540,1,0,0,0,541,542,1,0,0,0,542,93,1,0,0,0,543,548,3,96,48,0,544,
        545,5,46,0,0,545,547,3,96,48,0,546,544,1,0,0,0,547,550,1,0,0,0,548,
        546,1,0,0,0,548,549,1,0,0,0,549,95,1,0,0,0,550,548,1,0,0,0,551,552,
        7,2,0,0,552,97,1,0,0,0,553,554,5,16,0,0,554,556,3,86,43,0,555,557,
        5,45,0,0,556,555,1,0,0,0,556,557,1,0,0,0,557,99,1,0,0,0,558,559,
        5,17,0,0,559,101,1,0,0,0,560,561,5,18,0,0,561,103,1,0,0,0,562,563,
        5,34,0,0,563,564,3,86,43,0,564,565,5,35,0,0,565,566,3,86,43,0,566,
        567,5,3,0,0,567,575,1,0,0,0,568,569,5,34,0,0,569,570,3,86,43,0,570,
        571,5,36,0,0,571,572,3,86,43,0,572,573,5,3,0,0,573,575,1,0,0,0,574,
        562,1,0,0,0,574,568,1,0,0,0,575,105,1,0,0,0,576,578,5,33,0,0,577,
        579,5,45,0,0,578,577,1,0,0,0,578,579,1,0,0,0,579,107,1,0,0,0,580,
        581,5,27,0,0,581,582,5,64,0,0,582,583,5,43,0,0,583,584,3,130,65,
        0,584,585,7,3,0,0,585,586,3,130,65,0,586,587,5,24,0,0,587,588,3,
        88,44,0,588,109,1,0,0,0,589,590,5,25,0,0,590,591,3,86,43,0,591,592,
        5,26,0,0,592,594,3,118,59,0,593,595,5,45,0,0,594,593,1,0,0,0,594,
        595,1,0,0,0,595,111,1,0,0,0,596,601,3,130,65,0,597,598,5,46,0,0,
        598,600,3,130,65,0,599,597,1,0,0,0,600,603,1,0,0,0,601,599,1,0,0,
        0,601,602,1,0,0,0,602,113,1,0,0,0,603,601,1,0,0,0,604,605,5,23,0,
        0,605,606,3,118,59,0,606,607,5,24,0,0,607,608,3,88,44,0,608,115,
        1,0,0,0,609,610,5,14,0,0,610,611,3,118,59,0,611,612,5,15,0,0,612,
        615,3,88,44,0,613,614,5,16,0,0,614,616,3,88,44,0,615,613,1,0,0,0,
        615,616,1,0,0,0,616,117,1,0,0,0,617,621,3,130,65,0,618,619,3,120,
        60,0,619,620,3,130,65,0,620,622,1,0,0,0,621,618,1,0,0,0,621,622,
        1,0,0,0,622,119,1,0,0,0,623,624,7,4,0,0,624,121,1,0,0,0,625,626,
        5,2,0,0,626,627,3,86,43,0,627,628,5,3,0,0,628,123,1,0,0,0,629,630,
        3,126,63,0,630,631,5,43,0,0,631,633,3,130,65,0,632,634,5,45,0,0,
        633,632,1,0,0,0,633,634,1,0,0,0,634,125,1,0,0,0,635,644,5,32,0,0,
        636,640,5,64,0,0,637,639,3,128,64,0,638,637,1,0,0,0,639,642,1,0,
        0,0,640,638,1,0,0,0,640,641,1,0,0,0,641,644,1,0,0,0,642,640,1,0,
        0,0,643,635,1,0,0,0,643,636,1,0,0,0,644,127,1,0,0,0,645,646,5,42,
        0,0,646,660,5,64,0,0,647,648,5,51,0,0,648,653,3,130,65,0,649,650,
        5,46,0,0,650,652,3,130,65,0,651,649,1,0,0,0,652,655,1,0,0,0,653,
        651,1,0,0,0,653,654,1,0,0,0,654,656,1,0,0,0,655,653,1,0,0,0,656,
        657,5,54,0,0,657,660,1,0,0,0,658,660,5,55,0,0,659,645,1,0,0,0,659,
        647,1,0,0,0,659,658,1,0,0,0,660,129,1,0,0,0,661,662,3,132,66,0,662,
        131,1,0,0,0,663,668,3,134,67,0,664,665,5,21,0,0,665,667,3,134,67,
        0,666,664,1,0,0,0,667,670,1,0,0,0,668,666,1,0,0,0,668,669,1,0,0,
        0,669,133,1,0,0,0,670,668,1,0,0,0,671,676,3,136,68,0,672,673,5,22,
        0,0,673,675,3,136,68,0,674,672,1,0,0,0,675,678,1,0,0,0,676,674,1,
        0,0,0,676,677,1,0,0,0,677,135,1,0,0,0,678,676,1,0,0,0,679,684,3,
        138,69,0,680,681,5,20,0,0,681,683,3,138,69,0,682,680,1,0,0,0,683,
        686,1,0,0,0,684,682,1,0,0,0,684,685,1,0,0,0,685,137,1,0,0,0,686,
        684,1,0,0,0,687,691,3,140,70,0,688,689,3,120,60,0,689,690,3,140,
        70,0,690,692,1,0,0,0,691,688,1,0,0,0,691,692,1,0,0,0,692,139,1,0,
        0,0,693,698,3,142,71,0,694,695,7,5,0,0,695,697,3,142,71,0,696,694,
        1,0,0,0,697,700,1,0,0,0,698,696,1,0,0,0,698,699,1,0,0,0,699,141,
        1,0,0,0,700,698,1,0,0,0,701,706,3,144,72,0,702,703,7,6,0,0,703,705,
        3,144,72,0,704,702,1,0,0,0,705,708,1,0,0,0,706,704,1,0,0,0,706,707,
        1,0,0,0,707,143,1,0,0,0,708,706,1,0,0,0,709,710,5,19,0,0,710,724,
        3,144,72,0,711,712,5,56,0,0,712,724,3,126,63,0,713,724,3,126,63,
        0,714,724,3,66,33,0,715,724,5,10,0,0,716,724,5,67,0,0,717,724,5,
        66,0,0,718,724,5,63,0,0,719,720,5,52,0,0,720,721,3,130,65,0,721,
        722,5,53,0,0,722,724,1,0,0,0,723,709,1,0,0,0,723,711,1,0,0,0,723,
        713,1,0,0,0,723,714,1,0,0,0,723,715,1,0,0,0,723,716,1,0,0,0,723,
        717,1,0,0,0,723,718,1,0,0,0,723,719,1,0,0,0,724,145,1,0,0,0,725,
        733,5,40,0,0,726,727,5,40,0,0,727,729,5,52,0,0,728,730,3,148,74,
        0,729,728,1,0,0,0,729,730,1,0,0,0,730,731,1,0,0,0,731,733,5,53,0,
        0,732,725,1,0,0,0,732,726,1,0,0,0,733,147,1,0,0,0,734,739,3,150,
        75,0,735,736,5,46,0,0,736,738,3,150,75,0,737,735,1,0,0,0,738,741,
        1,0,0,0,739,737,1,0,0,0,739,740,1,0,0,0,740,149,1,0,0,0,741,739,
        1,0,0,0,742,745,5,63,0,0,743,745,3,130,65,0,744,742,1,0,0,0,744,
        743,1,0,0,0,745,151,1,0,0,0,76,158,170,177,182,189,194,196,202,209,
        224,235,241,254,260,270,277,285,292,301,305,314,324,333,349,355,
        363,377,384,389,394,402,408,417,422,426,432,437,440,443,451,458,
        464,473,480,486,497,501,505,521,529,533,541,548,556,574,578,594,
        601,615,621,633,640,643,653,659,668,676,684,691,698,706,723,729,
        732,739,744
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
    RULE_classParent = 10
    RULE_classBody = 11
    RULE_classMember = 12
    RULE_classFieldDeclaration = 13
    RULE_constructorDeclaration = 14
    RULE_destructorDeclaration = 15
    RULE_arrayDeclaration = 16
    RULE_arrayInitializer = 17
    RULE_arrayValueList = 18
    RULE_arrayType = 19
    RULE_arrayRange = 20
    RULE_typeName = 21
    RULE_simpleType = 22
    RULE_enumDeclaration = 23
    RULE_enumValueList = 24
    RULE_enumValue = 25
    RULE_recordDeclaration = 26
    RULE_recordFieldDeclaration = 27
    RULE_functionDeclaration = 28
    RULE_procedureDeclaration = 29
    RULE_formalParamList = 30
    RULE_formalParam = 31
    RULE_declaration = 32
    RULE_functionCallExpr = 33
    RULE_procedureCallStatement = 34
    RULE_actualParamList = 35
    RULE_actualParam = 36
    RULE_varSection = 37
    RULE_varDeclaration = 38
    RULE_varType = 39
    RULE_identList = 40
    RULE_block = 41
    RULE_localDeclaration = 42
    RULE_statementList = 43
    RULE_statement = 44
    RULE_caseStatement = 45
    RULE_caseItem = 46
    RULE_caseLabelList = 47
    RULE_caseLabel = 48
    RULE_caseElse = 49
    RULE_breakStatement = 50
    RULE_continueStatement = 51
    RULE_tryStatement = 52
    RULE_exitStatement = 53
    RULE_forStatement = 54
    RULE_repeatStatement = 55
    RULE_argumentList = 56
    RULE_whileStatement = 57
    RULE_ifStatement = 58
    RULE_condition = 59
    RULE_compareOp = 60
    RULE_compoundStatement = 61
    RULE_assignment = 62
    RULE_variableRef = 63
    RULE_variableSuffix = 64
    RULE_expr = 65
    RULE_boolOrExpr = 66
    RULE_boolXorExpr = 67
    RULE_boolAndExpr = 68
    RULE_compareExpr = 69
    RULE_addExpr = 70
    RULE_term = 71
    RULE_factor = 72
    RULE_writeLnStatement = 73
    RULE_writeArgList = 74
    RULE_writeArg = 75

    ruleNames =  [ "programFile", "declarationPart", "classMethodImplementation", 
                   "constSection", "constDeclaration", "constItem", "constValue", 
                   "typeSection", "typeDeclaration", "classDeclaration", 
                   "classParent", "classBody", "classMember", "classFieldDeclaration", 
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
            self.state = 152
            self.match(MiniPascalParser.PROGRAM)
            self.state = 153
            self.match(MiniPascalParser.IDENT)
            self.state = 154
            self.match(MiniPascalParser.SEMI)
            self.state = 158
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 155
                    self.declarationPart() 
                self.state = 160
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 161
            self.block()
            self.state = 162
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
            self.state = 170
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 164
                self.constSection()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 165
                self.typeSection()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 166
                self.varSection()
                pass
            elif token in [30]:
                self.enterOuterAlt(localctx, 4)
                self.state = 167
                self.procedureDeclaration()
                pass
            elif token in [31]:
                self.enterOuterAlt(localctx, 5)
                self.state = 168
                self.functionDeclaration()
                pass
            elif token in [38, 39]:
                self.enterOuterAlt(localctx, 6)
                self.state = 169
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
            self.state = 196
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [38]:
                self.enterOuterAlt(localctx, 1)
                self.state = 172
                self.match(MiniPascalParser.CONSTRUCTOR)
                self.state = 173
                self.match(MiniPascalParser.IDENT)
                self.state = 174
                self.match(MiniPascalParser.DOT)
                self.state = 175
                self.match(MiniPascalParser.IDENT)
                self.state = 177
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==52:
                    self.state = 176
                    self.formalParamList()


                self.state = 179
                self.match(MiniPascalParser.SEMI)
                self.state = 180
                self.block()
                self.state = 182
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==45:
                    self.state = 181
                    self.match(MiniPascalParser.SEMI)


                pass
            elif token in [39]:
                self.enterOuterAlt(localctx, 2)
                self.state = 184
                self.match(MiniPascalParser.DESTRUCTOR)
                self.state = 185
                self.match(MiniPascalParser.IDENT)
                self.state = 186
                self.match(MiniPascalParser.DOT)
                self.state = 187
                self.match(MiniPascalParser.IDENT)
                self.state = 189
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==52:
                    self.state = 188
                    self.formalParamList()


                self.state = 191
                self.match(MiniPascalParser.SEMI)
                self.state = 192
                self.block()
                self.state = 194
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==45:
                    self.state = 193
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
            self.state = 198
            self.match(MiniPascalParser.CONST)
            self.state = 200 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 199
                self.constDeclaration()
                self.state = 202 
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
            self.state = 204
            self.constItem()
            self.state = 209
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 205
                self.match(MiniPascalParser.COMMA)
                self.state = 206
                self.constItem()
                self.state = 211
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 212
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
            self.state = 214
            self.match(MiniPascalParser.IDENT)
            self.state = 215
            self.match(MiniPascalParser.EQ_OP)
            self.state = 216
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
            self.state = 218
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
            self.state = 220
            self.match(MiniPascalParser.TYPE)
            self.state = 222 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 221
                self.typeDeclaration()
                self.state = 224 
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
            self.state = 235
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 226
                self.match(MiniPascalParser.IDENT)
                self.state = 227
                self.match(MiniPascalParser.EQ_OP)
                self.state = 228
                self.typeName()
                self.state = 229
                self.match(MiniPascalParser.SEMI)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 231
                self.enumDeclaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 232
                self.recordDeclaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 233
                self.arrayDeclaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 234
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

        def classParent(self):
            return self.getTypedRuleContext(MiniPascalParser.ClassParentContext,0)


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
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 237
            self.match(MiniPascalParser.IDENT)
            self.state = 238
            self.match(MiniPascalParser.EQ_OP)
            self.state = 239
            self.match(MiniPascalParser.CLASS)
            self.state = 241
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 240
                self.classParent()


            self.state = 243
            self.classBody()
            self.state = 244
            self.match(MiniPascalParser.END)
            self.state = 245
            self.match(MiniPascalParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassParentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(MiniPascalParser.LPAREN, 0)

        def IDENT(self):
            return self.getToken(MiniPascalParser.IDENT, 0)

        def RPAREN(self):
            return self.getToken(MiniPascalParser.RPAREN, 0)

        def getRuleIndex(self):
            return MiniPascalParser.RULE_classParent

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassParent" ):
                listener.enterClassParent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassParent" ):
                listener.exitClassParent(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassParent" ):
                return visitor.visitClassParent(self)
            else:
                return visitor.visitChildren(self)




    def classParent(self):

        localctx = MiniPascalParser.ClassParentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_classParent)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 247
            self.match(MiniPascalParser.LPAREN)
            self.state = 248
            self.match(MiniPascalParser.IDENT)
            self.state = 249
            self.match(MiniPascalParser.RPAREN)
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
        self.enterRule(localctx, 22, self.RULE_classBody)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 254
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 38)) & ~0x3f) == 0 and ((1 << (_la - 38)) & 67108867) != 0):
                self.state = 251
                self.classMember()
                self.state = 256
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
        self.enterRule(localctx, 24, self.RULE_classMember)
        try:
            self.state = 260
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [64]:
                self.enterOuterAlt(localctx, 1)
                self.state = 257
                self.classFieldDeclaration()
                pass
            elif token in [38]:
                self.enterOuterAlt(localctx, 2)
                self.state = 258
                self.constructorDeclaration()
                pass
            elif token in [39]:
                self.enterOuterAlt(localctx, 3)
                self.state = 259
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
        self.enterRule(localctx, 26, self.RULE_classFieldDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 262
            self.identList()
            self.state = 263
            self.match(MiniPascalParser.COLON)
            self.state = 264
            self.typeName()
            self.state = 265
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
        self.enterRule(localctx, 28, self.RULE_constructorDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 267
            self.match(MiniPascalParser.CONSTRUCTOR)
            self.state = 268
            self.match(MiniPascalParser.IDENT)
            self.state = 270
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 269
                self.formalParamList()


            self.state = 272
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
        self.enterRule(localctx, 30, self.RULE_destructorDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 274
            self.match(MiniPascalParser.DESTRUCTOR)
            self.state = 275
            self.match(MiniPascalParser.IDENT)
            self.state = 277
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 276
                self.formalParamList()


            self.state = 279
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
        self.enterRule(localctx, 32, self.RULE_arrayDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 281
            self.match(MiniPascalParser.IDENT)
            self.state = 282
            self.match(MiniPascalParser.EQ_OP)
            self.state = 283
            self.arrayType()
            self.state = 285
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==57:
                self.state = 284
                self.arrayInitializer()


            self.state = 287
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
        self.enterRule(localctx, 34, self.RULE_arrayInitializer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 289
            self.match(MiniPascalParser.EQ_OP)
            self.state = 290
            self.match(MiniPascalParser.LPAREN)
            self.state = 292
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 63)) & ~0x3f) == 0 and ((1 << (_la - 63)) & 25) != 0):
                self.state = 291
                self.arrayValueList()


            self.state = 294
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
        self.enterRule(localctx, 36, self.RULE_arrayValueList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 296
            self.constValue()
            self.state = 301
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,18,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 297
                    self.match(MiniPascalParser.COMMA)
                    self.state = 298
                    self.constValue() 
                self.state = 303
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,18,self._ctx)

            self.state = 305
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==46:
                self.state = 304
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
        self.enterRule(localctx, 38, self.RULE_arrayType)
        self._la = 0 # Token type
        try:
            self.state = 324
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 307
                self.match(MiniPascalParser.ARRAY)
                self.state = 308
                self.match(MiniPascalParser.LBRACK)
                self.state = 309
                self.arrayRange()
                self.state = 314
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==46:
                    self.state = 310
                    self.match(MiniPascalParser.COMMA)
                    self.state = 311
                    self.arrayRange()
                    self.state = 316
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 317
                self.match(MiniPascalParser.RBRACK)
                self.state = 318
                self.match(MiniPascalParser.OF)
                self.state = 319
                self.typeName()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 321
                self.match(MiniPascalParser.ARRAY)
                self.state = 322
                self.match(MiniPascalParser.OF)
                self.state = 323
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
        self.enterRule(localctx, 40, self.RULE_arrayRange)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 326
            self.expr()
            self.state = 327
            self.match(MiniPascalParser.DOTDOT)
            self.state = 328
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
        self.enterRule(localctx, 42, self.RULE_typeName)
        try:
            self.state = 333
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11, 12, 63, 64]:
                self.enterOuterAlt(localctx, 1)
                self.state = 330
                self.simpleType()
                pass
            elif token in [55]:
                self.enterOuterAlt(localctx, 2)
                self.state = 331
                self.match(MiniPascalParser.CARET)
                self.state = 332
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
        self.enterRule(localctx, 44, self.RULE_simpleType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 335
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
        self.enterRule(localctx, 46, self.RULE_enumDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 337
            self.match(MiniPascalParser.IDENT)
            self.state = 338
            self.match(MiniPascalParser.EQ_OP)
            self.state = 339
            self.match(MiniPascalParser.LPAREN)
            self.state = 340
            self.enumValueList()
            self.state = 341
            self.match(MiniPascalParser.RPAREN)
            self.state = 342
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
        self.enterRule(localctx, 48, self.RULE_enumValueList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 344
            self.enumValue()
            self.state = 349
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 345
                self.match(MiniPascalParser.COMMA)
                self.state = 346
                self.enumValue()
                self.state = 351
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
        self.enterRule(localctx, 50, self.RULE_enumValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 352
            self.match(MiniPascalParser.IDENT)
            self.state = 355
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==57:
                self.state = 353
                self.match(MiniPascalParser.EQ_OP)
                self.state = 354
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
        self.enterRule(localctx, 52, self.RULE_recordDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 357
            self.match(MiniPascalParser.IDENT)
            self.state = 358
            self.match(MiniPascalParser.EQ_OP)
            self.state = 359
            self.match(MiniPascalParser.RECORD)
            self.state = 363
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==64:
                self.state = 360
                self.recordFieldDeclaration()
                self.state = 365
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 366
            self.match(MiniPascalParser.END)
            self.state = 367
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
        self.enterRule(localctx, 54, self.RULE_recordFieldDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 369
            self.identList()
            self.state = 370
            self.match(MiniPascalParser.COLON)
            self.state = 371
            self.typeName()
            self.state = 372
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
        self.enterRule(localctx, 56, self.RULE_functionDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 374
            self.match(MiniPascalParser.FUNCTION)
            self.state = 375
            self.match(MiniPascalParser.IDENT)
            self.state = 377
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 376
                self.formalParamList()


            self.state = 379
            self.match(MiniPascalParser.COLON)
            self.state = 380
            self.typeName()
            self.state = 381
            self.match(MiniPascalParser.SEMI)
            self.state = 382
            self.block()
            self.state = 384
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 383
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
        self.enterRule(localctx, 58, self.RULE_procedureDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 386
            self.match(MiniPascalParser.PROCEDURE)
            self.state = 387
            self.match(MiniPascalParser.IDENT)
            self.state = 389
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 388
                self.formalParamList()


            self.state = 391
            self.match(MiniPascalParser.SEMI)
            self.state = 392
            self.block()
            self.state = 394
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 393
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
        self.enterRule(localctx, 60, self.RULE_formalParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 396
            self.match(MiniPascalParser.LPAREN)
            self.state = 397
            self.formalParam()
            self.state = 402
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==45:
                self.state = 398
                self.match(MiniPascalParser.SEMI)
                self.state = 399
                self.formalParam()
                self.state = 404
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 405
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
        self.enterRule(localctx, 62, self.RULE_formalParam)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 408
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 407
                self.match(MiniPascalParser.VAR)


            self.state = 410
            self.identList()
            self.state = 411
            self.match(MiniPascalParser.COLON)
            self.state = 412
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
        self.enterRule(localctx, 64, self.RULE_declaration)
        try:
            self.state = 417
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 414
                self.varSection()
                pass
            elif token in [30]:
                self.enterOuterAlt(localctx, 2)
                self.state = 415
                self.procedureDeclaration()
                pass
            elif token in [31]:
                self.enterOuterAlt(localctx, 3)
                self.state = 416
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
        self.enterRule(localctx, 66, self.RULE_functionCallExpr)
        self._la = 0 # Token type
        try:
            self.state = 432
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,35,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 419
                self.match(MiniPascalParser.IDENT)
                self.state = 422
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==42:
                    self.state = 420
                    self.match(MiniPascalParser.DOT)
                    self.state = 421
                    self.match(MiniPascalParser.IDENT)


                self.state = 424
                self.match(MiniPascalParser.LPAREN)
                self.state = 426
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 10)) & ~0x3f) == 0 and ((1 << (_la - 10)) & 243269146672890369) != 0):
                    self.state = 425
                    self.argumentList()


                self.state = 428
                self.match(MiniPascalParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 429
                self.match(MiniPascalParser.IDENT)
                self.state = 430
                self.match(MiniPascalParser.DOT)
                self.state = 431
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
        self.enterRule(localctx, 68, self.RULE_procedureCallStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 434
            self.match(MiniPascalParser.IDENT)
            self.state = 437
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==42:
                self.state = 435
                self.match(MiniPascalParser.DOT)
                self.state = 436
                self.match(MiniPascalParser.IDENT)


            self.state = 440
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 439
                self.actualParamList()


            self.state = 443
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,38,self._ctx)
            if la_ == 1:
                self.state = 442
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
        self.enterRule(localctx, 70, self.RULE_actualParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 445
            self.match(MiniPascalParser.LPAREN)
            self.state = 446
            self.actualParam()
            self.state = 451
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 447
                self.match(MiniPascalParser.COMMA)
                self.state = 448
                self.actualParam()
                self.state = 453
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 454
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
        self.enterRule(localctx, 72, self.RULE_actualParam)
        try:
            self.state = 458
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,40,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 456
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 457
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
        self.enterRule(localctx, 74, self.RULE_varSection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 460
            self.match(MiniPascalParser.VAR)
            self.state = 462 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 461
                self.varDeclaration()
                self.state = 464 
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
        self.enterRule(localctx, 76, self.RULE_varDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 466
            self.identList()
            self.state = 467
            self.match(MiniPascalParser.COLON)
            self.state = 468
            self.varType()
            self.state = 469
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
        self.enterRule(localctx, 78, self.RULE_varType)
        try:
            self.state = 473
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11, 12, 55, 63, 64]:
                self.enterOuterAlt(localctx, 1)
                self.state = 471
                self.typeName()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 2)
                self.state = 472
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
        self.enterRule(localctx, 80, self.RULE_identList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 475
            self.match(MiniPascalParser.IDENT)
            self.state = 480
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 476
                self.match(MiniPascalParser.COMMA)
                self.state = 477
                self.match(MiniPascalParser.IDENT)
                self.state = 482
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
        self.enterRule(localctx, 82, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 486
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 3221225520) != 0):
                self.state = 483
                self.localDeclaration()
                self.state = 488
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 489
            self.match(MiniPascalParser.BEGIN_)
            self.state = 490
            self.statementList()
            self.state = 491
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
        self.enterRule(localctx, 84, self.RULE_localDeclaration)
        try:
            self.state = 497
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [30]:
                self.enterOuterAlt(localctx, 1)
                self.state = 493
                self.procedureDeclaration()
                pass
            elif token in [31]:
                self.enterOuterAlt(localctx, 2)
                self.state = 494
                self.functionDeclaration()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 495
                self.varSection()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 496
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
        self.enterRule(localctx, 86, self.RULE_statementList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 505
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 2)) & ~0x3f) == 0 and ((1 << (_la - 2)) & 4611686300865632257) != 0):
                self.state = 499
                self.statement()
                self.state = 501
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,46,self._ctx)
                if la_ == 1:
                    self.state = 500
                    self.match(MiniPascalParser.SEMI)


                self.state = 507
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
        self.enterRule(localctx, 88, self.RULE_statement)
        try:
            self.state = 521
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,48,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 508
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 509
                self.writeLnStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 510
                self.tryStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 511
                self.ifStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 512
                self.whileStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 513
                self.repeatStatement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 514
                self.forStatement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 515
                self.breakStatement()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 516
                self.continueStatement()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 517
                self.caseStatement()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 518
                self.procedureCallStatement()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 519
                self.exitStatement()
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 520
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
        self.enterRule(localctx, 90, self.RULE_caseStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 523
            self.match(MiniPascalParser.CASE)
            self.state = 524
            self.expr()
            self.state = 525
            self.match(MiniPascalParser.OF)
            self.state = 529
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==64 or _la==67:
                self.state = 526
                self.caseItem()
                self.state = 531
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 533
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16:
                self.state = 532
                self.caseElse()


            self.state = 535
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
        self.enterRule(localctx, 92, self.RULE_caseItem)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 537
            self.caseLabelList()
            self.state = 538
            self.match(MiniPascalParser.COLON)
            self.state = 539
            self.statement()
            self.state = 541
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 540
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
        self.enterRule(localctx, 94, self.RULE_caseLabelList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 543
            self.caseLabel()
            self.state = 548
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 544
                self.match(MiniPascalParser.COMMA)
                self.state = 545
                self.caseLabel()
                self.state = 550
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
        self.enterRule(localctx, 96, self.RULE_caseLabel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 551
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
        self.enterRule(localctx, 98, self.RULE_caseElse)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 553
            self.match(MiniPascalParser.ELSE)
            self.state = 554
            self.statementList()
            self.state = 556
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 555
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
        self.enterRule(localctx, 100, self.RULE_breakStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 558
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
        self.enterRule(localctx, 102, self.RULE_continueStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 560
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
        self.enterRule(localctx, 104, self.RULE_tryStatement)
        try:
            self.state = 574
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,54,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 562
                self.match(MiniPascalParser.TRY)
                self.state = 563
                self.statementList()
                self.state = 564
                self.match(MiniPascalParser.FINALLY)
                self.state = 565
                self.statementList()
                self.state = 566
                self.match(MiniPascalParser.END)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 568
                self.match(MiniPascalParser.TRY)
                self.state = 569
                self.statementList()
                self.state = 570
                self.match(MiniPascalParser.EXCEPT)
                self.state = 571
                self.statementList()
                self.state = 572
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
        self.enterRule(localctx, 106, self.RULE_exitStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 576
            self.match(MiniPascalParser.EXIT)
            self.state = 578
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,55,self._ctx)
            if la_ == 1:
                self.state = 577
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
        self.enterRule(localctx, 108, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 580
            self.match(MiniPascalParser.FOR)
            self.state = 581
            self.match(MiniPascalParser.IDENT)
            self.state = 582
            self.match(MiniPascalParser.ASSIGN)
            self.state = 583
            self.expr()
            self.state = 584
            _la = self._input.LA(1)
            if not(_la==28 or _la==29):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 585
            self.expr()
            self.state = 586
            self.match(MiniPascalParser.DO)
            self.state = 587
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
        self.enterRule(localctx, 110, self.RULE_repeatStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 589
            self.match(MiniPascalParser.REPEAT)
            self.state = 590
            self.statementList()
            self.state = 591
            self.match(MiniPascalParser.UNTIL)
            self.state = 592
            self.condition()
            self.state = 594
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,56,self._ctx)
            if la_ == 1:
                self.state = 593
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
        self.enterRule(localctx, 112, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 596
            self.expr()
            self.state = 601
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 597
                self.match(MiniPascalParser.COMMA)
                self.state = 598
                self.expr()
                self.state = 603
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
        self.enterRule(localctx, 114, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 604
            self.match(MiniPascalParser.WHILE)
            self.state = 605
            self.condition()
            self.state = 606
            self.match(MiniPascalParser.DO)
            self.state = 607
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
        self.enterRule(localctx, 116, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 609
            self.match(MiniPascalParser.IF)
            self.state = 610
            self.condition()
            self.state = 611
            self.match(MiniPascalParser.THEN)
            self.state = 612
            self.statement()
            self.state = 615
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,58,self._ctx)
            if la_ == 1:
                self.state = 613
                self.match(MiniPascalParser.ELSE)
                self.state = 614
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
        self.enterRule(localctx, 118, self.RULE_condition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 617
            self.expr()
            self.state = 621
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 9079256848778919936) != 0):
                self.state = 618
                self.compareOp()
                self.state = 619
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
        self.enterRule(localctx, 120, self.RULE_compareOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 623
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
        self.enterRule(localctx, 122, self.RULE_compoundStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 625
            self.match(MiniPascalParser.BEGIN_)
            self.state = 626
            self.statementList()
            self.state = 627
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
        self.enterRule(localctx, 124, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 629
            self.variableRef()
            self.state = 630
            self.match(MiniPascalParser.ASSIGN)
            self.state = 631
            self.expr()
            self.state = 633
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,60,self._ctx)
            if la_ == 1:
                self.state = 632
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
        self.enterRule(localctx, 126, self.RULE_variableRef)
        self._la = 0 # Token type
        try:
            self.state = 643
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [32]:
                self.enterOuterAlt(localctx, 1)
                self.state = 635
                self.match(MiniPascalParser.RESULT)
                pass
            elif token in [64]:
                self.enterOuterAlt(localctx, 2)
                self.state = 636
                self.match(MiniPascalParser.IDENT)
                self.state = 640
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 38284994879160320) != 0):
                    self.state = 637
                    self.variableSuffix()
                    self.state = 642
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
        self.enterRule(localctx, 128, self.RULE_variableSuffix)
        self._la = 0 # Token type
        try:
            self.state = 659
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [42]:
                self.enterOuterAlt(localctx, 1)
                self.state = 645
                self.match(MiniPascalParser.DOT)
                self.state = 646
                self.match(MiniPascalParser.IDENT)
                pass
            elif token in [51]:
                self.enterOuterAlt(localctx, 2)
                self.state = 647
                self.match(MiniPascalParser.LBRACK)
                self.state = 648
                self.expr()
                self.state = 653
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==46:
                    self.state = 649
                    self.match(MiniPascalParser.COMMA)
                    self.state = 650
                    self.expr()
                    self.state = 655
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 656
                self.match(MiniPascalParser.RBRACK)
                pass
            elif token in [55]:
                self.enterOuterAlt(localctx, 3)
                self.state = 658
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
        self.enterRule(localctx, 130, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 661
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
        self.enterRule(localctx, 132, self.RULE_boolOrExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 663
            self.boolXorExpr()
            self.state = 668
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==21:
                self.state = 664
                self.match(MiniPascalParser.OR)
                self.state = 665
                self.boolXorExpr()
                self.state = 670
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
        self.enterRule(localctx, 134, self.RULE_boolXorExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 671
            self.boolAndExpr()
            self.state = 676
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==22:
                self.state = 672
                self.match(MiniPascalParser.XOR)
                self.state = 673
                self.boolAndExpr()
                self.state = 678
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
        self.enterRule(localctx, 136, self.RULE_boolAndExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 679
            self.compareExpr()
            self.state = 684
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==20:
                self.state = 680
                self.match(MiniPascalParser.AND)
                self.state = 681
                self.compareExpr()
                self.state = 686
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
        self.enterRule(localctx, 138, self.RULE_compareExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 687
            self.addExpr()
            self.state = 691
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,68,self._ctx)
            if la_ == 1:
                self.state = 688
                self.compareOp()
                self.state = 689
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
        self.enterRule(localctx, 140, self.RULE_addExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 693
            self.term()
            self.state = 698
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==47 or _la==48:
                self.state = 694
                _la = self._input.LA(1)
                if not(_la==47 or _la==48):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 695
                self.term()
                self.state = 700
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
        self.enterRule(localctx, 142, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 701
            self.factor()
            self.state = 706
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==49 or _la==50:
                self.state = 702
                _la = self._input.LA(1)
                if not(_la==49 or _la==50):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 703
                self.factor()
                self.state = 708
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
        self.enterRule(localctx, 144, self.RULE_factor)
        try:
            self.state = 723
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,71,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 709
                self.match(MiniPascalParser.NOT)
                self.state = 710
                self.factor()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 711
                self.match(MiniPascalParser.AT)
                self.state = 712
                self.variableRef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 713
                self.variableRef()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 714
                self.functionCallExpr()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 715
                self.match(MiniPascalParser.NIL)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 716
                self.match(MiniPascalParser.NUMBER)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 717
                self.match(MiniPascalParser.FLOATNUMBER)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 718
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 719
                self.match(MiniPascalParser.LPAREN)
                self.state = 720
                self.expr()
                self.state = 721
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
        self.enterRule(localctx, 146, self.RULE_writeLnStatement)
        self._la = 0 # Token type
        try:
            self.state = 732
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,73,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 725
                self.match(MiniPascalParser.WRITELN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 726
                self.match(MiniPascalParser.WRITELN)
                self.state = 727
                self.match(MiniPascalParser.LPAREN)
                self.state = 729
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 10)) & ~0x3f) == 0 and ((1 << (_la - 10)) & 243269146672890369) != 0):
                    self.state = 728
                    self.writeArgList()


                self.state = 731
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
        self.enterRule(localctx, 148, self.RULE_writeArgList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 734
            self.writeArg()
            self.state = 739
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 735
                self.match(MiniPascalParser.COMMA)
                self.state = 736
                self.writeArg()
                self.state = 741
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
        self.enterRule(localctx, 150, self.RULE_writeArg)
        try:
            self.state = 744
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,75,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 742
                self.match(MiniPascalParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 743
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





