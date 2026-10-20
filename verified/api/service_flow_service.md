# Phân Tích Dịch Vụ Cốt Lõi: FlowService (69 Methods)

[STATUS: VERIFIED]
`FlowService` (`/google.internal.labs.aisandbox.proto.flow.v1.FlowService`) là dịch vụ trung tâm chịu trách nhiệm cho các năng lực trí tuệ nhân tạo tạo sinh (Generative AI), quản lý bảng vẽ (Canvas/Studio), phân cảnh (Scenes), quy trình (Workflows) và tài sản đa phương tiện.

---

## 1. Nhóm Hàm Sinh Nội Dung Video (Video Generation)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Cơ Chế Thực Thi |
|---|---|---|---|
| `L2jnw` | `StreamGenerateContent` | Mutation (Za: false, Streaming zU) | Sinh video dạng truyền dòng (Streamed token/progress) |
| `agJzFb` | `GenerateContent` | Mutation (Za: false) | Sinh video / nội dung đồng bộ |
| `CK0Pk` | `CancelMediaGeneration` | Mutation (Za: false) | Hủy bỏ tác vụ sinh video đang chạy trong hàng đợi |
| `iVqlKd` | `UpdateVideoOffset` | Mutation (Za: false) | Cập nhật mốc thời gian bắt đầu/kết thúc (Trim/Offset) |
| `a3UfBf` | `UploadVideo` | Mutation (Za: false) | Đăng ký metadata video sau khi upload qua Scotty |

---

## 2. Nhóm Hàm Sinh & Chỉnh Sửa Hình Ảnh (Image Generation & Manipulation)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Cơ Chế Thực Thi |
|---|---|---|---|
| `ogiZ0b` | `BatchGenerateImages` | Mutation (Za: false) | Sinh ảnh đồng bộ theo mẻ sử dụng mô hình Nano Banana (Abra) |
| `Z9cAtf` | `BatchAsyncGenerateImages` | Mutation (Za: false) | Gửi tác vụ sinh ảnh bất đồng bộ vào hàng đợi máy chủ |
| `sAVZzc` | `TransformImage` | Mutation (Za: false) | Chỉnh sửa, biến đổi ảnh (Image-to-Image transformation) |
| `SPrCad` | `UpsampleImage` | Mutation (Za: false) | Nâng cấp độ phân giải hình ảnh lên độ nét cao (Super-Resolution) |
| `maseQ` | `UploadImage` | Mutation (Za: false) | Đăng ký ảnh tải lên từ máy người dùng |

---

## 3. Nhóm Hàm Sinh Âm Thanh & Giọng Đọc (Audio & Voice)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Cơ Chế Thực Thi |
|---|---|---|---|
| `no0P6` | `BatchGenerateAudio` | Mutation (Za: false) | Sinh âm thanh, nhạc nền hoặc lồng tiếng theo mẻ |
| `epopJ` | `UploadGeneratedAudio` | Mutation (Za: false) | Tải lên và lưu trữ đoạn âm thanh đã sinh |

---

## 4. Nhóm Hàm Quản Lý Dự Án, Cảnh & Quy Trình (Studio Project Structure)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Cơ Chế Thực Thi |
|---|---|---|---|
| `Zzl0ze` | `GetProjectContents` | Query (Za: true) | **Tải toàn bộ nội dung dự án:** Danh sách Scenes, Workflows, Media Assets |
| `UpteDb` | `GetProjects` | Query (Za: true) | Danh sách dự án tóm tắt trên trang chủ |
| `Hnrtob` | `GetProject` | Query (Za: true) | Lấy chi tiết một dự án theo Project ID |
| `okjlg` | `ListProjects` | Query (Za: true) | Liệt kê dự án có phân trang |
| `uRk1o` | `BatchGetProjects` | Query (Za: true) | Lấy thông tin nhiều dự án cùng lúc |
| `rqZuUc` | `CreateScene` | Mutation (Za: false) | Tạo phân cảnh mới trong dự án |
| `O12LBf` | `GetScene` | Query (Za: true) | Lấy dữ liệu chi tiết một cảnh |
| `Xffewf` | `ListScenes` | Query (Za: true) | Danh sách cảnh trong dự án |
| `jtGUlf` | `BatchGetScenes` | Query (Za: true) | Lấy thông tin nhiều cảnh theo mẻ |
| `BpMsoe` | `UpdateScene` | Mutation (Za: false) | Cập nhật thông tin phân cảnh (tiêu đề, thứ tự) |
| `H5ewbd` | `UpdateScenes` | Mutation (Za: false) | Cập nhật nhiều cảnh đồng thời |
| `BLIwAb` | `BatchDeleteScenes` | Mutation (Za: false) | Xóa hàng loạt phân cảnh |
| `OSd63c` | `CopyScene` | Mutation (Za: false) | Sao chép nhân bản một cảnh |
| `L91dPd` | `GetWorkflow` | Query (Za: true) | Lấy chi tiết quy trình sinh (Prompt, Model, Params) |
| `kGwJ9b` | `ListWorkflows` | Query (Za: true) | Danh sách quy trình trong dự án |
| `LWkPYd` | `ListUserWorkflows` | Query (Za: true) | Danh sách quy trình của người dùng |
| `kDiqOe` | `GetSceneWorkflow` | Query (Za: true) | Lấy quy trình gắn liền với cảnh cụ thể |
| `ncZTKe` | `ListSceneWorkflows` | Query (Za: true) | Danh sách quy trình của cảnh |
| `yfXKib` | `BatchGetSceneWorkflows` | Query (Za: true) | Lấy nhiều quy trình cảnh theo mẻ |
| `mYWVGd` | `UpdateWorkflow` | Mutation (Za: false) | Cập nhật thông số quy trình sinh |
| `pGCYOe` | `BatchUpdateWorkflows` | Mutation (Za: false) | Cập nhật nhiều quy trình cùng lúc |
| `XKxtXb` | `CopyWorkflow` | Mutation (Za: false) | Sao chép quy trình |
| `oWTRd` | `AddWorkflowsToScene` | Mutation (Za: false) | Gán quy trình sinh vào phân cảnh |

