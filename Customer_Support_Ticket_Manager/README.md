# Customer Support API

A backend service for managing customer-support tickets. The project is being built incrementally, starting with a reliable REST API and relational database, then evolving into an AI-assisted support workflow.

> **Project status:** Development in progress. This repository is currently in the backend foundation stage. Features listed as *Planned* describe the target architecture and may not be implemented yet.

## Goals

- Provide a well-structured REST API for creating, retrieving, updating, filtering, and deleting support tickets.
- Persist ticket data in PostgreSQL using SQLAlchemy.
- Validate request and response data with Pydantic.
- Build confidence in testing, configuration, database migrations, and operational reliability.
- Later add AI-assisted support capabilities with LangChain and LangGraph, with tracing and evaluation through LangSmith.

## Technology Stack

| Technology | Purpose | Status |
|---|---|---|
| Python | Application language | In use |
| FastAPI | REST API and dependency injection | Core stack |
| Pydantic | Request validation and response schemas | Core stack |
| SQLAlchemy 2.x | ORM, queries, and session management | Core stack |
| PostgreSQL | Persistent relational storage | Core stack |
| Psycopg 3 | PostgreSQL driver | Core stack |
| Alembic | Database schema migrations | Planned |
| Pytest + HTTPX | Automated unit and API tests | Planned |
| LangChain | LLM integrations and reusable AI components | Planned |
| LangGraph | Stateful, multi-step support workflows | Planned |
| LangSmith | LLM tracing, debugging, and evaluation | Planned |
| RAG | Answers grounded in approved support documents | Planned |
| MCP | Expose selected support capabilities to compatible AI clients | Optional future integration |

## Target Capabilities

### Ticket management

- Create a support ticket.
- List tickets and retrieve a ticket by ID.
- Update ticket details and status.
- Filter tickets by status or priority.
- Delete tickets when appropriate.
- Validate input and return consistent error responses.

### Reliability and maintainability

- Keep API schemas, database models, and application logic clearly separated.
- Use environment variables for configuration and keep secrets out of source control.
- Manage database sessions per request and handle transaction failures safely.
- Add automated tests for business logic, API behavior, and database interactions.
- Use Alembic migrations for schema changes after the initial model setup.
- Add structured logging, health checks, and deployment configuration as the service matures.

### AI-assisted support — later phase

- Classify tickets and summarize customer messages.
- Retrieve relevant passages from approved support policies using RAG.
- Generate draft responses grounded in retrieved information.
- Use LangGraph to coordinate workflow steps, conditional routing, retries, and human approval where needed.
- Use LangSmith to inspect traces and evaluate AI behavior.

AI features will be introduced only after the core API and database behavior are tested and stable. AI-generated responses should remain reviewable, and sensitive or consequential actions should not be performed without appropriate authorization and safeguards.

## Architecture Direction

The intended request flow is:

```text
Client
  |
  v
FastAPI routes
  |
  v
Pydantic request/response schemas
  |
  v
Application logic
  |
  v
SQLAlchemy session and ORM models
  |
  v
PostgreSQL
```

In a later phase, selected workflows may call AI services:

```text
Support request
  |
  v
LangGraph workflow
  |---- ticket classification / summarization (LangChain)
  |---- retrieval from approved support documents (RAG)
  |---- draft response and routing
  |---- human review when required
  |
  v
Trace and evaluate AI runs with LangSmith
```

These diagrams describe the intended architecture; they are not a claim that every component is already implemented.

## Development Setup

### Prerequisites

- Python 3.10 or newer
- PostgreSQL installed and running locally, or access to a PostgreSQL instance
- Git (recommended)

### 1. Create and activate a virtual environment

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, use:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install the initial backend dependencies

```bash
python -m pip install --upgrade pip
python -m pip install fastapi "uvicorn[standard]" sqlalchemy "psycopg[binary]"
```

Testing, settings management, and migration dependencies will be added as the relevant project stages are implemented.

### 3. Create the PostgreSQL database

For a local PostgreSQL installation, create a database named `customer_support_db` using your preferred PostgreSQL role and authentication setup. For example, if your local PostgreSQL configuration permits it:

```bash
createdb customer_support_db
```

The database must exist before the application connects to it. SQLAlchemy's `Base.metadata.create_all()` can create tables inside an existing database; it does **not** create the PostgreSQL database itself.

### 4. Configure the database connection

Set `DATABASE_URL` in your local environment. The following is an example format, not a real credential:

```bash
export DATABASE_URL="postgresql+psycopg://DB_USER:DB_PASSWORD@localhost:5432/customer_support_db"
```

Replace the placeholders with your local database credentials. If a password contains reserved URL characters, URL-encode those characters. Do not commit credentials, API keys, or `.env` files containing secrets to Git.

### 5. Run the API

The API entry point and run command will be documented here once the first FastAPI application module and health endpoint are implemented. Until then, the repository is still in the setup/model-building stage.

## Database and Schema Management

The initial learning stage will use SQLAlchemy models and `Base.metadata.create_all()` to create missing tables in the existing database. `create_all()` is suitable for bootstrapping a learning project, but it does not replace schema migrations. Once the schema starts evolving, Alembic will be used to create, review, and apply migrations.

## Testing Strategy

The project will grow a test suite that covers:

- Model and business-logic behavior
- Request validation and response shapes
- Successful CRUD operations and not-found cases
- Invalid input and error responses
- Database persistence and transaction behavior
- AI retrieval and workflow evaluations when AI features are added

Tests should use isolated test data and a dedicated test database or other explicit test setup. Avoid running destructive tests against a production database.

## Configuration and Security Principles

- Keep credentials and service keys in environment variables or an appropriate secrets manager.
- Do not log passwords, authorization headers, or sensitive customer content unnecessarily.
- Add authentication and authorization before exposing private ticket data beyond a trusted local environment.
- Validate user input and enforce allowed status/priority values at the API boundary and, where appropriate, in the database.
- Apply least-privilege database permissions.
- Treat AI output as untrusted input; validate it and require human approval for sensitive actions.
- Define retention and access rules before sending customer information to external AI providers.

## Suggested Project Structure

The structure will grow as features are implemented. A likely target is:

```text
customer-support-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and lifespan setup
│   ├── database.py      # Engine, session factory, and Base
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── dependencies.py  # Shared FastAPI dependencies
│   ├── routes/           # API endpoints
│   ├── services/         # Business logic
│   └── ai/               # Later: LangChain / LangGraph workflows
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt     # Or another dependency/lock-file approach
```

This is a proposed structure, not a claim that all listed modules already exist.

## Roadmap

- [ ] Establish the local Python environment and PostgreSQL database.
- [ ] Configure SQLAlchemy engine, session factory, and declarative base.
- [ ] Define the `Ticket` ORM model and create the initial table.
- [ ] Add Pydantic schemas and a FastAPI health endpoint.
- [ ] Implement ticket CRUD endpoints.
- [ ] Add filtering, consistent errors, and request validation.
- [ ] Add automated tests and database test fixtures.
- [ ] Add environment-based settings, Alembic migrations, and operational logging.
- [ ] Add ticket classification and summarization with LangChain.
- [ ] Add LangSmith tracing and evaluation.
- [ ] Add policy-grounded RAG.
- [ ] Add a LangGraph support workflow with human review where appropriate.
- [ ] Evaluate whether MCP is needed for external AI-tool integration.

## Scope

This is a learning project intended to build toward a commercially useful backend. It should not be described as production-ready until security, authorization, migrations, observability, test coverage, deployment, backup/recovery, and operational requirements have been implemented and verified.
