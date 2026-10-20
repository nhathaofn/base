# Hạn Mức Tín Dụng, Quota & Phòng Ngừa Lạm Dụng (Quotas & Limits)

[STATUS: VERIFIED]
Tài liệu này ghi lại cơ chế phân bổ tín dụng (Credits), gói dịch vụ (Tiers), chu kỳ đặt lại (Reset Cycle) và kiểm soát tốc độ (Rate Limiting) của Google Flow.

---

## 1. Cấu Trúc Dữ Liệu Tín Dụng (Credits Schema)

Được giải mã từ RPC `nzlxg` (`/VideoFxService.GetCredits`):
```json
[
  58,
  1,
  2,
  2,
  null,
  58,
  [
    1793162716,
    562000000
  ]
]
```

### Ý Nghĩa Các Trường:
1. `remainingCredits` (`58`): Số lượng tín dụng Flow Credits khả dụng tại thời điểm kiểm tra.
2. `tierLevel` (`1`): Gói cước tài khoản (`1` = Google One AI Premium / Pro Tier).
3. `status` (`2`): Trạng thái tài khoản hoạt động bình thường.
4. `dailyQuota` (`58`): Hạn mức tín dụng được phân bổ theo ngày/tháng.
5. `resetTimestamp` (`[1793162716, 562000000]`): Thời điểm chính xác tín dụng sẽ được cấp mới hoặc đặt lại tự động theo chu kỳ (Epoch timestamp).

---

## 2. Chính Sách Ưu Đãi Gói Cước (Subscription Tiers)

Trích xuất từ biểu ngữ thông báo chính thức của hệ thống (`cPZSdc`):
- **Gói Google AI Plan (Google One AI Premium):**
  - Được tự động cộng thêm **50 Flow credits mỗi ngày** (`"Your Google AI plan now comes with 50 additional Flow credits daily."`).
  - Hỗ trợ mô hình cao cấp nhất: Veo 3.1 Quality, Gemini Omni Flash, Nano Banana 2.1.
- **Cảnh báo khi sắp hết hạn ngạch (Low Credit Warning Threshold):**
  - Khi số dư xuống thấp, giao diện hiển thị thanh thông báo màu vàng:
    `"Bạn sắp dùng hết tín dụng Google Flow. Tín dụng của bạn sẽ được đặt lại hằng tháng hoặc bạn có thể nạp tiền để nhận thêm ngay."`
  - Đi kèm liên kết mở trang nạp: `https://one.google.com/ai?utm_source=flow...`

---

## 3. Kiểm Soát Tần Suất & Phòng Chống Lạm Dụng (Rate Limiting)

Hệ thống bảo vệ hạ tầng điện toán đám mây bằng 3 lớp:
1. **Lớp Token Recaptcha Enterprise:**
   - Mỗi lệnh sinh bắt buộc phải có 1 token Recaptcha mới được sinh ra trong vòng vài giây gần nhất. Ngăn chặn triệt để việc viết script curl/python spam API mà không có trình duyệt tương tác thực tế.
2. **Lớp Giới Hạn Tác Vụ Đồng Thời (Concurrency Limit):**
   - Mỗi tài khoản chỉ được phép có tối đa một số lượng nhỏ các tác vụ render video chạy song song trong hàng đợi (Job Queue).
   - Khi vượt quá giới hạn, máy chủ trả về mã trạng thái bận hoặc yêu cầu chờ tác vụ trước đó hoàn tất.
3. **Lớp Kiểm Tra Điều Kiện Pháp Lý & Khu Vực (Compliance & Age Gate):**
   - Bắt buộc tài khoản Google đã xác minh trên 18 tuổi.
   - Kiểm tra IP khu vực địa lý qua RPC `rThb8d` (`CheckFlowAvailability`).
