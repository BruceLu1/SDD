FastAPI Clean Architecture — LLM 規則指南

此文件定義 LLM 在產生程式碼時必須遵守的規則，確保輸出內容維持 Clean Architecture 並正確套用 FastAPI。

✅ 1. Domain Layer 規則（必守）
✔ Domain 不得使用 ORM
✔ Domain 不得使用 requests / HTTP Client
✔ Domain 不得使用 FastAPI / Depends / APIRouter
✔ Domain 不得 import Infrastructure / Application / Presentation


Domain 只能包含：

Entities

Value Objects

Domain Services

Repository Interface（abstract class / protocol）

✅ 2. 層級依賴規則（硬性規範 LLM）
presentation → application → domain
infrastructure → application / domain


不允許：

Presentation → infrastructure

Application → infrastructure

Domain → 任何其他層

✅ 3. Interface（抽象介面）規則
✔ 所有跨層依賴都透過 interface（protocol / abstract class）
✔ UseCase 只能依賴 Domain 的 Repository interface
✔ Infrastructure 的 repository 實作必須實作 Domain 介面
✔ UseCase 不得依賴 infrastructure 實作

✅ 4. Repository 分層要求
domain/repositories/   → interface (抽象)
infrastructure/...     → implementation (具體)


LLM 在產生程式碼時必須確保：

Domain 定義 interface

Infrastructure 實作 interface

Application (UseCase) 只依賴 interface，不依賴實作

✅ 5. Controller 不寫商業邏輯

Controller 的責任：

✔ 接收 request
✔ 調用 UseCase
✔ 回傳結果


禁止：

✘ 資料庫存取
✘ 商業規則
✘ 外部 API 呼叫
✘ ORM 操作

✅ 6. Router 不直接 new UseCase（避免硬耦合）

禁止：

router = APIRouter()
repo = UserRepositoryImpl()
use_case = CreateUserUseCase(repo)


推薦：Router 使用工廠傳入 use_case

# main.py
app.include_router(user_router(use_case))

🔵 FastAPI 特化規則（LLM 版）

以下是 FastAPI 專用的 Clean Architecture 設計規範。

✅（1）FastAPI Router 必須放在 Presentation 層

放在：

presentation/routes/
presentation/controllers/
presentation/schemas/


禁止放在：

application

infrastructure

domain

原因：

FastAPI = framework

Presentation = framework 接觸點層

Domain & Application 不可 import FastAPI

✅（2）DI（依賴注入）只能在 presentation 層做

UseCase 本身不能 new repository 實作。

正確方式（main.py 注入）：

from fastapi import FastAPI
from presentation.routes.user_routes import router as user_router
from infrastructure.db.repository_impl.user_repository_impl import UserRepositoryImpl
from application.use_cases.create_user import CreateUserUseCase

app = FastAPI()

repo = UserRepositoryImpl()
use_case = CreateUserUseCase(repo)

app.include_router(user_router(use_case), prefix="/users")


重點規則：

✔ UseCase 不得依賴 FastAPI
✔ Router 用工廠傳入 UseCase
✔ 主程式 main.py 負責組合依賴

🔵 Enum 放置位置（FastAPI 特化）

位置：

app/core/enums/


原因：

Pydantic model 會使用 Enum

Router 會用 Enum 做驗證（path/query）

Application / Domain 都可能用到

不屬於任何單一 Clean Architecture 層 → 放 core 最乾淨

🔵 Exception 放置位置（FastAPI 特化）
app/core/exceptions/


拆三層避免 LLM 混淆：

層級	檔案	用途
domain_exceptions	InvalidEmail	商業規則錯誤
application_exceptions	UserNotFound	UseCase 流程錯誤
infrastructure_exceptions	DBConnectionError	DB/API 錯誤

FastAPI 在 controller 層轉換成 HTTP 回應：

try:
    result = use_case.execute(...)
except UserNotFound:
    raise HTTPException(status_code=404)

🔵 External API 放置位置（FastAPI 特化）
app/infrastructure/api/


範例：

weather_api.py
payment_gateway_api.py
auth_provider_api.py


規則（LLM 必須遵守）：

✘ Domain 不可呼叫 external API
✘ Router 不可直接呼叫 external API
✔ UseCase 若需外部 API → 必須先定義 interface