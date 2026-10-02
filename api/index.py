"""Mizani agents as one Vercel serverless function.

Both Omega agents (community + facility) run in this deployment, mounted at
/api/community and /api/facility. On hyperon each agent keeps its own atom
space, exactly like the two local PeTTa processes. State lives in Vercel
Edge Config.
"""
import os
import pathlib
import sys
from contextlib import asynccontextmanager

# hyperon writes its MeTTa module catalog under $HOME; Vercel's filesystem
# is read-only except /tmp, so point HOME there before hyperon initializes.
os.environ.setdefault("HOME", "/tmp")

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent"))

from fastapi import FastAPI  # noqa: E402

from mizani.app import create_app  # noqa: E402

community = create_app("community")
facility = create_app("facility")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Starlette does not run mounted apps' lifespans; drive the outbox loop
    # of the community agent from the parent.
    comm_state = community.state.agent
    if comm_state.outbox:
        await comm_state.outbox.start_loop()
    yield
    if comm_state.outbox:
        await comm_state.outbox.stop_loop()


app = FastAPI(title="Mizani agents", lifespan=lifespan)
app.mount("/api/community", community)
app.mount("/api/facility", facility)




@app.get("/api/blobtest")
def blob_test():
    """Probe Vercel Blob OIDC auth end to end (PUT then GET)."""
    import os
    import traceback
    from mizani.blobstore import BlobClient
    try:
        b = BlobClient()
        out = b.put("mizani/probe.txt", b"hello from mizani")
        got = b.get("mizani/probe.txt")
        return {"put": out.get("url", "")[:80], "get": got}
    except Exception as exc:
        import httpx
        detail = {"error": type(exc).__name__, "message": str(exc)[:300],
                  "has_oidc": bool(os.environ.get("VERCEL_OIDC_TOKEN")),
                  "has_store": bool(os.environ.get("BLOB_STORE_ID")),
                  "trace": traceback.format_exc()[-800:]}
        if isinstance(exc, httpx.HTTPStatusError):
            detail["status"] = exc.response.status_code
            detail["body"] = exc.response.text[:300]
        return detail

@app.get("/api/health")
def agents_health():
    return {
        "community": community.state.agent.engine.health(),
        "facility": facility.state.agent.engine.health(),
    }
