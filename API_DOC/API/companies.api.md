Feature： 企業資訊查詢
===

Description : 
---
本 API 支援一次查詢多筆公司統一編號， 系統將依序處理每一筆統一編號， 並回傳各公司目前於系統中可取得之稅籍資料與對應狀態。

## Related Specifications

- **API Contract**
  - 定義 Request / Response 結構與欄位說明
  - 請參考：`/Users/bruce/SDD/API_DOC/Contract/01_companies.contract.md`

- **Database Schema**
  - 稅籍資料表、排程記錄表與即時發查紀錄表之結構與欄位定義
  - 請參考`/Users/bruce/SDD/API_DOC/DB_Schema`下：
    - `companies.schema.md`
    - `tasks.schema.md`
    - `instant-query-record.schema.md`

- **相關外部 API 文件**
  - 外部API Request / Response 結構與欄位說明
  - 網爬平台-企業資訊查詢申請:請參考：`External_API_Spec/online-crawler/contract/01_company-job.contract.md`

## Status Model（Item-level / Normative）

狀態（status）於 API Response 中以字串（string）形式回傳，
其值為下列狀態名稱之一。

| 狀態名稱 | 業務語意（簡化描述） | 類別 |
|---------|------------------|------|
| SUCCESS | 查詢成功：已取得稅籍資料 | 最終狀態 |
| NO_DATA | 查無資料：官方來源確認無此統一編號 | 最終狀態 |
| FAILED | 查詢失敗：系統錯誤或發查中斷 | 最終狀態 |
| PROCESSING | 處理中：正在同步／發查，請稍後再試 | 中間狀態 |

* FAILED 為內部判斷狀態，用於表示前一次即時發查流程已結束且失敗。API Response 不對外回傳 FAILED 狀態。


## Workflow：

```markdown

API Request 參數為 統一編號清單(list<party_id>)

ffor party_id :
    查詢 `排程記錄表`（DB: TASKS）是否成功  
    （where update_dttm = "{前一日}" and type = "稅籍" and status = `SUCCESS`（成功））

    是：
        `稅籍資料表`（DB: Companies）查詢最新資料  
        （where party_id = "{統一編號}" order by update_dttm desc limit 1）
            - 有資料：加入回傳資料
            - 查無資料：
                表示稅籍資料中沒有該筆資料，
                回傳統一編號，
                並將狀態（status）標記為 `NO_DATA`（無資料），
                加入回傳資料

    否：
        `即時發查紀錄表`（DB: instant_query_record）查詢最新資料  
        （where ID = "{統一編號}" and type = "稅籍" order by create_dttm desc limit 1）

            - 有最新資料：
                - status = `SUCCESS`（成功）：
                    查詢 `稅籍資料表`（DB: Companies）取得最新資料  
                    （where check_dttm = "{今日}" and party_id = "{統一編號}"），
                    並將狀態（status）標記為 `SUCCESS`（成功），
                    加入回傳資料

                - status = `NO_DATA`（無資料）：
                    將統一編號狀態（status）標記為 `NO_DATA`（無資料），
                    加入回傳資料

                - status = `PROCESSING`（處理中）：
                    將統一編號狀態（status）標記為 `PROCESSING`（處理中），
                    加入回傳資料

            - 無最新資料：
                - 若即時發查紀錄表中不存在任何紀錄，
                  或存在紀錄但最新一筆狀態（status）為 `FAILED`（失敗），
                  表示前一次查詢已結束且失敗，
                  系統視為「新的查詢請求」：
                    - 呼叫 `網爬平台-企業資訊查詢申請` 取得 {task_id}
                    - 新增一筆即時發查紀錄  
                      （instant_query_record：task_id, type = "稅籍", ID = "{統一編號}", status = `PROCESSING`（處理中））
                    - 回傳該統一編號
                    - 狀態（status）標記為 `PROCESSING`（處理中）

end for loop

return List<稅籍查詢結果>

```

### background
1.稅籍資料表由每日排程功能新增稅籍資料，update_dttm會標記為前一日(D-1)
2.排程記錄表(TASKS)由每日排程功能新增當日是否已進行排程，狀態為PROCESSING（處理中）、FAILED（失敗）、SUCCESS（成功)，或是無資料表示尚未進行排程，排程會更新所有稅籍資料
3.即時發查紀錄表會記錄正在發查的項目，之後會由排程檢查稅籍資料是否更新完成，更新完成後會排程會新增到稅籍資料表並且在check_dttm填入今日
4.每日僅會有一筆稅籍排程記錄
5.所有稅籍資料只會由排程進行更新
6.task_id 為內部即時發查識別碼，僅用於系統與外部網爬平台間之處理，API Response 不對外回傳 task_id。


