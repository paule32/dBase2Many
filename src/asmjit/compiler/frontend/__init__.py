# ---------------------------------------------------------------------------
# File:   __init__py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from .pascal.generator import PascalGenerator
from .basic .generator import BasicGenerator
from .elan  .generator import ElanGenerator
from .lisp  .generator import LispGenerator

FRONTEND_CLASSES = {
    "pascal": PascalGenerator,
    "basic" : BasicGenerator,
    'elan'  : ElanGenerator,
    "lisp"  : LispGenerator,
}
