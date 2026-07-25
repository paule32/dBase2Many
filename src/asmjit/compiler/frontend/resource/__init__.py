from __future__ import annotations

__version__ = "0.1.0"


def compile_resource_script(*args, **kwargs):
    # Lazy import keeps low-level encoders/test utilities usable before the
    # ANTLR-generated parser files have been created.
    from .compiler import compile_resource_script as implementation
    return implementation(*args, **kwargs)


__all__ = ["compile_resource_script", "__version__"]
