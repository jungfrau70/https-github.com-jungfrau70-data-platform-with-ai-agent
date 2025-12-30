# Frontend Guide (frontend/AGENTS.md)

## 1. 개요
GC101의 프론트엔드는 **Nuxt 3** (Vue.js)로 구축되어 있으며, 사용자에게 대화형 AI 경험을 제공합니다.

## 2. 주요 기술 스택
- **Framework**: Nuxt 3 (Vue 3)
- **Styling**: TailwindCSS
- **State**: Pinia
- **HTTP Client**: Axios / UseFetch

## 3. 개발 환경 설정 (Setup)
```bash
cd frontend
npm install
```

## 4. 실행 (Run)
```bash
npm run dev
```
- 접속 주소: `http://localhost:3000`

## 5. 테스트 (Test)
- **E2E Test**: Playwright
```bash
npx playwright test
```

## 6. 주요 디렉토리
- `components/`: UI 컴포넌트
- `pages/`: 라우팅 페이지
- `stores/`: Pinia 상태 관리
