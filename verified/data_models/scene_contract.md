# Hợp Đồng Dữ Liệu: Phân Cảnh (Scene Contract)

[STATUS: VERIFIED]
Hợp đồng dữ liệu của đối tượng **Scene** được trích xuất từ phản hồi của `Zzl0ze` (`/FlowService.GetProjectContents`, section `contents[1]`).

---

## 1. Cấu Trúc Đối Tượng Mảng JSON (Wire Format)

Mỗi phân cảnh (Scene) đại diện cho một khối hình ảnh hoặc đoạn video độc lập trên timeline của dự án:

```json
[
  "SCENE_UUID",
  null,
  null,
  [
    "SCENE_TITLE",
    [
      "CREATED_AT_SECONDS",
      "CREATED_AT_NANOS"
    ],
    "IS_PINNED_OR_FLAG",
    null,
    "PRIMARY_WORKFLOW_ID",
    "GENERATION_TASK_ID",
    [
      "COMPLETED_AT_SECONDS",
      "COMPLETED_AT_NANOS"
    ]
  ],
  "PROJECT_UUID"
]
```

### Chi Tiết Từng Thuộc Tính:

| Chỉ Mục (Index) | Tên Trường | Kiểu Dữ Liệu | Phân Loại | Ý Nghĩa / Quy Tắc |
|---|---|---|---|---|
| `[0]` | `sceneId` | String (UUIDv4) | Server-generated | Định danh duy nhất của phân cảnh (ví dụ: `5142f879-3dd3-444c-809e-4a1808c494be`). |
| `[3][0]` | `title` | String | Dynamic | Tiêu đề hoặc tóm tắt prompt của cảnh (ví dụ: `"Man acting naturally in public"`). |
| `[3][1][0]` | `createdAtSeconds` | Integer (Epoch sec) | Server-generated | Mốc thời gian tạo cảnh (ví dụ: `1791942461`). |
| `[3][1][1]` | `createdAtNanos` | Integer | Server-generated | Nano giây tạo cảnh. |
| `[3][2]` | `isPinned` | Boolean / Null | Dynamic | Cờ ghim phân cảnh trên timeline hoặc trạng thái xem trước. |
| `[3][4]` | `workflowId` | String (UUIDv4) | Server-generated | ID của Workflow chịu trách nhiệm tạo ra nội dung cho cảnh này (ví dụ: `8eb41f86-bae8-4452-b5bb-39406e6343ee`). |
| `[3][5]` | `taskId` | String (UUID) | Server-generated | Mã định danh tác vụ sinh của backend (Task/Job UUID viết hoa: `82F8AAB2-BEC7-49E8-9BA6-37D09F82B3D3`). |
| `[3][6][0]` | `completedAtSeconds`| Integer (Epoch sec) | Server-generated | Thời điểm tác vụ render video hoàn tất (ví dụ: `1791942467`). |
| `[4]` | `projectId` | String (UUIDv4) | Server-generated | ID của dự án cha chứa phân cảnh này (ví dụ: `22d33fe3-5afe-4106-8913-dc66336677f8`). |

---

## 2. Tính Chất & Mối Quan Hệ (Relationships)

- **Quan hệ 1-Nhiều với Project:** Một dự án có thể chứa nhiều Scenes xếp theo thứ tự thời gian.
- **Quan hệ 1-1 với Workflow:** Mỗi Scene liên kết với một Workflow chính (`primaryWorkflowId`) lưu giữ toàn bộ prompt, mô hình và hạt giống (seed) đã sinh ra nó.
- **Tính toán thời gian render (Latency Metric):**
  - Thời gian render thực tế = `completedAtSeconds - createdAtSeconds`.
  - Trong ví dụ thực tế trên: `1791942467 - 1791942461 = 6 giây` cho một video 10 giây (tốc độ sinh của mô hình Veo / Abra).
