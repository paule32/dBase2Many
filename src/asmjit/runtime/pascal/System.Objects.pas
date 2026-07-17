// ---------------------------------------------------------------------------
// File:   System.Objects.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
unit System.Objects;

interface

type
    TClass  = Pointer;

    TObject = class
    public
        constructor Create;
        destructor Destroy; virtual;

        procedure Free;
        procedure FreeInstance;

        function ClassType: TClass;
        function ClassParent: TClass;
        function ClassNameAddress: Pointer;
        
        function InstanceSize: Integer;
        function InheritsFrom(AClass: TClass): Boolean;
    end;

const DLL_FILE = 'libdbase2many.32.dll';

function  _jit_object_instance_new (AVmt:    Pointer): Pointer; cdecl; external DLL_FILE name '_jit_object_instance_new';
procedure _jit_object_instance_free(AObject: Pointer);          cdecl; external DLL_FILE name '_jit_object_instance_free';
procedure _jit_object_free         (AObject: Pointer);          cdecl; external DLL_FILE name '_jit_object_free';
function  _jit_object_class_type   (AObject: Pointer): Pointer; cdecl; external DLL_FILE name '_jit_object_class_type';

function  _jit_class_parent        (AVmt:    Pointer): Pointer; cdecl; external DLL_FILE name '_jit_class_parent';
function  _jit_class_name          (AVmt:    Pointer): Pointer; cdecl; external DLL_FILE name '_jit_class_name';
function  _jit_class_instance_size (AVmt:    Pointer): Integer; cdecl; external DLL_FILE name '_jit_class_instance_size';

function  _jit_inherits_from_class (ACurrentClass: Pointer; AExpectedClass: Pointer): Integer; cdecl; external DLL_FILE name '_jit_inherits_from_class';
function  _jit_inherits_from_object(AObject:       Pointer; AExpectedClass: Pointer): Boolean; cdecl; external DLL_FILE name '_jit_inherits_from_object';

implementation

constructor TObject.Create;
begin
end;

destructor TObject.Destroy;
begin
end;

procedure TObject.Free;
begin
    if Self <> nil then
        _jit_object_free(Pointer(Self));
end;

procedure TObject.FreeInstance;
begin
    if Self <> nil then
        _jit_object_instance_free(Pointer(Self));
end;

function TObject.ClassType: TClass;
begin
    Result := _jit_object_class_type(Pointer(Self));
end;

function TObject.ClassParent: TClass;
begin
    Result := _jit_class_parent(
        _jit_object_class_type(Pointer(Self))
    );
end;

function TObject.ClassNameAddress: Pointer;
begin
    Result := _jit_class_name(
        _jit_object_class_type(Pointer(Self))
    );
end;

function TObject.InstanceSize: Integer;
begin
    Result := _jit_class_instance_size(
        _jit_object_class_type(Pointer(Self))
    );
end;

function TObject.InheritsFrom(
    AClass: TClass
): Boolean;
begin
    Result := (_jit_inherits_from_object(Pointer(Self), AClass ) <> 0);
end;

end.
