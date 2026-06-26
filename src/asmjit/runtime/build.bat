:: ----------------------------------------------------------------------------
:: file: build.bat
:: author: (c) 2026 Jens Kallup - paule32
:: all rights reserved.
:: ----------------------------------------------------------------------------
mkdir obj
::g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -x c++-header dbase2many.hpp -o dbase2many.hpp.gch

:: 32-Bit
g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/error.32.o   error.cc
g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/print.32.o   print.cc
g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/mapping.32.o mapping.cc
g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/misc.32.o    misc.cc
g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/memory.32.o  memory.cc
g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/windows.32.o windows.cc

:: 64-Bit
g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/error.64.o   error.cc
g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/print.64.o   print.cc
g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/mapping.64.o mapping.cc
g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/misc.64.o    misc.cc
g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/memory.64.o  memory.cc
g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/windows.64.o windows.cc

ar rcs libdBase2Many.32.a obj/*.32.o
ar rcs libdBase2Many.64.a obj/*.64.o

g++ -O2 -m32 -std=c++20 -s -shared -fPIC -Wl,--subsystem,console obj/*.32.o -LT:/msys64/mingw32/lib -L. -lkernel32 -o dbase2many.32.dll
    
g++ -O2 -m64 -std=c++20 -s -shared -fPIC -Wl,--subsystem,console obj/*.64.o  -L. -lkernel32 -o dbase2many.64.dll

gendef dbase2many.32.dll
gendef dbase2many.64.dll

dlltool -d dbase2many.32.def -l libdbase2many.32.dll.a
dlltool -d dbase2many.64.def -l libdbase2many.32.dll.a
