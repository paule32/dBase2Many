# Patch-Inhalt

Enthalten sind:

- `src/dBaseRunner.py`
  - `Ansicht -> Debug Window` als erster Eintrag im View-Menü
  - Action öffnet das vorhandene Debug-Fenster über `ensure_debug_console(...)`
  - Fenstertitel des Debug-Fensters auf `Debug Window` vereinheitlicht
  - optionale Titelumschaltung je Runner über `DBASERUNNER_LANGUAGE`
- `src/share.py`
  - fehlende gemeinsame Start-Hilfe für `pascalRunner.py`, `ccRunner.py`, `lispRunner.py`
- `src/pascalLexer.g4`
  - Lexer-Seed für Object Pascal / Delphi
- `src/pascalParser.g4`
  - Parser-Seed für Programme, Units, Klassen, Records, Routinen und Standard-Statements
- `src/parser_pascal.bat`
  - separates Build-Skript für den Pascal-Parser

## Nächste sinnvolle Schritte

1. `pascalLexer.g4` und `pascalParser.g4` mit deinen gewünschten Delphi/Object-Pascal-Dialekt-Erweiterungen verfeinern.
2. Danach eine `PascalParserFacade` bauen, die dieselben Hooks liefert wie dein dBase-Pfad.
3. Anschließend Dateifilter/Dateiendungen (`.pas`, `.dpr`, `.pp`, `.inc`) im gemeinsamen Runner auf Pascal umstellen.