## Scenario

以下情境皆以 **單一統一編號（party_id）** 為說明單位；  
實際 API 行為為 batch 處理，對每一筆 party_id 皆獨立套用以下情境判斷。

---

### Scenario 1：Happy Path — 排程成功且資料存在（最常見）

**Given**
- 前一日稅籍排程已成功完成（TASKS.status = SUCCESS（成功））
- 稅籍資料表中存在該統一編號之資料

**When**
- 呼叫企業資訊查詢 API
- 傳入該統一編號

**Then**
- 系統自稅籍資料表取得最新一筆資料
- 回傳該公司稅籍資料
- 狀態標記為 SUCCESS（成功）

---

### Scenario 2：排程成功但官方查無資料（合法但無登錄）

**Given**
- 前一日稅籍排程已成功完成
- 稅籍資料表中查無該統一編號之任何資料

**When**
- 呼叫企業資訊查詢 API
- 傳入該統一編號

**Then**
- 系統不進行即時發查
- 回傳該統一編號
- 狀態（status）標記為 NO_DATA(無資料)
- 代表官方稅籍來源中查無該企業

**Response Example**
```json
{
  "party_id": "12345678",
  ...
  "status": "NO_DATA"
}
```

---

### Scenario 3：排程未成功，且已有今日即時查詢完成資料

**Given**
- 前一日稅籍排程未成功或尚未執行
- 稅籍資料表中存在該統一編號，且 check_dttm = 今日

**When**
- 呼叫企業資訊查詢 API
- 傳入該統一編號

**Then**
- 系統直接回傳該筆稅籍資料
- 狀態（status）標記為 SUCCESS(成功)
- 不再重新發起即時發查

---

### Scenario 4：排程未成功，且尚未取得今日資料（需即時發查）

**Given**
- 前一日稅籍排程未成功或尚未執行
- 稅籍資料表中查無該統一編號，或資料非今日即時查詢結果

**When**
- 呼叫企業資訊查詢 API
- 傳入該統一編號

**Then**
- 系統呼叫網爬平台 API 發起即時發查
- 取得網爬平台回傳之 task_id
- 寫入即時發查紀錄表，狀態為 PROCESSING(處理中)
- 回傳該統一編號
- 狀態（status）標記為 PROCESSING(處理中)

**Response Example**
```json
{
  "party_id": "87654321",
  ...
  "status": "PROCESSING",
}
```

---

### Scenario 5：同一日重複查詢同一公司（冪等行為）

**Given**
- 該統一編號於今日已進行過即時發查
- 即時發查尚未完成

**When**
- 再次呼叫企業資訊查詢 API
- 傳入相同統一編號

**Then**
- 系統判斷該即時發查仍在處理中
- 回傳該統一編號
- 狀態（status）標記為 `PROCESSING`（處理中）

---

### Scenario 6：Batch 查詢 — 多家公司混合結果

**Given**
- API Request 傳入多筆統一編號
- 各公司分別符合不同查詢情境

**When**
- 呼叫企業資訊查詢 API

**Then**
- 系統依序處理每一筆統一編號
- 每家公司皆回傳一筆對應結果
- 回傳結果清單中可能同時包含：
  - SUCCESS（成功）
  - NO_DATA（無資料）
  - PROCESSING（處理中）
- 各公司查詢結果彼此獨立，互不影響

**Response Example**
```json
[
  {
    "party_id": "11111111",
    ...
    "status": "SUCCESS",

  },
  {
    "party_id": "22222222",
    ...
    "status": "NO_DATA"
  },
  {
    "party_id": "33333333",
    ...
    "status": "PROCESSING",
  }
]
```

### Scenario 7：最新一筆即時發查為 FAILED，觸發重新發查

**Given**
前一日稅籍排程未成功或尚未執行
即時發查紀錄表（instant_query_record）中存在該統一編號的紀錄
且最新一筆紀錄狀態為 FAILED

**When**
呼叫企業資訊查詢 API
傳入該統一編號

**Then**
- 系統呼叫網爬平台 API 
- 發起即時發查並取得 task_id
- 系統於即時發查紀錄表新增一筆紀錄：
  ID = party_id
  type = "稅籍"
  task_id = {task_id}
  status = PROCESSING
- API 回傳該統一編號
- 狀態（status）標記為 PROCESSING(處理中)

Response Example
```json
[
  {
    "party_id": "12345678",
    ...
    "status": "PROCESSING"
  }
]
```