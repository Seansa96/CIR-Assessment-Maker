# Antigravity Implementation Plan: LAN Server Distribution and Shared-Token Access

## Status

- **Audience:** Antigravity IDE agent
- **Project:** CIR Assessment Maker
- **Branch:** `codex/server-lan-access`
- **Feature:** First browser-accessible LAN server distribution
- **Plan state:** Ready for implementation
- **Priority:** Reachable, encrypted, authenticated vertical slice

Before implementation, read:

- `AGENTS.md`
- `GEMINI.md`
- `docs/agent-coexistence.md`
- `README.md`
- `backend/src/QuizApp.Api/Program.cs`
- `frontend/src/pages/index.astro`
- `frontend/astro.config.mjs`
- `utility_user_scripts/start_cir.ps1`
- Current attempt/session, SQLite retention, Guided Project, settings, and code-runner configuration

Run `git status --short --branch` before editing. Work only on `codex/server-lan-access`. Do not reset, clean, delete, rewrite, or merge unrelated work.

## Execution Constraints

- Prioritize a working LAN-hosted vertical slice over production-scale identity features.
- Do not implement user accounts, registration, password recovery, email, roles, cloud hosting, internet exposure, or per-user grade books in V1.
- Do not expose the Piston service, SQLite database, project-session directory, symbolic adapter, or development server directly to the LAN.
- Do not transmit the shared access token over plain HTTP.
- Do not store the shared access token in source control or in reversible plaintext configuration.
- Keep the existing localhost development workflow available.
- Keep storage migrations additive and non-destructive.
- Avoid broad frontend/backend refactors.
- Run only focused security tests, builds, and one LAN smoke check.
- At completion, report files changed, commands run, checks passed/failed, server URL, certificate setup, and remaining manual checks.

## Summary

Package the Astro frontend and ASP.NET Core backend as one same-origin HTTPS server that can bind to a LAN interface. A browser visiting the server receives a login screen, enters a shared access token, and receives an encrypted, `HttpOnly` authentication cookie after successful verification.

V1 is intentionally one shared study workspace:

- all authorized testers see the same assessment catalog
- attempts, grades, settings, and analytics remain shared
- existing attempt IDs and lifecycle remain unchanged
- active in-memory attempts remain restart-volatile unless explicitly saved/paused
- no user-specific ownership or privacy guarantees exist yet

The authentication ticket should contain a random browser-session identifier so later work can associate attempts and grades with a user or anonymous tester without replacing the authentication boundary.

## Target Runtime Shape

Use one externally reachable application origin:

```text
Browser on LAN
    |
    | HTTPS :5443
    v
ASP.NET Core / Kestrel
    |-- serves built Astro files
    |-- serves /api/*
    |-- shared-token authentication
    |-- SQLite retention
    |-- YAML/JSON assessment catalog
    |
    +-- localhost-only Piston adapter
    +-- local Node symbolic adapter
```

Do not run the Astro development server for the LAN distribution. It remains a development-only process.

## Phase 1: Same-Origin Server Distribution

### Serve The Frontend From ASP.NET Core

- Keep Astro output static.
- Change the production frontend API base from a hard-coded localhost URL to same-origin `/api`.
- Preserve `PUBLIC_API_BASE` as a development override.
- Add static-file and SPA fallback handling to `QuizApp.Api`:
  - `UseDefaultFiles`
  - `UseStaticFiles`
  - map API endpoints before fallback
  - fallback unknown non-API routes to `index.html`
- Ensure `/api/*` never falls through to the SPA.
- Do not serve source maps in the packaged server unless explicitly enabled for diagnostics.

### Publish Pipeline

Add a deterministic PowerShell publish script, for example:

```text
utility_user_scripts/publish_lan_server.ps1
```

It should:

1. Run `npm ci` only when dependencies must be restored.
2. Run the Astro production build.
3. Copy `frontend/dist/` into the API publish `wwwroot`.
4. Run `dotnet publish` for `QuizApp.Api`.
5. Produce one versioned output directory under `artifacts/lan-server/`.
6. Include configuration templates and server-start documentation.
7. Exclude runtime databases, access tokens, certificates, Data Protection keys, logs, and personal attempt data from the distributable.

Prefer a framework-dependent Windows build initially because the host already uses .NET 8. Optionally support a self-contained `win-x64` publish flag, but do not make it the only path.

### Data Location

Do not assume the published executable's directory is writable forever.

Add an explicit server data-root setting:

```text
CIR_DATA_ROOT
```

Default behavior:

- development: existing repository `data/`
- packaged server: a configured writable directory outside the immutable application files

The server should fail startup with a clear message if its data root or SQLite directory cannot be created or written.

Do not copy personal `quizapp.db`, project sessions, logs, or active attempt files into the distribution automatically.

## Phase 2: Shared-Token Authentication

