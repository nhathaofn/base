# Nhật Ký Quan Sát Hành Vi Thực Tế (Observed Behaviors)

[STATUS: OBSERVED]
Tài liệu này ghi lại các hành vi quan sát trực tiếp trên giao diện trình duyệt và các tương tác thời gian thực được thu thập qua Chrome DevTools Protocol (CDP).

---

## 1. Hành Vi Giao Diện Người Dùng (UI/UX Behaviors in Project Studio)

### A. Thanh Tiêu Đề (Header Bar):
- Nút `home`: Quay về danh sách dự án `/projects`.
- Ô nhập tiêu đề: Cho phép chỉnh sửa trực tiếp tên dự án (`contenteditable` hoặc input text). Khi mất tiêu điểm (`blur`), kích hoạt mutation `MUTATE_PROJECT`.
- Biểu tượng `PRO`: Huy hiệu tài khoản đã kích hoạt gói trả phí Google AI Plan.
- Menu tùy chọn `more_vert`: Chia sẻ dự án, xuất xưởng, xóa dự án.

### B. Thanh Điều Hướng Bên Trái (Left Navigation Panel):
- Bộ lọc danh mục tài sản:
  - `Tất cả nội dung nghe nhìn`: Hiển thị toàn bộ assets trên canvas.
  - `Hình ảnh`: Lọc chỉ hiển thị ảnh tĩnh tạo bởi Nano Banana.
  - `Video`: Lọc chỉ hiển thị clip tạo bởi Veo.
  - `Nhân vật`: Danh sách diễn viên/khuôn mặt nhất quán.
  - `Cảnh`: Danh sách phân cảnh theo thứ tự kịch bản.
  - `Tệp tải lên`: Các tài sản người dùng tự tải lên từ máy tính.
  - `Thư viện`: Các bộ sưu tập lưu trữ.
  - `Công cụ` & `Tạo công cụ`: Danh mục các Applets AI tùy biến.
  - `Thùng rác`: Các mục đã xóa tạm thời.
- Nút thu gọn: `left_panel_close` để mở rộng tối đa không gian làm việc của Canvas.

### C. Khu Vực Soạn Thảo Lệnh & Chọn Mô Hình (Bottom Prompt Dock):
- Textarea đa dòng: `"Bạn muốn tạo những gì?"`. Hỗ trợ xuống dòng, tự động co giãn chiều cao theo nội dung prompt.
- Nút chuyển chế độ: `"Tác nhân"` (Agent Mode). Khi bật, câu lệnh chuyển sang giao diện đàm thoại với Gemini Flash thay vì sinh trực tiếp.
- Nút cấu hình mô hình:
  - Hiển thị mô hình hiện tại: `🍌 Nano Banana 2.1`.
  - Tỉ lệ khung hình: `crop_16_9` (hoặc `crop_9_16`, `crop_1_1`).
  - Số lượng biến thể sinh ra: `x2` (sinh 2 ảnh/video cùng lúc cho mỗi prompt).
- Nút thực thi: `arrow_forward` (gửi lệnh sinh).

---

## 2. Nhật Ký Kết Nối & Telemetry (Network Traces)

Trong quá trình tương tác, ngoài các RPC batchexecute chính, trình duyệt liên tục trao đổi dữ liệu với các hệ thống hỗ trợ:
1. **AsyncDataService:**
   - URL: `https://ogads-pa.clients6.google.com/$rpc/google.internal.onegoogle.asyncdata.v1.AsyncDataService/GetAsyncData`
   - Phương thức: `POST` (với `OPTIONS` preflight).
   - Mục đích: Đồng bộ avatar người dùng, trạng thái Google One và các dịch vụ Google liên kết.
2. **Clearcut Logging:**
   - URL: `https://play.google.com/log`
   - Gửi các gói batch chứa thông tin sự kiện giao diện (UI click, model switch, prompt submission duration).
