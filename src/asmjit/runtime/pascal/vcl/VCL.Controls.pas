// ---------------------------------------------------------------------------
// File:   VCL.Controls.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
unit VCL.Controls;

interface
uses System,
     Windows.Types,
     Windows.Kernel,
     Windows.User;

type
    TControl = class(TObject)
    private
        FHandle: HWND;
        FParent: HWND;
        FControlId: Integer;
        
        FLeft  : Integer;
        FTop   : Integer;
        FWidth : Integer;
        FHeight: Integer;
        
        FCaption: String;
        FVisible: Boolean;
        FEnabled: Boolean;
    protected
        function GetWindowClass  : String; virtual;
        function GetWindowStyle  : DWORD ; virtual;
        function GetWindowExStyle: DWORD ; virtual;
        
        procedure CreateHandle ; virtual;
        procedure DestroyHandle; virtual;
    public
        constructor Create(AParent: HWND; AControlID: Integer);
        destructor Destroy;
        
        procedure SetBounds(ALeft, ATop, AWidth, AHeight: Integer);
        procedure SetCaption(const ACaption: String);
        
        procedure Show;
        procedure Hide;
        
        procedure Enable;
        procedure Disable;
        
    published
        property Handle: HWND read FHandle;
        property ParentHandle: HWND read FParent;
        property ControlId: Integer read FControlId;
    end;

type
    TButton = class(TControl)
    protected
        function GetWindowClass: String; override;
        function GetWindowStyle: DWORD; override;
    public
        constructor Create(
            AParent: HWND;
            AControlID: Integer;
            const ACaption: String);
            
        procedure Click;
    end;
    
implementation

{ TControl }

constructor TControl.Create(
    AParent: HWND;
    AControlId: Integer);
begin
    inherited Create;
    
    FHandle    := nil;
    FParent    := AParent;
    FControlId := AControlId;
    
    FLeft    := 0;
    FTop     := 0;
    FWidth   := 80;
    FHeight  := 25;
    
    FCaption := '';
    
    FVisible := True;
    FEnabled := True;
end;
destructor TControl.Destroy;
begin
    DestroyHandle;
    inherited Destroy;
end;

function TControl.GetWindowClass: String;
begin
    result := '';
end;

function TControl.GetWindowStyle: DWORD;
begin
    result := WS_CHILD or WS_CLIPSIBLINGS;
end;

function TControl.GetWindowExStyle: DWORD;
begin
    result := 0;
end;

procedure TControl.CreateHandle;
var
    Style: DWORD;
begin
    if FHandle <> nil then
        Exit;

    Style := GetWindowStyle;

    if FVisible then
        Style := Style or WS_VISIBLE;

    if not FEnabled then
        Style := Style or WS_DISABLED;

    FHandle := CreateWindowExA(
        GetWindowExStyle,
        GetWindowClass,
        FCaption,
        Style,
        FLeft,
        FTop,
        FWidth,
        FHeight,
        FParent,

        { Bei einem Child-Window enthält hMenu die Control-ID. }
        HMENU(FControlId),

        GetModuleHandleA(nil),
        Self
    );
    
    if FHandle = nil then
    begin
        _jit_error_runtime(
        'TControl.CreateHandle: CreateWindowExA failed.');
    end;
end;

procedure TControl.DestroyHandle;
begin
    if FHandle = nil then
    Exit;

    if IsWindow(FHandle) then
    DestroyWindow(FHandle);

    FHandle := nil;
end;

procedure TControl.SetBounds(
    ALeft: Integer;
    ATop: Integer;
    AWidth: Integer;
    AHeight: Integer);
begin
    FLeft   := ALeft;
    FTop    := ATop;
    FWidth  := AWidth;
    FHeight := AHeight;

    if FHandle <> nil then
        MoveWindow(
            FHandle,
            FLeft,
            FTop,
            FWidth,
            FHeight,
            True
        );
end;

procedure TControl.SetCaption(const ACaption: String);
begin
    FCaption := ACaption;

    if FHandle <> nil then
        SetWindowTextA(
            FHandle,
            FCaption
        );
end;

procedure TControl.Show;
begin
    FVisible := True;

    if FHandle <> nil then
        ShowWindow(
            FHandle,
            SW_SHOW
        );
end;

procedure TControl.Hide;
begin
    FVisible := False;

    if FHandle <> nil then
        ShowWindow(
            FHandle,
            SW_HIDE
        );
end;

procedure TControl.Enable;
begin
    FEnabled := True;

    if FHandle <> nil then
        EnableWindow(
            FHandle,
            True
        );
end;

procedure TControl.Disable;
begin
    FEnabled := False;

    if FHandle <> nil then
        EnableWindow(
            FHandle,
            False
        );
end;


{ TButton }

constructor TButton.Create(
    AParent: HWND;
    AControlId: Integer;
    const ACaption: String);
begin
    inherited Create(
        AParent,
        AControlId
    );
    
    SetCaption(ACaption);
    SetBounds(10, 10, 100, 32);
    
    CreateHandle;
end;
destructor TButton.Destroy;
begin
    inherited Destroy;
end;

function TButton.GetWindowClass: String;
begin
    result := 'BUTTON';
end;

function TButton.GetWindowStyle: DWORD;
begin
    result := inherited GetWindowStyle or
        WS_TABSTOP or
        BS_PUSHBUTTON;
end;

procedure TButton.Click;
begin
    WriteLn('TButton: clicked');
end;

end.
