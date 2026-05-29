(**!
 * @mainpage Mein Projekt
 *
 * Willkommen in der Dokumentation.
 *
 * @section Übersicht
 * Diese Engine erzeugt Pascal-Dokumentation.
 *
 * @subsection Features
 * Klassen, Interfaces, Records und Typverlinkungen.
 *
 * @subsubsection Details
 * Später kommen Graphviz, Call-Graphs und Unit-Dependencies dazu.
 *)
unit TestUnit;

interface

uses
  SysUtils (**! @brief System Utils function's *);

uses
  Classes  (**! @brief Pascal Class'es *),
  Dialogs;
  
const
  (**!
   * @brief Maximale Anzahl.
   *
   * Dieser Wert begrenzt die Verarbeitung.
   *)
  MAX_COUNT   = 100;
  
const
  PI_VALUE    = 3.1415 ;   (**! @brief This is the documentation for the PI const *)
  APP_NAME    = 'MyApp';   (**! @brief This is the application name *)
  APP_VERSION = $1001  ;   (**! @brief This is the Version *)

var
  (**! @brief Player values *)
  score_board : Integer;    (**! @brief point score board *)
  score_text  : string;     (**! @brief player name text *)

  (**! @brief Window values *)
  main_width  : Integer;
  main_height : Integer;

type
  (**!
   * @brief Beispiel-Record.
   * @details Dieser Record speichert X- und Y-Werte.
   *)
  TPoint = record
    X: Integer; (**! @brief give the X position *)
    Y: Integer; (**! @brief give the Y position *)
  end;

  TIntArray = array[0..10] of Integer;  (**! @brief this is a integer array 0 .. 10 *)
  TCharSet  = set of Char;              (**! @brief a char set *)

type
  TCard = (One, Two, Three); (**! @brief available cards *)
  
type
  TColor = (
    Red,   (**! @brief red color   *)
    Green, (**! @brief green color *)
    Blue   (**! @brief blue color  *)
  );       (**! @brief available colors *)

type
  (**!
   * @brief Basisklasse.
   *
   * Dies ist die ausführliche Beschreibung der Basisklasse.
   *)
  TBaseClass = class
  public
    procedure BaseMethod;
  end;

  (**! @brief Abgeleitete Klasse *)
  TChildClass = class(TBaseClass)
  public
    procedure ChildMethod;
  end;

type
  (**!
   * @brief Beispiel-Interface.
   * @details Dies ist eine längere Beschreibung
   * für das Interface.
   *)
  IExample = interface
    procedure Execute;
  end;

  (**!
   * @brief Beispielklasse.
   *
   * Diese Klasse zeigt @brief und automatische Details.
   *)
  TExampleClass = class(TBaseClass, IExample)
  public
    (**!
     * @brief Führt die Aktion aus.
     *
     * Diese Methode implementiert die Interface-Methode.
     *)
    procedure Execute;
  end;

type
  (**! @brief Basis-Interface für zeichnbare Objekte *)
  IDrawable = interface
    (**! @brief Zeichnet das Objekt *)
    procedure Draw;

    (**! @brief Sichtbarkeit des Objekts *)
    property Visible: Boolean
      read FVisible (**! @brief Liefert den Sichtbarkeitsstatus *)
      write FVisible (**! @brief Setzt den Sichtbarkeitsstatus *);
  end;

  (**! @brief Interface für geometrische Formen *)
  IShape = interface(IDrawable)
    (**! @brief Berechnet die Fläche *)
    function Area: Double;

    (**! @brief Name der Form *)
    property Name: string
      read FName (**! @brief Liefert den Namen *)
      write FName (**! @brief Setzt den Namen *);
  end;

  (**! @brief Generisches Listen-Interface *)
  IList<T> = interface
    (**! @brief Fügt ein Element hinzu *)
    procedure Add(Item: T);

    (**! @brief Liefert ein Element anhand des Index *)
    function GetItem(Index: Integer): T;

    (**! @brief Anzahl der Elemente *)
    property Count: Integer read FCount (**! @brief Liefert die Anzahl *);
  end;

type
  (**! @brief Sprite class implementing IDrawable *)
  TSprite = class(TObject, IDrawable)
  public
    procedure Draw;
  end;

type
  TWeapon = class
  end;

  TInventory = class
  end;

  IRenderable = interface
    procedure Render;
  end;

  TPlayer = class(TObject, IRenderable)
  private
    FWeapon: TWeapon;
    FInventory: TInventory;
  public
    procedure Equip(AWeapon: TWeapon);
    procedure Render;
  end;

type
  (**!
   * @brief This is the TPerson class
   *)
  TPerson = class(TObject)
  private
    FName: string;
    FAge: Integer;
  protected
    procedure Paint;
  public
    (**!
     * @brief   Erzeugt ein neues Objekt
     * @details This is the default constructor.
     *)
    constructor Create; overload;
    (**!
     * @brief   Erzeugt ein neues Objekt mit einen string.
     * @details This is the constructor with a string.
     *)
    constructor Create(S1: String); overload;
    constructor Create(P1: TPoint); overload;
    destructor Destroy; override;
    (**!
     * @brief Speichert die aktuellen Daten
     *
     * @param S1 string 1
     * @param S2 string 2
     *
     * @note Wird intern gecached.
     * @info Diese Methode ist thread-safe.
     * @warn X und Y dürfen nicht negativ sein.
     *)
    procedure Save(S1: string; S2: string); virtual;
    procedure Point(A: TPoint; B: TPoint);
    (**!
     * @brief Get the name of the class
     * @return string - Ein String als Rückgabe
     *)
    function GetName: string;
    property  Name: string (**! @brief Datentyp *)
        read  FName (**! @brief getter of Name *)
        write FName (**! @brief setter of Name *);
  end;

type
  (**! @brief Generic list interface *)
  IList<T> = interface
    (**! @brief Add one item to the list *)
    procedure Add(Item: T);

    (**! @brief Get item by index *)
    function GetItem(Index: Integer): T;

    property Count: Integer (**! @brief number datatype *)
      read GetCount (**! @brief returns item count *);
  end;

  (**! @brief Generic key value pair record *)
  TPair<TKey, TValue> = record
    Key   : TKey;   (**! @brief key value *)
    Value : TValue; (**! @brief stored value *)
  end;

  (**! @brief Generic repository class *)
  TRepository<T> = class
  private
    FItems: IList<T>;

  public
    (**! @brief Add entity *)
    procedure Add(Entity: T);

    (**! @brief Find entity by id *)
    function FindById(Id: Integer): T;

    property Items: IList<T> (**! @brief list datatype *)
      read FItems (**! @brief returns internal list *);
  end;
  
implementation

uses
  Windows (**! @brief Windows XP System stuff *),
  VCL     (**! @brief Visual Control Library  *),
  Forms   (**! @brief Window Forms stuff      *);

procedure TExampleClass.Execute;
begin
end;

end.
