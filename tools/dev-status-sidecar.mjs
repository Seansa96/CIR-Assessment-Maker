import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import process from "node:process";

const projectRoot = process.env.CIR_PROJECT_ROOT
  ? path.resolve(process.env.CIR_PROJECT_ROOT)
  : process.cwd();
const statusPath = process.env.CIR_PROCESS_STATUS_PATH
  ? path.resolve(process.env.CIR_PROCESS_STATUS_PATH)
  : path.join(projectRoot, ".cir-processes.json");
const port = Number(process.env.CIR_STATUS_PORT ?? 4789);
const host = process.env.CIR_STATUS_HOST ?? "127.0.0.1";

function pidAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

function normalizeService(raw, fallbackUrl) {
  const pid = Number(raw?.pid ?? raw?.Pid ?? raw?.BackendPid ?? raw?.FrontendPid ?? 0) || null;
  const rawState = String(raw?.state ?? raw?.State ?? "unknown");
  const alive = pidAlive(pid);
  let state = rawState;

  if ((rawState === "running" || rawState === "starting") && pid && !alive) {
    state = "crashed";
  }

  return {
    state,
    pid,
    alive,
    url: raw?.url ?? raw?.Url ?? fallbackUrl,
    lastMessage: raw?.lastMessage ?? raw?.LastMessage ?? null,
    startedAt: raw?.startedAt ?? raw?.StartedAt ?? null,
    exitedAt: raw?.exitedAt ?? raw?.ExitedAt ?? null,
    exitCode: raw?.exitCode ?? raw?.ExitCode ?? null
  };
}

async function readStatus() {
  if (!existsSync(statusPath)) {
    return {
      schemaVersion: 1,
      updatedAt: new Date().toISOString(),
      source: statusPath,
      sidecar: {
        state: "running",
        pid: process.pid,
        url: `http://${host}:${port}`
      },
      backend: {
        state: "unknown",
        pid: null,
        alive: false,
        url: "http://localhost:5000",
        lastMessage: ".cir-processes.json not found"
      },
      frontend: {
        state: "unknown",
        pid: null,
        alive: false,
        url: "http://127.0.0.1:4321"
      }
    };
  }

  const text = await readFile(statusPath, "utf8");
  const raw = JSON.parse(text);
  const backendRaw = raw.backend ?? raw.Backend ?? { BackendPid: raw.BackendPid };
  const frontendRaw = raw.frontend ?? raw.Frontend ?? { FrontendPid: raw.FrontendPid };

  return {
    schemaVersion: raw.schemaVersion ?? raw.SchemaVersion ?? 1,
    updatedAt: raw.updatedAt ?? raw.UpdatedAt ?? null,
    source: statusPath,
    sidecar: {
      state: "running",
      pid: process.pid,
      url: `http://${host}:${port}`
    },
    backend: normalizeService(backendRaw, "http://localhost:5000"),
    frontend: normalizeService(frontendRaw, "http://127.0.0.1:4321")
  };
}

const server = createServer(async (request, response) => {
  response.setHeader("Access-Control-Allow-Origin", "*");
  response.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  response.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (request.method === "OPTIONS") {
    response.writeHead(204);
    response.end();
    return;
  }

  if (request.url === "/health") {
    response.writeHead(200, { "Content-Type": "application/json" });
    response.end(JSON.stringify({ ok: true, pid: process.pid }));
    return;
  }

  if (request.url === "/dev/process-status") {
    try {
      const status = await readStatus();
      response.writeHead(200, { "Content-Type": "application/json" });
      response.end(JSON.stringify(status));
    } catch (error) {
      response.writeHead(500, { "Content-Type": "application/json" });
      response.end(JSON.stringify({
        error: "STATUS_READ_FAILED",
        message: error instanceof Error ? error.message : "Could not read process status."
      }));
    }
    return;
  }

  response.writeHead(404, { "Content-Type": "application/json" });
  response.end(JSON.stringify({ error: "NOT_FOUND" }));
});

server.listen(port, host, () => {
  console.log(`[dev-status-sidecar] listening on http://${host}:${port}`);
  console.log(`[dev-status-sidecar] reading ${statusPath}`);
});
