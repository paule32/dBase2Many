#!/bin/bash
# ----------------------------------------------------------------------------
# file: build.sh for 32-bit MingW32
# author: (c) 2026 Jens Kallup - paule32
# all rights reserved.
# ----------------------------------------------------------------------------
export PATH=/mingw64/bin:$PATH
mkdir -p win64/obj
#g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -x c++-header dbase2many.hpp -o dbase2many.hpp.gch

g++ -O2 -m64 -std=c++20 -shared -DDLL_EXPORT -fPIC -c -o win64/obj/error.o   error.cc
g++ -O2 -m64 -std=c++20 -shared -DDLL_EXPORT -fPIC -c -o win64/obj/print.o   print.cc
g++ -O2 -m64 -std=c++20 -shared -DDLL_EXPORT -fPIC -c -o win64/obj/mapping.o mapping.cc
g++ -O2 -m64 -std=c++20 -shared -DDLL_EXPORT -fPIC -c -o win64/obj/misc.o    misc.cc
g++ -O2 -m64 -std=c++20 -shared -DDLL_EXPORT -fPIC -c -o win64/obj/memory.o  memory.cc
g++ -O2 -m64 -std=c++20 -shared -DDLL_EXPORT -fPIC -c -o win64/obj/windows.o windows.cc

ar rcs win64/libdBase2Many.64.a win64/obj/*.o

g++ -O2 -m64 -std=c++20 -s -shared -fPIC -Wl,--subsystem,console win64/obj/*.o -L. -lkernel32 -o win64/dbase2many.64.dll

gendef win64/dbase2many.64.dll
cp dbase2many.64.def win32/dbase2many.64.def
rm -f dbase2many.64.def
dlltool -d win64/dbase2many.64.def -l win64/libdbase2many.64.dll.a
