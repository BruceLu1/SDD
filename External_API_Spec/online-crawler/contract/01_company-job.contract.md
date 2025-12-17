# 企業資訊查詢申請

## 1. Metadata

| Item | Description |
|-----|-------------|
| URL | https://www.crawler.com/api/v1/company/job |
| Method | POST |
| Purpose | 根據統一編號（party_id）提交企業資訊查詢申請，系統將在背景進行非同步處理 |
| Auth | None |

## 2. Request Structure

### Query Params
| name | type | required | description |
|------|------|----------|-------------|

> `N/A`

### Headers（如有）
| header | required | description |
|--------|----------|-------------|
| content-type | Yes | `application/json; charset=utf-8` |

### Request Body
| field | type | required | description |
|-------|-------|----------|-------------|
| party_id | string | Yes | 統一編號為 8 位數字（含檢查碼驗證），一次僅允許單筆 |

## 3. Enum Specification

> `N/A`

## 4. Response Format

### 通用回應欄位說明
| field | type | description | notes |
|------|------|-------------|-------|
| success | boolean | 請求是否成功 | 全域欄位 |
| code | number | 業務狀態碼 | 跟 HTTP status 一致，200 表示成功 |
| message | string | 回傳訊息 | 成功或錯誤描述 |
| result | object | 回傳資料主體 | 依 API 定義 |

`result.data` 含單筆任務資料，包含 `party_id` 與 `task_id`。

### Success
```json
{
  "success": true,
  "code": 200,
  "message": null,
  "result": {
    "data": {
      "party_id": "38965019",
      "task_id": "19ab3cec-53d8-cdef-3238-74e1b80b89ce"
    }
  }
}
```

### Error（Http Code 皆回傳 200）

#### Response Fields
| field | type | description | notes |
|-------|------|-------------|-------|
| success | boolean | 請求是否成功 | 全域欄位 |
| code | string | 業務狀態碼 | 依照錯誤規則回傳 |
| message | string | 訊息/錯誤描述 | |
| data/result | object | 回傳主體 | `null` 或空物件 |

```json
{
  "success": false,
  "code": "L001",
  "message": "輸入參數錯誤"
}
```

#### Error Codes
| code | message | description |
|------|---------|-------------|
| L001 | 輸入參數錯誤 | 請求欄位型別或格式不符 |

## 5. Pagination

### Pagination Support
| Supported | Description |
|----------|-------------|
| No | 回傳單一任務資料，不支援分頁。 |

## 6. Notes / Open Questions（選填）
* `task_id` 後續需用於查詢狀態。仍需確認 task processing time 及重試上限。