---

## 5. Nhóm Hàm Quản Lý Mô Hình AI (AI Model Catalog)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Cơ Chế Thực Thi |
|---|---|---|---|
| `HTrJv` | `GetModels` | Query (Za: true) | **Danh mục 54 biến thể mô hình:** Veo 3.1, Veo 3, Abra (Nano Banana), Omni, Upsamplers |
| `yBhWQ` | `ListModelStatuses` | Query (Za: true) | Trạng thái sẵn sàng và độ khả dụng thời gian thực của từng mô hình |

---

## 6. Nhóm Hàm Quản Lý Tài Sản & Phương Tiện (Media & Assets)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Cơ Chế Thực Thi |
|---|---|---|---|
| `as29s` | `GetMedia` | Query (Za: true) | Lấy metadata của tệp phương tiện |
| `Iyc41d` | `BatchGetMedia` | Query (Za: true) | Lấy metadata nhiều phương tiện theo mẻ |
| `bOKtO` | `ListMedia` | Query (Za: true) | Danh sách phương tiện trong dự án |
| `HU68fc` | `GetMediaServingUrl` | Query (Za: true) | Lấy URL CDN công khai để hiển thị (`lh3.googleusercontent.com/asb/...`) |
| `uurnC` | `GetMediaUrl` | Query (Za: true) | Lấy URL tải xuống gốc có chữ ký thời hạn |
| `GLc8O` | `BatchEnrichMedia` | Mutation (Za: false) | Làm giàu dữ liệu phương tiện (Metadata AI tagging) |
| `cz8Z4b` | `BatchDeleteAssets` | Mutation (Za: false) | Xóa hàng loạt tệp tài sản |
| `Sc7aEb` | `CopyProjectMedia` | Mutation (Za: false) | Sao chép tài sản sang dự án khác |
| `J2mwWb` | `ShareMedia` | Mutation (Za: false) | Tạo liên kết chia sẻ tài sản |
| `BLuntc` | `UnshareMedia` | Mutation (Za: false) | Thu hồi liên kết chia sẻ |
| `cMxpTd` | `GetSharedMedia` | Query (Za: true) | Xem tài sản được chia sẻ |
| `pmaQ3b` | `ImportSharedMedia` | Mutation (Za: false) | Nhập tài sản chia sẻ vào dự án hiện tại |

---

## 7. Nhóm Hàm Bộ Sưu Tập (Collections)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Cơ Chế Thực Thi |
|---|---|---|---|
| `Uxbujd` | `CreateCollection` | Mutation (Za: false) | Tạo thư mục bộ sưu tập mới |
| `QiuWMe` | `GetCollection` | Query (Za: true) | Lấy thông tin bộ sưu tập |
| `rEhmZd` | `ListCollections` | Query (Za: true) | Liệt kê các bộ sưu tập của người dùng |
| `O2COMe` | `UpdateCollection` | Mutation (Za: false) | Đổi tên hoặc chỉnh sửa bộ sưu tập |
| `kVdhHf` | `BatchMoveToCollection` | Mutation (Za: false) | Chuyển hàng loạt tài sản vào bộ sưu tập |

---

## 8. Nhóm Hàm Người Dùng & Quản Trị Doanh Nghiệp (User & Enterprise)

| RPC ID | Tên Hàm Protobuf | Kiểu (Za) | Vai Trò & Cơ Chế Thực Thi |
|---|---|---|---|
| `Yizz8d` | `GetUserSettings` | Query (Za: true) | Lấy cài đặt tài khoản và tính năng kích hoạt (`["MODEL", "AGENT"]`) |
| `DA4VGb` | `UpdateUserSettings` | Mutation (Za: false) | Cập nhật tùy chọn cá nhân |
| `m1QyH` | `InitializeFlowEnterprise` | Mutation (Za: false) | Khởi tạo môi trường doanh nghiệp (Google Cloud Enterprise Project) |
| `Dp1eae` | `CheckUserCloudPermission` | Query (Za: true) | Kiểm tra quyền truy cập Google Cloud Project liên kết |
| `Mf1z1c` | `ListUserFlowEnterpriseCloudProjects` | Query (Za: true) | Danh sách dự án Cloud liên kết của tài khoản doanh nghiệp |
| `QLXvEd` | `GetG1Interventions` | Query (Za: true) | Kiểm tra ưu đãi gói Google One AI Premium |
| `yvJRsc` | `GrantG1Incentive` | Mutation (Za: false) | Nhận ưu đãi tín dụng Google One |
| `RaYiHf` | `RecordG1InterventionInteraction` | Mutation (Za: false) | Ghi nhận tương tác biểu ngữ Google One |
| `WuwhI` | `BatchLogFrontendEvents` | Mutation (Za: false) | Gửi nhật ký sự kiện client về server |
