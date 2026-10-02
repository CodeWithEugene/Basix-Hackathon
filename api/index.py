"""Mizani agents as one Vercel serverless function.

Both Omega agents (community + facility) run in this deployment, mounted at
/api/community and /api/facility. On hyperon each agent keeps its own atom
space, exactly like the two local PeTTa processes. State lives in Vercel
Edge Config.
"""
import pathlib
import sys
from contextlib import asynccontextmanager

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


@app.get("/api/health")
def agents_health():
    return {
        "community": community.state.agent.engine.health(),
        "facility": facility.state.agent.engine.health(),
    }
