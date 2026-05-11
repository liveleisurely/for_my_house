# for_my_house

풍무 해링턴 74A 분양권을 기준으로 실거래, 전세, 뉴스, 5호선 이벤트를 매일 점검하는 **리스크 모니터링 대시보드**입니다. 이 프로젝트는 집값을 예측하거나 매수/매도 결정을 자동화하지 않고, 원천 데이터와 deterministic 지표를 먼저 계산한 뒤 AI 요약을 마지막 레이어로 붙이는 방향을 따릅니다.

## MVP 범위

- FastAPI 백엔드
- PostgreSQL + SQLAlchemy ORM
- 실거래/뉴스 수집 클라이언트 스캐폴드
- 중복 수집 방지를 위한 `source_hash` 기반 upsert
- 룰 기반 일일 리포트 생성
- Next.js + Tailwind 전문가형 대시보드 UI
- Docker Compose 로컬 실행 환경

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

## 주요 엔드포인트

- `GET /api/health`
- `GET /api/dashboard/summary`
- `GET /api/transactions`
- `GET /api/news`

## 운영 원칙

1. 가격, 전세가율, 손익분기점 계산은 LLM이 아니라 Python/SQL에서 수행합니다.
2. LLM은 검증된 숫자와 기사 메타데이터를 입력으로 받아 요약만 담당합니다.
3. 수집 작업은 각 job마다 독립 DB session을 사용해야 합니다.
4. API 실패는 timeout, retry, 실패 이력 저장으로 다룹니다.
5. 거래 표본이 3건 미만이면 가격 해석 신뢰도를 낮춥니다.

## 향후 작업

- 국토교통부 아파트 매매/전월세 XML parser 구현
- 법정동 코드 및 관심 단지 seed 데이터 추가
- Alembic 마이그레이션 도입
- Prefect 또는 Celery Beat 기반 수집 job 운영화
- OpenAI/LangGraph 기반 뉴스·일일 리포트 요약 레이어 추가
- Telegram/Slack 알림 추가
