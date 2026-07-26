// ---------------------------------------------------------------------------
// File:   Windows.Application.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
unit Windows.Application;

interface
uses System,
    Windows.Types,
    Windows.kernel,
    Windows.user,

    VCL.Windows;

const
    ID_BUTTON_INFO = 1001;

var
    AppInstance: HINSTANCE;
    MainWindow : HWND;
    RegisterResult: Integer;
    WndClass: TWndClassA;
    
type
    TApplication = class(TObject)
    private
        FAppForm    : TForm;
    protected
        //procedure RunMessageLoop;
    public
        constructor Create;
        destructor Destroy; override;
    end;

implementation

{ TApplication }

function WindowProc(
    hWnd:   HWND;
    uMsg:   UINT;
    wParam: WPARAM;
    lParam: LPARAM
    ): LRESULT; stdcall;
    var
    ButtonWindow: HWND;
begin
    if uMsg = WM_CREATE then
    begin
        ButtonWindow := CreateWindowExA(
            0,
            PAnsiChar('BUTTON'),
            PAnsiChar('Information'),
            WS_BUTTON,
            16,
            16,
            140,
            32,
            hWnd,
            ID_BUTTON_INFO,
            AppInstance,
            nil
        );
        Result := 0;
        Exit;
    end;

    if uMsg = WM_COMMAND then
    begin
        if wParam = ID_BUTTON_INFO then
        begin
            MessageBoxA(
                hWnd,
                PAnsiChar('Die Win32-GUI funktioniert.'),
                PAnsiChar('dBase2Many Pascal'),
                MB_OK + MB_ICONINFORMATION
            );
        end;

        Result := 0;
        Exit;
    end;

    if uMsg = WM_DESTROY then
    begin
        PostQuitMessage(0);
        Result := 0;
        Exit;
    end;

    Result := DefWindowProcA(
        hWnd,
        uMsg,
        wParam,
        lParam
    );
end;

procedure RunMessageLoop;
var
    msg: TMsg;
    status: Integer;
begin

    status := GetMessageA(msg, 0, 0, 0);

    while status > 0 do
    begin
        TranslateMessage(msg);
        DispatchMessageA(msg);
        status := GetMessageA(msg, 0, 0, 0);
    end;
end;

constructor TApplication.Create;
begin
    inherited Create;
    WriteLn('TApplication: Create');
    try
        AppInstance := GetModuleHandleA(nil);
        
        WndClass.style         := CS_REDRAW;
        WndClass.lpfnWndProc   := @WindowProc;
        WndClass.cbClsExtra    := 0;
        WndClass.cbWndExtra    := 0;
        WndClass.hInstance     := AppInstance;
        WndClass.hIcon         := LoadIconA(0, IDI_APPLICATION);
        WndClass.hCursor       := LoadCursorA(0, IDC_ARROW);
        WndClass.hbrBackground := COLOR_WINDOW + 1;
        WndClass.lpszMenuName  := nil;
        WndClass.lpszClassName := PAnsiChar('Win32Gui.Window');
        
        RegisterResult := RegisterClassA(WndClass);
        if RegisterResult = 0 then
        begin
            MessageBoxA(
                0,
                PAnsiChar('Die Fensterklasse konnte nicht registriert werden.'),
                PAnsiChar('Win32-Fehler'),
                MB_OK + MB_ICONERROR
            );
            ExitProcess(3);
        end;
        
        MainWindow := CreateWindowExA(
            0,
            PAnsiChar('Win32Gui.Window'),
            PAnsiChar('Win32 API GUI - dBase2Many Pascal'),
            WS_OVERLAPPEDWINDOW,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            640,
            420,
            0,
            0,
            AppInstance,
            nil
        );

        if MainWindow = 0 then
        begin
            MessageBoxA(
                0,
                PAnsiChar('Das Hauptfenster konnte nicht erzeugt werden.'),
                PAnsiChar('Win32-Fehler'),
                MB_OK + MB_ICONERROR
            );
            ExitProcess(2);
        end;

        ShowWindow(MainWindow, SW_SHOWDEFAULT);
        UpdateWindow(MainWindow);
        RunMessageLoop;

    except
        ExitProcess(45);
    end;
end;

destructor TApplication.Destroy;
begin
    inherited Destroy;
end;

end.
