# for_my_house

풍무 해링턴 74A 분양권을 기준으로 실거래, 전세, 뉴스, 5호선 이벤트를 매일 점검하는 **리스크 모니터링 대시보드**입니다. 이 프로젝트는 집값을 예측하거나 매수/매도 결정을 자동화하지 않고, 원천 데이터와 deterministic 지표를 먼저 계산한 뒤 AI 요약을 마지막 레이어로 붙이는 방향을 따릅니다.

## MVP 범위

- FastAPI 백엔드
- PostgreSQL + SQLAlchemy ORM
- 실거래/뉴스 수집 클라이언트 스캐폴드
- 중복 수집 방지를 위한 `source_hash` 기반 upsert
- 룰 기반 일일 리포트 생성
- Next.js + Tailwind 밝은 톤 대시보드 UI
- Docker Compose 로컬 실행 환경
- 로컬 첫 실행용 데모 데이터 seed

## 아키텍처

```text
Next.js Dashboard
        ↓
FastAPI API Server
        ↓
PostgreSQL
        ↑
Collector / Scheduler
        ↑
MOLIT OpenAPI + Naver News API
        ↓
Deterministic Metrics
        ↓
Rule-based / Future LLM Report
```

## 실행 방법

```bash
cp .env.example .env
docker compose up --build
```

초기 DB 테이블은 백엔드 컨테이너 시작 시 `python -m app.db.init_db`로 생성됩니다. 운영 환경에서는 Alembic 마이그레이션으로 전환하는 것을 권장합니다.

## 처음 화면에 데이터가 안 보일 때

이 MVP는 실제 공공 API 수집 배치가 아직 자동 완성된 단계가 아니므로, 로컬 실행에서는 데모 데이터로 화면과 API 연결을 먼저 검증합니다.

### 1. Docker Compose 기본값

`docker-compose.yml`의 backend 서비스에는 로컬 편의를 위해 아래 환경변수가 켜져 있습니다.

```yaml
SEED_DEMO_DATA: "true"
```

따라서 `docker compose up --build`로 백엔드가 뜰 때 `backend/app/db/init_db.py`가 테이블을 만들고 `backend/app/services/demo_seed.py`의 데모 지표/뉴스/거래 데이터를 idempotent하게 적재합니다.

### 2. 이미 빈 DB로 한 번 실행한 경우

기존 PostgreSQL volume에 빈 리포트가 남아 있으면, 아래 API로 데모 데이터를 다시 넣을 수 있습니다.

```bash
curl -X POST http://localhost:8000/api/dev/seed-demo
```

이 엔드포인트는 `ENVIRONMENT=local`일 때만 동작합니다. 운영 환경에서는 임의 seed가 들어가지 않도록 403으로 막습니다.

### 3. 실제 데이터를 붙일 때 수정할 곳

- 국토교통부 실거래 수집: `backend/app/services/molit_client.py`
- 네이버 뉴스 수집: `backend/app/services/news_client.py`
- 원천 데이터 정규화/해시: `backend/app/services/normalization.py`
- DB upsert/list 조회: `backend/app/services/repositories.py`
- 대시보드 API 응답 조립: `backend/app/api/routes.py`
- 일일 리포트/KPI 룰: `backend/app/services/reporting.py`
- 프론트 API base URL/fallback: `frontend/lib/api.ts`
- 화면 테이블/뉴스 카드 렌더링: `frontend/app/page.tsx`
- Next.js 정적 프리렌더링 방지: `frontend/app/page.tsx`의 `dynamic = 'force-dynamic'`

실제 투자 판단에 사용할 때는 `SEED_DEMO_DATA=false`로 끄고, 수집 배치가 넣은 `source=molit`, `provider=naver` 데이터만 화면에서 신뢰해야 합니다.

## Docker Desktop 오류 대응

Windows에서 아래 오류가 나오면 애플리케이션 문제가 아니라 Docker Engine 연결 문제입니다.

```text
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

확인 순서:

1. Docker Desktop을 실행합니다.
2. Docker Desktop 좌하단 또는 상단 상태가 `Engine running`인지 확인합니다.
3. Settings → General에서 WSL2 based engine이 켜져 있는지 확인합니다.
4. PowerShell에서 `docker version`이 정상 출력되는지 확인합니다.
5. 그 다음 프로젝트 루트에서 `docker compose up --build`를 다시 실행합니다.

## 주요 엔드포인트

- `GET /api/health`
- `GET /api/dashboard/summary`
- `POST /api/dev/seed-demo` — 로컬 데모 데이터 적재
- `GET /api/transactions`
- `GET /api/news`

## 운영 원칙

1. 가격, 전세가율, 손익분기점 계산은 LLM이 아니라 Python/SQL에서 수행합니다.
2. LLM은 검증된 숫자와 기사 메타데이터를 입력으로 받아 요약만 담당합니다.
3. 수집 작업은 각 job마다 독립 DB session을 사용해야 합니다.
4. API 실패는 timeout, retry, 실패 이력 저장으로 다룹니다.
5. 거래 표본이 3건 미만이면 가격 해석 신뢰도를 낮춥니다.
6. 데모 데이터와 실제 데이터는 `source`/`provider`로 분리하고, 운영 화면에서는 데모 데이터를 섞지 않습니다.

## 향후 작업

- 국토교통부 아파트 매매/전월세 XML parser 구현
- 법정동 코드 및 관심 단지 seed 데이터 추가
- Alembic 마이그레이션 도입
- Prefect 또는 Celery Beat 기반 수집 job 운영화
- OpenAI/LangGraph 기반 뉴스·일일 리포트 요약 레이어 추가
- Telegram/Slack 알림 추가
