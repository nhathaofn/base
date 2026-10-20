# Bản Kê Khai Mô Hình AI Đầy Đủ (AI Model Manifest Contract)

[STATUS: VERIFIED]
Bản kê khai này giải mã chi tiết toàn bộ **54 biến thể mô hình trí tuệ nhân tạo** được đăng ký và hỗ trợ trong Google Flow, trích xuất từ dữ liệu thực tế của `HTrJv` (`/FlowService.GetModels`) và `yBhWQ` (`/FlowService.ListModelStatuses`).

---

## 1. Họ Mô Hình Video Cao Cấp: Google Veo 3.1 & Veo 3

| Mã Mô Hình Nội Bộ | Nhãn Giao Diện | Chế Độ Hoạt Động (Mode) | Đặc Tính Kỹ Thuật & Khả Năng |
|---|---|---|---|
| `veo_3_1_quality` | Veo 3.1 - Quality | T2V, I2V | Mô hình video chất lượng cao nhất, độ chân thực vật lý và ánh sáng điện ảnh tối đa. |
| `veo_3_1_fast` | Veo 3.1 - Fast | T2V, I2V, Extension | Mô hình tối ưu hóa tốc độ sinh, phục vụ dựng cảnh nhanh (thời gian sinh ~6-10s). |
| `veo_3_1_lite` | Veo 3.1 - Lite | Preview | Mô hình siêu nhẹ phục vụ xem trước bản nháp thời gian thực trên timeline. |
| `veo_3_1_t2v_fast_4s_relaxed` | Veo 3.1 - Fast | Text-to-Video | Sinh video 4 giây từ câu lệnh văn bản. |
| `veo_3_1_t2v_fast_6s_relaxed` | Veo 3.1 - Fast | Text-to-Video | Sinh video 6 giây từ câu lệnh văn bản. |
| `veo_3_1_i2v_s_fast_6s_relaxed` | Veo 3.1 - Fast | Image-to-Video | Động hóa một bức ảnh tĩnh thành video 6 giây. |
| `veo_3_1_extend_fast_6s_relaxed`| Veo 3.1 - Fast | Video Extension | Mở rộng thêm 6 giây cho một đoạn video đã có, giữ nguyên chuyển động và bối cảnh. |
| `veo_3_1_r2v_fast_landscape_ultra_relaxed` | Veo 3.1 - Fast | Reference-to-Video | Tạo video khung hình ngang (16:9) tuân thủ ảnh nhân vật tham chiếu. |
| `veo_3_1_t2v_fast_portrait_ultra_relaxed` | Veo 3.1 - Fast | Text-to-Video | Tạo video khung hình dọc (9:16) chuẩn định dạng smartphone / mạng xã hội. |
| `veo_3_1_upsampler_1080p` | Veo 3.1 - Upsampler | Super Resolution | Nâng cấp video từ độ phân giải 720p lên 1080p Full HD với độ chi tiết cao. |

---

## 2. Họ Mô Hình Video Chuyên Dụng: Veo 2 & Reshoot Engine

| Mã Mô Hình Nội Bộ | Nhãn Giao Diện | Chức Năng Đột Phá |
|---|---|---|
| `veo_2_camera_control` | Veo 2 - Fast | **Điều khiển camera chuyển động:** Cho phép chỉ định góc quay: lia ngang (pan), trượt (truck), đẩy tới (push-in), bay lên (crane). |
| `veo_2_1_fast_d_15_with_start_image_and_end_image_interpolation` | Veo 2 - Quality | **Nội suy khung hình đầu và cuối (Interpolation):** Sinh chuyển động liền mạch giữa 2 ảnh bất kỳ. |
| `veo_3_0_reshoot_portrait` | Reshoot | **Quay lại phân cảnh (Reshoot):** Giữ nguyên hành động của nhân vật nhưng đổi góc máy hoặc đổi ánh sáng bối cảnh. |
| `veo_3_0_reshoot_landscape` | Reshoot | Quay lại phân cảnh với khung hình ngang 16:9. |
| `veo_2_0_object_removal_landscape` | Removal | **Xóa vật thể / Inpainting:** Tự động loại bỏ người hoặc đồ vật thừa trong video và vẽ bù bối cảnh phía sau. |
| `veo_2_0_object_removal_portrait` | Removal | Xóa vật thể trên video dọc 9:16. |
| `veo_2_1080p_upsampler_8s` | Veo 2 - Upsampler | Nâng cấp độ nét video độ dài 8 giây lên 1080p. |

---

## 3. Họ Mô Hình Tạo Ảnh: Nano Banana (Mã Nội Bộ: `Abra`)

- **Tên thương mại:** **Nano Banana 2.1** (hiển thị trên nút chọn mô hình: `🍌 Nano Banana 2.1`).
- **Mã nội bộ:** `abra` và `abra_r2v_10s`.
- **Năng lực cốt lõi:**
  1. Giữ độ nhất quán chủ thể (Subject consistency) vượt trội.
  2. Vẽ chữ và văn bản chính xác (Text rendering inside image).
  3. Khả năng suy luận chi tiết (Enhanced reasoning for complex prompts).
  4. Tạo video 10 giây từ ảnh tham chiếu: `abra_r2v_10s`.

---

## 4. Họ Mô Hình Tác Nhân & Đạo Diễn Ảo: Gemini Flash

- **Mã mô hình:** `gemini-3-flash-preview`
- **Nhiệm vụ:**
  - Điều khiển giao tiếp với người dùng qua tính năng "Tác nhân" (Agent).
  - Phân tích kịch bản, đề xuất cấu trúc phân cảnh (Storyboard planning).
  - Tự động sinh prompt tối ưu cho Veo và Nano Banana.