### Authentication Model

Add a small Core/API abstraction for the authenticated browser context:

```csharp
public interface IAccessContext
{
    bool IsAuthenticated { get; }
    string? SessionId { get; }
}
```

V1 authentication has:

- one configured shared access token
- no username
- no account record
- no profile
- one random `SessionId` per authenticated browser login
- one shared authorization level with full current app access

The session ID is a future ownership hook only. Do not scope attempts, grades, settings, or analytics by it in this slice.

### Token Configuration

Use environment variables or a protected local secret file outside source control:

```text
CIR_ACCESS_TOKEN_HASH
CIR_ACCESS_TOKEN_SALT
```

Preferred implementation:

- hash the distributed token with ASP.NET Core's supported PBKDF2 password-hashing facilities
- compare through the framework verifier
- never log the submitted token
- never return the configured hash or salt through an API
- never place the plaintext token in `appsettings.json`, scripts, GitHub Actions, command history examples, or generated distributions

Add a local token-hash utility mode or dedicated script that prompts without echoing:

```powershell
.\utility_user_scripts\configure_lan_access.ps1
```

The utility should:

- securely prompt for a token
- require a reasonable minimum length, recommended 20+ random characters
- generate a verifier/hash
- write only protected local configuration or print an environment-variable command for the operator
- never print the plaintext token after entry

If a local configuration file is used, add its concrete path/pattern to `.gitignore`.

### Login Flow

Add unauthenticated endpoints:

```http
GET  /api/access/status
POST /api/access/login
POST /api/access/logout
GET  /health/live
```

Behavior:

- `status` reports only whether this browser is authenticated.
- `login` accepts the token, verifies it, creates a random session ID, and signs in.
- `logout` clears the authentication cookie.
- `health/live` returns minimal process health without catalog, path, version, database, or secret details.

All existing application API endpoints must require authentication. Swagger and Swagger JSON remain development-only and localhost-only.

### Authentication Cookie

Use ASP.NET Core cookie authentication:

- `HttpOnly: true`
- `Secure: true`
- `SameSite: Strict`
- explicit short name, such as `cir_access`
- finite lifetime, recommended 12 hours
- sliding expiration allowed
- no persistent cookie unless the user explicitly chooses a future "remember this browser" option
- protected by ASP.NET Core Data Protection

Persist Data Protection keys in an operator-controlled directory outside the published binaries so logins survive normal process restarts:

```text
CIR_KEY_RING_PATH
```

Protect that directory with host filesystem permissions. Add it to ignore rules if it is inside the repository during development.

### Login UI

Add a compact server-access gate before app initialization:

- product name
- token input with show/hide control
- Connect button
- concise invalid-token and connection messages
- no account/profile language
- no access-token storage in localStorage or sessionStorage

On page load:

1. Request `/api/access/status`.
2. If authenticated, initialize the existing application.
3. Otherwise show only the access gate.
4. After successful login, initialize the application without a full client install.
5. On a `401` from any API call, clear sensitive in-memory UI state and return to the gate.

All production fetches should use same-origin URLs. Cookie credentials then follow the browser's same-origin defaults; setting `credentials: "same-origin"` explicitly is acceptable.

## Phase 3: TLS And LAN Binding

### Kestrel Binding

Add a server configuration profile that binds Kestrel to a configurable LAN endpoint:

```text
CIR_BIND_URL=https://0.0.0.0:5443
```

Do not replace localhost development URLs. The LAN start script should opt into the external bind explicitly.

### Certificate

HTTPS is mandatory because the shared token must be encrypted in transit.

Support a configured PFX:

```text
CIR_CERTIFICATE_PATH
CIR_CERTIFICATE_PASSWORD
```

Recommended LAN testing workflow:

1. Give the server a stable hostname or DHCP reservation.
2. Generate a certificate for that hostname and/or LAN IP using `mkcert` or another locally trusted CA.
3. Install/trust the local CA certificate on each approved test device.
4. Configure Kestrel with the generated PFX.
5. Share only the application access token with approved testers.

Document that a self-signed certificate producing browser warnings is not an acceptable final testing path. Users should not be trained to bypass TLS warnings.

Do not commit:

- `.pfx`, `.pem`, `.key`, or CA private keys
- certificate passwords
- Data Protection keys
- token hashes tied to the live server

### HTTP Behavior

For V1:

- either do not bind an HTTP LAN port at all, or
- bind a dedicated HTTP port only to redirect to the configured HTTPS hostname

Never accept login tokens over the HTTP endpoint.

### Host Firewall

Add operator documentation and an optional helper script for a narrowly scoped Windows Firewall rule:

- inbound TCP only
- selected application port only
- Private network profile only
- optional `LocalSubnet` remote-address scope
- no public-profile rule
- no automatic router port forwarding

