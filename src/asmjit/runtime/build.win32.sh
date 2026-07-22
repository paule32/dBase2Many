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
    if ! g++ -O1 -m32 -std=c++20 -shared -fPIC -DDLL_BUILD -I$BASEDIR -I. \
       -nostdinc -fno-exceptions -fno-rtti -nostdlib++ \
       -fno-threadsafe-statics \
       -Wno-write-strings   \
       -fno-builtin-memset  \
       -fno-builtin-memcpy  \
       -fno-builtin-memmove \
       -S -o win32/obj/crypto/$dir/$dir.s crypto/$dir/$dir.cc ; then
       echo "assemble run error."
       exit 1
    fi
    echo "sed:      win32/obj/crypto/$dir/$dir.s"
    if ! sed -i \
       -e '/^[[:space:]]*\.ident/d'     \
       -e '/^[[:space:]]*\.file/d'      \
       -e '/^[[:space:]]*\.linkonce/d'  \
       -e '/^[[:space:]]*\.def/d'       \
       -e '/^[[:space:]]*\.cfi_/d'      \
       -e 's/\(\.section[[:space:]]*\.text\)\$.*/\1/' \
       -e '/^[[:space:]]*\.section[[:space:]]*\.note\.GNU\-stack/d' \
       win32/obj/crypto/$dir/$dir.s ; then
       echo "sed error."
       exit 1
    fi
    echo "compile:  win32/obj/crypto/$dir/$dir.s"
    if ! g++ -o win32/obj/crypto/$dir/$dir.o -c win32/obj/crypto/$dir/$dir.s ; then
       echo "compile time error."
       exit 1
    fi
    # tiny
    if ! nasm -Ox -f win32 -o win32/obj/crypto/$dir/$dir.o crypto/$dir/$dir.asm ; then
       echo "nasm assembler error."
       exit 1
    fi
  done
  
  RUNTIME_FILES=( jitObject
    args loader allocator diskio/diskio error exception iostream memory
    print string vector locale windows
    dllmain
  )
  if ! mkdir -p win32/obj/diskio ; then
     echo "could not create directory: win32/obj/diskio."
     exit 1
  fi
  for file in "${RUNTIME_FILES[@]}"; do
    echo "assemble: $file.cc"
    if ! g++ -O1 -m32 -std=c++20 -shared -fPIC -DDLL_BUILD -I$BASEDIR -I. \
       -nostdinc -fno-exceptions -fno-rtti -nostdlib++ \
       -fno-threadsafe-statics \
       -Wno-write-strings   \
       -fno-builtin-memset  \
       -fno-builtin-memcpy  \
       -fno-builtin-memmove \
       -S -o win32/obj/$file.s $file.cc ; then
       echo "assemble run error."
       exit 1
    fi
    echo "sed:      $file.s"
    if ! sed -i \
       -e '/^[[:space:]]*\.ident/d'     \
       -e '/^[[:space:]]*\.file/d'      \
       -e '/^[[:space:]]*\.linkonce/d'  \
       -e '/^[[:space:]]*\.def/d'       \
       -e '/^[[:space:]]*\.cfi_/d'      \
       -e 's/\(\.section[[:space:]]*\.text\)\$.*/\1/' \
       -e '/^[[:space:]]*\.section[[:space:]]*\.note\.GNU\-stack/d' win32/obj/$file.s ; then
       echo "sed error."
       exit 1
    fi
    echo "compile:  $file.s"
    if ! g++ -o win32/obj/$file.o -c win32/obj/$file.s ; then
       echo "compile time error."
       exit 1
    fi
  done
  
  nasm -fwin32 -o win32/obj/setjmp32.o setjmp32.asm
  
  RUNTIME_OBJECTS=("${RUNTIME_FILES[@]/#/win32/obj/}")
  RUNTIME_OBJECTS=("${RUNTIME_OBJECTS[@]/%/.o}")
  
  echo "create compact DLL..."
  if ! gcc -m32 -fPIC -shared -nostdlib -o win32/libruntime_mini.dll \
     win32/obj/allocator.o \
     win32/obj/args.o      \
     win32/obj/dllmain.o   \
     win32/obj/error.o     \
     win32/obj/exception.o \
     win32/obj/iostream.o  \
     win32/obj/jitObject.o \
     win32/obj/loader.o    \
     win32/obj/locale.o    \
     win32/obj/memory.o    \
     win32/obj/print.o     \
     win32/obj/setjmp32.o  \
     win32/obj/string.o    \
     win32/obj/vector.o    \
     win32/obj/windows.o   \
     win32/libruntime_mini.def \
     -Wl,--out-implib,win32/libruntime_mini.dll.a; then
     echo "relocation link error."
     exit 1
  fi
  strip win32/libruntime_mini.dll
  
  
  if ! nasm -Ox -f win32 -o win32/obj/crypto/sha512/sha512.o crypto/sha512/sha512.asm ; then
       echo "assemlber could not create object file: sha512.o."
       exit 1
  fi
  ar rcs win32/libcrypto.a win32/obj/crypto/sha512/sha512.o
  
  echo "create ALL in One DLL..."
  if ! gcc -m32 -fPIC -shared -nostdlib -o win32/libruntime_all.dll \
     win32/obj/allocator.o \
     win32/obj/args.o      \
     win32/obj/dllmain.o   \
     win32/obj/error.o     \
     win32/obj/exception.o \
     win32/obj/iostream.o  \
     win32/obj/jitObject.o \
     win32/obj/loader.o    \
     win32/obj/locale.o    \
     win32/obj/memory.o    \
     win32/obj/print.o     \
     win32/obj/setjmp32.o  \
     win32/obj/string.o    \
     win32/obj/vector.o    \
     win32/obj/windows.o   \
     \
     win32/obj/crypto/blake2/blake2.o \
     win32/obj/crypto/crc16/crc16.o   \
     win32/obj/crypto/crc32/crc32.o   \
     win32/obj/crypto/crc32c/crc32c.o \
     win32/obj/crypto/crc64/crc64.o   \
     win32/obj/crypto/md5/md5.o       \
     win32/obj/crypto/sha1/sha1.o     \
     win32/obj/crypto/sha3/sha3.o     \
     win32/obj/crypto/sha224/sha224.o \
     win32/obj/crypto/sha256/sha256.o \
     win32/obj/crypto/sha384/sha384.o \
     win32/obj/crypto/sha512/sha512.o \
     \
     win32/obj/diskio/diskio.o        \
     \
     win32/libruntime_all.def   \
     -Wl,--out-implib,win32/libruntime_all.dll.a; then
     echo "relocation link error."
     exit 1
  fi
  strip win32/libruntime_all.dll
    
  
  echo "compact PE32 DLL sections..."
  if ! python compact_pe32_dll.py   \
     win32/libruntime_mini.dll \
     win32/libruntime_mini.dll.c --drop-empty-idata ; then
     echo "PE32:mini compaction failed."
     exit 1
  fi
  if ! python compact_pe32_dll.py   \
     win32/libruntime_all.dll \
     win32/libruntime_all.dll.c --drop-empty-idata ; then
     echo "PE32:all compaction failed."
     exit 1
  fi

  #echo "create, and copy ordinals ..."
  #if ! python makedef.32.py --ignore --python ; then
  #   echo "could not patch import file..."
  #   exit 1
  #fi

  #echo "check python import file..."
  #if ! python -m py_compile \
  #   ../compiler/common/runtime_imports.py \
  #   ../compiler/common/types.py ; then
  #   echo "python: fail -m py_compile"
  #   exit 1
  #fi

  #echo "verify dll exports..."
  #if ! python verify_exports.32.py \
  #   win32/libdbase2many.32.dll    \
  #   ../compiler/frontend/dllimports.py ; then
  #   echo "could not start python."
  #   exit 1
  #fi
  
  echo "packaging PE32:all DLL per zip level 9"
  if ! python pack_dll.py       \
     win32/libruntime_all.dll.c \
     win32/libruntime_all.dll.z --level 9 ; then
     echo "pack PE32 dll failed."
     exit 1
  fi
  echo "packaging PE32:mini DLL per zip level 9"
  if ! python pack_dll.py        \
     win32/libruntime_mini.dll \
     win32/libruntime_mini.dll.z --level 9 ; then
     echo "pack PE32 dll failed."
     exit 1
  fi
  
  echo "create Windows coff32 .o resource"
  echo "#include <windows.h>"                > win32/obj/libruntime_all.rc
  echo "#define IDR_DBASE2MANY_RUNTIME 101" >> win32/obj/libruntime_all.rc
  echo "IDR_DBASE2MANY_RUNTIME RCDATA \"win32/libruntime_all.dll.z\"" >> win32/obj/libruntime_all.rc
  echo "#include <windows.h>"                > win32/obj/libruntime_mini.rc
  echo "#define IDR_DBASE2MANY_RUNTIME 101" >> win32/obj/libruntime_mini.rc
  echo "IDR_DBASE2MANY_RUNTIME RCDATA \"win32/libruntime_mini.dll.z\"" >> win32/obj/libruntime_mini.rc
  if ! windres \
     --input  win32/obj/libruntime_all.rc   \
     --output win32/libruntime_all.o        \
     --output-format=coff  ; then
     echo "error: windres could not create resource file."
     exit 1
  fi
  if ! windres \
     --input  win32/obj/libruntime_mini.rc  \
     --output win32/libruntime_mini.o       \
     --output-format=coff  ; then
     echo "error: windres could not create resource file."
     exit 1
  fi
  if ! cp win32/libruntime_mini.o win32/dll_runtime.o ; then
     echo "could not copy default (mini) runtime"
     exit 1
  fi

  if ! g++ -m32 -O1 -std=c++20 \
           -nostdinc -fno-exceptions -fno-rtti -nostdlib++ \
           -fno-threadsafe-statics \
           -Wno-write-strings   \
           -fno-builtin-memset  \
           -fno-builtin-memcpy  \
           -fno-builtin-memmove \
           -S dll_runtime_bindings.cc \
           -o win32/obj/dll_runtime_bindings.s ; then
       echo "assemble run error."
       exit 1
  fi
  if ! sed -i \
       -e '/^[[:space:]]*\.ident/d'     \
       -e '/^[[:space:]]*\.file/d'      \
       -e '/^[[:space:]]*\.linkonce/d'  \
       -e '/^[[:space:]]*\.def/d'       \
       -e '/^[[:space:]]*\.cfi_/d'      \
       -e 's/\(\.section[[:space:]]*\.text\)\$.*/\1/' \
       -e '/^[[:space:]]*\.section[[:space:]]*\.note\.GNU\-stack/d' win32/obj/dll_runtime_bindings.s ; then
       echo "sed error."
       exit 1
  fi
  if ! gcc -o win32/dll_runtime_bindings.o -c win32/obj/dll_runtime_bindings.s ; then
       echo "gcc could not create dll_runtime_bindings.o"
       exit 1
  fi

  echo "create faked zlib..."
  if ! g++ -m32 -O1 \
           -nostdinc -fno-exceptions -fno-rtti -nostdlib   \
           -Wno-builtin-declaration-mismatch \
           -fno-threadsafe-statics \
           -Wno-write-strings      \
           -fno-builtin-memset     \
           -fno-builtin-memcpy     \
           -fno-builtin-memmove    \
           \
           -S dll_inflate.cc \
           -o win32/obj/dll_inflate.s  ; then
     echo "assemble run error"
     exit 1
  fi
  if ! sed -i \
       -e '/^[[:space:]]*\.ident/d'     \
       -e '/^[[:space:]]*\.file/d'      \
       -e '/^[[:space:]]*\.linkonce/d'  \
       -e '/^[[:space:]]*\.def/d'       \
       -e '/^[[:space:]]*\.cfi_/d'      \
       -e 's/\(\.section[[:space:]]*\.text\)\$.*/\1/' \
       -e '/^[[:space:]]*\.section[[:space:]]*\.note\.GNU\-stack/d' win32/obj/dll_inflate.s ; then
       echo "sed error."
       exit 1
  fi
  if ! gcc -o win32/dll_inflate.o -c win32/obj/dll_inflate.s ; then
     echo "gcc could not create db_inflate.o"
     exit 1
  fi

  echo "create packed dll loader..."
  if ! g++ -m32 -O1 \
           -nostdinc -fno-exceptions -fno-rtti -nostdlib   \
           -Wno-builtin-declaration-mismatch \
           -fno-threadsafe-statics \
           -Wno-write-strings      \
           -fno-builtin-memset     \
           -fno-builtin-memcpy     \
           -fno-builtin-memmove    \
           \
           -S dll_loader.cc -o win32/obj/dll_loader.s  ; then
     echo "assemble run error"
     exit 1
  fi
  if ! sed -i \
       -e '/^[[:space:]]*\.ident/d'     \
       -e '/^[[:space:]]*\.file/d'      \
       -e '/^[[:space:]]*\.linkonce/d'  \
       -e '/^[[:space:]]*\.def/d'       \
       -e '/^[[:space:]]*\.cfi_/d'      \
       -e 's/\(\.section[[:space:]]*\.text\)\$.*/\1/' \
       -e '/^[[:space:]]*\.section[[:space:]]*\.note\.GNU\-stack/d' win32/obj/dll_loader.s ; then
       echo "sed error."
       exit 1
  fi
  if ! g++ -o win32/dll_loader.o -c win32/obj/dll_loader.s ; then
     echo "g++ could not create packed_dll_loader.o"
     exit 1
  fi

  echo "copy dll file..."
  if ! cp win32/libruntime_all.dll.c ../x32/libruntime_all.dll ; then
     echo "PE32 dll could not be copied."
     exit 1
  fi

  ###
  if ! nasm -f win32 -o win32/dll_inflate.o dll_inflate.asm ; then
       echo "gcc could not create db_inflate.o"
       exit 1
  fi
  if ! nasm -f win32 -o win32/dll_loader.o dll_loader.asm ; then
       echo "gcc could not create db_loader.o"
       exit 1
  fi
  if ! nasm -f win32 -o win32/dll_runtime_thunks.o dll_runtime_thunks.asm ; then
       echo "assemlber could not create object file."
       exit 1
  fi
  if ! nasm -f win32 -o win32/obj/inttostr.o pascal/inttostr.asm ; then
       echo "assemlber could not create object file: inttostr.o."
       exit 1
  fi
  if ! nasm -f win32 -o win32/obj/strtoint.o pascal/strtoint.asm ; then
       echo "assemlber could not create object file: strtoint.o."
       exit 1
  fi
    
  ar rcs win32/libruntime.a        \
      win32/dll_inflate.o \
      win32/dll_loader.o  \
      win32/dll_runtime_bindings.o \
      win32/dll_runtime.o \
      win32/dll_runtime_thunks.o
  ###

  
  #echo "pre-compile python cpascal.py files..."
  #if ! python -m compileall cpascal.py ; then
  #   echo "python: could not run -m compileall"
  #   exit 1
  #fi
  
  echo "done."
  exit 0
  
#  echo "compile: pascal/registry.pas"  ; ./pas2asmjit -Twinnt --backend exe pascal/registry.pas
#  exit 0
  
  echo "compile: error.cc"  ; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o \
  win32/obj/error.o   error.cc
  
  echo "compile: mapping.cc"; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o \
  win32/obj/mapping.o mapping.cc
  
  echo "compile: misc.cc"   ; g++ -O2 -m32 -std=c++20 -shared \
  -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -DDLL_EXPORT -fPIC -c -o \
  win32/obj/misc.o    misc.cc
   
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
