@echo off
set PATH=T:\msys64\mingw64\bin;%CD%;%PATH%
test3.exe
nasm -fwin64 -o test3.o test3.s
