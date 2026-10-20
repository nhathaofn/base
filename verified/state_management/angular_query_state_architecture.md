# Kiến Trúc Quản Lý Trạng Thái: Angular Query & Signals (State Management)

[STATUS: VERIFIED]
Google Flow áp dụng mô hình quản lý trạng thái hiện đại kết hợp giữa **Angular Query** (thư viện port của TanStack Query cho Angular) và **Angular Signals** để đảm bảo khả năng phản ứng thời gian thực (Reactivity), bộ nhớ đệm (Caching) và cập nhật lạc quan (Optimistic UI).

---

## 1. Phân Loại Khóa Truy Vấn (Query Keys Taxonomy)

Hệ thống quản lý dữ liệu máy chủ (Server State) thông qua cây phân cấp khóa truy vấn rõ ràng:

| Nhóm Dữ Liệu | Query Key Mẫu | Mục Đích Lưu Trữ & Chiến Lược Cache |
|---|---|---|
| **Dự Án Tổng Thể** | `["PROJECTS"]` | Danh sách dự án hiển thị ở màn hình Dashboard |
| **Chi Tiết Dự Án** | `["PROJECT", projectId]` | Metadata của một dự án đơn lẻ |
| **Các Khối Dòng Thời Gian** | `["PROJECT_TILES", projectId]` | Toàn bộ các ô phân cảnh (tiles), clip video, ảnh trên canvas |
| **Tài Sản Đa Phương Tiện** | `["MEDIA", mediaId]` | Metadata chi tiết của một tệp ảnh/video |
| **Nguồn Ảnh CDN** | `["IMAGE_SRC", assetId, ...]` | Cache URL hiển thị ảnh có chữ ký tạm thời |
| **Nguồn Video CDN** | `["VIDEO_URLS", assetId, ...]` | Cache các biến thể stream và URL phát MP4 |
| **Trạng Thái Mô Hình AI** | `["MODEL_STATUSES"]` | Trạng thái sẵn sàng của 54 model (lấy từ `yBhWQ`) |
| **Danh Mục Công Cụ** | `["APPLETS"]` | Danh sách các công cụ cộng đồng |
| **Phiên Bản Công Cụ** | `["APPLET_VERSION", appletId, version]` | Logic và cấu hình của một phiên bản tool cụ thể |
| **Công Cụ Đã Lưu** | `["SAVED_SHARED_APPLETS"]` | Danh sách công cụ người dùng đã bookmark |
| **Thực Thể Ngữ Nghĩa** | `["ENTITY", entityId]` | Cache thực thể nhân vật, bối cảnh (`staleTime: Infinity`) |

---

## 2. Vòng Đời Tác Vụ Đột Biến (Mutation Lifecycle)

Toàn bộ các thao tác chỉnh sửa dữ liệu được đóng gói thành các Mutation:

```
[Bắt đầu] ──► onMutate() ────────────► mutationFn() ──────────► onSuccess() ──► Hoàn tất
                 │                            │                      │
                 ▼                            ▼                      ▼
        Optimistic Update             Gọi BatchExecute RPC      Invalidate Queries
       (Chèn Tile tạm thời)           (YhhmEf / ogiZ0b)         (["PROJECT_TILES"])
                                              │
                                              ▼
                                         onError()
                                      (Rollback Tile)
```

### Các Khóa Đột Biến (Mutation Keys) Đã Xác Minh:
1. `["CREATE_PROJECT"]`
2. `["DELETE_PROJECT", projectId]`
3. `["MUTATE_PROJECT", projectId]`
4. `["MUTATE_PROJECT_TILES", projectId]`
5. `["GENERATE_VIDEO"]`
6. `["GENERATE_IMAGE"]`
7. `["GENERATE_TEXT"]`
8. `["GENERATE_GIF"]`
9. `["GENERATE_VOICE_PREVIEW"]`
10. `["TRANSFORM_IMAGE"]`
11. `["UPSAMPLE_IMAGE"]`
12. `["UPSAMPLE_VIDEO"]`
13. `["UPLOAD_IMAGE"]`
14. `["UPLOAD_VIDEO"]`
15. `["MUTATE_APPLET"]`
16. `["FORK_SHARED_APPLET"]`

---

## 3. Tích Hợp Angular Signals (Reactive Primitives)

Mã nguồn client sử dụng các hàm nguyên thủy của Angular Signals:
- `_.P(initialValue)`: Writable Signal (tương đương `signal(initialValue)`).
- `_.X(() => expr)`: Computed Signal (tương đương `computed(() => expr)`).
- `_.nj(() => effect)`: Reactive Effect (tương đương `effect(() => ...)`).
- `b.vc()` / `signal.asReadonly()`: Chuyển đổi thành Read-only Signal để bảo vệ tính toàn vẹn trạng thái ngoài view.

---

## 4. Bộ Nhớ Trình Duyệt (Browser Storage Breakdown)

### LocalStorage (Trạng thái tĩnh phía client):
- `bcsp`: Lưu chủ đề giao diện (`"dark"` / `"light"`).
- `flow-projects-sort-order`: Thứ tự sắp xếp dự án (`"3"` = Sắp xếp theo ngày cập nhật mới nhất).
- `flow-smart-app-banner-dismissed`: Cờ ghi nhớ việc đóng thanh gợi ý cài ứng dụng (`"false"`).
- `flow-debug-flag-overrides`: Ghi đè cờ tính năng nội bộ (`"{}"`).
- `flow-debug-pinned-flags`: Danh sách cờ debug được ghim (`"[]"`).

### SessionStorage:
- Hoàn toàn rỗng (`[]`). Hệ thống không lưu trữ token nhạy cảm trong SessionStorage để giảm thiểu nguy cơ đánh cắp phiên qua XSS.
