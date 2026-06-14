:: ----------------------------------------------------------------------------
:: file: build.bat
:: author: (c) 2026 Jens Kallup - paule32
:: all rights reserved.
:: ----------------------------------------------------------------------------
mkdir obj
::g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -x c++-header dbase2many.hpp -o dbase2many.hpp.gch

g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/error.o   error.cc
g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/print.o   print.cc
g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/mapping.o mapping.cc
g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/misc.o    misc.cc
g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/memory.o  memory.cc
g++ -O2 -m64 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o obj/windows.o windows.cc

ar rcs libdBase2Many.a obj/*.o

g++ -O2 -m64 -std=c++20 -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF ^
	-s -shared -fPIC -Wl,--subsystem,windows obj/*.o ^
	-LT:/GitHub/asmjit/build-dll -L. -lasmjit -o dbase2many.dll

gendef dbase2many.dll
dlltool -d dbase2many.def -l libdbase2many.dll.a
