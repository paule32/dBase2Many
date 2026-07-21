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

const DLL_FILE = 'libruntime_mini.dll';

function  _jit_object_instance_new (AVmt:    Pointer): Pointer; cdecl; external DLL_FILE name '_jit_object_instance_new' ordinal 77;
procedure _jit_object_instance_free(AObject: Pointer);          cdecl; external DLL_FILE name '_jit_object_instance_free' ordinal 78;
procedure _jit_object_free         (AObject: Pointer);          cdecl; external DLL_FILE name '_jit_object_free' ordinal 79;
function  _jit_object_class_type   (AObject: Pointer): Pointer; cdecl; external DLL_FILE name '_jit_object_class_type' ordinal 80;

function  _jit_class_parent        (AVmt:    Pointer): Pointer; cdecl; external DLL_FILE name '_jit_class_parent' ordinal 81;
function  _jit_class_name          (AVmt:    Pointer): Pointer; cdecl; external DLL_FILE name '_jit_class_name' ordinal 82;
function  _jit_class_instance_size (AVmt:    Pointer): Integer; cdecl; external DLL_FILE name '_jit_class_instance_size' ordinal 83;

function  _jit_inherits_from_class (ACurrentClass: Pointer; AExpectedClass: Pointer): Integer; cdecl; external DLL_FILE name '_jit_inherits_from_class' ordinal 84;
function  _jit_inherits_from_object(AObject:       Pointer; AExpectedClass: Pointer): Boolean; cdecl; external DLL_FILE name '_jit_inherits_from_object' ordinal 85;

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
