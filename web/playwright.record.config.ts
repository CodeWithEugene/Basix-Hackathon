import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  testMatch: "record-demo.spec.ts",
  timeout: 480_000,
  retries: 0,
  workers: 1,
  use: {
    viewport: { width: 1920, height: 1080 },
    video: { mode: "on", size: { width: 1920, height: 1080 } },
    trace: "off",
    colorScheme: "light",
  },
  outputDir: "/tmp/mizani-video/record",
});
