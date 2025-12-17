# Table name : Companies

## Description
公司稅籍資料表。

## Schema

| 欄位名稱          | 型別        | 說明             | 範例值     | 索引    |
| ----------------- | ----------- | ---------------- | ---------- | ------- |
| `party_id`        | `string`      | 企業統一編號     | `38965019` |     v    |
| `party_addr`      | `string`      | 企業地址         | `南投縣中寮鄉中寮村永平路３７１號一樓`          |         |
| `parent_party_id` | `string`      | 母企業統一編號   | -          |         |
| `party_name`      | `string`      | 企業名稱         | `原味商行`          |         |
| `paid_in_capital`  | `number`  | 資本額           | `100000`          |         |
| `setup_date`      | `date`        | 註冊日期(yyyMMdd) 民國年         | `1040413`       |         |
| `party_type`      | `string`      | 公司型態         | `獨資`        |         |
| `use_invoice`     | `string`     | 是否開立發票     | `N`        |         |
| `ind_code`        | `number`       | 主要產業類別代碼 | `472927`    |         |
| `ind_name`        | `string`      | 主要產業類別名稱 | `豆類製品零售`     |         |
| `ind_code1`       | `number`       |                  | -          |         |
| `ind_name1`       | `string`      |                  | -          |         |
| `ind_code2`       | `number`       |                  | -          |         |
| `ind_name2`       | `string`      |                  | -          |         |
| `ind_code3`       | `number`       |                  | -          |         |
| `ind_name3`       | `string`      |                  | -          |         |
| `update_dttm`     | `string`        | 資料更新時間(yyyyMMdd)西元年     | `20251217`       | |         |
| `check_dttm`     | `string`        | 資料更新時間(yyyyMMdd)西元年     | `20251217`       | |         |

## 備註
- 必填欄位：`party_id`、`party_addr`。
