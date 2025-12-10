DAG-RAG 기반 전문가 챗봇 (Gem) 상세 구현 및 배포 매니페스토본 가이드는 Nuxt 3 (Frontend), FastAPI (Backend), Qdrant (Vector Memory), Neo4j (Graph Memory) 스택을 DAG(방향성 비순환 그래프) 채팅 구조와 삼중 기억 시스템에 맞춰 Docker Compose 환경에서 실질적으로 동작하도록 구성합니다.I. 시스템 구성 요소 및 역할 매핑컴포넌트역할 (RAG/Memory)통신 포트 (내부)환경 변수 의존성FastAPI단기/장기/룰 기능, DAG 병합, Gemini 통합8000QDRANT_HOST, NEO4J_HOST, GEMINI_API_KEYNeo4j장기 기억 (Graph RAG)7687 (Bolt)NEO4J_PASSWORDQdrant장기 기억 (Vector RAG)6333 (REST)없음Nuxt 3채팅 UI, DAG 분기/합류 UX 관리3000API_BASE_URLII. DAG-RAG 로직 통합을 위한 서비스 설계2.1. 장기 기억 통합 (Neo4j & Qdrant)FastAPI 백엔드는 Qdrant와 Neo4j라는 두 개의 장기 기억 저장소를 활용하여 RAG를 수행합니다.FastAPI 환경 설정: 백엔드 서비스는 컨테이너 간 통신을 위해 docker-compose.yml에 정의된 내부 서비스 이름(qdrant, neo4j)을 사용하여 데이터베이스에 접근해야 합니다.QDRANT_HOST: http://qdrant:6333NEO4J_URI: bolt://neo4j:7687 (Neo4j는 기본적으로 Bolt 프로토콜 사용)영속성 및 헬스 체크: 데이터베이스 컨테이너는 데이터 손실 방지를 위해 Named Volume을 사용하며, FastAPI는 데이터베이스가 트랜잭션을 처리할 준비가 완료될 때까지 service_healthy 조건을 통해 시작을 지연시킵니다.2.2. 단기 기억 및 룰 기능 (FastAPI)FastAPI 컨테이너 내에서 실행되는 Python 코드가 단기 기억과 룰 기반 기능을 담당합니다.단기 기억 (DAG Context Merging):사용자 요청 시, FastAPI는 다중 parent_ids 리스트를 받아 DB에서 모든 부모 노드의 대화 히스토리를 역추적합니다.이 모든 히스토리를 병합하고, 토큰 제한 내에서 가장 관련성 높은 부분만 필터링하는 룰을 적용합니다.룰 기반 역할 (Persona & Tool Use):GEMINI_API_KEY 환경 변수를 사용하여 Gemini API 호출 권한을 확보합니다.LLM 호출 시 **system_instruction**에 "딥러닝 전문가 Gem" 페르소나를 정의합니다.FastAPI 코드는 사용자 질문의 키워드를 분석하여, GraphRAG 추론이 필요한지(관계 키워드 존재 시), File Search가 필요한지(파일 URI 첨부 시) 룰에 따라 동적으로 판단하고 Gemini에 필요한 컨텍스트와 도구를 전달합니다.2.3. Nuxt 3 프런트엔드 (DAG UX)프런트엔드는 백엔드에 대한 의존성을 외부에서 주입받고, 오직 HTTP 요청만을 통해 통신하며 백엔드에 완벽히 격리됩니다.API 엔드포인트 설정: API_BASE_URL 환경 변수를 http://backend:8000으로 설정하여, Nuxt가 내부 Docker 네트워크를 통해 FastAPI 서비스에 접근하도록 합니다.외부 노출: Nuxt 컨테이너만 호스트 포트(80)에 바인딩되어 외부 사용자의 접근을 허용합니다.III. 최종 Docker Compose 매니페스토 (Runnable)다음은 위에 기술된 모든 DAG-RAG 및 메모리 통합 전략이 반영된 docker-compose.yml 파일입니다.⚠️ 주의사항: 실행 전 프로젝트 루트에 .env 파일을 생성하고 GEMINI_API_KEY, NEO4J_PASSWORD를 설정해야 합니다.YAMLversion: '3.8'

# Docker Named Volumes: 데이터 영속성 보장
volumes:
  neo4j_data:
  qdrant_storage:

