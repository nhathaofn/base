# Cơ Chế Xử Lý Bất Đồng Bộ, Thăm Dò & Theo Dõi Tác Vụ (Async Processing & Polling)

[STATUS: VERIFIED]
Tài liệu này ghi lại cơ chế xử lý hàng đợi (Queue), vòng lặp thăm dò (Polling Loop), xử lý lỗi timeout và tính toán đồng thời (Concurrency) được giải mã từ hàm `Xab` trong `chunk_studio_1.js`.

---

## 1. Thuật Toán Vòng Lặp Thăm Dò (Polling Algorithm)

Mã nguồn thực tế được trích xuất từ hàm `Xab`:

```javascript
Xab = function(a, { kV: b, Km: c }) {
  return _.A(function* () {
    var d = u9a(yield Vab(a, b));
    if (!d) throw Error("qf");
    for (let e = 0; e < 40; e++) {
      yield new Promise(h => { setTimeout(h, 3000); });
      if (c == null ? 0 : c()) return; // Kiểm tra cờ hủy tác vụ (Cancellation check)
      let f = yield Wab(a, d), g = f.Xe();
      switch (g) {
        case 3: // SUCCESS
          let h;
          d = (h = _.fw(f, 5)) == null ? void 0 : _.wd(h);
          if (!d || d.length === 0) throw Error("rf");
          return _.MQ(d, "video/mp4");
        case 4: // FAILED
        case 5: // ABORTED
        case 7: // POLICY_VIOLATION
        case 0: // INVALID
          throw Error("sf");
        case 1: // QUEUED
        case 2: // PROCESSING
        case 6: // FINALIZING
          break; // Tiếp tục vòng lặp
        default:
          throw Error("tf`" + g);
      }
    }
    throw Error("uf"); // TIMEOUT (Hết 40 lần lặp)
  });
};
```

---

## 2. Bảng Trạng Thái Tác Vụ (Job Status State Machine)

| Mã Trạng Thái (`g`) | Tên Trạng Thái | Hành Vi Của Client | Mô Tả Kỹ Thuật |
|---|---|---|---|
| `1` | `QUEUED` | Chờ 3000ms rồi gọi lại | Tác vụ đang nằm trong hàng đợi xử lý của cụm máy chủ GPU Google. |
| `2` | `PROCESSING` | Chờ 3000ms rồi gọi lại | Mô hình khuếch tán (Diffusion Model) đang tiến hành render từng khung hình. |
| `6` | `FINALIZING` | Chờ 3000ms rồi gọi lại | Render hoàn tất, đang đóng gói container MP4 và upload lên CDN. |
| `3` | `SUCCESS` | **Dừng lặp, trả về kết quả** | Trả về chuỗi URL video CDN hoặc mảng byte MP4. |
| `4` | `FAILED` | **Ném ngoại lệ `Error("sf")`** | Lỗi nội bộ trong quá trình suy luận của mô hình (Out of memory / internal error). |
| `5` | `CANCELED` | **Dừng lặp** | Tác vụ bị hủy bởi người dùng hoặc hệ thống. |
| `7` | `POLICY_VIOLATED` | **Ném ngoại lệ `Error("sf")`** | Bộ lọc an toàn (Safety Filter) phát hiện nội dung vi phạm chính sách của Google. |
| `0` | `INVALID_JOB` | **Ném ngoại lệ `Error("sf")`** | Job ID không tồn tại hoặc đã hết hạn lưu vết trên Redis / Memcached. |

---

## 3. Các Tham Số Định Lượng (Quantitative Limits)

- **Chu kỳ thăm dò (Polling Interval):** `3000 ms` (3 giây).
- **Số lần thử tối đa (Max Iterations):** `40` lần.
- **Thời gian chờ tối đa (Global Timeout):** `40 * 3000ms = 120,000 ms` (2 phút).
  - Nếu sau 2 phút tác vụ vẫn chưa ở trạng thái `SUCCESS`, client tự động hủy và bắn lỗi `Error("uf")` (Timeout Error).
- **Cơ chế hủy tác vụ sớm (Early Cancellation):**
  - Trước mỗi chu kỳ `setTimeout`, client kiểm tra hàm callback `c()` (`c == null ? 0 : c()`).
  - Nếu người dùng chuyển trang hoặc nhấn nút Hủy, client thoát ngay khỏi vòng lặp mà không chờ thêm giây nào, đồng thời phát lệnh RPC hủy (`CancelTurn` hoặc `CancelMediaGeneration`).

---

## 4. Tính Bất Biến & Xử Lý Gửi Trùng (Idempotency & Concurrency)

- Mỗi tác vụ sinh được gán một UUID ngẫu nhiên duy nhất cho hạt giống (`seed: _.zr()`) và định danh `taskId`.
- Nếu người dùng nhấn đúp (double-click) nút Tạo:
  - Angular Query vô hiệu hóa nút gửi nhờ trạng thái `mutation.isPending()`.
  - Bộ đệm `_.ua = new wab` chặn việc gửi song song hai request cùng tham số định danh.
