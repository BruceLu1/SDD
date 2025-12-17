### Table name : InstantQueryRecord

## Description
記錄排程功能

## Schema

| 欄位名稱     | 型別             | 說明       | 範例值        | 索引    |
| ----------- | --------------- | --------- |------------- | ------- |
| `task_id`   | `string`        | Task ID    | `4597688f-f80b-4105-a648-70fafe8a8034` |         |
| `type`      | `string`        | 類別        | `稅籍`       |         |
| `ID`        | `string`        | 目標ID      | `16590299`  |         |
| `status`    | `TASKS_STATUS`  | 發查狀態     | `2025-01-15T14:00:00Z`    |         |
| `create_dttm`    | `date`  | 創建日期     | `2025-01-15T14:00:00Z`    |         |
| `update_dttm`    | `date`  | 更新日期     | `2025-01-15T14:00:00Z`    |         |

## 備註
1. Enum: `TASKS_STATUS`（對應 `status` 欄位）
    - `SUCCESS` = 1
    - `FAILED` = 2
    - `PENDING` = 3
    - `NO_DATA` = 4