The script must require explicit operator confirmation and include a matching remove-rule command. Do not modify firewall state during build or ordinary startup.

## Phase 4: Request Security

### Authorization Boundary

Apply authorization centrally:

- use a fallback authorization policy requiring authentication
- explicitly allow anonymous access only to login/status/logout as appropriate, health, and required static login assets
- avoid manually adding token checks to dozens of endpoints

Static application assets may be served before authentication because they contain no user data, but API data and operations must remain protected.

### Login Rate Limiting

Use ASP.NET Core rate limiting on the login endpoint:

- small burst, for example 5 attempts
- refill window, for example 5 minutes
- partition by remote IP when available
- add a conservative global limiter as fallback
- return `429` without indicating whether the token was close or malformed

Use a constant generic failure response:

```text
Access token was not accepted.
```

Do not expose hash timing, configuration state, or token length rules to remote clients.

### CSRF And Origin Checks

Cookie authentication makes state-changing endpoints CSRF-relevant.

For unsafe API methods (`POST`, `PUT`, `PATCH`, `DELETE`):

- use ASP.NET Core antiforgery with a readable request token and protected cookie, or
- implement an equally strong same-origin request-token pattern
- validate `Origin`/`Host` as defense in depth

Do not rely only on CORS. `SameSite=Strict` is helpful but should not be the sole future-proof control.

### Security Headers

Add focused headers suitable for the current frontend:

