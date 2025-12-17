Clean Architecture（LLM Friendly Version）
🎯 設計原則（LLM 最容易理解的 3 條規則）

Rule 1 — 分層只允許單向依賴：

presentation → application → domain
infrastructure → application / domain


Rule 2 — Domain 不依賴任何外部框架（FastAPI / DB / API）。

Rule 3 — 所有跨層抽象都寫成 interface（protocol）。

📁 推薦的 FastAPI Clean Architecture 目錄
app/
├── core/                     # 全域設定、enum、exception
│   ├── config.py
│   ├── enums/
│   │   └── user_role.py
│   ├── exceptions/
│   │   ├── domain_exceptions.py
│   │   ├── application_exceptions.py
│   │   └── infrastructure_exceptions.py
│   └── utils/
│       └── helpers.py
│
├── domain/                   # Domain: 核心商業邏輯（無 FastAPI / ORM / requests）
│   ├── entities/
│   │   └── user.py
│   ├── value_objects/
│   │   └── email.py
│   ├── repositories/         # 抽象介面（interface）
│   │   └── user_repository.py
│   └── services/
│       └── user_rules.py
│
├── application/              # Use Case 層（流程控制）
│   ├── dto/
│   │   └── user_dto.py
│   ├── use_cases/
│   │   └── create_user.py
│   └── interfaces/           # UseCase 要使用的 service interface
│       └── user_service.py
│
├── infrastructure/           # DB / 外部 API / 實作（FastAPI 不放這層）
│   ├── db/
│   │   ├── models/
│   │   │   └── user_model.py
│   │   └── repository_impl/
│   │       └── user_repository_impl.py
│   ├── api/
│   │   └── external_user_api.py
│   └── clients/
│       └── http_client.py
│
├── presentation/             # FastAPI 入口層（routers + controllers）
│   ├── routes/
│   │   └── user_routes.py
│   ├── controllers/
│   │   └── user_controller.py
│   └── schemas/
│       └── user_schema.py    # Pydantic request/response
│
└── main.py                   # FastAPI application entry