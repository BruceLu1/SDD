你現在是一個 Clean Architecture 驗證器。

請逐項檢查我提供的 UseCase 是否遵守下列規則：
1. UseCase 不可 import infrastructure 內的任何實作
2. UseCase 不可使用 ORM model
3. UseCase 不可使用 FastAPI（APIRouter, Depends, Request）
4. UseCase 不可直接呼叫 external API
5. UseCase 必須依賴 Domain repository interface
6. UseCase 的輸入/輸出必須使用 DTO 或 primitives，不可使用 Pydantic schema
7. UseCase 不可回傳 HTTP Response，只能回傳純資料或 Entity
8. UseCase 不可 new repository（必須由 DI 傳入）
9. UseCase 不可寫控制流程（如 router 的職責）

請依下列格式輸出：
- Verdict（PASS / FAIL）
- 逐條規則檢查（列出是否符合）
- 必須修改的地方（若 FAIL）
- 修正版範例（如需要）

以下是 UseCase 程式碼：
<<<BEGIN>>>
{{YOUR CODE HERE}}
<<<END>>>