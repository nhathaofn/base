# Phân Tích Dịch Vụ: FlowCreationAgentService (Agent Sáng Tạo & Đạo Diễn Ảo)

[STATUS: VERIFIED]
`FlowCreationAgentService` (`/google.internal.labs.aisandbox.proto.flow.agent.v1.FlowCreationAgentService`) cung cấp tác nhân thông minh (Creative Agent / Copilot) tích hợp trực tiếp trong Project Studio, hỗ trợ người dùng lên ý tưởng, viết prompt, điều chỉnh camera và ra lệnh chỉnh sửa video bằng ngôn ngữ tự nhiên.

---

## 1. Danh Mục Các Phương Thức RPC Đã Xác Minh

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Cơ Chế Hoạt Động |
|---|---|---|---|
| `csbIsb` | `CreateSession` | Mutation (Za: false) | Tạo một phiên trò chuyện mới với Agent trong dự án. |
| `GN0Bre` | `GetSession` | Query (Za: true) | Lấy toàn bộ lịch sử tin nhắn và trạng thái của một phiên trò chuyện. |
| `mrlkwd` | `ListSessions` | Query (Za: true) | Liệt kê các phiên Agent đang có trong dự án: `["{project_id}"]`. |
| `TunYMc` | `RenameSession` | Mutation (Za: false) | Đổi tên phiên trò chuyện. |
| `Dcn2Le` | `DeleteSession` | Mutation (Za: false) | Xóa một phiên Agent. |
| `xNyCid` | `StreamChat` | Mutation (Za: false, Streaming zU) | **Truyền dòng hội thoại thời gian thực (SSE):** Gửi prompt của người dùng và nhận câu trả lời dạng dòng từ Agent. |
| `Az898d` | `CancelTurn` | Mutation (Za: false) | **Hủy lượt trả lời:** Dừng ngay lập tức tác vụ suy luận hoặc sinh dở dang của Agent. |
| `P0WGvd` | `RecordSessionView` | Mutation (Za: false) | Ghi nhận sự kiện người dùng mở phiên làm việc để tính toán telemetry. |

---

## 2. Mô Hình Nền Tảng Bên Dưới (Underlying Model)

Được trích xuất trực tiếp từ mã nguồn thực thi của studio (`chunk_studio_1.js` dòng 3501456):
```javascript
a.ka.ha.Kd || "gemini-3-flash-preview"
```
Agent sử dụng **`gemini-3-flash-preview`** (phiên bản Flash thế hệ thứ 3 của Google Gemini) để tối ưu hóa tốc độ phản hồi và năng lực hiểu ngữ cảnh đa phương thức (hình ảnh, video, âm thanh) trong dự án.

---

## 3. Khả Năng Điều Khiển Studio Của Agent (Agent Tool Use / Function Calling)

Agent không chỉ trả lời câu hỏi mà còn có khả năng gọi các mutation nội bộ:
- Đề xuất thay đổi prompt của phân cảnh.
- Gợi ý thay đổi góc quay camera (`veo_2_camera_control`).
- Kích hoạt sinh phân cảnh mới (`CreateScene` + `GenerateVideo`).
- Điều chỉnh tỉ lệ khung hình (16:9, 9:16) phù hợp với kịch bản.
