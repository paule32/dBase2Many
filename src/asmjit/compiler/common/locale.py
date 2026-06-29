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
        self.translations = []
        self.filename     = ""
        self.trans        = gettext.NullTranslations()
        
        self._langSwitch(self.lang)
    
    def _trres(self, msgid:str) -> str:
        for trans in self.translations:
            text = trans.gettext(msgid)
            if text != msgid:
                return text
        return msgid
    
    def _langSwitch(self, lang: str):
        self.lang = lang
        self.translations.clear()
        self.filename = f"locales/{lang}/pascal.mo"
        try:
            if not os.path.isfile(self.filename):
                print("language file not found, fail back to english.")
            else:
                self.trans = self.load_mo(self.filename)
                self.add_trans(self.trans)
            
        except FileNotFoundError as e:
            app = self.ensure_app()
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
    
    def load_mo(self, filename: str) -> gettext.GNUTranslations:
        with open(filename, "rb") as f:
            data = f.read()
        return gettext.GNUTranslations(fp = io.BytesIO(data))
    
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
