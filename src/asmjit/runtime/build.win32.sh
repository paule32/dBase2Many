#!/bin/bash
# ----------------------------------------------------------------------------
# file: build.sh for 32-bit MingW32
# author: (c) 2026 Jens Kallup - paule32
# all rights reserved.
# ----------------------------------------------------------------------------
export PATH=/mingw32/bin:$PATH
TOOLSYS=$(echo $MSYSTEM)
TARGET=$(gcc -dumpmachine)

# ----------------------------------------------------------------------------
# first, we check if we under mingw32, else - abort ...
# ----------------------------------------------------------------------------
if [ "$TOOLSYS" = "MINGW32" ]; then
  echo "MingW32: ok"
else
  echo "Not in MingW32 Shell - aborted."
  exit 1
fi

# ----------------------------------------------------------------------------
# next, we check if we have gcc 32-bit toolchain, else - abort ...
# ----------------------------------------------------------------------------
if [ "$TARGET" = "i686-w64-mingw32" ]; then
  echo "Toolchain: 32-bit - ok."
  mkdir -p win32/obj

  g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o win32/obj/error.o   error.cc
  g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o win32/obj/print.o   print.cc
  g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o win32/obj/mapping.o mapping.cc
  g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o win32/obj/misc.o    misc.cc
  g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o win32/obj/memory.o  memory.cc
  g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o win32/obj/windows.o windows.cc

  ar rcs win32/libdbase2many.32.a win32/obj/*.o

  g++ -O2 -m32 -std=c++20 -shared -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC win32/obj/*.o -L. -lkernel32 -o libdbase2many.32.dll

  gendef     libdbase2many.32.dll
  dlltool -d libdbase2many.32.def -l libdbase2many.32.dll.a

  cp libdbase2many.32.def   win32/libdbase2many.32.def
  cp libdbase2many.32.dll   win32/libdbase2many.32.dll
  cp libdbase2many.32.dll.a win32/libdbase2many.32.dll.a

  rm libdbase2many.32*
  
else
  echo "No MingW32 Toolchain - aborted."
  exit 2
fi
