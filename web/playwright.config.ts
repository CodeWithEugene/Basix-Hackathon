import { defineConfig } from "@playwright/test";

const agentCmd = (role: string, port: string) =>
  `cd ../agent && MIZANI_ROLE=${role} PETTA_PATH=$PWD/vendor/petta MIZANI_MEMORY_DIR=$PWD/memory MIZANI_PEER=http://127.0.0.1:8102 exec .venv/bin/python -m uvicorn mizani.app:create_app --factory --port ${port}`;

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 120_000,
  retries: 0,
  use: {
    baseURL: "http://localhost:3100",
    trace: "retain-on-failure",
  },
  webServer: [
    {
      command: agentCmd("community", "8101"),
      port: 8101,
      reuseExistingServer: false,
      timeout: 120_000,
    },
    {
      command: agentCmd("facility", "8102"),
      port: 8102,
      reuseExistingServer: false,
      timeout: 120_000,
    },
    {
      command: "pnpm dev -p 3100",
      port: 3100,
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
});
