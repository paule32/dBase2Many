# ---------------------------------------------------------------------------
# File:   locales.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__    import annotations
from share.common  import *

LANGUAGE_CODES = [
    ("ENU", "English (USA)" , "enu"),
    ("ENG", "English"       , "eng"),
    ("DEU", "German"        , "deu"),
    ("FRA", "French"        , "fra"),
    ("ESP", "Spanish"       , "esp"),
    ("ITA", "Italian"       , "ita"),
    ("NLD", "Dutch"         , "nld"),
    
    ("PTB", "Portuguese (Brazil)", "ptb"),
    
    ("POR", "Portuguese"    , "por"),
    ("PLK", "Polish"        , "plk"),
    ("RUS", "Russian"       , "rus"),

    ("AFR", "Afrikaans"     , "afr"),
    ("ALB", "Albanian"      , "alb"),
    ("ARA", "Arabic"        , "ara"),
    ("ARM", "Armenian"      , "arm"),
    ("AZE", "Azerbaijani"   , "aze"),
    ("BAQ", "Basque"        , "baq"),
    ("BEL", "Belarusian"    , "bel"),
    ("BEN", "Bengali"       , "ben"),
    ("BOS", "Bosnian"       , "bos"),
    ("BGR", "Bulgarian"     , "bgr"),
    ("CAT", "Catalan"       , "cat"),
    
    ("CHS", "Chinese (Simplified)" , "chs"),
    ("CHT", "Chinese (Traditional)", "cht"),
    
    ("HRV", "Croatian"      , "hrv"),
    ("CSY", "Czech"         , "csy"),
    ("DAN", "Danish"        , "dan"),
    ("ETI", "Estonian"      , "eti"),
    ("FIN", "Finnish"       , "fin"),
    ("GLC", "Galician"      , "glc"),
    ("GEO", "Georgian"      , "geo"),
    ("ELL", "Greek"         , "ell"),
    ("HEB", "Hebrew"        , "heb"),
    ("HIN", "Hindi"         , "hin"),
    ("HUN", "Hungarian"     , "hun"),
    ("ISL", "Icelandic"     , "isl"),
    ("IND", "Indonesian"    , "ind"),
    ("GLE", "Irish"         , "gle"),
    ("JPN", "Japanese"      , "jpn"),
    ("KAN", "Kannada"       , "kan"),
    ("KAZ", "Kazakh"        , "kaz"),
    ("KOR", "Korean"        , "kor"),
    ("LVI", "Latvian"       , "lvi"),
    ("LTH", "Lithuanian"    , "lth"),
    ("MKD", "Macedonian"    , "mkd"),
    ("MSL", "Malay"         , "msl"),
    ("MAL", "Malayalam"     , "mal"),
    ("MAR", "Marathi"       , "mar"),
    ("MON", "Mongolian"     , "mon"),
    ("NEP", "Nepali"        , "nep"),
    ("NOR", "Norwegian"     , "nor"),
    
    ("NOB", "Norwegian Bokmål" , "nob"),
    ("NNO", "Norwegian Nynorsk", "nno"),
    
    ("FAR", "Persian"       , "far"),
    ("ROM", "Romanian"      , "rom"),
    ("SRB", "Serbian"       , "srb"),
    
    ("SRL", "Serbian (Latin)", "srl"),
    
    ("SKY", "Slovak"        , "sky"),
    ("SLV", "Slovenian"     , "slv"),
    ("SVE", "Swedish"       , "sve"),
    ("SWA", "Swahili"       , "swa"),
    ("TAM", "Tamil"         , "tam"),
    ("TEL", "Telugu"        , "tel"),
    ("THA", "Thai"          , "tha"),
    ("TRK", "Turkish"       , "trk"),
    ("UKR", "Ukrainian"     , "ukr"),
    ("URD", "Urdu"          , "urd"),
    ("VIT", "Vietnamese"    , "vit"),
]

# ---------------------------------------------------------------------------
# locales (gnu gettext) support ...
# Loads GNU gettext .mo files from a zip and provides tr().
# ---------------------------------------------------------------------------
class TranslationManager:
    def get_default_lang(self) -> str:
        loc = locale.getdefaultlocale()
        
        if loc is None:
            return "en"
        
        lang = loc[0]
        if not lang:
            return "en"
        
        return lang
    
    def load_mo_from_resource(self, resource_path: str) -> gettext.GNUTranslations | None:
        f = QFile(resource_path)
        if not f.open(QFile.ReadOnly):
            raise FileNotFoundError(resource_path)
        data = bytes(f.readAll())
        f.close()
        return gettext.GNUTranslations(BytesIO(data))
    
    def ensure_app(self):
        try:
            from PyQt5.QtWidgets import QApplication
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            return app
        except Exception:
            return False, None
    
    def add_trans(self, trans: gettext.GNUTranslations):
        self.translations.append(trans)
        
    def __init__(self, zip_path: Optional[Union[str, Path]] = None, mode: int = 0, domain: str = "dbase"):
        self.domain       = domain
        self.zip_path     = Path(zip_path) if zip_path else None
        self.lang         = self.get_default_lang().split("_")[0].lower()
        self.mode         = mode
        self.style_name   = "dark"
        self.translations = []
        self.trans        = gettext.NullTranslations()

        self._langSwitch(self.lang)
    
    def _trres(self, msgid:str) -> str:
        for trans in self.translations:
            text = trans.gettext(msgid)
            if text != msgid:
                return text
        return msgid
    
    def _langSwitch(self, lang: str):
        try:
            self.translations.clear()
            if lang == "en":
                return
            
            self.filename = f":/locales/{lang}/dbase.mo"
            self.add_trans( self.load_mo_from_resource(self.filename))
            
            self.filename = f":/locales/{lang}/doxygen.mo"
            self.add_trans( self.load_mo_from_resource(self.filename))
            
            self.filename = f":/locales/{lang}/runner.mo"
            self.add_trans( self.load_mo_from_resource(self.filename))
            
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
        
        return
    
    def set_zip(self, zip_path: Union[str, Path]):
        self.zip_path = Path(zip_path)
    
    def load_mo(self, lang: str) -> bool:
        lang            = lang.strip().lower()
        self.style_name = lang
        self.lang       = lang
        self.trans      = gettext.NullTranslations()
        
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
            self.trans = gettext.GNUTranslations(fp=io.BytesIO(data))
            return True
        except KeyError:
            # not found in zip
            self.trans = gettext.NullTranslations()
            return False
        except Exception:
            self.trans = gettext.NullTranslations()
            return False
    
    def _tr(self, msgid: str) -> str:
        try:
            return self.trans.gettext(msgid)
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

def  LangSwitch(lang: str): return I18N._langSwitch(lang)
