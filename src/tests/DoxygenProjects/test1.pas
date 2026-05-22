program TestUnit;

const
  PI_VALUE    = 3.1415 ;   (**! @brief This is the documentation for the PI const *)
  APP_NAME    = 'MyApp';   (**! @brief This is the application name *)
  APP_VERSION = $1001  ;   (**! @brief This is the Version *)

var
  score_board : Integer;
  score_text  : string;

type
  TPoint = record
    X: Integer;
    Y: Integer;
  end;

  TIntArray = array[0..10] of Integer;
  TCharSet  = set of Char;
  
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
     * @brief Erzeugt ein neues Objekt
     *)
    constructor Create;
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
    (**!
     * @brief Get the name of the class
     * @return string - Ein String als Rückgabe
     *)
    function GetName: string;
    property Name: string read FName write FName;
  end;

begin
end.
