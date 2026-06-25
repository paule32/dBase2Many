#!/bin/bash
# ----------------------------------------------------------------------------
# file: build.sh for 32-bit MingW32
# author: (c) 2026 Jens Kallup - paule32
# all rights reserved.
# ----------------------------------------------------------------------------
export PATH=/mingw32/bin:$PATH
mkdir -p win32/obj
#g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -x c++-header dbase2many.hpp -o dbase2many.hpp.gch

g++ -O2 -m32 -std=c++20 -shared -DDLL_EXPORT -fPIC -c -o win32/obj/error.o   error.cc
g++ -O2 -m32 -std=c++20 -shared -DDLL_EXPORT -fPIC -c -o win32/obj/print.o   print.cc
g++ -O2 -m32 -std=c++20 -shared -DDLL_EXPORT -fPIC -c -o win32/obj/mapping.o mapping.cc
g++ -O2 -m32 -std=c++20 -shared -DDLL_EXPORT -fPIC -c -o win32/obj/misc.o    misc.cc
g++ -O2 -m32 -std=c++20 -shared -DDLL_EXPORT -fPIC -c -o win32/obj/memory.o  memory.cc
g++ -O2 -m32 -std=c++20 -shared -DDLL_EXPORT -fPIC -c -o win32/obj/windows.o windows.cc

ar rcs win32/libdBase2Many.a win32/obj/*.o

g++ -O2 -m32 -std=c++20 -s -shared -fPIC -Wl,--subsystem,console win32/obj/*.o -L. -lkernel32 -o win32/dbase2many.32.dll

gendef win32/dbase2many.32.dll
cp dbase2many.32.def win32/dbase2many.32.def
rm -f dbase2many.32.def
dlltool -d win32/dbase2many.32.def -l win32/libdbase2many.32.dll.a
