:: ------------------------------------------------------------ 
:: Copyright (c) 2026 by Jens Kallup - paule32 
:: all rights reserved. 
:: ------------------------------------------------------------ 
@echo off 
set PATH=T:\GitHub\dBase2Many\src\asmjit;T:\msys64\mingw64\bin;T:\GitHub\asmjit\build-dll;..\runtime;T:\GitHub\dBase2Many\src\asmjit;T:\GitHub\dBase2Many\src\venv\Scripts;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;T:\Program Files\Git\cmd;T:\Program Files\doxygen\bin;C:\Program Files\dotnet\;T:\Program Files\Inkscape\bin;C:\Users\admin\AppData\Local\Microsoft\WindowsApps;C:\Users\admin\AppData\Local\Python\bin;C:\Users\admin\AppData\Local\GitHubDesktop\bin;T:\Program Files\7-Zip;T:\Program Files\doxygen\bin;C:\Program Files\dotnet\sdk\10.0.203;C:\Program Files\dotnet\shared\Microsoft.NETCore.App\10.0.7;C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App\10.0.7;C:\Users\admin\.dotnet\tools;T:\msys64\usr\bin;T:\mingw64\bin; 

g++ -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -I. -m64 -mconsole -O2 -L../runtime ^
    -nostartfiles ^
    -o test2a.exe test2.o -ldbase2many.dll -lkernel32 ^
    -Wl,-e,_main

echo final exe:
strip test2a.exe
test2a.exe
