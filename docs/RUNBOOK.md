# RUNBOOK - Cloud Security Platform (Local)

## Goal
Run a local, cloud-style platform that:
- exposes a web API
- stores data in Postgres
- produces alerts from events
- runs consistently via Docker Compose

## Prerequisites
- Windows 10/11
- Docker Desktop running
- PowerShell

## Standard Commands (to be completed as we build)
- Validate compose config: docker compose config
- Start services: docker compose up --build
- Stop services: docker compose down
- Reset everything (including DB volume): docker compose down -v

## Verification Checklist
- [ ] docker compose config succeeds
- [ ] API reachable at http://localhost:8000/health
- [ ] Postgres container is running
- [ ] API can talk to Postgres
- [ ] Alerts endpoint returns JSON

## Troubleshooting (starter)
- If Docker commands fail: confirm Docker Desktop is running
- If ports are in use: identify process using the port and stop it
