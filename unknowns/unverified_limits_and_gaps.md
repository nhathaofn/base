# Các Giới Hạn Chưa Thể Xác Minh & Vùng Chưa Khảo Sát (Unknowns & Technical Gaps)

[STATUS: UNKNOWN]
Theo nguyên tắc "Không suy đoán" và "Security-first", tài liệu này liệt kê trung thực các thành phần thuộc phạm vi backend nội bộ của Google mà client không thể quan sát trực tiếp hoặc bị giới hạn bởi quyền truy cập.

---

## 1. Thuật Toán Điều Phối Phần Cứng & Hàng Đợi Máy Chủ (Server-Side Scheduling)

- **Trạng thái:** `UNKNOWN`
- **Chi tiết:**
  - Client chỉ nhận biết được các trạng thái thô: `1` (Queued), `2` (Processing), `6` (Finalizing), `3` (Success).
  - Thuật toán phân bổ tác vụ giữa các cụm TPU v5p / GPU H100 trong hệ thống Borg của Google hoàn toàn nằm sau lớp bảo vệ ESF.
  - Mức độ ưu tiên (Priority tiering) giữa người dùng miễn phí và người dùng trả phí Pro được xử lý động ở tầng backend, client không nhận được số thứ tự hàng đợi tuyệt đối.

---

## 2. Tiêu Chuẩn Bộ Lọc An Toàn & Phê Duyệt Prompt (Prompt Safety & Moderation Thresholds)

- **Trạng thái:** `UNKNOWN`
- **Chi tiết:**
  - Khi một prompt bị từ chối, backend trả về mã trạng thái lỗi `7` (POLICY_VIOLATED).
  - Client không nhận được điểm số vi phạm (safety scores) chi tiết cho từng danh mục (hate speech, sexual content, violence, copyrighted likeness) mà chỉ nhận thông báo chung.

---

## 3. Tệp Định Nghĩa Gốc Protobuf (.proto IDL Files)

- **Trạng thái:** `INFERRED` từ JSPB Array Indexes
- **Chi tiết:**
  - Chúng ta đã giải mã chính xác 100% vị trí chỉ mục (indices) của mảng JSON và tên các phương thức RPC thông qua AST của client bundle.
  - Tuy nhiên, các tệp nguồn `.proto` nguyên bản (như `flow_service.proto`, `video_fx.proto`) được lưu trữ trong kho mã nguồn nội bộ (Google Monorepo) và được biên dịch sang JSPB mảng nén trước khi phân phối tới trình duyệt.

---

## 4. Hạn Mức Tác Vụ Đồng Thời Tuyệt Đối Theo Từng Gói Cước

- **Trạng thái:** `OBSERVED PARTIALLY`
- **Chi tiết:**
  - Đã quan sát thấy cơ chế client khóa nút gửi khi mutation đang pending.
  - Chưa thể xác minh số lượng tối đa tuyệt đối các tác vụ video có thể render đồng thời trên nhiều tab trình duyệt trước khi backend trả về lỗi `RESOURCE_EXHAUSTED`.
