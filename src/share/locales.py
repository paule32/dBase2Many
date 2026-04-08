# ---------------------------------------------------------------------------
# File:   locales.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__             import annotations

from   share.common          import *
from   share.utildef.sysinfo import *

# ---------------------------------------------------------------------------
# locales (gnu gettext) support ...
# ---------------------------------------------------------------------------
class TranslationManager:
    """Loads GNU gettext .mo files from a zip and provides tr()."""
    def __init__(self, zip_path: Optional[Union[str, Path]] = None, mode: int = 0, domain: str = "dbase"):
        self.domain     = domain
        self.zip_path   = Path(zip_path) if zip_path else None
        self.lang       = "de"
        self.mode       = mode
        self.style_name = "dark"
        self._trans     = gettext.NullTranslations()
    
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

def  tr(msgid: str) -> str: return I18N._tr(msgid)
def css(msgid: str) -> str: return QCSS._tr(msgid)
