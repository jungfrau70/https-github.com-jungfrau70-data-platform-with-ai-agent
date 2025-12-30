# Backend Guide (backend/AGENTS.md)

## 1. 개요
GC101의 백엔드는 **FastAPI**를 기반으로 하며, **LangGraph**를 통한 에이전트 오케스트레이션과 **GraphRAG** (Neo4j + Qdrant)를 수행합니다.

## 2. 주요 기술 스택
- **Framework**: FastAPI (Async)
- **AI/Agent**: LangChain, LangGraph
- **Database**: 
  - Neo4j (Graph DB)
  - Qdrant (Vector DB)

## 3. 개발 환경 설정 (Setup)
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. 실행 (Run)
```bash
uvicorn main:app --reload
```
- Swagger UI 확인: `http://localhost:8000/docs`

## 5. 테스트 (Test)
```bash
pytest
```
- DB 통합 테스트 시 Docker 컨테이너가 실행 중이어야 합니다.

## 6. 디렉토리 구조
- `app/core/agent_graph.py`: LangGraph 정의 (Router, Nodes)
- `app/services/`: 비즈니스 로직
- `app/api/`: API 엔드포인트
