"""Mizani community agent as a Vercel serverless function.

Runs on the hyperon MeTTa runtime (pure pip, no SWI-Prolog in serverless)
with state in Vercel Blob. Omega's lib_nal.metta is loaded unmodified from
the pinned submodule, exactly like the local PeTTa deployment.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agent"))

from mizani.app import create_app  # noqa: E402

_PREFIX = "/api/community"


class _StripPrefix:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] in {"http", "websocket"} and scope["path"].startswith(_PREFIX):
            scope = dict(scope)
            scope["path"] = scope["path"][len(_PREFIX):] or "/"
        return await self.app(scope, receive, send)


app = _StripPrefix(create_app("community"))
