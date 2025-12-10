# Speckit Project Constitution (헌법 및 코딩 규칙)

## 1. 프로젝트 비전 및 철학
- **Golden Circle**: "WHY - HOW - WHAT" 프레임워크를 적용하여 데이터의 본질적 가치를 탐구하고, 이를 콘텐츠로 확장한다.
- **Data Integrity**: 모든 분석과 콘텐츠는 검증된 데이터에 기반해야 한다 (Grounding).
- **Automation First**: 반복적인 분석 및 콘텐츠 생성 과정은 AI를 통해 자동화한다.

## 2. 기술 스택 및 아키텍처
- **4-Tier Architecture**:
    - **Frontend**: Nuxt.js (Vue 3, TypeScript, TailwindCSS, Pinia).
    - **Backend**: FastAPI (Python 3.10+, Pydantic).
    - **Vector DB**: Qdrant (지식 검색/RAG).
    - **Graph DB**: Neo4j (관계 추론/Context).
    - **Infra**: Docker Compose 기반 컨테이너 오케스트레이션.
- **AI/ML**:
    - LangChain (Orchestration).
    - HeyGen (Video Synthesis).
    - Google Gemini / OpenAI GPT (LLM).

## 3. 코딩 표준 (Coding Standards)
### 3-1. General
- **언어**: 코드는 영어, 주석 및 문서는 한국어/영어 병기를 원칙으로 한다.
- **네이밍**:
    - Python: `snake_case` (변수/함수), `PascalCase` (클래스).
    - JS/TS: `camelCase` (변수/함수), `PascalCase` (컴포넌트/클래스).
- **Type Safety**:
    - Python: Type Hinting 필수 (`typing` 모듈, Pydantic 모델).
    - TypeScript: `any` 사용 지양, 인터페이스/타입 정의 필수. (Strict Mode 준수).

### 3-2. Testing & Quality (TDD)
- **TDD (Test Driven Development)**:
    - 새로운 기능 구현 시 실패하는 테스트를 먼저 작성(Red)하고 통과하는 코드(Green)를 작성한다.
    - 주요 로직(Service, Utils)에 대한 단위 테스트 커버리지를 유지한다.
- **Testing Tools**:
    - Backend: `pytest`, `pytest-asyncio`.
- **Linting**:
    - ESLint, Prettier, Black/Ruff 준수.

### 3-3. Commit & Git
- **Conventional Commits**: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `ore:` 접두어 사용.
- **Branch Strategy**: `main` (Production), `develop` (Dev), `feature/*`.

## 4. 보안 가이드라인
- **Secrets**: API Key 등 민감 정보는 `.env`로 관리하며 Repo에 커밋하지 않는다.
- **Auth**:
    - JWT Access (Short) / Refresh (Long) 토큰 정책 준수.
    - Refresh Token은 `HttpOnly Secure Cookie`에 저장.
    - Refresh Token Rotation 적용.
- **Input Validation**: 모든 사용자 입력은 검증(Sanitization) 후 처리한다.
