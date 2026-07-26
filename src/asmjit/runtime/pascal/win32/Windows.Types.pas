// ---------------------------------------------------------------------------
// File:   Windows.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
unit Windows.Types;
interface
uses System.Types, Windows.Kernel, Windows.User;

const
    // Window messages
    WM_CREATE           = $0001;
    WM_DESTROY          = $0002;
    WM_COMMAND          = $0111;

    // Window class styles
    CS_REDRAW           = $0003;        // CS_VREDRAW or CS_HREDRAW

    // Window/control styles
    WS_OVERLAPPEDWINDOW = $00CF0000;
    WS_BUTTON           = $50010000;    // WS_CHILD | WS_VISIBLE | WS_TABSTOP

    // CreateWindow defaults
    CW_USEDEFAULT       = $0; //-2147483648;

    // Stock resources
    IDI_APPLICATION     = 32512;
    IDC_ARROW           = 32512;
    COLOR_WINDOW        = 5;

    // ShowWindow
    SW_SHOWDEFAULT      = 10;

    // MessageBox
    MB_OK               = $00000000;
    MB_ICONERROR        = $00000010;
    MB_ICONINFORMATION  = $00000040;

type
    BOOL      = Integer;
    UINT      = Integer;
    DWORD     = Integer;
    LONG      = Integer;
    WPARAM    = Integer;
    LPARAM    = Integer;
    LRESULT   = Integer;

    HANDLE    = Integer;
    HINSTANCE = Integer;
    HMODULE   = Integer;
    HWND      = Integer;
    HICON     = Integer;
    HCURSOR   = Integer;
    HBRUSH    = Integer;
    HMENU     = Integer;

    TPoint = record
        x: LONG;
        y: LONG;
    end;

    TMsg = record
        hwnd:    HWND;
        message: UINT;
        wParam:  WPARAM;
        lParam:  LPARAM;
        time:    DWORD;
        pt:      TPoint;
    end;

    TWndClassA = record
        style:         UINT;
        lpfnWndProc:   Pointer;
        cbClsExtra:    Integer;
        cbWndExtra:    Integer;
        hInstance:     HINSTANCE;
        hIcon:         HICON;
        hCursor:       HCURSOR;
        hbrBackground: HBRUSH;
        lpszMenuName:  PAnsiChar;
        lpszClassName: PAnsiChar;
    end;

implementation
end.
