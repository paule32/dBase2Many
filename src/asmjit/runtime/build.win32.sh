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
  mkdir -p win32/obj/crypto/blake2
  mkdir -p win32/obj/crypto/blake3
  mkdir -p win32/obj/crypto/crc16
  mkdir -p win32/obj/crypto/crc32
  mkdir -p win32/obj/crypto/crc32c
  mkdir -p win32/obj/crypto/crc64
  mkdir -p win32/obj/crypto/md5
  mkdir -p win32/obj/crypto/sha1
  mkdir -p win32/obj/crypto/sha3
  mkdir -p win32/obj/crypto/sha224
  mkdir -p win32/obj/crypto/sha256
  mkdir -p win32/obj/crypto/sha384
  mkdir -p win32/obj/crypto/sha512
  
  mkdir -p win32/obj/diskio

  echo "compile: error.cc"  ; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o \
  win32/obj/error.o   error.cc
  
  echo "compile: print.cc"  ; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o \
  win32/obj/print.o   print.cc
  
  echo "compile: mapping.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o \
  win32/obj/mapping.o mapping.cc
  
  echo "compile: misc.cc"   ; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o \
  win32/obj/misc.o    misc.cc
  
  echo "compile: memory.cc" ; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o \
  win32/obj/memory.o  memory.cc
  
  # ----------------------------------------------
  # hash algorythms ...
  # ----------------------------------------------
  echo "compile: crypto/blake2/blake2.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/blake2  -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/blake2/blake2.o crypto/blake2/blake2.cc
  
  echo "compile: crypto/blake3/blake3.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/blake3 -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/blake3/blake3.o crypto/blake3/blake3.cc
  
  echo "compile: crypto/crc16/crc16.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/crc16 -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/crc16/crc16.o crypto/crc16/crc16.cc
  
  echo "compile: crypto/crc32/crc32.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/crc32  -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/crc32/crc32.o crypto/crc32/crc32.cc
  
  echo "compile: crypto/crc32c/crc32c.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/crc32c  -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/crc32c/crc32c.o crypto/crc32c/crc32c.cc
  
  echo "compile: crypto/crc64/crc64.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/crc64 -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/crc64/crc64.o crypto/crc64/crc64.cc
  
  echo "compile: crypto/md5/md5.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/md5 -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/md5/md5.cc.o crypto/md5/md5.cc
  
  echo "compile: crypto/sha1/sha1.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/sha1  -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/sha1/sha1.o crypto/sha1/sha1.cc
  
  echo "compile: crypto/sha3/sha3.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/sha3  -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/sha3/sha3.o crypto/sha3/sha3.cc
    
  echo "compile: crypto/sha224/sha224.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/sha224 -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/sha224/sha224.o crypto/sha223/sha224.cc
  
  echo "compile: crypto/sha256/sha256.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/sha256 -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/sha256/sha256.o crypto/sha256/sha256.cc
  
  echo "compile: crypto/sha384/sha384.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/sha384 -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/sha384/sha384.o crypto/sha384/sha384.cc
  
  echo "compile: crypto/sha512/sha512.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Icrypto/sha512 -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/crypto/sha512/sha512.o crypto/sha512/sha512.cc
  
  # ----------------------------------------------
  # disk informations input output
  # ----------------------------------------------
  echo "compile: diskio/diskio.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF \
  -I. -Idiskio -DDLL_EXPORT -fPIC -c -o  \
  win32/obj/diskio/diskio.o diskio/diskio.cc
          
  # ----------------------------------------------
  # Windows 32-bit API stuff ...
  # ----------------------------------------------
  echo "compile: windows.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o \
  win32/obj/windows.o windows.cc

  echo "create static .a rchive file"
  ar rcs win32/libdbase2many.32.a \
  win32/obj/*.o                \
  win32/obj/crypto/md5/*.o     \
  win32/obj/crypto/sha1/*.o

  echo "create .dll file"
  python makedef.32.py
  g++ -m32 -shared -O2 -fPIC   \
  win32/obj/*.o                \
  win32/obj/crypto/blake2/*.o  \
  win32/obj/crypto/blake3/*.o  \
  win32/obj/crypto/crc16/*.o   \
  win32/obj/crypto/crc32/*.o   \
  win32/obj/crypto/crc32c/*.o  \
  win32/obj/crypto/crc64/*.o   \
  win32/obj/crypto/md5/*.o     \
  win32/obj/crypto/sha1/*.o    \
  win32/obj/crypto/sha3/*.o    \
  win32/obj/crypto/sha224/*.o  \
  win32/obj/crypto/sha256/*.o  \
  win32/obj/crypto/sha384/*.o  \
  win32/obj/crypto/sha512/*.o  \
  win32/obj/diskio/*.o         \
  libdbase2many.32.def -lmpr -o libdbase2many.32.dll

  echo "create dynamic .a rchive file"
  #gendef    libdbase2many.32.dll  > libdbase2many.32.dll.raw
  dlltool -d libdbase2many.32.def -l libdbase2many.32.dll.a

  echo "strip debug informations"
  strip libdbase2many.32.dll

  echo "copy files to win32/"
  cp libdbase2many.32.def   win32/libdbase2many.32.def
  cp libdbase2many.32.dll   win32/libdbase2many.32.dll
  cp libdbase2many.32.dll.a win32/libdbase2many.32.dll.a

  echo "clean up"
  rm libdbase2many.32*
  
  echo "done."
else
  echo "No MingW32 Toolchain - aborted."
  exit 2
fi
