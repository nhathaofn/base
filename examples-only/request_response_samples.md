# Dữ Liệu Mẫu Minh Họa (Examples & Request/Response Samples)

[CHÚ Ý: TÀI LIỆU NÀY CHỈ CHỨA DỮ LIỆU MẪU MINH HỌA - KHÔNG PHẢI TÀI LIỆU CHUẨN XÁC MINH]

Tài liệu này lưu trữ các mẫu cấu trúc request/response giả định để các lập trình viên hình dung cách đóng gói dữ liệu mà không làm sai lệch tài liệu chuẩn trong `verified/`.

---

## 1. Mẫu Gửi Lệnh Lấy Danh Sách Dự Án (`GetProjects` - `UpteDb`)

### Request Payload (`f.req` URL-decoded):
```json
[
  [
    [
      "UpteDb",
      "[\"projects/*\", 21, null, null, null, null, [1]]",
      null,
      "generic"
    ]
  ]
]
```

### Response Payload (`wrb.fr` decoded):
```json
[
  [
    [
      "sample-project-uuid-1111-2222-3333",
      [
        "Demo Project Video",
        null,
        [1791882476, 407749000],
        "https://lh3.googleusercontent.com/asb/EXAMPLE_HASH=s1600-rw",
        "sample-asset-uuid-4444",
        ["https://lh3.googleusercontent.com/asb/EXAMPLE_HASH=s1600-rw"]
      ]
    ]
  ]
]
```

---

## 2. Mẫu Gửi Lệnh Sinh Video Văn Bản (`BatchAsyncGenerateVideoText` - `YhhmEf`)

### Request Payload (`f.req` URL-decoded):
```json
[
  [
    [
      "YhhmEf",
      "[null, [[[null, \"Cinematic drone shot of sunset over mountains\", null, null, null, null, null, null, 1, 3], null, 1]], 1, null, \"RECAPTCHA_TOKEN_STRING\"]",
      null,
      "generic"
    ]
  ]
]
```

### Response Payload:
```json
[
  "TASK_UUID_EXAMPLE_9999",
  1,
  [1792489000, 0]
]
```

---

## 3. Mẫu Thăm Dò Trạng Thái Video (`RunVideoFxCheckConcatenationStatus` - `IxdSwd`)

### Request:
```json
[
  [
    [
      "IxdSwd",
      "[\"TASK_UUID_EXAMPLE_9999\"]",
      null,
      "generic"
    ]
  ]
]
```

### Response (Trạng thái đang xử lý):
```json
[
  2,
  null,
  null
]
```

### Response (Trạng thái thành công):
```json
[
  3,
  null,
  null,
  null,
  null,
  "https://lh3.googleusercontent.com/asb/FINAL_VIDEO_HASH.mp4"
]
```
