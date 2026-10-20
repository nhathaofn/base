# Hợp Đồng Dữ Liệu: Dự Án (Project Contract)

[STATUS: VERIFIED]
Hợp đồng dữ liệu của đối tượng **Project** được giải mã trực tiếp từ payload phản hồi của `UpteDb` (`/FlowService.GetProjects`) và `ngNC2` (`/AiSandbox.GetProject`).

---

## 1. Cấu Trúc Đối Tượng Mảng JSON (Wire Format)

Trong giao thức Protobuf-over-JSON của Google Boq, một Dự Án được đại diện bằng một mảng có thứ tự:

```json
[
  "PROJECT_UUID",
  [
    "PROJECT_TITLE",
    "OPTIONAL_DESCRIPTION_OR_TAG",
    [
      "UPDATED_TIMESTAMP_SECONDS",
      "UPDATED_TIMESTAMP_NANOS"
    ],
    "PRIMARY_THUMBNAIL_URL",
    "PRIMARY_ASSET_ID",
    [
      "ASSET_URL_1",
      "ASSET_URL_2"
    ]
  ]
]
```

### Chi Tiết Từng Thuộc Tính:

| Chỉ Mục (Index) | Tên Trường | Kiểu Dữ Liệu | Phân Loại Giá Trị | Ý Nghĩa / Quy Tắc |
|---|---|---|---|---|
| `[0]` | `projectId` | String (UUIDv4) | Server-generated | Định danh duy nhất toàn cục của dự án (ví dụ: `22d33fe3-5afe-4106-8913-dc66336677f8`). |
| `[1][0]` | `title` | String | Dynamic (User input) | Tên hiển thị của dự án (mặc định lấy theo ngày giờ tạo: `Tháng 10 13 - 16:07`). |
| `[1][1]` | `description` | String / Null | Dynamic | Mô tả chi tiết hoặc ghi chú của dự án. |
| `[1][2][0]` | `updatedAtSeconds` | Integer (Epoch sec) | Server-generated | Mốc thời gian cập nhật gần nhất tính bằng giây Unix epoch (ví dụ: `1791882476`). |
| `[1][2][1]` | `updatedAtNanos` | Integer | Server-generated | Phần nano giây của thời gian cập nhật. |
| `[1][3]` | `thumbnailUrl` | String (URL) | Derived / Server-generated | URL hình ảnh đại diện hiển thị trên trang chủ (`https://lh3.googleusercontent.com/asb/...=s1600-rw`). |
| `[1][4]` | `primaryAssetId` | String (UUIDv4) | Server-generated | ID của tệp tài sản (ảnh hoặc video) được chọn làm ảnh bìa chính. |
| `[1][5]` | `assetUrls` | Array<String> | Derived | Mảng chứa danh sách URL xem trước của các phân cảnh con trong dự án. |

---

## 2. Định Danh Đường Dẫn Tài Nguyên (Resource Name)

Khi truy vấn chi tiết qua `ngNC2` (`AiSandbox.GetProject`):
- Đường dẫn định danh: `tools/{toolId}/projects/{projectId}`
- Ví dụ thực tế: `tools/PINHOLE/projects/22d33fe3-5afe-4106-8913-dc66336677f8`
- `toolId`: Mặc định là `"PINHOLE"`. Đối với các dự án tạo bằng Custom Tool, `toolId` là UUID của Applet tương ứng.