services:

  #######################################
  # 1. GRAPH DB: NEO4J (장기 기억 - 관계) #
  #######################################
  neo4j:
    image: neo4j:5.16.0-community
    container_name: neo4j_db
    restart: unless-stopped
    hostname: neo4j
    environment:
      NEO4J_AUTH: 'neo4j/${NEO4J_PASSWORD}'
      NEO4J_dbms_memory_heap_max__size: '512m'
    
    volumes:
      - neo4j_data:/var/lib/neo4j/data  # 데이터 영속성 [1]
      
    expose:
      - 7687 # Bolt 프로토콜 포트 (내부 접근)

    # 헬스 체크: cypher-shell을 통한 트랜잭션 준비 상태 검증 (긴 초기화 시간 반영)
    healthcheck:
      test:
      interval: 20s
      timeout: 10s
      retries: 6
      start_period: 30s 

    networks:
      - backend-net

  #######################################
  # 2. VECTOR DB: QDRANT (장기 기억 - 벡터) #
  #######################################
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant_db
    restart: unless-stopped
    hostname: qdrant
    
    volumes:
      - qdrant_storage:/qdrant/storage # 벡터 데이터 영속성 [2]
      
    expose:
      - 6333 # REST/gRPC API 포트 (내부 접근)

    # 헬스 체크: API 응답 및 기능적 준비 상태 확인 [3]
    healthcheck:
      test:
      interval: 15s
      timeout: 5s
      retries: 4
      start_period: 15s

    networks:
      - backend-net

  #######################################
  # 3. BACKEND API: FASTAPI (메모리, 룰, DAG 로직) #
  #######################################
  backend:
    build:
      context:.
      dockerfile: Dockerfile.backend 
    container_name: fastapi_api
    restart: unless-stopped
    hostname: backend
    
    # 의존성: 두 데이터베이스가 완전히 Healthy 상태가 될 때까지 대기 [4]
    depends_on:
      qdrant:
        condition: service_healthy
      neo4j:
        condition: service_healthy

    environment:
      # 핵심 환경 변수: API 키 및 내부 서비스 연결 설정 (FastAPI 로직에 주입)
      GEMINI_API_KEY: ${GEMINI_API_KEY}
      QDRANT_URL: http://qdrant:6333
      NEO4J_URI: bolt://neo4j:7687
      NEO4J_PASSWORD: ${NEO4J_PASSWORD} 
      FASTAPI_WORKERS: ${FASTAPI_WORKERS:-4} # 성능 튜닝 변수

    expose:
      - 8000 # 내부 API 포트

    # 로깅 관리: 디스크 고갈 방지를 위한 로테이션 설정 [5]
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

    # 헬스 체크: API 응답성 확인
    healthcheck:
      test:
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 5s

    networks:
      - backend-net

  #######################################
  # 4. FRONTEND UI: NUXT NODE SERVER (DAG UX) #
  #######################################
  frontend:
    build:
      context:./frontend
      dockerfile: Dockerfile.frontend
      args:
        NITRO_PRESET: node-server
    container_name: nuxt_app
    restart: unless-stopped
    
    # 의존성: 백엔드 API가 준비될 때까지 대기
    depends_on:
      backend:
        condition: service_healthy
        
    ports:
      - "80:3000" # 외부 노출 (호스트 포트 80)

    environment:
      # Nuxt 런타임 환경 변수 설정 (내부 서비스 이름 사용)
      API_BASE_URL: http://backend:8000 
      NUXT_HOST: 0.0.0.0 

    # 헬스 체크: Node 서버가 트래픽을 처리하는지 확인
    healthcheck:
      test:
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 10s

    networks:
      - backend-net

# 네트워크 정의: 모든 서비스가 격리된 내부 네트워크에서 통신
networks:
  backend-net:
    driver: bridge
IV. 실습 실행 지침4.1. 사전 준비 파일이 매니페스토를 실행하려면 프로젝트 루트 디렉토리에 다음 파일이 존재해야 합니다..env 파일 (루트 디렉토리):Code snippetGEMINI_API_KEY=YOUR_API_KEY_HERE
NEO4J_PASSWORD=strong_secure_password
FASTAPI_WORKERS=4
Dockerfile.backend (FastAPI 다중 단계 빌드 파일):Dockerfile# Stage 1: Build Stage
FROM python:3.11-slim as builder
WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn uvicorn neo4j qdrant-client chromadb

# Install curl for healthcheck [3]
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Stage 2: Runtime Stage
FROM python:3.11-slim
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/bin/curl /usr/bin/curl
COPY..

# Production Command: Gunicorn + Uvicorn으로 워커 관리 (Graceful Shutdown 및 Proxy Headers) [5]
CMD
Dockerfile.frontend (Nuxt 3 다중 단계 빌드 파일):Dockerfile# Stage 1: Build Stage
FROM node:lts-alpine AS build
WORKDIR /app

COPY package*.json.
RUN npm install
COPY..
# Nitro Preset 환경 변수를 사용하여 SSR 모드 빌드 [6]
ARG NITRO_PRESET
RUN NITRO_PRESET=${NITRO_PRESET} npm run build

# Install curl for healthcheck [3]
RUN apk add --no-cache curl

# Stage 2: Runtime Stage
FROM node:lts-alpine
WORKDIR /app

# 빌드 결과물과 프로덕션 종속성만 복사
COPY --from=build /app/.output./.output
COPY --from=build /app/node_modules/.
COPY --from=build /usr/bin/curl /usr/bin/curl

# CMD: 빌드된 Nuxt 서버 실행
CMD [ "node", ".output/server/index.mjs" ]
4.2. 실행 명령어프로젝트 루트 디렉토리에서 다음 명령을 실행하여 서비스를 시작합니다.Bash# 1. 컨테이너 빌드 및 백그라운드 모드로 시작
docker compose up --build -d

# 2. 서비스 상태 및 헬스 체크 확인
# 모든 서비스가 'Up (healthy)' 상태여야 합니다.
docker compose ps 

# 3. 로그 스트리밍 (선택 사항 - 디버깅용)
docker compose logs -f 

# 4. 서비스 중지 및 컨테이너/네트워크 제거 (볼륨은 유지)
docker compose down
