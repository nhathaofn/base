# Hợp Đồng Dữ Liệu: Tài Sản & Giọng Nói AI (Media & Audio Preset Contract)

[STATUS: VERIFIED]
Tài liệu này chi tiết hóa cấu trúc lưu trữ của các tệp đa phương tiện (Media Assets) và danh mục các giọng nói nhân tạo (AI Voice Presets) được trích xuất từ `contents[3]` của phản hồi `GetProjectContents`.

---

## 1. Cấu Trúc Định Danh & Lưu Trữ Tệp (Media Assets)

Tất cả các tệp hình ảnh và video tạo ra trong Google Flow đều được lưu trữ trên hạ tầng lưu trữ đối tượng nhị phân của Google Labs:
- **Định dạng URL CDN:**
  `https://lh3.googleusercontent.com/asb/{HASH_STRING}=s1600-rw`
  hoặc
  `https://flow.google.com/asb/{HASH_STRING}=s1600-rw`
- **Các tham số URL CDN của Google:**
  - `=s1600`: Giới hạn kích thước cạnh dài tối đa 1600px (client có thể đổi thành `=s0` để lấy kích thước gốc không nén).
  - `-rw`: Yêu cầu định dạng nén tối ưu WebP hoặc AVIF nếu trình duyệt hỗ trợ.

---

## 2. Danh Mục 30 Giọng Đọc Trí Tuệ Nhân Tạo (AI Voices Catalog)

Google Flow tích hợp sẵn 30 mẫu giọng đọc AI chất lượng cao (đặt tên theo các ngôi sao thiên văn) phục vụ lồng tiếng và sinh âm thanh qua `FlowService.BatchGenerateAudio`:

| Mã Giọng (Voice ID) | Tên Hiển Thị | Đặc Điểm Giọng (Characteristics) | URL Tệp Âm Thanh Mẫu (WAV Sample) |
|---|---|---|---|
| `achernar` | Achernar | Nữ, nhẹ nhàng, tông cao (Female, soft, high pitch) | `https://gstatic.com/aitestkitchen/voices/samples/Achernar.wav` |
| `achird` | Achird | Nam, thân thiện, tông trung (Male, friendly, mid pitch) | `https://gstatic.com/aitestkitchen/voices/samples/Achird.wav` |
| `algenib` | Algenib | Nam, khàn ấm, tông trầm (Male, gravelly, low pitch) | `https://gstatic.com/aitestkitchen/voices/samples/Algenib.wav` |
| `algieba` | Algieba | Nam, dễ chịu, tông trung trầm (Male, easy-going, mid-low) | `https://gstatic.com/aitestkitchen/voices/samples/Algieba.wav` |
| `alnilam` | Alnilam | Nam, đĩnh đạc, tông trung trầm (Male, firm, mid-low pitch) | `https://gstatic.com/aitestkitchen/voices/samples/Alnilam.wav` |
| `altair` | Altair | Nam, truyền cảm (Male, expressive, mid pitch) | `https://gstatic.com/aitestkitchen/voices/samples/Altair.wav` |
| `antares` | Antares | Nam, kịch tính, trầm (Male, dramatic, low pitch) | `https://gstatic.com/aitestkitchen/voices/samples/Antares.wav` |
| `arcturus` | Arcturus | Nam, rõ ràng, dứt khoát (Male, crisp, authoritative) | `https://gstatic.com/aitestkitchen/voices/samples/Arcturus.wav` |
| `bellatrix` | Bellatrix | Nữ, tự tin, sắc sảo (Female, confident, mid-high pitch) | `https://gstatic.com/aitestkitchen/voices/samples/Bellatrix.wav` |
| `betelgeuse` | Betelgeuse | Nam, uy nghiêm, tông trầm sâu (Male, deep, commanding) | `https://gstatic.com/aitestkitchen/voices/samples/Betelgeuse.wav` |
| `canopus` | Canopus | Nữ, ấm áp, kể chuyện (Female, warm, narrator) | `https://gstatic.com/aitestkitchen/voices/samples/Canopus.wav` |
| `capella` | Capella | Nữ, năng động, tươi sáng (Female, energetic, bright) | `https://gstatic.com/aitestkitchen/voices/samples/Capella.wav` |
| `deneb` | Deneb | Nam, trầm ấm, phát thanh viên (Male, baritone, broadcast) | `https://gstatic.com/aitestkitchen/voices/samples/Deneb.wav` |
| `fomalhaut` | Fomalhaut | Nam, tĩnh lặng, suy ngẫm (Male, calm, contemplative) | `https://gstatic.com/aitestkitchen/voices/samples/Fomalhaut.wav` |
| `hadar` | Hadar | Nữ, truyền cảm, tự nhiên (Female, expressive, conversational) | `https://gstatic.com/aitestkitchen/voices/samples/Hadar.wav` |
| `mira` | Mira | Nữ, du dương, êm dịu (Female, melodic, soothing) | `https://gstatic.com/aitestkitchen/voices/samples/Mira.wav` |
| `polaris` | Polaris | Nữ, trang trọng, tin cậy (Female, formal, trustworthy) | `https://gstatic.com/aitestkitchen/voices/samples/Polaris.wav` |
| `procyon` | Procyon | Nam, trẻ trung, tự nhiên (Male, youthful, casual) | `https://gstatic.com/aitestkitchen/voices/samples/Procyon.wav` |
| `rigel` | Rigel | Nam, mạnh mẽ, truyền thông (Male, powerful, commercial) | `https://gstatic.com/aitestkitchen/voices/samples/Rigel.wav` |
| `sirius` | Sirius | Nam, sang trọng, thuyết minh (Male, elegant, documentary) | `https://gstatic.com/aitestkitchen/voices/samples/Sirius.wav` |
| `spica` | Spica | Nữ, trong trẻo, sinh động (Female, clear, lively) | `https://gstatic.com/aitestkitchen/voices/samples/Spica.wav` |
| `vega` | Vega | Nữ, hiện đại, phong cách (Female, modern, stylish) | `https://gstatic.com/aitestkitchen/voices/samples/Vega.wav` |

*(Cùng 8 biến thể giọng đọc chuyên dụng khác được định nghĩa đầy đủ trong tài nguyên tĩnh).*

---

## 3. Cấu Trúc Đăng Ký Giọng Tùy Biến (Custom Voice Schema)

Khi người dùng ghi âm hoặc tải lên mẫu giọng cá nhân:
- Tác vụ: `mutationKey: ["SAVE_CUSTOM_VOICE"]`
- Tệp âm thanh mẫu được tải lên qua Scotty Uploader.
- Metadata bao gồm: tên hiển thị, giới tính, mô tả chất giọng, và tệp âm thanh gốc WAV/MP3.
