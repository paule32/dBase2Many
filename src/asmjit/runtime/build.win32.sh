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
  BASEDIR=$(pwd)

  # ------------------------------
  # compile crypto modules ...
  # ------------------------------
  CRYPTO_FILES=(
    blake2 blake3
    crc16  crc32  crc32c crc64 md5
    sha1   sha3   sha224
    sha256 sha384 sha512
  )
  for dir in "${CRYPTO_FILES[@]}"; do
    mkdir -p "win32/obj/crypto/$dir"
    echo "assemble: crypto/$dir/$dir.cc"
    g++ -O2 -m32 -std=c++20 -shared -fPIC -DDLL_BUILD -I$BASEDIR -I. \
    -nostdinc -fno-exceptions -fno-rtti -nostdlib++ \
    -S -o win32/obj/crypto/$dir/$dir.s crypto/$dir/$dir.cc
    echo "sed:      win32/obj/crypto/$dir/$dir.s"
    sed -i \
      -e '/^[[:space:]]*\.ident/d'     \
      -e '/^[[:space:]]*\.file/d'      \
      -e '/^[[:space:]]*\.linkonce/d'  \
      -e '/^[[:space:]]*\.def/d'       \
      -e '/^[[:space:]]*\.cfi_/d'      \
      -e 's/\(\.section[[:space:]]*\.text\)\$.*/\1/' \
      -e '/^[[:space:]]*\.section[[:space:]]*\.note\.GNU\-stack/d' \
      win32/obj/crypto/$dir/$dir.s
    echo "compile:  win32/obj/crypto/$dir/$dir.s"
    g++ -o win32/obj/crypto/$dir/$dir.o -c win32/obj/crypto/$dir/$dir.s
  done
  
  RUNTIME_FILES=(
    loader allocator diskio/diskio exception iostream vector windows
  )
  mkdir -p win32/obj/diskio
  for file in "${RUNTIME_FILES[@]}"; do
    echo "assemble: $file.cc"
    g++ -O2 -m32 -std=c++20 -shared -fPIC -DDLL_BUILD -I$BASEDIR -I. \
    -nostdinc -fno-exceptions -fno-rtti -nostdlib++ \
    -S -o win32/obj/$file.s $file.cc
    echo "sed:      $file.s"
    sed -i \
        -e '/^[[:space:]]*\.ident/d'     \
        -e '/^[[:space:]]*\.file/d'      \
        -e '/^[[:space:]]*\.linkonce/d'  \
        -e '/^[[:space:]]*\.def/d'       \
        -e '/^[[:space:]]*\.cfi_/d'      \
        -e 's/\(\.section[[:space:]]*\.text\)\$.*/\1/' \
        -e '/^[[:space:]]*\.section[[:space:]]*\.note\.GNU\-stack/d' win32/obj/$file.s
    echo "compile:  $file.s"
    g++ -o win32/obj/$file.o -c win32/obj/$file.s
  done
  
  exit 0
  echo "assemble: vector.cc"; g++ -O2 -m32 -std=c++20 -shared -DDLL_BUILD -fPIC \
  -nostdinc -fno-exceptions -fno-rtti -nostdlib++ \
  -S -o win32/obj/vector.s vector.cc
  echo "sed:      vector.s"
  sed -i \
      -e '/^[[:space:]]*\.ident/d'     \
      -e '/^[[:space:]]*\.file/d'      \
      -e '/^[[:space:]]*\.linkonce/d'  \
      -e '/^[[:space:]]*\.def/d'       \
      -e '/^[[:space:]]*\.cfi_/d'      \
      -e 's/\(\.section[[:space:]]*\.text\)\$.*/\1/' \
      -e '/^[[:space:]]*\.section[[:space:]]*\.note\.GNU\-stack/d' win32/obj/vector.s
  echo "compile:  vector.s"
  g++ -o win32/obj/vector.o -c win32/obj/vector.s

  echo "assemble: iostream.cc"; g++ -O2 -m32 -std=c++20 -shared -DDLL_BUILD -fPIC \
  -nostdinc -fno-exceptions -fno-rtti -nostdlib++ \
  -S -o win32/obj/iostream.s iostream.cc
  echo "sed:      iostream.s"
  sed -i \
      -e '/^[[:space:]]*\.ident/d'     \
      -e '/^[[:space:]]*\.file/d'      \
      -e '/^[[:space:]]*\.linkonce/d'  \
      -e '/^[[:space:]]*\.def/d'       \
      -e '/^[[:space:]]*\.cfi_/d'      \
      -e 's/\(\.section[[:space:]]*\.text\)\$.*/\1/' \
      -e '/^[[:space:]]*\.section[[:space:]]*\.note\.GNU\-stack/d' win32/obj/iostream.s
  echo "compile:  iostream.s"
  g++ -o win32/obj/iostream.o -c win32/obj/iostream.s
  
  echo "assemble: print.cc"; g++ -O2 -m32 -std=c++20 -shared -DDLL_BUILD -fPIC \
  -nostdinc -fno-exceptions -fno-rtti -nostdlib++ \
  -S -o win32/obj/print.s print.cc
  echo "sed:      print.s"
  sed -i \
      -e '/^[[:space:]]*\.ident/d'     \
      -e '/^[[:space:]]*\.file/d'      \
      -e '/^[[:space:]]*\.linkonce/d'  \
      -e '/^[[:space:]]*\.def/d'       \
      -e '/^[[:space:]]*\.cfi_/d'      \
      -e 's/\(\.section[[:space:]]*\.text\)\$.*/\1/' \
      -e '/^[[:space:]]*\.section[[:space:]]*\.note\.GNU\-stack/d' win32/obj/print.s
  echo "compile:  print.s"
  g++ -o win32/obj/print.o -c win32/obj/print.s
                                                          
  exit 0
  
#  echo "compile: pascal/registry.pas"  ; ./pas2asmjit -Twinnt --backend exe pascal/registry.pas
#  exit 0

  nasm -fwin32 -o setjmp32.o setjmp32.asm
  
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
  rm setjmp32.o
  
  echo "done."
else
  echo "No MingW32 Toolchain - aborted."
  exit 2
fi
