# ---------------------------------------------------------------------------
# \file  : ccRunner.py
# \author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# \note  : All rights reserved
# ---------------------------------------------------------------------------
# Gemeinsame Bootstrap-/Kompatibilitätsschicht für sprachspezifische Runner.
#
# Diese Schicht kapselt den aktuellen dBaseRunner-Monolithen und stellt
# stabile Importpunkte bereit. So können Implementierungen später Stück für
# Stück aus dBaseRunner.py in echte Einzelmodule verschoben werden, ohne dass
# sich die Einstiegspunkte der Anwendungen wieder ändern.
# ---------------------------------------------------------------------------
from .app import run_language_app
from .language_profiles import LanguageProfile, get_language_profile

__all__ = [
    "run_language_app",
    "LanguageProfile",
    "get_language_profile",
]
