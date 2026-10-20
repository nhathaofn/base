# Hợp Đồng Dữ Liệu: Quy Trình Sinh Nội Dung (Workflow Contract)

[STATUS: VERIFIED]
Hợp đồng dữ liệu của đối tượng **Workflow** được trích xuất trực tiếp từ phản hồi của `Zzl0ze` (`contents[2]`). Đây là thực thể quan trọng nhất lưu trữ đầy đủ thông số tái lập (Reproducibility parameters) của một tác vụ sinh AI.

---

## 1. Cấu Trúc Đối Tượng Mảng JSON (Wire Format)

```json
[
  "WORKFLOW_UUID",
  "PROJECT_UUID",
  "SCENE_UUID",
  null,
  null,
  [
    [
      "CREATED_TIMESTAMP_SECONDS",
      "CREATED_TIMESTAMP_NANOS"
    ],
    null,
    null,
    null,
    null,
    "MEDIA_OUTPUT_URL",
    [
      null,
      [
        [
          "MODEL_ID",
          "MODE_ENUM",
          [
            "ASPECT_RATIO_ENUM"
          ],
          null,
          "COUNT_INT",
          "FLAG_INT"
        ],
        [
          [
            null,
            "REF_TYPE_INT",
            "REFERENCE_ASSET_UUID"
          ]
        ]
      ],
      [
        [
          null,
          null,
          [
            [
              [
                "PROMPT_TEXT_STRING"
              ]
            ]
          ]
        ]
      ],
      null,
      1
    ],
    null,
    [
      "RESOLUTION_OR_FORMAT_ENUM"
    ],
    "STATUS_ENUM",
    "MEDIA_OUTPUT_URL_MIRROR",
    null,
    null,
    "FILE_SIZE_BYTES_INT"
  ]
]
```

---

## 2. Bảng Ánh Xạ Thuộc Tính Chi Tiết

| Vị Trí Chỉ Mục | Tên Trường | Kiểu Dữ Liệu | Ví Dụ Thực Tế | Ý Nghĩa Kỹ Thuật |
|---|---|---|---|---|
| `[0]` | `workflowId` | UUIDv4 | `"0b01ebbb-f01d-4c66-a735-5aa6c2ff961f"` | Định danh duy nhất của lượt sinh |
| `[1]` | `projectId` | UUIDv4 | `"22d33fe3-5afe-4106-8913-dc66336677f8"` | Định danh dự án chứa lượt sinh |
| `[2]` | `sceneId` | UUIDv4 | `"8c52f1bf-1298-4a48-a70f-a8d5ec738175"` | Định danh phân cảnh liên kết |
| `[5][0][0]` | `timestamp` | Epoch Sec | `1791882939` | Thời điểm bắt đầu chạy lượt sinh |
| `[5][5]` | `outputMediaUrl` | URL String | `"https://lh3.googleusercontent.com/asb/ANqv..."` | Đường dẫn tệp video/ảnh thành phẩm |
| `[5][6][1][0][0]` | `modelId` | String | `"abra_r2v_10s"` | Mã định danh mô hình (Abra R2V 10s) |
| `[5][6][1][0][2][0]` | `aspectRatio` | Enum Int | `5` | Mã tỉ lệ: `5` = Dọc 9:16 (Vertical) |
| `[5][6][1][1][0][2]` | `referenceAssetId` | UUIDv4 | `"ab123739-eaaf-4b2f-aa71-231027ef37ee"` | ID tệp ảnh/video được làm mốc tham chiếu |
| `[5][6][2][0][2][0][0][0]` | `prompt` | String | `"Create a highly realistic vertical 9:16 smartphone video..."` | Nội dung câu lệnh điều khiển sinh |
| `[5][9]` | `status` | Enum Int | `1` | Trạng thái: `1` = Hoàn thành thành công |
| `[5][13]` | `fileSizeBytes` | Integer | `4004167` | Dung lượng tệp video (khoảng ~4MB) |
| `[7][1][2][0]` | `durationSeconds` | Integer | `10` | Thời lượng video xuất ra (10 giây) |

---

## 3. Các Giá Trị Enum Đã Xác Minh

### A. Tỉ Lệ Khung Hình (Aspect Ratio Enum)
- `1`: Vuông 1:1 (`crop_square`)
- `3`: Ngang 16:9 (`crop_16_9`)
- `5`: Dọc 9:16 (`crop_portrait` / `crop_9_16`)

### B. Thời Lượng Video (Duration Enum)
- `4`: 4 giây (Veo 3.1 Fast 4s)
- `6`: 6 giây (Veo 3.1 Fast 6s)
- `10`: 10 giây (Abra R2V 10s)
