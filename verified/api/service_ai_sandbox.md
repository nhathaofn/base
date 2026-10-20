# Phân Tích Dịch Vụ: AiSandbox (28 Methods)

[STATUS: VERIFIED]
`AiSandbox` là dịch vụ kế thừa và tầng dữ liệu thực thể cơ bản (Data Abstraction Layer) của Google Labs, quản lý metadata của Projects, Scenes, Workflows, cùng các tác vụ nối video (Concatenation) và sở thích người dùng.

---

## 1. Quản Trị Dự Án & Định Danh Tài Nguyên (Resource Hierarchy)

Google Flow tổ chức tài nguyên theo cấu trúc phân cấp đường dẫn:
```
tools/{tool_id}/projects/{project_id}
```
(Trong đó `tool_id` mặc định là `"PINHOLE"` - engine cốt lõi của Google Flow).

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Schema Đầu Vào |
|---|---|---|---|
| `jHPbke` | `CreateProject` | Mutation (Za: false) | Tạo dự án mới. Trả về UUID của dự án. |
| `ngNC2` | `GetProject` | Query (Za: true) | Lấy chi tiết dự án theo resource path: `["tools/PINHOLE/projects/{uuid}"]` |
| `QI2zvc` | `DeleteProject` | Mutation (Za: false) | Xóa dự án (chuyển vào thùng rác hoặc xóa vĩnh viễn) |
| `o8DA4` | `UpdateProjectInfo` | Mutation (Za: false) | Cập nhật tên dự án, ảnh bìa thumbnail, mô tả |
| `OylIJd` | `SearchUserProjects` | Query (Za: true) | Tìm kiếm dự án của người dùng theo từ khóa |

---

## 2. Quản Trị Phân Cảnh (Scene Hierarchy)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Chức Năng |
|---|---|---|---|
| `dpwTMe` | `CreateScene` | Mutation (Za: false) | Tạo phân cảnh mới thuộc về dự án |
| `X1yU8` | `GetScene` | Query (Za: true) | Lấy dữ liệu phân cảnh |
| `bk2bVd` | `UpdateScene` | Mutation (Za: false) | Cập nhật thông số cảnh |
| `Adnnof` | `DeleteScene` | Mutation (Za: false) | Xóa phân cảnh |
| `GI4k8` | `SearchProjectScenes` | Query (Za: true) | Tìm kiếm các cảnh trong một dự án |

---

## 3. Quản Trị Quy Trình & Luồng Công Việc (Workflows)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Chức Năng |
|---|---|---|---|
| `e1OaUd` | `GetWorkflow` | Query (Za: true) | Đọc chi tiết quy trình |
| `SIzNd` | `SearchProjectWorkflows` | Query (Za: true) | Tìm kiếm workflow trong dự án |
| `aZDXX` | `SearchUserWorkflows` | Query (Za: true) | Tìm kiếm workflow của người dùng trên toàn hệ thống |

---

## 4. Ghép Nối Video & Xử Lý Bất Đồng Bộ (Video Concatenation Engine)

Đây là cơ chế quan trọng giúp ghép nhiều phân cảnh (scenes) thành một video liền mạch hoàn chỉnh:
- **Khởi động ghép nối:**
  - RPC: `GjQLTd` (`/AiSandbox.RunVideoFxConcatenation`)
  - Gửi danh sách các đoạn video cần ghép. Trả về mã định danh tác vụ ghép `concatenation_job_id`.
- **Thăm dò trạng thái (Polling):**
  - RPC: `IxdSwd` (`/AiSandbox.RunVideoFxCheckConcatenationStatus`)
  - Vòng lặp tối đa 40 lần, chu kỳ 3000ms.
  - Khi hoàn tất (Status 3), trả về mảng byte hoặc URL tệp MP4 đã xuất xưởng.

---

## 5. Tùy Chọn & Trạng Thái Tài Khoản (User Preferences & Flags)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Schema Dữ Liệu |
|---|---|---|---|
| `xI9TVb` | `GetUserPreferences` | Query (Za: true) | `["userPreferences/"]` -> Trả về `[true, null, true]` (các cờ thông báo, tips, preview) |
| `mu42vc` | `UpdateUserPreferences` | Mutation (Za: false) | Cập nhật tùy chọn người dùng |
| `NfrxTb` | `CheckUserAcknowledgement` | Query (Za: true) | Kiểm tra người dùng đã đồng ý điều khoản tính năng chưa (e.g. `[16]`, `[17]`, `[null, 22]`) -> Trả về `[true]` |
| `JJH6Ub` | `AddUserAcknowledgement` | Mutation (Za: false) | Ghi nhận người dùng đã chấp thuận điều khoản / thông báo |
| `KV2T2d` | `CheckToolAvailability` | Query (Za: true) | Kiểm tra quyền truy cập các công cụ AI (e.g. `[22]` -> `[1]`) |
| `cO7JOb` | `CheckAppAvailability` | Query (Za: true) | Kiểm tra ứng dụng có khả dụng với tài khoản không |
| `pmmFvb` | `AddUserRegistration` | Mutation (Za: false) | Đăng ký tài khoản vào hệ thống Labs Sandbox |
| `s6Qwyc` | `UpdateUserRetentionNotificationCount` | Mutation (Za: false) | Đếm số lần hiển thị thông báo giữ chân người dùng |
| `DviW9c` | `GetUserVideoCreditStatusAction` | Query (Za: true) | Kiểm tra trạng thái gói tín dụng video chi tiết |
| `LPzVkd` | `FetchUserRecommendations` | Query (Za: true) | Gợi ý prompt, công cụ hoặc nội dung theo sở thích cá nhân |
| `Uhba0c` | `GetMedia` | Query (Za: true) | Đọc tệp media qua tầng Sandbox |