- `Content-Security-Policy` compatible with Astro, KaTeX, MathLive, CodeMirror, and local media
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: no-referrer`
- `Permissions-Policy` disabling unused capabilities
- frame protection through CSP `frame-ancestors 'none'`
- HSTS for the LAN HTTPS profile after certificate trust is confirmed

Do not weaken CSP with broad remote script origins. Current app assets should remain local.

### Proxy Awareness

Do not trust arbitrary forwarded headers by default. Add a documented, disabled-by-default reverse-proxy mode for future Caddy/nginx/Tailscale deployment with explicit known proxy addresses/networks.

## Phase 5: Session And Concurrency Foundation

### Authentication Sessions

Authentication sessions are maintained by the protected cookie and Data Protection key ring. The server does not need a persistent server-side login-session table in V1.

Include these claims in the ticket:

- random session ID
- issued-at time
- authentication scheme/version

Keep claim creation behind an interface so a future user ID can replace or accompany the anonymous session ID.

### Existing Assessment Sessions

Preserve current behavior:

- in-progress attempts remain in the process memory store
- paused/completed attempts remain in SQLite
- Guided Project working files remain file-backed
- explicit Save and Quit remains the restart-safe checkpoint

Add clear server-mode UI wording:

> Active work is saved across browser refreshes, but a server restart can discard progress unless you use Save and Quit.

Do not silently persist every answer merely because the app is network-accessible.

### Shared Workspace Warning

V1 authorized users share:

- settings
- grade log
- analytics
- attempt history
- assessment creator and authored content

Document this prominently for the host. Do not claim that the token provides user separation.

Because current attempt endpoints are addressed only by attempt ID, all authorized users can technically access shared history. Treat the shared token as membership in one trusted testing group.

### Future Ownership Hooks

Do not implement filtering yet, but design the next migration around:

```text
users
access_sessions
attempts.owner_user_id
grade_entries.owner_user_id
guided_project_sessions.owner_user_id
settings scope: server or user
```

Keep the V1 `SessionId` available through `IAccessContext`, but do not write it into durable academic records until the ownership policy is designed.

Future access modes should fit the same boundary:

- shared token
- invite token
- local account
- external identity provider

## Phase 6: External Services

### Piston

Piston remains server-side and localhost/container-network only:

- bind Piston to loopback or a private Docker network
- never expose port `2000` to the LAN
- browser clients call only the CIR server
- CIR server calls Piston

In server mode, hide or restrict the code-runner URL setting so an authorized browser cannot redirect code execution to an arbitrary remote service unintentionally. Prefer an operator-level environment setting for server deployments.

### Symbolic Adapter

The Node symbolic adapter remains a child/local process and requires no LAN port.

### Media

Serve assessment media through the same HTTPS origin. Verify that absolute `/assessments/...` paths continue working in the packaged frontend.

## Operator Scripts And Documentation

Add:

```text
utility_user_scripts/publish_lan_server.ps1
utility_user_scripts/start_lan_server.ps1
utility_user_scripts/configure_lan_access.ps1
docs/lan-server-hosting.md
```

The start script should:

- resolve paths relative to the script/repository or publish directory
- validate required environment variables
- validate certificate and data directories
- bind only the configured HTTPS endpoint
- show the LAN URL and local health URL
- avoid printing secrets
- run one ASP.NET process
- write PID/runtime metadata outside tracked source files

Documentation should cover:

- choosing a stable host IP/hostname
- generating and trusting a LAN certificate
- configuring the shared token
- publishing and starting
- adding/removing the firewall rule
- connecting from another device
- Save and Quit behavior
- shared-workspace limitations
- backup of YAML content, SQLite, project sessions, and Data Protection keys
- token rotation and forced logout
- stopping the server
- troubleshooting certificate, firewall, and binding failures

## Configuration Shape

Support environment variables with optional non-secret JSON defaults:

```text
CIR_SERVER_MODE=true
CIR_BIND_URL=https://0.0.0.0:5443
CIR_PUBLIC_ORIGIN=https://cir-study.lan:5443
CIR_DATA_ROOT=C:\CIR\data
CIR_KEY_RING_PATH=C:\CIR\keys
CIR_ACCESS_TOKEN_HASH=...
CIR_CERTIFICATE_PATH=C:\CIR\certs\cir-study.pfx
CIR_CERTIFICATE_PASSWORD=...
CIR_CODE_RUNNER_BASE_URL=http://127.0.0.1:2000/api/v2
```

Validate configuration at startup and fail closed:

- missing token verifier: server mode does not start
- missing/unreadable certificate: server mode does not start
- HTTP-only public origin: server mode does not start
- unwritable data/key directory: server mode does not start
- wildcard public origin for CSRF validation: server mode does not start

Development mode should continue using current defaults without requiring these settings.

## Focused Tests

### Authentication

- valid token returns an authenticated secure cookie
- invalid token returns the same generic error
- missing token verifier prevents server-mode startup
- unauthenticated API request returns `401`
- authenticated request reaches a representative read endpoint
- authenticated state survives app restart when the same Data Protection key ring is used
- logout invalidates the browser cookie
- login limiter returns `429` after the configured threshold

### Request Security

- unsafe authenticated request without antiforgery token is rejected
- unsafe request with a valid token succeeds
- insecure HTTP login is unavailable or redirected before reading a body
- production responses include required security headers
- Swagger is unavailable in the LAN production profile

### Static Hosting

- `/` returns the built Astro app
- `/api/categories` remains an API response rather than SPA fallback
- an unknown frontend route returns `index.html`
- an unknown `/api/*` route returns API `404`
- assessment media loads from the same origin

### Existing Behavior

- start an attempt from a remote-browser session
- answer a question and refresh the browser
- Save and Quit, restart the server, and resume from SQLite
- run one symbolic question
- run one code question while Piston remains inaccessible from another LAN machine

## Minimum Verification

Run once:

```powershell
dotnet build backend\QuizApp.sln --no-restore
dotnet test backend\QuizApp.sln --no-build --filter "AccessToken|ServerHosting|Antiforgery|StaticFrontend"
npm run build
```

Perform one two-device LAN smoke test:

1. Start the published server on the host.
2. Confirm the host can open the HTTPS URL without a certificate warning.
3. Confirm a second approved device can open the same URL.
4. Confirm an invalid token is rejected.
5. Confirm the approved token signs in.
6. Start and Save and Quit one assessment from the second device.
7. Restart the server and resume that paused attempt.
8. Confirm port `2000` is not reachable from the second device.

Do not run port scans, broad penetration tools, internet exposure tests, exhaustive browser automation, or the complete backend test suite in this slice.

## Acceptance Criteria

- The app is usable from a normal browser on another approved LAN device.
- No client application installation is required.
- Frontend and API are served from one HTTPS origin.
- The shared token is encrypted in transit and never stored in plaintext by the app.
- Successful login creates a protected browser session cookie.
- All application APIs require authentication.
- Login attempts are rate-limited.
- State-changing APIs have CSRF protection.
- The server binds to a configurable LAN interface and port.
- Certificates, secrets, key rings, databases, and runtime files are not committed or bundled accidentally.
- Existing localhost development remains functional.
- Existing attempt, SQLite, Guided Project, symbolic, and code-runner behavior remains compatible.
- Documentation clearly states that V1 is one shared trusted workspace without user privacy or ownership separation.

## Deferred Work

- individual user accounts and profiles
- per-user attempt, grade, settings, and analytics isolation
- invitations and token revocation per person
- administrator/read-only roles
- account recovery and email
- WebSockets or server-push synchronization
- multi-instance hosting and distributed sessions
- cloud deployment and public internet exposure
- reverse-proxy automation
- packet/protocol optimization
- audit-log UI
- automatic certificate enrollment

## Assumptions

- The host controls the LAN machine and can configure its firewall and certificate trust.
- Approved testers are trusted with shared workspace access.
- The router will not forward the CIR port to the public internet.
- One ASP.NET server instance is sufficient.
- SQLite remains the durable store.
- Existing in-memory active-attempt behavior is acceptable for V1.
- The browser is the only required client.
- The operator can rotate the shared token and Data Protection key ring if access must be revoked.
