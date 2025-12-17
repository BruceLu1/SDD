# 企業資訊查詢 - GET /api/v1/companies

## 1. Metadata

| Item | Description |
|-----|-------------|
| URL | https://{domain}/api/v1/companies |
| Method | GET |
| Purpose | 根據統一編號查詢企業詳細資訊 |
| Auth | None |

## 2. Request Structure

### Query Params
| name | type | required | description |
|------|------|----------|-------------|
| party_id | string | Yes | 統一編號 8 位數字（含檢查碼），可透過 `?party_id=xxx&party_id=yyy` 傳入多筆，不可重複，最多 10 筆。 |

### Headers（如有）
| header | required | description |
|--------|----------|-------------|
| Content-Type | No | application/json; charset=utf-8 |

### Request Body
| field | type | required | description |
|-------|-------|----------|-------------|
| N/A | - | - | - |

## 3. Response Format

### 通用回應欄位說明
| field | type | description | notes |
|------|------|-------------|-------|
| code | number | 業務狀態碼 | 非 HTTP Status Code |
| message | string | 回傳訊息 | 成功或錯誤描述，可為 null |
| result | object | 回傳資料主體 | 依 API 定義 |

### 資料結構說明

#### 資料欄位（result / result.items[]）

| field | type | description | notes |
|------|------|-------------|-------|
| result | object | 查詢結果容器 |  |
| result.item[] | object | 查詢的企業資料陣列 |  |
| result.item[].party_id | string | 企業統一編號 | 8 位數字，含檢查碼 |
| result.item[].party_name | string | 企業名稱 |  |
| result.item[].party_addr | string | 企業地址 |  |
| result.item[].paid_in_capital | number | 資本額 |  |
| result.item[].setup_date | string | 註冊日期 | 格式 YYYYMMDD |
| result.item[].party_type | string | 公司型態 |  |
| result.item[].ind_code | number | 主要產業分類 |  |
| result.item[].update_time | string | 資料更新時間 | 格式 YYYYMMDD |
| result.item[].status | string | 資料狀態 | enum：SUCCESS、FAILED、PROCESSING、NO_DATA |
| result.total_count | number | 回傳筆數 |  |

---

### Success
```json
{
  "code": 1000,
  "message": "",
  "result": {}
}
```

### Error（Http Code 皆回傳 200）

HTTP Status Code 200 代表 服務正常啟用並成功回應請求。

#### Response Fields

| field | type | description | notes |
|------|------|-------------|-------|
| code | number | 請求處理結果 | 依 error-code.policy.md |
| message | string | 狀態或錯誤說明 | 可為 null |
| result | object | 回傳資料主體 | 依 API 定義 |

```json
{
  "code": 1400,
  "message": "Error message",
  "result": null
}
```

#### Error Codes

| code | message | description |
|------|---------|-------------|
| N/A | N/A | N/A |

## 4. Pagination

### Pagination Support
| Supported | Description |
|----------|-------------|
| No | 不支援分頁，單次回傳所有符合條件的資料。 |

---

## 5. Notes / Open Questions（選填）
* status 目前會回傳 SUCCESS、FAILED、PROCESSING、NO_DATA。
