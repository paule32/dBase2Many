# ---------------------------------------------------------------------------
# File: locale.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

# ---------------------------------------------------------------------------
# i18n / gettext (mo inside zip: <lang>/LC_MESSAGES/dbase.mo)
# ---------------------------------------------------------------------------
import locale
import gettext
import polib
import os
import sys

from pathlib import Path

# ---------------------------------------------------------------------------
# locales (gnu gettext) support ...
# Loads GNU gettext .mo files from a zip and provides tr().
# ---------------------------------------------------------------------------
class TranslationManager:
    def get_default_lang(self) -> str:
        loc = locale.getlocale()
        if loc is None: return "en"
        
        lang = loc[0]
        if not lang: return "en"
        return lang
    
    def add_trans(self, trans: gettext.GNUTranslations):
        self.translations.append(trans)
        
    def __init__(self, mode: int = 0):
        self.lang         = self.get_default_lang().split("_")[0].lower()
        self.mode         = mode
        self.po           = None
        self.filename     = ""
        self.trans        = gettext.NullTranslations()
        
        self._langSwitch(self.lang)
    
    def _trres(self, msgid:str) -> str:
        text = self.po.find(msgid)
        if text is not None:
            return text
        return msgid
    
    def _langSwitch(self, lang: str):
        self.lang = lang
        self.filename = f"locales/{lang}/pascal.mo"
        self.filename = Path(self.filename).resolve()
        
        try:
            self.po = polib.mofile(self.filename)
            
        except FileNotFoundError as e:
            print(f"{self._tr('File not found Error')}:")
            print(f"{self._tr('The requested file')}: {self.filename} {tr('could not be found')}.")
            return
            
        except PermissionError as e:
            print(f"{self._tr('File Permission Error')}:")
            print(f"{self._tr('You have not enough permissions to open file')}: {self.filename}.")
            return
            
        except RuntimeError as e:
            print(f"{self._tr('Runtime Error')}:")
            print(f"{self._tr('The Python Library throws a Runtime Error on opening file')}: {self.filename}.")
            return
            
        except OSError as e:
            print(f"{self._tr('Operating System Error')}:")
            print(f"{self._tr('The System is not able to open file')}: {self.filename}.")
            return
            
        except Exception as e:
            print(f"{self._tr('Common Exception Error')}:")
            print(f"{self._tr('Common Exception throwed on open file')}: {self.filename}.")
            print("default language is English.")
            return
        return
    
    def _tr(self, msgid: str) -> str:
        try:
            return self._trres(msgid)
        except Exception:
            return msgid

# ---------------------------------------------------------------------------
# Global translation hook used by UI code: tr("File") -> "Datei" if de loaded
# ---------------------------------------------------------------------------
I18N = TranslationManager()

# ---- Standard-Locale beim Start setzen ----
def tr(msgid: str) -> str: return I18N._trres(msgid)
def LangSwitch(lang: str): return I18N._langSwitch(lang)
