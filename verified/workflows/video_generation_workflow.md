# Quy Trình Thực Thi: Sinh Video Hoàn Chỉnh (Video Generation Workflow)

[STATUS: VERIFIED]
Tài liệu này mô tả toàn bộ vòng đời tác vụ (Action Lifecycle) từ khi người dùng nhập câu lệnh đến khi nhận được tệp video hoàn chỉnh.

---

## 1. Sơ Đồ Trình Tự Thực Thi (Sequence Diagram)

```
[Người Dùng]        [UI Studio]           [Recaptcha Enterprise]      [Boq ESF Edge]          [VideoFx Backend]
     │                   │                          │                       │                        │
     ├─ Nhập Prompt ────►│                          │                       │                        │
     ├─ Chọn Model/Tỉ lệ─►│                          │                       │                        │
     ├─ Nhấn "Tạo" ─────►│                          │                       │                        │
     │                   ├─ execute("VIDEO_GEN") ──►│                       │                        │
     │                   │◄─ Recaptcha Token ───────┤                       │                        │
     │                   │                                                  │                        │
     │                   ├─ Gói Payload (QZa) & đính kèm Token              │                        │
     │                   ├─ POST batchexecute (YhhmEf / MZZa6b) ───────────►│                        │
     │                   │  (Header: X-Same-Domain: 1, Body: f.req + at)    ├─ Chuyển tiếp RPC ─────►│
     │                   │                                                  │                        ├─ Khởi tạo Job ID
     │                   │◄─ Trả về Job Envelope [["wrb.fr", ...]] ─────────┴────────────────────────┤  (Trừ tín dụng)
     │                   │                                                                           │
     │                   ├─ [Lớp Thăm Dò Polling / Stream]                                           │
     │                   ├─ Lặp 3s/lần kiểm tra trạng thái ─────────────────────────────────────────►│
     │                   │◄─ Trả về Status: 1 (Queued) / 2 (Rendering) ──────────────────────────────┤
     │                   │◄─ Trả về Status: 3 (Success) + CDN Media URL ─────────────────────────────┤
     │                   │                                                                           │
     │◄─ Hiển thị video ─┤ (Lưu cache Angular Query ["PROJECT_TILES"])                               │
```

---

## 2. Chi Tiết Từng Bước Trong Vòng Đời Tác Vụ

### Bước 1: Tiếp nhận dữ liệu đầu vào & Chuẩn bị tham số
- Client đọc từ form:
  - `prompt`: Chuỗi văn bản người dùng nhập.
  - `aspectRatio`: Giá trị enum (`1` = 1:1, `3` = 16:9, `5` = 9:16).
  - `duration`: `4`, `6`, hoặc `10` giây.
  - `resolution`: Enum độ phân giải (mặc định 720p).
  - `firstFrame` / `lastFrame`: (Nếu chọn chế độ I2V hoặc Interpolation).
  - `references`: Mảng chứa UUID của các ảnh/nhân vật tham chiếu.
  - `seed`: Số nguyên ngẫu nhiên hoặc do client sinh bằng hàm `_.zr()`.

### Bước 2: Kích hoạt bảo vệ Anti-Bot (Recaptcha Enterprise)
- Hàm `this.ua.Sp("VIDEO_GENERATION")` được gọi ngầm.
- WebWorker Recaptcha gửi tín hiệu về `https://www.google.com/recaptcha/enterprise/anchor`.
- Nhận về một chuỗi mã hóa `recaptchaToken`.
- Đóng gói token vào envelope protobuf `_.hS`.

### Bước 3: Đóng gói Protobuf Request (`QZa` & `aT`)
- Hàm `QZa` chuyển đổi cấu hình giao diện thành đối tượng Protobuf:
  - Chuyển `prompt` qua bộ chuẩn hóa chuỗi `_.VO(prompt).trim()`.
  - Thiết lập chế độ sinh `gs`: `"TEXT"`, `"REFERENCES"`, `"START_FRAME"`, `"START_END_FRAMES"`, `"EDIT_VIDEO"`, hoặc `"EXTEND_VIDEO"`.
  - Gán token CSRF `at` từ `WIZ_global_data.SNlM0e`.

### Bước 4: Phát lệnh gọi mạng qua BatchExecute
Client chọn RPC ID tương ứng với chế độ sinh:
- **Text:** `YhhmEf` (`/VideoFxService.BatchAsyncGenerateVideoText`)
- **Reference:** `MZZa6b` (`/VideoFxService.BatchAsyncGenerateVideoReferenceImages`)
- **Start Image:** `eb1hJf` (`/VideoFxService.BatchAsyncGenerateVideoStartImage`)
- **Interpolation:** `nprQif` (`/VideoFxService.BatchAsyncGenerateVideoStartAndEndImage`)
- **Edit:** `jIps6` (`/VideoFxService.BatchAsyncGenerateVideoEditVideo`)
- **Extend:** `fZytfe` (`/VideoFxService.BatchAsyncGenerateVideoExtendVideo`)

### Bước 5: Cập nhật lạc quan giao diện (Optimistic UI Update)
- Ngay khi nhận được phản hồi khởi tạo từ backend (hoặc ngay trước khi gửi), client chèn một khối khung nháp (Placeholder Tile) vào dòng thời gian.
- Hiển thị thanh tiến độ quay vòng và ước tính thời gian chờ.

### Bước 6: Thăm dò tiến độ (Job Polling / Status Tracking)
- Vòng lặp thăm dò chạy với chu kỳ 3000ms.
- Phân tích mã trạng thái phản hồi `g = f.Xe()`:
  - `1`, `2`, `6`: Đang xếp hàng / Đang render. Tiếp tục lặp.
  - `3`: Thành công! Máy chủ trả về URL CDN `https://lh3.googleusercontent.com/asb/...`.
  - `4`, `5`, `7`: Thất bại (hết hạn ngạch, vi phạm chính sách an toàn prompt, hoặc lỗi máy chủ). Bắn ngoại lệ `Error("sf")`.
- Hạn mức thời gian chờ tối đa (Timeout): 40 lượt x 3s = 120 giây (2 phút).

### Bước 7: Cập nhật trạng thái và hoàn tất
- Sau khi nhận được tệp video hoàn chỉnh, client gọi cập nhật cache:
  - `["PROJECT_TILES", projectId]`
  - `["MEDIA", mediaId]`
  - Cập nhật số dư tín dụng `["CREDITS"]` qua `nzlxg`.
- Video sẵn sàng để xem lại, cắt ghép (trim), kéo dài (extend) hoặc xuất xưởng (export).
