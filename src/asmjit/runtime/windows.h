// ---------------------------------------------------------------------------
// File: windows.h
// Note: Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
#ifndef __DBASE2MANY_WINDOWS_HH__
#define __DBASE2MANY_WINDOWS_HH__

# pragma once
# include "stddef.h"

extern "C" {

// --------------------------------------------------------------------
// historical constant's ...
// --------------------------------------------------------------------
constexpr WORD MAX_PATH = 260;

// --------------------------------------------------------------------
// GetLastError()
// --------------------------------------------------------------------
constexpr DWORD NO_ERROR                = 0;
constexpr DWORD ERROR_SUCCESS           = 0;
constexpr DWORD ERROR_FILE_NOT_FOUND    = 2;
constexpr DWORD ERROR_PATH_NOT_FOUND    = 3;
constexpr DWORD ERROR_ACCESS_DENIED     = 5;
constexpr DWORD ERROR_INVALID_HANDLE    = 6;
constexpr DWORD ERROR_INVALID_DRIVE     = 15;
constexpr DWORD ERROR_NOT_READY         = 21;
constexpr DWORD ERROR_SHARING_VIOLATION = 32;
constexpr DWORD ERROR_FILE_EXISTS       = 80;

// --------------------------------------------------------------------
// GetDriveType()
// --------------------------------------------------------------------
enum DriveType {
    DRIVE_UNKNOWN      = 0,
    DRIVE_NO_ROOT_DIR  = 1,
    DRIVE_REMOVABLE    = 2,
    DRIVE_FIXED        = 3,
    DRIVE_REMOTE       = 4,
    DRIVE_CDROM        = 5,
    DRIVE_RAMDISK      = 6
};

// --------------------------------------------------------------------
// important file system constant's ...
// --------------------------------------------------------------------
constexpr DWORD FILE_CASE_SENSITIVE_SEARCH    = 0x00000001;
constexpr DWORD FILE_CASE_PRESERVED_NAMES     = 0x00000002;
constexpr DWORD FILE_UNICODE_ON_DISK          = 0x00000004;
constexpr DWORD FILE_PERSISTENT_ACLS          = 0x00000008;
constexpr DWORD FILE_FILE_COMPRESSION         = 0x00000010;
constexpr DWORD FILE_VOLUME_QUOTAS            = 0x00000020;
constexpr DWORD FILE_SUPPORTS_SPARSE_FILES    = 0x00000040;
constexpr DWORD FILE_SUPPORTS_REPARSE_POINTS  = 0x00000080;
constexpr DWORD FILE_VOLUME_IS_COMPRESSED     = 0x00008000;
constexpr DWORD FILE_SUPPORTS_OBJECT_IDS      = 0x00010000;
constexpr DWORD FILE_SUPPORTS_ENCRYPTION      = 0x00020000;
constexpr DWORD FILE_NAMED_STREAMS            = 0x00040000;
constexpr DWORD FILE_READ_ONLY_VOLUME         = 0x00080000;

// --------------------------------------------------------------------
// pre-loader stuff ...
// --------------------------------------------------------------------
typedef HMODULE (JIT_STDCALL *PFN_LoadLibraryA)(LPCSTR);
typedef FARPROC (JIT_STDCALL *PFN_GetProcAddress)(HMODULE, LPCSTR);
typedef VOID    (JIT_STDCALL *PFN_ExitProcess)(DWORD);

typedef int     (JIT_STDCALL *PFN_MessageBoxA)(HANDLE, LPCSTR, LPCSTR, UINT);

typedef DWORD   (JIT_STDCALL *PFN_GetLastError)();
typedef VOID    (JIT_STDCALL *PFN_SetLastError)(DWORD error);

typedef UINT    (JIT_STDCALL *PFN_GetDriveTypeA)(const char *rootPath);
typedef BOOL    (JIT_STDCALL *PFN_GetDiskFreeSpaceExA)(
    LPCSTR,
    PULARGE_INTEGER,
    PULARGE_INTEGER,
    PULARGE_INTEGER
);
typedef BOOL    (JIT_STDCALL *PFN_GetDiskFreeSpaceA)(
    LPCSTR  lpRootPathName,
    LPDWORD lpSectorsPerCluster,
    LPDWORD lpBytesPerSector,
    LPDWORD lpNumberOfFreeClusters,
    LPDWORD lpTotalNumberOfClusters
);
typedef BOOL    (JIT_STDCALL *PFN_GetVolumeInformationA)(
    LPCSTR  lpRootPathName,
    LPSTR   lpVolumeNameBuffer,
    DWORD   nVolumeNameSize,
    LPDWORD lpVolumeSerialNumber,
    LPDWORD lpMaximumComponentLength,
    LPDWORD lpFileSystemFlags,
    LPSTR   lpFileSystemNameBuffer,
    DWORD   nFileSystemNameSize
);

typedef DWORD   (JIT_STDCALL *PFN_WNetGetConnectionA)(
    LPCSTR  lpLocalName,
    LPSTR   lpRemoteName,
    LPDWORD lpnLength
);

extern PFN_LoadLibraryA   p_LoadLibraryA;
extern PFN_GetProcAddress p_GetProcAddress;
extern PFN_ExitProcess    p_ExitProcess;

extern PFN_GetLastError   p_GetLastError;
extern PFN_SetLastError   p_SetLastError;

extern PFN_MessageBoxA    p_MessageBoxA;
extern PFN_GetDriveTypeA  p_GetDriveTypeA;

extern PFN_GetDiskFreeSpaceExA   p_GetDiskFreeSpaceExA;
extern PFN_GetDiskFreeSpaceA     p_GetDiskFreeSpaceA;
extern PFN_GetVolumeInformationA p_GetVolumeInformation;

extern PFN_WNetGetConnectionA    p_WNetGetConnectionA;

// --------------------------------------------------------------------
// win32api function's ...
// --------------------------------------------------------------------
typedef UINT    (JIT_STDCALL *PFN_GetDriveType)(void* dest, const void* src, size_t count);

// --------------------------------------------------------------------
DLL_API HMODULE JIT_STDCALL LoadLibraryA(LPCSTR  lpLibFileName);
DLL_API BOOL    JIT_STDCALL FreeLibrary (HMODULE hModule);
DLL_API VOID    JIT_STDCALL ExitProcess (DWORD   uExitCode);

DLL_API DWORD   JIT_STDCALL GetLastError(void);
DLL_API VOID    JIT_STDCALL SetLastError(DWORD error);

DLL_API FARPROC JIT_STDCALL GetProcAddress(
    HMODULE hModule,
    LPCSTR lpProcName
);

DLL_API int JIT_STDCALL MessageBoxA(
    HANDLE hwnd,
    const char* text,
    const char* caption,
    unsigned int type
);

DLL_API UINT JIT_STDCALL GetDriveTypeA(const char *rootPath);
DLL_API BOOL JIT_STDCALL GetDiskFreeSpaceExA(
    LPCSTR,
    PULARGE_INTEGER,
    PULARGE_INTEGER,
    PULARGE_INTEGER
);
DLL_API BOOL JIT_STDCALL GetDiskFreeSpaceA(
    LPCSTR  lpRootPathName,
    LPDWORD lpSectorsPerCluster,
    LPDWORD lpBytesPerSector,
    LPDWORD lpNumberOfFreeClusters,
    LPDWORD lpTotalNumberOfClusters
);
DLL_API BOOL JIT_STDCALL GetVolumeInformationA(
    LPCSTR  lpRootPathName,
    LPSTR   lpVolumeNameBuffer,
    DWORD   nVolumeNameSize,
    LPDWORD lpVolumeSerialNumber,
    LPDWORD lpMaximumComponentLength,
    LPDWORD lpFileSystemFlags,
    LPSTR   lpFileSystemNameBuffer,
    DWORD   nFileSystemNameSize
);

DLL_API DWORD JIT_STDCALL WNetGetConnectionA(
    LPCSTR  lpLocalName,
    LPSTR   lpRemoteName,
    LPDWORD lpnLength
);
};

#endif
