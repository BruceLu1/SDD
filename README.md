Clean FastAPI (Clean Architecture)
==================================

Project scaffold for FastAPI 0.115.2 following Clean Architecture separation (domain/application/infrastructure/presentation).

Tech stack / versions
---------------------
- Python 3.13 (developed on)
- FastAPI 0.115.2
- Uvicorn 0.30.1
- SQLAlchemy 2.0.34
- Pydantic 2.9.0 (+ email-validator 2.2.0)
- pydantic-settings 2.4.0

Installation
------------
1) 建議使用虛擬環境：`python -m venv .venv && .venv\\Scripts\\activate`
2) 安裝依賴：`pip install -r requirements.txt`

Configuration
-------------
- 環境變數（可於 `.env`）：`DATABASE_URL`（預設 `sqlite:///./data/app.db`），`APP_NAME`、`DEBUG`。
- 預設會在 `data/` 建立 SQLite DB。

Run
---
開發模式（自動 reload）：`uvicorn app.main:app --reload`

API docs
--------
- Swagger UI: `http://127.0.0.1:8000/swagger`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

Architecture notes
------------------
- Domain：實體、Value Object、Repository 介面、Domain Service，無 FastAPI/ORM/HTTP client 依賴。
- Application：UseCase 與 DTO，只依賴 Domain 介面。
- Infrastructure：SQLAlchemy models 與 repository 實作、外部 client。
- Presentation：Schema/Controller/Router，透過 DI 工廠注入 UseCase。
- `app/main.py` 組合 DI、建立 engine/session、註冊 router，並提供 `/health`。
