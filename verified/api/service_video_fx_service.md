# Phân Tích Dịch Vụ: VideoFxService (22 Methods)

[STATUS: VERIFIED]
`VideoFxService` là backend chuyên trách xử lý các thuật toán tạo video nâng cao (Veo video generation pipeline), tính toán tín dụng (Credits), các chỉ dẫn hệ thống (Preambles) và cấu hình ứng dụng.

---

## 1. Pipeline Tạo Video Bất Đồng Bộ (Async Video Generation Pipeline)

Tất cả các hàm này đều nhận tham số protobuffer `aT`, bao gồm: prompt, aspect ratio, duration, resolution, references, start/end frame và Recaptcha Enterprise token.

| RPC ID | Tên Hàm Protobuf | Mode Giao Diện | Mô Tả & Đầu Vào |
|---|---|---|---|
| `YhhmEf` | `BatchAsyncGenerateVideoText` | `TEXT` | **Text-to-Video:** Tạo video hoàn chỉnh trực tiếp từ câu lệnh văn bản. |
| `MZZa6b` | `BatchAsyncGenerateVideoReferenceImages` | `REFERENCES` | **Reference-to-Video (R2V):** Tạo video tuân thủ một hoặc nhiều hình ảnh tham chiếu (nhân vật, bối cảnh, đạo cụ). |
| `eb1hJf` | `BatchAsyncGenerateVideoStartImage` | `START_FRAME` | **Image-to-Video (I2V):** Tạo video động bắt đầu từ một khung hình gốc cố định. |
| `nprQif` | `BatchAsyncGenerateVideoStartAndEndImage` | `START_END_FRAMES` | **Interpolation Video:** Sinh video nội suy chuyển động mượt mà giữa khung hình đầu và khung hình cuối. |
| `jIps6` | `BatchAsyncGenerateVideoEditVideo` | `EDIT_VIDEO` | **Conversational Video Editing:** Sửa đổi video đã có (thay đổi góc quay, thời tiết, trang phục, hành động) theo prompt. |
| `fZytfe` | `BatchAsyncGenerateVideoExtendVideo` | `EXTEND_VIDEO` | **Video Length Extension:** Mở rộng độ dài của video hiện tại về phía trước hoặc phía sau. |
| `p0UkFb` | `BatchAsyncGenerateVideoUpsampleVideo` | `UPSAMPLE_VIDEO` | **Video Upsampling:** Nâng cấp độ phân giải video (từ 720p lên 1080p sắc nét). |

---

## 2. Quản Lý Tín Dụng & Hạn Mức (Credits & Quota)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Cấu Trúc Dữ Liệu Phản Hồi Thực Tế |
|---|---|---|---|
| `nzlxg` | `GetCredits` | Query (Za: true) | `[remaining_credits, tier, reset_status, flag, null, daily_limit, [timestamp_sec, nanos]]`<br>Ví dụ thực tế: `[58, 1, 2, 2, null, 58, [1793162716, 562000000]]` -> 58 tín dụng còn lại, chu kỳ đặt lại tương ứng timestamp. |

---

## 3. Quản Lý Chỉ Dẫn Hệ Thống & Persona (Preambles)

Preambles cho phép người dùng định nghĩa các "quy tắc chỉ đạo nghệ thuật" (style guide / camera rules / system instructions) được tự động nối vào prompt khi sinh:

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Chức Năng |
|---|---|---|---|
| `Yw72Rc` | `CreatePreamble` | Mutation (Za: false) | Tạo chỉ dẫn nghệ thuật / persona mới |
| `OqcWz` | `ListPreambles` | Query (Za: true) | Danh sách chỉ dẫn đã lưu |
| `JnpaK` | `UpdatePreamble` | Mutation (Za: false) | Sửa đổi nội dung chỉ dẫn |
| `x9P9ne` | `DeletePreamble` | Mutation (Za: false) | Xóa chỉ dẫn |

---

## 4. Cấu Hình Ứng Dụng & Trải Nghiệm Khởi Tạo (App Config & Onboarding)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Chức Năng |
|---|---|---|---|
| `cPZSdc` | `GetFlowAppConfig` | Query (Za: true) | Trả về phiên bản hệ thống (`2026-10-06-v0-nb21...`), danh sách Banner thông báo, khuyến mãi tặng 50 credits/ngày cho gói Google AI, link sự kiện workshop. |
| `rThb8d` | `CheckFlowAvailability` | Query (Za: true) | Kiểm tra tính khả dụng của dịch vụ tại vùng địa lý của người dùng. |
| `e97Odc` | `SetupStarterProjects` | Mutation (Za: false) | Khởi tạo các dự án mẫu (Starter templates) cho người dùng mới. |
| `QZasKb` | `GeneratePinholeGif` | Query (Za: true) | Tạo ảnh GIF động xem trước nhanh cho clip video trong Pinhole engine. |
| `BejPuf` | `LogMediaBookmark` | Mutation (Za: false) | Đánh dấu yêu thích phương tiện. |
| `okiZaf` | `DismissSiteContentIds` | Mutation (Za: false) | Ghi nhận người dùng đã đóng một biểu ngữ hoặc thông báo. |
| `gS5h8c` | `GetUserSettings` | Query (Za: true) | Lấy cấu hình VideoFx riêng biệt của người dùng. |
| `wX5DAe` | `UpdateUserSettings` | Mutation (Za: false) | Cập nhật cấu hình VideoFx. |
