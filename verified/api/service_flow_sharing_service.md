# Phân Tích Dịch Vụ: FlowSharingService (Chia Sẻ & Cộng Tác)

[STATUS: VERIFIED]
`FlowSharingService` chịu trách nhiệm tạo liên kết chia sẻ công khai, quản lý quyền truy cập và đồng bộ hóa các dự án Google Flow giữa nhiều người dùng.

---

## 1. Danh Mục Các Phương Thức RPC Đã Xác Minh

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Cơ Chế |
|---|---|---|---|
| `uhRpkc` | `ShareProject` | Mutation (Za: false) | **Xuất bản dự án:** Sinh liên kết chia sẻ (`/shared/project/{share_id}`), cấp quyền chỉ xem (View-only) hoặc cho phép nhân bản (Clone/Remix). |
| `Qrv5xc` | `GetSharedProjects` | Query (Za: true) | Liệt kê danh sách các dự án mà tài khoản này đã chia sẻ ra ngoài hoặc được người khác chia sẻ cho. |
| `syFRRe` | `GetProjectDetails` | Query (Za: true) | Đọc thông tin công khai của dự án chia sẻ (tên, tác giả, mô tả, danh sách phân cảnh) khi truy cập qua liên kết không cần đăng nhập hoặc bằng tài khoản khác. |

---

## 2. Quy Trình Chia Sẻ & Remix Dự Án

```
[Chủ Dự Án] -> ShareProject (uhRpkc) -> Sinh Share ID
                                                │
                                                ▼
[Người Nhận] <- GetProjectDetails (syFRRe) <- Mở liên kết /shared/...
                                                │
                                                ▼
                                   Nhấn nút "Remix / Clone"
                                                │
                                                ▼
                                       CreateProject (jHPbke)
                                       + CopyWorkflow (XKxtXb)
```
Dự án được sao chép hoàn toàn độc lập vào tài khoản của người nhận, đảm bảo không ảnh hưởng đến bản gốc của tác giả ban đầu.
