# Phân Tích Dịch Vụ: FlowAppletAgentService (Hệ Thống Công Cụ Tùy Chỉnh & Applets)

[STATUS: VERIFIED]
`FlowAppletAgentService` (`/google.internal.labs.aisandbox.proto.flow.agent.v1.FlowAppletAgentService`) là hạ tầng cho phép người dùng tự tạo, chia sẻ, sao chép (fork) và thực thi các công cụ tạo sinh tùy biến (Applets / Tools) trên nền tảng Google Flow.

---

## 1. Danh Mục Các Phương Thức RPC Đã Xác Minh (28 Methods)

### A. Thực Thi Công Cụ (Execution)
| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Cơ Chế Hoạt Động |
|---|---|---|---|
| `cNQB4b` | `RunAppletAgentSse` | Mutation (Za: false, Streaming zU) | **Thực thi công cụ dạng Server-Sent Events:** Chạy workflow tùy chỉnh và stream tiến độ về giao diện |
| `Z8KLDf` | `RunAppletAgent` | Mutation (Za: false) | Chạy công cụ đồng bộ |
| `HqMS3` | `ClearAppletSession` | Mutation (Za: false) | Xóa phiên thực thi của công cụ |

### B. Quản Lý & Phiên Bản (Applet CRUD & Versioning)
| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Chức Năng |
|---|---|---|---|
| `tRARke` | `ListApplets` | Query (Za: true) | Lấy danh sách toàn bộ công cụ của người dùng và cộng đồng |
| `e6lwif` | `GetApplet` | Query (Za: true) | Đọc cấu hình chi tiết của một công cụ |
| `ZLaYcd` | `GetAppletVersion` | Query (Za: true) | Lấy chi tiết một phiên bản cụ thể của công cụ |
| `sd0GXe` | `UpdateApplet` | Mutation (Za: false) | Cập nhật logic, prompt mẫu, hoặc UI của công cụ |
| `zpwzEe` | `DeleteApplet` | Mutation (Za: false) | Xóa công cụ |
| `CvpHmb` | `RevertAppletVersion` | Mutation (Za: false) | Quay lại phiên bản cũ hơn của công cụ |
| `YRmDpc` | `SeedApplet` | Mutation (Za: false) | Khởi tạo cấu hình mặc định ban đầu cho công cụ mới |

### C. Chia Sẻ & Cộng Đồng (Sharing, Forking & Marketplace)
| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Chức Năng |
|---|---|---|---|
| `vEIlvc` | `ShareApplet` | Mutation (Za: false) | Xuất bản công cụ ra cộng đồng qua liên kết chia sẻ |
| `h4NnAe` | `UnshareApplet` | Mutation (Za: false) | Thu hồi quyền truy cập công khai của công cụ |
| `J0KDW` | `GetSharedAppletVersion` | Query (Za: true) | Đọc phiên bản của công cụ được chia sẻ |
| `cIafDb` | `GetSharedAppletVersionPreview` | Query (Za: true) | Xem trước giao diện và tính năng của công cụ được chia sẻ |
| `CSvxid` | `ForkSharedApplet` | Mutation (Za: false) | **Fork (Tạo nhánh sao chép):** Nhập công cụ của người khác về tài khoản của mình để tiếp tục chỉnh sửa |
| `VVrfbf` | `CopyApplet` | Mutation (Za: false) | Sao chép công cụ nội bộ |
| `VdM3v` | `SaveSharedApplet` | Mutation (Za: false) | Lưu công cụ chia sẻ vào danh sách yêu thích của tài khoản |
| `qJcgMc` | `ListSavedSharedApplets` | Query (Za: true) | Liệt kê danh sách các công cụ cộng đồng đã lưu |
| `ipGN1` | `DeleteSavedSharedApplet` | Mutation (Za: false) | Bỏ lưu công cụ cộng đồng |
| `eDee9c` | `FavoriteApplet` | Mutation (Za: false) | Đánh dấu sao yêu thích công cụ |
| `TsaPHc` | `UnfavoriteApplet` | Mutation (Za: false) | Bỏ đánh dấu sao |
| `NpB2cd` | `SubmitAppletReview` | Mutation (Za: false) | Gửi đánh giá / bình luận về công cụ |

### D. Quản Trị Hệ Thống & Kiểm Duyệt (Admin & Moderation)
| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Chức Năng |
|---|---|---|---|
| `tmHIkc` | `BlockApplet` | Mutation (Za: false) | Chặn công cụ vi phạm chính sách |
| `Ifmob` | `UnblockApplet` | Mutation (Za: false) | Bỏ chặn công cụ |
| `UaAwic` | `AdminDeleteApplet` | Mutation (Za: false) | Quyền quản trị xóa công cụ |
| `AmBK3b` | `DeleteGoogleOwnedApplet` | Mutation (Za: false) | Xóa công cụ chính thức do Google tạo |
| `XbyPOc` | `UpdateGoogleOwnedAppletMetadata` | Mutation (Za: false) | Cập nhật thông tin công cụ chính thức của Google |

---

## 2. Dữ Liệu Quan Sát Thực Tế (Observed Applet Data)

Trong network capture `project_studio.json`, RPC `tRARke` trả về danh mục các công cụ cộng đồng nổi bật:
- Applet ID: `41f88220-763c-4b39-b31e-8cba4872a62d`
- Tên công cụ: `"Remix of LyricFlow"`
- Mô tả: `"Generate AI music videos and high-quality audio from your lyrics"`
- Tác giả: Tác giả cộng đồng, có khả năng fork và tùy biến luồng sinh video kết hợp âm thanh.
