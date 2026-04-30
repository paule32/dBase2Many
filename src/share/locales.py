# ---------------------------------------------------------------------------
# File:   locales.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__      import annotations

import gettext
#from   share.common  import *
from   share.modules.locales import *
#from   share.utildef.sysinfo import *

def get_default_lang():
    loc = locale.getdefaultlocale()
    
    if loc is None:
        return "en"
    
    lang = loc[0]
    if not lang:
        return "en"
    
    return lang

def load_mo_from_resource(resource_path: str):
    f = QFile(resource_path)
    if not f.open(QFile.ReadOnly):
        raise FileNotFoundError(resource_path)
    data = bytes(f.readAll())
    f.close()
    return gettext.GNUTranslations(BytesIO(data))
        
# ---------------------------------------------------------------------------
# locales (gnu gettext) support ...
# Loads GNU gettext .mo files from a zip and provides tr().
# ---------------------------------------------------------------------------
class TranslationManager:
    def ensure_app(self):
        try:
            from PyQt5.QtWidgets import QApplication
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            return app
        except Exception:
            return False, None

    def __init__(self, zip_path: Optional[Union[str, Path]] = None, mode: int = 0, domain: str = "dbase"):
        self.domain       = domain
        self.zip_path     = Path(zip_path) if zip_path else None
        self.lang         = "de"
        self.mode         = mode
        self.style_name   = "dark"
        self._trans       = gettext.NullTranslations()
        
        self.filename     = ""
        self.trdb         = None
        try:
            self.lang     = get_default_lang().split("_")[0].lower()
            self.filename = f":/locales/{self.lang}/dbase.mo"
            self.trdb     = load_mo_from_resource(self.filename)
        except FileNotFoundError as e:
            app = self.ensure_app()
            dlg = ErrorMessage("File not found Error",
            f"The requested file: {self.filename} could not be found.")
            dlg.exec_()
            return
        except PermissionError as e:
            app = self.ensure_app()
            dlg = ErrorMessage("File Permission Error",
            f"You have not enough permissions to open file: {self.filename}.")
            dlg.exec_()
            return
        except RuntimeError as e:
            app = self.ensure_app()
            dlg = ErrorMessage("Runtime Error",
            f"The Python Library throws a Runtime Error on opening file: {self.filename}.")
            dlg.exec_()
            return
        except OSError as e:
            app = self.ensure_app()
            dlg = ErrorMessage("Operating System Error",
            f"The System is not able to open file: {self.filename}.")
            dlg.exec_()
            return
        except Exception as e:
            app = self.ensure_app()
            dlg = share.excepts.ErrorMessage("Common Exception Error",
            f"Common Exception throwed on open file: {self.filename}.")
            dlg.exec_()
            return
    
    def _trres(self, msgid:str) -> str:
        if self.trdb is not None:
            return self.trdb.gettext(msgid)
        return msgid
    
    def set_zip(self, zip_path: Union[str, Path]):
        self.zip_path = Path(zip_path)
    
    def load_mo(self, lang: str) -> bool:
        lang            = lang.strip().lower()
        self.style_name = lang
        self.lang       = lang
        self._trans     = gettext.NullTranslations()
        
        if not self.zip_path:
            return False
        
        #AppMode.lang   = lang
        #share.common.AppMode.domain = self.domain
        
        if self.mode == 0:
            inner = f"{lang}/LC_MESSAGES/{self.domain}.mo"
        elif self.mode == 1:
            inner = f"styles/default/{self.style_name}.mo"
        try:
            with zipfile.ZipFile(str(self.zip_path), "r") as zf:
                data = zf.read(inner)  # bytes
            self._trans = gettext.GNUTranslations(fp=io.BytesIO(data))
            return True
        except KeyError:
            # not found in zip
            self._trans = gettext.NullTranslations()
            return False
        except Exception:
            self._trans = gettext.NullTranslations()
            return False
    
    def _tr(self, msgid: str) -> str:
        try:
            return self._trans.gettext(msgid)
        except Exception:
            return msgid

# ---------------------------------------------------------------------------
# Global translation hook used by UI code: tr("File") -> "Datei" (if de loaded)
# ---------------------------------------------------------------------------
I18N = TranslationManager( mode = 0 )
QCSS = TranslationManager( mode = 1 )

# ---- Standard-Locale beim Start setzen ----
if SystemInfo.is_windows():
    I18N.set_zip(Path(__file__).parent / "data\\locales.zip"); I18N.load_mo("de"  ) # Deutsch als Default
    QCSS.set_zip(Path(__file__).parent / "data\\styles.zip" ); QCSS.load_mo("dark") # dark mode style
else:
    I18N.set_zip(Path(__file__).parent / "data/locales.zip"); I18N.load_mo("de"  ) # Deutsch als Default
    QCSS.set_zip(Path(__file__).parent / "data/styles.zip" ); QCSS.load_mo("dark") # dark mode style

def  tr(msgid: str) -> str: return I18N._trres(msgid)
def css(msgid: str) -> str: return QCSS._tr(msgid)
