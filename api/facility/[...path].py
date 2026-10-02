"""Mizani facility agent as a Vercel serverless function.

Same code as the community agent with MIZANI_ROLE=facility: the full rule
pack plus the mother's longitudinal record, on hyperon with Blob state.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agent"))

from mizani.app import create_app  # noqa: E402

_PREFIX = "/api/facility"


class _StripPrefix:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] in {"http", "websocket"} and scope["path"].startswith(_PREFIX):
            scope = dict(scope)
            scope["path"] = scope["path"][len(_PREFIX):] or "/"
        return await self.app(scope, receive, send)


app = _StripPrefix(create_app("facility"))
