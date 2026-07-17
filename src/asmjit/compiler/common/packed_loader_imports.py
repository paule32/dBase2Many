# ---------------------------------------------------------------------------
# File: packed_loader_imports.py
# ---------------------------------------------------------------------------
from __future__ import annotations

PACKED_DLL_LOADER_IMPORTS = {
    "kernel32.dll": [
        {"symbol": "__imp__CloseHandle@4",       "name": "CloseHandle"},
        {"symbol": "__imp__CreateFileA@28",      "name": "CreateFileA"},
        {"symbol": "__imp__DeleteFileA@4",       "name": "DeleteFileA"},
        {"symbol": "__imp__FindResourceA@12",    "name": "FindResourceA"},
        {"symbol": "__imp__FreeLibrary@4",       "name": "FreeLibrary"},
        {"symbol": "__imp__GetLastError@0",      "name": "GetLastError"},
        {"symbol": "__imp__GetModuleHandleA@4",  "name": "GetModuleHandleA"},
        {"symbol": "__imp__GetProcessHeap@0",    "name": "GetProcessHeap"},
        {"symbol": "__imp__GetTempFileNameA@16", "name": "GetTempFileNameA"},
        {"symbol": "__imp__GetTempPathA@8",      "name": "GetTempPathA"},
        {"symbol": "__imp__HeapAlloc@12",        "name": "HeapAlloc"},
        {"symbol": "__imp__HeapFree@12",         "name": "HeapFree"},
        {"symbol": "__imp__LoadLibraryA@4",      "name": "LoadLibraryA"},
        {"symbol": "__imp__LoadResource@8",      "name": "LoadResource"},
        {"symbol": "__imp__LockResource@4",      "name": "LockResource"},
        {"symbol": "__imp__SetLastError@4",      "name": "SetLastError"},
        {"symbol": "__imp__SizeofResource@8",    "name": "SizeofResource"},
        {"symbol": "__imp__WriteFile@20",        "name": "WriteFile"},
        {"symbol": "__imp__lstrcpynA@12",        "name": "lstrcpynA"},
        {"symbol": "__imp__GetProcAddress@8",    "name": "GetProcAddress"},
    ],
}


def install_packed_dll_loader_imports(imports: dict) -> None:
    for dll_name, descriptors in PACKED_DLL_LOADER_IMPORTS.items():
        target = imports.setdefault(dll_name, [])
        known = set()

        for item in target:
            if isinstance(item, dict):
                known.add(item.get("symbol") or item.get("internal_name") or item.get("name"))
            elif isinstance(item, tuple) and item:
                known.add(item[0])
            elif isinstance(item, str):
                known.add(item)

        for descriptor in descriptors:
            symbol = descriptor["symbol"]
            if symbol not in known:
                target.append(dict(descriptor))
                known.add(symbol)
