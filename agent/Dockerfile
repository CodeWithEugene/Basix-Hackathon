# Mizani agent image: SWI-Prolog + PeTTa + Omega + the Mizani FastAPI app.
# One image, two services: MIZANI_ROLE=community or MIZANI_ROLE=facility.
FROM swipl:10.0.2

# Python 3.12 via uv
COPY --from=ghcr.io/astral-sh/uv:0.11.25 /uv /uvx /bin/
ENV UV_PYTHON_INSTALL_DIR=/opt/uv-python
RUN uv python install 3.12

# OS deps for janus-swi (Python.h comes with the uv-managed python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/agent

# Pinned vendor dependencies at build time (same pins as the repo submodules)
RUN mkdir -p vendor && \
    git clone --depth 1 https://github.com/trueagi-io/PeTTa.git vendor/petta && \
    git -C vendor/petta fetch --depth 1 origin tag v1.0.4 && \
    git -C vendor/petta checkout v1.0.4 && \
    git clone https://github.com/singnet/Omega.git vendor/omega && \
    git -C vendor/omega checkout 31ff0aad24fbfc071cfc741101ece4d313e7f3e2

# Python deps first for layer caching
COPY agent/pyproject.toml agent/uv.lock ./
RUN PETTA_PATH=/app/agent/vendor/petta uv sync --python 3.12 --no-dev

# App code
COPY agent/mizani ./mizani
COPY agent/plugins ./plugins

ENV PETTA_PATH=/app/agent/vendor/petta \
    MIZANI_MEMORY_DIR=/data \
    MIZANI_ROLE=community \
    MIZANI_PEER= \
    TYPESAFE_API_KEY= \
    PORT=8101

EXPOSE 8101

# Seed the role's memory, then serve. Seeds are idempotent per fresh volume.
CMD ["/bin/sh", "-c", "mkdir -p /data && \
  if [ \"$MIZANI_SEED\" != \"no\" ]; then \
    .venv/bin/python -m mizani.seed truncate && \
    .venv/bin/python -m mizani.seed community && \
    if [ \"$MIZANI_ROLE\" = \"facility\" ]; then .venv/bin/python -m mizani.seed facility; fi; \
  fi && \
  .venv/bin/python -m uvicorn mizani.app:create_app --factory --host 0.0.0.0 --port ${PORT}"]
