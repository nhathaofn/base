# Kiến Trúc Nền Tảng & Runtime (Boq Platform Runtime)

[STATUS: VERIFIED]
Tài liệu này ghi lại kiến trúc hạ tầng thực tế được xác minh thông qua phân tích mạng và mã nguồn phía client của Google Flow (`flow.google.com`).

---

## 1. Nền Tảng Máy Chủ (Backend Platform)

Google Flow vận hành trên nền tảng **Google Boq** (Borg-based platform for Web applications), cụ thể là service:
- **Tên Service nội bộ:** `boq-labs-ai-sandbox`
- **Phiên bản Build (Build Label):** `boq_labs-ai-sandbox-frontend_20261018.05_p0` (quan sát được trong URL param `bl` và `WIZ_global_data.cfb2h`).
- **Server Header:** `Server: ESF` (Enterprise Security Frontend / Google Frontend Edge Proxy).
- **Giao thức mạng:** HTTP/3 (QUIC) và HTTP/2 qua TLS 1.3.

---

## 2. Công Nghệ Giao Diện (Frontend Framework & Architecture)

- **Framework:** **Google Wiz + Angular** (tên nội bộ: `AiSandboxAngularFrontend`).
- **State Management:** `@tanstack/angular-query-experimental` (Angular Query) kết hợp với Angular Signals (`_.X`, `_.P`, `_.nj`).
- **Gói mã nguồn (Bundling):** Google Closure Compiler kết hợp chunking động theo Module Loader nội bộ (`exm`, `excm`, `m` parameters).
  - Main bundle: `k=boq-labs-ai-sandbox.AiSandboxAngularFrontend.vi.1dcxrhzrvVk.2018.O`
  - Core Chunk: `m=_b` (Bootstrapper, Polymer/Wiz base, Network layer)
  - Studio Lazy Chunks: `m=wO1vlb`, `m=XRV0Af`, `m=zxMy9c`, `m=rZcQQd`

---

## 3. Cấu Trúc Khởi Tạo SSR & Global Data (`WIZ_global_data`)

Khi tải trang HTML từ máy chủ, Google Boq chèn trực tiếp một đối tượng cấu hình toàn cục `window.WIZ_global_data`. Các khóa quan trọng đã xác minh:

| Khóa (Key) | Mục đích / Ý nghĩa | Bằng chứng kiểm chứng |
|---|---|---|
| `SNlM0e` | CSRF Token (Header / Body param `at`) | Dùng trong tất cả các request `batchexecute` mutation (`at=AFfZ...`) |
| `oPEP7c` | Email người dùng đăng nhập | Chuỗi email định dạng `user@gmail.com` |
| `S06Grb` | Gaia ID (Google Account ID) | Mã số định danh tài khoản Google 21 chữ số |
| `cfb2h` | Build Label của frontend service | Trùng khớp với param `bl` trong API request |
| `f_sid` | Session ID | Định danh phiên làm việc client-server (truyền qua URL param `f.sid`) |
| `xZbWve` | Recaptcha Enterprise Site Key | Dùng cho `grecaptcha.enterprise.ready()` với actions `IMAGE_GENERATION`, `VIDEO_GENERATION` |
| `bcsp` | Theme giao diện (`dark` / `light`) | Lưu trữ trong LocalStorage và WIZ data |

---

## 4. Phân Tuyến Tài Nguyên & Dịch Vụ Lưu Trữ (Media & CDN)

Hệ thống phân tách rõ ràng giữa máy chủ dữ liệu logic và máy chủ tài nguyên nhị phân:
1. **API & Logic:** `https://flow.google.com/_/AiSandboxAngularFrontend/data/batchexecute`
2. **Media Upload (Scotty Service):** `https://flow.google.com/upload/v1/flow/upload/video/{upload_id}`
3. **Asset Serving CDN (AiSandbox Binary):** `https://lh3.googleusercontent.com/asb/...` và `https://flow.google.com/asb/...`
4. **Static Assets & Presets:** `https://www.gstatic.com/aitestkitchen/website/flow/...` và `https://gstatic.com/aitestkitchen/voices/samples/{VoiceName}.wav`
5. **Anti-Abuse Verification:** `https://www.google.com/recaptcha/enterprise.js`

---

## 5. Hệ Thống Giám Sát & Đo Lường (Telemetry)

1. **Google Clearcut Logger:**
   - Endpoint: `POST https://play.google.com/log`
   - Báo cáo lỗi ứng dụng, độ trễ và sự kiện người dùng theo chu kỳ.
2. **Google Analytics 4 & GTM:**
   - Measurement ID: `G-X2GNH8R5NS`
   - Container ID: `GTM-NZ9M8LQL`
   - Endpoint: `https://www.google-analytics.com/g/collect`
