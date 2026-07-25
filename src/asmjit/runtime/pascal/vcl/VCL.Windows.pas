// ---------------------------------------------------------------------------
// File:   VCL.Windows.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
unit VCL.Windows.pas

interface
uses System, Windows;

type
    TForm = class(TObject)
    private
        FWidth: Integer;
        FHeight: Integer;
        FLeft: Integer;
        FTop: Integer;
        FCaption: String;
    public
        constructor Create;
        destructor Destroy; override;
    published
        property Height: Integer read FHeight write FHeight;
        property Width: Integer read FWidth write FWidth;
        property Top: Integer read FTop write FTop;
        property Left: Integer read FLeft write FLeft;
        property Caption: String read FCaption write FCaption;
    end;

implementation

constructor TForm.Create;
begin
    inherited Create;
    FCaption := 'TForm';
end;

destructor TForm.Destroy;
begin
    inherited Destroy;
end;

end.
