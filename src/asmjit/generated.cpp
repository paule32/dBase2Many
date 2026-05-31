#include <asmjit/asmjit.h>
#include <array>
#include <iostream>

using namespace asmjit;

typedef void (*JitFunc)(int* vars);

int main() {
    JitRuntime rt;
    CodeHolder code;

    code.init(rt.environment());

    x86::Assembler a(&code);

    a.mov(x86::eax, 10);
    a.push(x86::rax);
    a.mov(x86::eax, 20);
    a.pop(x86::rcx);
    a.add(x86::eax, x86::ecx);
    a.mov(x86::dword_ptr(x86::rdi, 0), x86::eax); // x
    a.ret();

    JitFunc fn = nullptr;
    Error err = rt.add(&fn, &code);

    if (err) {
        std::cerr << "AsmJit error: " << DebugUtils::errorAsString(err) << std::endl;
        return 1;
    }

    std::array<int, 1> vars{};
    fn(vars.data());

    std::cout << "x = " << vars[0] << std::endl;

    rt.release(fn);
    return 0;
}

