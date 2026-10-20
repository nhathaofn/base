# Phân Loại Giá Trị Dữ Liệu (Value Classification Matrix)

[STATUS: VERIFIED]
Tài liệu này hệ thống hóa các trường dữ liệu xuất hiện trong toàn bộ chu trình hoạt động của Google Flow theo 4 cấp độ phân loại: **Static (Tĩnh)**, **Dynamic (Động do người dùng)**, **Derived (Phái sinh)**, và **Server-generated (Máy chủ sinh ra)**.

---

## 1. Ma Trận Phân Loại Toàn Diện (Classification Matrix)

| Danh Mục Dữ Liệu | Tên Trường Dữ Liệu | Cấp Phân Loại | Nguồn Gốc / Cơ Chế Tính Toán |
|---|---|---|---|
| **Hệ thống / Runtime** | `Build Label` (`cfb2h`) | **Static** | Cố định theo từng phiên bản phát hành backend (`boq_labs-ai-sandbox...`). |
| **Hệ thống / Runtime** | `Recaptcha Site Key` | **Static** | Cố định trong mã nguồn cấu hình của Google (`WIZ_global_data.xZbWve`). |
| **Hệ thống / Runtime** | `Product ID` (`og_pid`) | **Static** | Cố định mã sản phẩm Google Flow (`749`). |
| **Xác thực / Phiên** | `CSRF Token` (`SNlM0e` / `at`) | **Server-generated** | Máy chủ ký mã HMAC kèm timestamp epoch (`AFfZ...:<timestamp>`). |
| **Xác thực / Phiên** | `Session ID` (`f.sid`) | **Server-generated** | Máy chủ cấp phát khi bắt đầu phiên HTTP. |
| **Xác thực / Phiên** | `Gaia ID` (`S06Grb`) | **Server-generated** | Định danh tài khoản người dùng 21 chữ số gắn liền tài khoản Google. |
| **Dự án (Project)** | `projectId` | **Server-generated** | Chuỗi UUIDv4 sinh ra khi gọi `CreateProject` (`jHPbke`). |
| **Dự án (Project)** | `title` | **Dynamic** | Người dùng nhập hoặc mặc định sinh theo ngày giờ (`Tháng 10 13 - 16:07`). |
| **Dự án (Project)** | `updatedAt` | **Server-generated** | Cặp số nguyên Unix epoch `[seconds, nanos]` cập nhật sau mỗi thao tác. |
| **Dự án (Project)** | `thumbnailUrl` | **Derived** | Phái sinh từ URL hình ảnh/video của phân cảnh chính đầu tiên trong dự án. |
| **Dự án (Project)** | `resourcePath` | **Derived** | Phái sinh theo quy tắc ghép chuỗi: `tools/{toolId}/projects/{projectId}`. |
| **Phân cảnh (Scene)** | `sceneId` | **Server-generated** | Chuỗi UUIDv4 duy nhất của phân cảnh. |
| **Phân cảnh (Scene)** | `title` | **Dynamic** | Tóm tắt prompt hoặc tên do người dùng sửa đổi. |
| **Phân cảnh (Scene)** | `isPinned` | **Dynamic** | Trạng thái cờ đánh dấu ghim cảnh trên timeline. |
| **Quy trình (Workflow)**| `workflowId` | **Server-generated** | Chuỗi UUIDv4 định danh lần chạy sinh nội dung. |
| **Quy trình (Workflow)**| `prompt` | **Dynamic** | Chuỗi câu lệnh văn bản do người dùng nhập hoặc chỉnh sửa. |
| **Quy trình (Workflow)**| `seed` | **Dynamic / Derived** | Số nguyên ngẫu nhiên sinh bằng `_.zr()` hoặc do người dùng cố định để tái lập. |
| **Quy trình (Workflow)**| `aspectRatio` | **Dynamic** | Lựa chọn tỉ lệ enum của người dùng (`1` = 1:1, `3` = 16:9, `5` = 9:16). |
| **Quy trình (Workflow)**| `duration` | **Dynamic** | Lựa chọn thời lượng video (`4`, `6`, `10` giây). |
| **Quy trình (Workflow)**| `modelId` | **Dynamic** | Mã mô hình AI được chọn (`veo_3_1_fast`, `abra_r2v_10s`, ...). |
| **Quy trình (Workflow)**| `status` | **Server-generated** | Mã trạng thái tiến độ từ máy chủ (`1` = Queued, `2` = Processing, `3` = Success). |
| **Tài sản (Media)** | `mediaId` | **Server-generated** | UUID định danh tệp phương tiện. |
| **Tài sản (Media)** | `servingUrl` | **Derived** | URL hiển thị CDN: `https://lh3.googleusercontent.com/asb/{hash}=s1600-rw`. |
| **Tài sản (Media)** | `fileSizeBytes` | **Server-generated** | Dung lượng tệp tính bằng byte do máy chủ đo lường sau khi render. |
| **Hạn mức (Quota)** | `remainingCredits` | **Server-generated** | Số dư tín dụng khả dụng, tự động trừ sau mỗi tác vụ sinh. |
| **Hạn mức (Quota)** | `resetTimestamp` | **Server-generated** | Mốc thời gian chu kỳ đặt lại tiếp theo của gói dịch vụ. |

---

## 2. Ý Nghĩa Đối Với Thiết Kế Hệ Thống Zero-Hardcode

- **Các trường `Static`:** Có thể duy trì làm fallback nhưng phải được cập nhật qua cấu hình tải ngoài hoặc giải mã tự động từ bundle.
- **Các trường `Server-generated`:** Tuyệt đối không được gán cứng (hardcode) trong client; phải luôn đọc trực tiếp từ phản hồi của các lệnh gọi `CreateProject`, `BatchAsyncGenerateVideoText`, hoặc `GetProjectContents`.
- **Các trường `Dynamic`:** Phải được mô hình hóa thành các form input / options có ràng buộc kiểm tra hợp lệ (validation rules) rõ ràng.
- **Các trường `Derived`:** Phải được tính toán thông qua các hàm tiện ích thuần túy (pure utility functions) để đảm bảo đồng bộ 100% với giao diện người dùng.
