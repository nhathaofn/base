# Phân Tích Dịch Vụ: FlowLikenessService (Huấn Luyện Nhân Vật Nhất Quán)

[STATUS: VERIFIED]
`FlowLikenessService` là dịch vụ chuyên biệt cung cấp tính năng **Nhân vật nhất quán (Character Consistency)** trong Google Flow. Tính năng này cho phép nhà sáng tạo đăng ký diện mạo khuôn mặt hoặc hình thể của một diễn viên/nhân vật và giữ nguyên diện mạo đó trên toàn bộ các cảnh quay video khác nhau.

---

## 1. Danh Mục Các Phương Thức RPC Đã Xác Minh

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Cơ Chế |
|---|---|---|---|
| `ve2Lsc` | `CheckUserLikenessEligibility` | Query (Za: true) | **Kiểm tra điều kiện tài khoản:** Xác minh xem người dùng có đủ điều kiện pháp lý, độ tuổi (18+) và gói cước (Google One AI / Pro) để sử dụng tính năng tạo nhân vật hay không. |
| `DTaVef` | `ListUserLikenesses` | Query (Za: true) | Danh sách các nhân vật (Likeness profiles) mà người dùng đã huấn luyện và lưu trữ. |
| `T3Zezf` | `GetLikenessRegistrationUrl` | Query (Za: true) | Sinh URL bảo mật để tải lên video hoặc ảnh chụp góc cạnh khuôn mặt phục vụ huấn luyện (Onboarding/Registration flow). |
| `lv2lXd` | `GetLikenessRegistrationStatus` | Query (Za: true) | Kiểm tra tiến độ xử lý và trạng thái sẵn sàng của mô hình nhân vật đang huấn luyện. |
| `KaLHHf` | `DeleteUserLikeness` | Mutation (Za: false) | Xóa bỏ vĩnh viễn dữ liệu nhận diện khuôn mặt / nhân vật khỏi máy chủ theo chính sách quyền riêng tư. |

---

## 2. Ý Nghĩa Trong Pipeline Tạo Video

Khi người dùng chọn một nhân vật đã đăng ký:
1. `Likeness ID` được đính kèm vào mảng tham chiếu `references` của RPC tạo video (ví dụ: `MZZa6b` - Reference Images).
2. Mô hình Veo sử dụng bộ vector nhúng (embedding) của nhân vật để khóa các đặc trưng nhận diện (mắt, mũi, tỉ lệ khuôn mặt, tóc) trong quá trình khuếch tán (diffusion process), ngăn chặn hiện tượng méo mặt (face morphing) khi quay các góc phức tạp.
