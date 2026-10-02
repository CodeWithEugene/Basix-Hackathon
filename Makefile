# Mizani: two Omega agents reconcile a maternal referral.
# Requires: swi-prolog (10.0.2), uv, pnpm, Node 20+.

SHELL := /bin/zsh
AGENT_DIR := agent
WEB_DIR := web
export PETTA_PATH := $(abspath $(AGENT_DIR)/vendor/petta)

.PHONY: setup seed dev dev-agents dev-web test test-agent test-web clean

setup:
	cd $(AGENT_DIR) && uv sync --python 3.12
	printf 'import os\nif os.environ.get("COVERAGE_PROCESS_START"):\n    import coverage\n    coverage.process_startup()\n' > $(AGENT_DIR)/.venv/lib/python3.12/site-packages/sitecustomize.py
	cd $(WEB_DIR) && pnpm install

seed:
	cd $(AGENT_DIR) && uv run python -m mizani.seed truncate
	cd $(AGENT_DIR) && uv run python -m mizani.seed community
	cd $(AGENT_DIR) && uv run python -m mizani.seed facility

dev:
	./scripts/dev.sh

test:
	cd $(AGENT_DIR) && PETTA_PATH=$(PETTA_PATH) COVERAGE_PROCESS_START=pyproject.toml uv run pytest --cov=mizani --cov-report=term-missing
	$(MAKE) seed
	cd $(WEB_DIR) && pnpm exec playwright test tests/e2e/demo.spec.ts

lint:
	cd $(WEB_DIR) && pnpm lint
	./scripts/check-no-dashes.sh

screenshots:
	$(MAKE) seed
	cd $(WEB_DIR) && pnpm exec playwright test tests/e2e/screenshots.spec.ts

clean:
	rm -rf $(AGENT_DIR)/memory/*.metta $(AGENT_DIR)/memory/*.json $(AGENT_DIR)/memory/*.jsonl $(AGENT_DIR)/memory/*.tmp
