# Enrichment Hub / Hypatos Setup Screenshot Notes

Use these notes when the current repository is `hypatos/enrichment-hub` or the user asks for Enrichment Hub screenshots.

## Known Local Stack

- Frontend lives in `ui/` and can run with `ui/node_modules/.bin/rsbuild dev`.
- Frontend dev URL is commonly `http://localhost:3001/`.
- Backend runs on `http://localhost:8087/` via `./gradlew run`.
- Prompting Service may already run on `http://localhost:8000/`.
- Redis may be required: `docker compose up -d redis`.

## Useful Environment

For local screenshot runs where Prompting Service is already available:

- `SECURITY__ENABLED=false`
- `PROMPTING_SERVICE__URL=http://localhost:8000/`
- `API_GATEWAY__URL=http://localhost:18080`
- `USERS_API__URL=http://localhost:18080`
- `COMPANY_API__URL=http://localhost:18080`
- `PROJECTS_API__URL=http://localhost:18080`
- `TEMPORALIO__ENABLED=false`

If backend feature-flag env override fails, do not force config edits. In the chosen UI automation layer, intercept only `POST /v1/feature-flags` and enable the specific feature flag under test.

## Support Stub Pattern

A small local stub on `localhost:18080` can unblock unrelated platform dependencies:

- `POST /auth/token`
- `GET /users/idp/{id}`
- `GET /users/{id}`
- `GET /users`
- `GET /companies`
- `GET /projects`

Do not stub workflow template or agent template data when validating template UI. Those should come through Enrichment Hub from Prompting Service.

## Template UI Context

Known company for local UI validation:

- `653faf4b8a0bc680a6bff124`

Useful localStorage preload:

- `selectedCompanyId = "653faf4b8a0bc680a6bff124"`
- `user = {"id":"stub-user","name":"Dummy User","email":"dummy@example.com","active":true,"internal":true}`

Useful routes:

- Workflows list: `/llm-prompting/settings`
- New agent editor: `/llm-prompting/agents/new`

Useful checks:

- `GET http://localhost:8087/v1/health`
- `GET http://localhost:3001/`
- `GET http://localhost:8087/v1/workflow-templates/prebuilt`
- `GET http://localhost:8087/v1/prompting-settings/templates`

For prebuilt workflow templates, verify labels such as:

- `Prebuilt Workflow Templates`
- `Import unavailable`
- `Workflow data model`
- `Configuration Variables`

For agent templates, verify labels such as:

- `Use Template`
- `Invoice Extraction (Generic)`
- `Prompt`
- `Copy Template`
