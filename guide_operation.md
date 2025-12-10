# 서비스 운영 및 테스트 가이드 (Operation & Test Guide)

본 문서는 로컬 개발 환경(Test)과 도커 환경(Docker)에서의 서비스 시작 및 종료 방법을 안내합니다.

## 1. Docker 환경 (Production-like)
전체 서비스를 컨테이너 기반으로 통합 실행할 때 사용합니다.

### 1-1. 서비스 시작
루트 디렉토리에서 다음 명령어를 실행하여 이미지를 빌드하고 컨테이너를 실행합니다.
```bash
docker-compose up -d --build
```
- `-d`: 백그라운드 모드로 실행.
- `--build`: 변경 사항이 있을 경우 이미지를 다시 빌드.

### 1-2. 상태 확인
실행 중인 컨테이너 상태를 확인합니다.
```bash
docker-compose ps
```

### 1-3. 로그 확인
전체 또는 특정 서비스의 로그를 실시간으로 확인합니다.
```bash
# 전체 로그
docker-compose logs -f

# 특정 서비스 로그 (예: backend)
docker-compose logs -f backend
```

### 1-4. 서비스 종료
모든 컨테이너를 중지하고 제거합니다. (데이터 볼륨은 유지됨)
```bash
docker-compose down
```
- 볼륨까지 삭제하려면: `docker-compose down -v`

---

## 2. 로컬 테스트 환경 (Development)
개별 모듈을 로컬에서 실행하거나 테스트 코드를 수행할 때 사용합니다.

### 2-1. 백엔드 (Backend)
**실행**:
```bash
cd backend
# 가상환경 활성화 (권장)
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**테스트 수행 (Pytest)**:
```bash
cd backend
pytest
```

### 2-2. 프론트엔드 (Frontend)
**실행**:
```bash
cd frontend
npm install
npm run dev
```
- 브라우저 접속: `http://localhost:3000`

### 2-3. 데이터베이스 (DB Only)
백엔드 로컬 개발 시 DB만 Docker로 띄워야 할 경우:
```bash
docker-compose up -d neo4j qdrant
```

## 3. 주요 접속 정보
- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474 (ID: neo4j / PW: password)
- **Qdrant Dashboard**: http://localhost:6333/dashboard
