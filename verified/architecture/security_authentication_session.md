# Cơ Chế Xác Thực, Phiên Làm Việc & Bảo Mật (Authentication & Security)

[STATUS: VERIFIED]
Tài liệu này chi tiết hóa toàn bộ cơ chế bảo mật, quản lý phiên làm việc và phòng chống tấn công của Google Flow.

---

## 1. Cơ Chế Xác Thực Người Dùng (Authentication)

Google Flow sử dụng hạ tầng xác thực tập trung **Google Gaia / Google Accounts**:
- **Cơ chế lưu trữ:** HTTP-Only Secure Cookies (`__Secure-1PSID`, `__Secure-3PSID`, `SAPISID`, `SSID`, `HSID`, `SID`).
- **Quy tắc bảo mật (Security Policy):** Không lưu trữ bất kỳ cookie hoặc token thực tế nào trong tài liệu này; toàn bộ token được hiển thị dưới dạng mẫu đại diện (`[REDACTED_SENSITIVE_AUTH]`).
- **Google Product ID (`og_pid`):** `749` (Mã định danh sản phẩm của Google Flow trong hệ sinh thái Google).
- **Cơ chế xoay vòng Cookie (Cookie Rotation):**
  - Hệ thống nhúng một iframe ẩn kết nối tới máy chủ Google Accounts để duy trì và làm mới phiên:
  - `https://accounts.google.com/RotateCookiesPage?og_pid=749&rot=3&origin=https%3A%2F%2Fflow.google.com&exp_id=0`
  - Khi token hết hạn hoặc cần cập nhật, iframe này gửi sự kiện `postMessage` để client đồng bộ lại trạng thái.

---

## 2. Phòng Chống Tấn Công Giả Mạo Yêu Cầu (CSRF / XSRF Protection)

Mọi yêu cầu thay đổi dữ liệu (POST mutation) bắt buộc phải có hai lớp bảo vệ:
1. **Header `X-Same-Domain: 1`:**
   - Ngăn chặn các request cross-origin thông thường từ trình duyệt.
2. **CSRF Token (`at` parameter):**
   - Lấy từ `WIZ_global_data.SNlM0e`.
   - Token có định dạng mã hóa HMAC kết hợp timestamp:
     `AFfZ<random_hash>:<epoch_timestamp_ms>` (Ví dụ: `AFfZSpglWqiM3Y12bDIAW4Y4-BHL:1792488790606`).
   - Được gửi trong thân request dưới dạng URL-encoded `at=...`.
3. **Scotty Upload Token:**
   - Khi upload tệp nhị phân qua Scotty, header bắt buộc: `X-Framework-Xsrf-Token: <token>`.

---

## 3. Lớp Bảo Vệ Chống Bot & Lạm Dụng (Recaptcha Enterprise)

Trước khi thực hiện các tác vụ tốn kém tài nguyên tính toán (GPU Generation), hệ thống kích hoạt **Recaptcha Enterprise**:
- **Site Key:** Nằm trong `WIZ_global_data.xZbWve` (`6LdsFiUsAAAAAIjVDZcuLhaHiDn5nnHVXVRQGeMV`).
- **Web Worker:** `https://www.google.com/recaptcha/enterprise/webworker.js` chạy nền để thu thập tín hiệu hành vi phần cứng và tương tác người dùng.
- **Hành động kiểm tra (Action Triggers):**
  - `IMAGE_GENERATION`: Khi nhấn nút tạo ảnh với Nano Banana / Abra.
  - `VIDEO_GENERATION`: Khi nhấn nút tạo video với Veo 3.1 / Omni.
  - `FLOW_UPLOAD`: Khi tải lên tệp video hoặc ảnh tham chiếu.
- **Cơ chế đóng gói Token:**
  - Token được sinh bất đồng bộ: `yield grecaptcha.enterprise.execute(siteKey, { action: "IMAGE_GENERATION" })`.
  - Token được đóng gói vào đối tượng Protobuf `_.hS`:
    `_.Eu(_.gS(_.fS(new _.hS, recaptchaToken)))`
  - Đưa trực tiếp vào payload nhị phân / mảng JSON của RPC `BatchGenerateImages` hoặc `BatchAsyncGenerateVideoText`.

---

## 4. Chính Sách Bảo Mật Trình Duyệt (Browser Security Headers)

Quan sát được từ các phản hồi thực tế của máy chủ ESF:
- **Content-Security-Policy:**
  `require-trusted-types-for 'script'; report-uri /_/AiSandboxAngularFrontend/cspreport`
  (Bắt buộc sử dụng Trusted Types cho mọi thao tác DOM script injection).
- **Cross-Origin-Opener-Policy:** `same-origin-allow-popups`
- **X-Frame-Options:** `SAMEORIGIN`
- **X-Content-Type-Options:** `nosniff`
- **Permissions-Policy:** `ch-ua-arch=*, ch-ua-bitness=*, ch-ua-full-version=*, ch-ua-platform=*` (Kích hoạt Client Hints cho Google Edge).
