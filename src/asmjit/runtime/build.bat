mkdir obj
g++     -m64 -std=c++20 -x c++-header dbase2many.hpp -o dbase2many.hpp.gch
g++ -O2 -m64 -std=c++20 -c -o obj/error.o error.cc

ar rcs libdBase2Many.a obj/*.o
