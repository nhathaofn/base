# Cơ Chế Tải Lên Phương Tiện: Google Scotty Protocol (Media Upload)

[STATUS: VERIFIED]
Google Flow sử dụng hạ tầng tải lên tệp hiệu năng cao **Google Scotty** để tiếp nhận các tệp video và hình ảnh dung lượng lớn từ người dùng, trích xuất từ các hàm `Pab` và `Yab` trong `chunk_studio_1.js`.

---

## 1. Điểm Cuối Dịch Vụ & Cấu Trúc URL (Upload Endpoint)

```
POST https://flow.google.com/upload/v1/flow/upload/video/{upload_session_id}
```

- Endpoint phục vụ riêng cho các tệp video và tài sản media đầu vào.
- `{upload_session_id}`: Chuỗi định danh phiên upload duy nhất do client hoặc server cấp phát.

---

## 2. Các Tiêu Đề Bắt Buộc (Required Headers)

| Tên Header | Ví Dụ Giá Trị | Mục Đích Kỹ Thuật |
|---|---|---|
| `X-Framework-Xsrf-Token` | `AFfZSpg...` | Token bảo mật chống CSRF của framework Boq |
| `Slug` | `my_reference_video.mp4` | Tên tệp gốc được mã hóa URI (`encodeURIComponent(file.name)`) |
| `x-trim-start` | `1500` | Mốc thời gian bắt đầu cắt (tính bằng mili giây) nếu người dùng có thao tác trim |
| `x-trim-end` | `7500` | Mốc thời gian kết thúc cắt (tính bằng mili giây) |
| `X-Enterprise-Cloud-Project-Number` | `106433...` | Mã dự án Google Cloud của tài khoản doanh nghiệp (nếu có) |
| `Content-Type` | `video/mp4` hoặc `image/jpeg` | MIME type thực tế của tệp tải lên |

---

## 3. Cơ Chế Thử Lại & Xử Lý Sự Cố (Retry Policy)

Được định nghĩa tường minh qua token cấu hình `VIDEO_UPLOAD_RETRY_DELAY_MS`:
```javascript
Oab = new _.Ye("VIDEO_UPLOAD_RETRY_DELAY_MS", {
  Fc: "root",
  Pa: () => 500
});
```

- **Độ trễ thử lại (Retry Delay):** `500 ms`.
- **Số lần thử tối đa:** `2` lần (vòng lặp `for (d = 1; d <= 2; d++)`).
- Nếu lần 1 thất bại do lỗi mạng tạm thời, client chờ đúng 500ms trước khi kích hoạt phiên truyền dữ liệu lần 2.

---

## 4. Báo Cáo Đo Lường (Upload Telemetry)

Trước khi bắt đầu truyền byte dữ liệu, client phát sự kiện telemetry về hệ thống:
```javascript
_.Ju(a.Ga, "FLOW_UPLOAD", {
  FLOW_UPLOAD_TYPE: "VIDEO",
  FLOW_UPLOAD_SOURCE: source,
  FLOW_UPLOAD_SETTINGS: JSON.stringify({
    mimeType: mimeType,
    dimensions: dimensions,
    aspectRatio: aspectRatio
  })
});
```
Sự kiện này theo dõi nguồn gốc tải lên (từ thanh công cụ, từ kéo thả, hoặc từ thư viện) kèm kích thước và tỉ lệ khung hình của video.
