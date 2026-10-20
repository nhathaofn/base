# Bản Đồ Điều Hướng & Routing Phía Client (Client Routing & Navigation)

[STATUS: VERIFIED]
Tài liệu này ghi lại toàn bộ bảng định tuyến SPA (Single Page Application) được trích xuất trực tiếp từ Abstract Syntax Tree (AST) của `bundle_0.js`.

---

## 1. Bảng Định Tuyến Đầy Đủ (Complete Route Table)

| Tuyến Đường (Path) | Mục Đích / Chức Năng | Thành Phần Giao Diện Tương Ứng |
|---|---|---|
| `/` hoặc `projects` | Trang tổng quan dự án | Danh sách dự án đã tạo, banner sự kiện, nút tạo dự án mới |
| `project/:projectId` | **Studio Sáng Tạo Chính (Main Studio)** | Bảng vẽ (Canvas), dòng thời gian (Timeline), trình nhập prompt, bộ chọn mô hình AI, thanh tài sản bên trái |
| `scene/:sceneId` | Trình biên tập cảnh độc lập | Xem chi tiết và chỉnh sửa từng phân cảnh (Scene) |
| `edit/:workflowId` | Trình kiểm tra quy trình (Workflow Inspector) | Xem tham số sinh chi tiết: prompt, seed, model, duration, aspect ratio |
| `character` | Quản lý nhân vật & diễn viên AI | Danh sách khuôn mặt / hình mẫu nhân vật đã đăng ký |
| `character/:characterId` | Huấn luyện nhân vật nhất quán | Đăng ký ảnh chân dung, huấn luyện mô hình nhân vật (Likeness Service) |
| `create-tool` | Trình tạo công cụ AI tùy chỉnh | Xây dựng công cụ Applet / Tool mới với agent logic riêng |
| `tools` | Thư viện công cụ cộng đồng | Khám phá các công cụ sinh nội dung do cộng đồng và Google phát triển |
| `tool/:appletId` | Thực thi công cụ tùy chỉnh | Giao diện chạy và tương tác với một Applet cụ thể |
| `collection/:collectionId` | Bộ sưu tập tài sản (Collections) | Nhóm các video, ảnh, âm thanh thành các thư mục dự án |
| `trash` | Thùng rác (Trash) | Khôi phục hoặc xóa vĩnh viễn dự án, cảnh và tệp media |
| `trash/collection/:collectionId` | Thùng rác theo bộ sưu tập | Xem các mục bị xóa trong một bộ sưu tập cụ thể |
| `shared/:mediaType/:mediaShareId` | Xem tệp chia sẻ công khai | Giao diện xem và import video/ảnh được chia sẻ từ người dùng khác |
| `shared/tool/:appletShareId` | Xem công cụ được chia sẻ | Xem trước và Fork (sao chép) công cụ Applet về tài khoản |
| `/ai/credits` | Bảng quản lý tín dụng & gói cước | Xem số lượng Flow credits còn lại, chu kỳ đặt lại, nạp thêm tín dụng |
| `/ai/activity` | Lịch sử hoạt động | Xem nhật ký các tác vụ tạo nội dung đã thực hiện |
| `/settings` | Cài đặt người dùng | Tùy chỉnh ngôn ngữ, quyền riêng tư, thông báo |
| `debug` | Bảng điều khiển Debug nội bộ | Bật/tắt cờ thử nghiệm (Phenotype feature flags), mock môi trường |

---

## 2. Các Tuyến Đường Hệ Thống & Kiểm Tra Điều Kiện (System & Guard Routes)

- `about` / `flow/about`: Trang giới thiệu sản phẩm (khi chưa đăng nhập hoặc xem thông tin tổng quan).
- `age-restricted`: Chặn người dùng dưới 18 tuổi (Google Flow yêu cầu tài khoản 18+).
- `unsupported-browser`: Thông báo trình duyệt không tương thích (yêu cầu Chromium/Chrome hiện đại).
- `unsupported-country`: Thông báo khu vực địa lý chưa được hỗ trợ.
- `unavailable`: Thông báo hệ thống bảo trì hoặc quá tải.
- `changelogs`: Nhật ký cập nhật tính năng mới.
- `404` / `**`: Tuyến fallback khi không tìm thấy trang.

---

## 3. Quy Ước Tham Số URL Toàn Cục (Global URL Parameters)

- `pli=1`: Cờ chỉ định tài khoản đã hoàn tất kiểm tra trạng thái đăng nhập Google Accounts.
- `hl=vi` (hoặc `en`, etc.): Mã ngôn ngữ giao diện (Host Language), đồng bộ với backend Boq.
- `authuser=0`: Định danh chỉ số tài khoản Google đang hoạt động trong phiên trình duyệt đa tài khoản.
