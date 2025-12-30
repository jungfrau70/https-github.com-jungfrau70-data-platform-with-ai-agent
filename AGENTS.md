# Project Guide for Agents (AGENTS.md)

This file provides context and instructions for AI agents working on this project.

## Project Overview
**Name**: GC101
**Type**: AI-powered Data Platform
**Stack**:
- **Backend**: Python (FastAPI), LangChain, Neo4j (Graph DB), Qdrant (Vector DB).
- **Frontend**: Nuxt 3 (Vue.js), TailwindCSS, Pinia.
- **Infrastructure**: Docker Compose.

## Directory Structure
- `backend/`: FastAPI application.
  - `app/`: Core logic (API, Models, Services).
  - `tests/`: Pytest suite.
- `frontend/`: Nuxt 3 application.
  - `pages/`, `components/`: UI logic.
- `docker-compose.yml`: Orchestrates Backend, Frontend, Neo4j, and Qdrant.

## Coding Standards & Rules
- **MCP Priority**: When extending functionality or integrating external tools, prioritize using **MCP (Model Context Protocol) Servers** over custom implementations.
- **Language**: All documentation (READMEs, design docs, comments for logic explanation) MUST be written in **Korean** (Hangul).
- **Logging**: All major logic (Agent decisions, API requests, DB operations) MUST be logged to both console and file for debugging and state tracking.
  - Use `app.core.logger.get_logger`.
  - Log `INFO` for state transitions and `ERROR` for exceptions.
- **State Management**: Agent state transitions should be explicit and traceable.

## 서브프로젝트별 가이드 (Sub-project Guides)
각 컴포넌트의 상세 설정 및 개발 가이드는 아래 문서를 참조하십시오:

- **Backend API & AI Logic**: [backend/AGENTS.md](backend/AGENTS.md)
  - 내용: FastAPI 설정, LangGraph 구조, Pytest 실행법.
- **Frontend UI**: [frontend/AGENTS.md](frontend/AGENTS.md)
  - 내용: Nuxt 3 설정, UI 컴포넌트 구조, Playwright 테스트.

## 공통 작업 (Common Tasks)
- **Infrastructure**: `docker-compose.yml`을 통해 전체 스택 실행.
  ```bash
  docker-compose up --build
  ```

## 중요 파일 (Critical Files)
- `docker-compose.yml`: 전체 서비스 정의.
- `README.md`: 프로젝트 전체 개요 (Why/How/What).