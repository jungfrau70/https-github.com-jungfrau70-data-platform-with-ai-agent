# Speckit Implementation Plan (구현 계획)

## 1. Infra & Environment Setup
- [x] **Project Structure**: 디렉토리 구조 초기화 (`backend`, `frontend`, `speckit`).
- [x] **Docker Compose**: `docker-compose.yml` 작성 (Neo4j, Qdrant, FastAPI, Nuxt).
- [x] **Environment**: `.env` 설정 및 의존성 관리 (`requirements.txt`, `package.json`).

## 2. Backend Implementation (FastAPI)
- [x] **Core**: Config (Pydantic), DB Connections (Neo4j/Qdrant).
- [x] **Auth**:
    - JWT (Access/Refresh) 발급 및 검증 로직.
    - User Model & CRUD.
    - API Endpoints (`/auth/login`, `/auth/signup`).
- [x] **Chat Feature**:
    - `ChatService`: 대화 내역 Graph(Neo4j) 저장/조회.
    - API: `/chat/conversations`, `/chat/messages`.
- [x] **Analysis Feature**:
    - `AnalysisService`: 파일 업로드(CSV, Excel, **Pickle**) 및 EDA.
    - API: `/analysis/upload`.
- [x] **Video Feature**:
    - `VideoService`: HeyGen API 연동 (Simulation).
    - API: `/video/generate`.
- [x] **Integrations**:
    - `PaymentService`: PortOne 결제 검증.
    - `SNSService`: YouTube OAuth/Upload Stub.

## 3. Frontend Implementation (Nuxt 3)
- [x] **Setup**: Nuxt 3 + TailwindCSS + Pinia.
- [x] **Auth**:
    - `useAuthStore`: 로그인/회원가입 상태 관리.
    - Middleware: `auth.ts` (Route Protection).
    - Pages: `login.vue`, `signup.vue`.
- [x] **Chat UI**:
    - `useChatStore`.
    - `pages/chat/index.vue`: 사이드바(대화목록), 메시지창.
- [x] **Dashboard UI**:
    - `useAnalysisStore`.
    - `pages/dashboard.vue`: 파일 업로드 및 통계 시각화.

## 4. Testing & Quality (TDD)
- [x] **Environment**: `pytest` 설정 (`pytest.ini`).
- [x] **TDD Execution**: `.pkl` 파일 지원 기능에 대한 Red-Green 테스트 수행.
    - `tests/test_analysis.py` 통과 확인.

## 5. Verification
- [x] **Spec Alignment**: 기능 명세서(`specification.md`)와 구현 사항 일치 확인.
- [x] **Type Safety**: Frontend TypeScript Strict Mode 준수 확인 (`tsconfig.json`).
