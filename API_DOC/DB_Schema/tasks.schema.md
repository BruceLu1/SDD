### Table name : Tasks

## Description
Task 為非同步任務由外部 API 提供內容，用於紀錄任務狀態；外部 API 回應時會回傳一個 `task_id` (UUID)，此刻 `status` 只會是 `PENDING`。排程會根據 `task_id` 追蹤並更新這些 task 的狀態與資料。

## Schema

| 欄位名稱        | 型別                           | 說明                      | 範例值          | 索引    |
| ------------- | ------------------------------ | ------------------------ | -------------- | ------- |
| `type`        | `string`                       | 業務別                    | `16590299`     |         |
| `status`      | `number` (enum `TASKS_STATUS`) | 更新狀態                  | `1 (SUCCESS)`   |         |
| `create_dttm` | `string`                       | 建立時間(yyyyMMdd)西元年   | `20250101`      |         |
| `update_dttm` | `string`                       | 更新時間(yyyyMMdd)西元年   | `20250115`      |         |

## 備註

Enum: `TASKS_STATUS`（對應 `status` 欄位）

- `SUCCESS` = 1
- `FAILED` = 2
- `PENDING` = 3
- `NO_DATA` = 4
