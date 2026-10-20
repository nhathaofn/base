# Đặc Tả Giao Thức Google Boq BatchExecute RPC (Protocol Specification)

[STATUS: VERIFIED]
Tài liệu này mô tả chi tiết định dạng truyền tải trên đường truyền (wire format) của giao thức **Google Boq BatchExecute** được Google Flow sử dụng cho 100% các cuộc gọi API.

---

## 1. Cấu Trúc URL Yêu Cầu (Request URL Format)

Mọi yêu cầu RPC đều gửi tới cùng một endpoint gốc:
```
POST https://flow.google.com/_/AiSandboxAngularFrontend/data/batchexecute?<QUERY_PARAMS>
```

### Các tham số Query Parameters bắt buộc:
| Tham Số | Ví Dụ Giá Trị Thực Tế | Mô Tả & Nguồn Gốc Giá Trị |
|---|---|---|
| `rpcids` | `UpteDb` hoặc `YhhmEf,ogiZ0b` | Danh sách các RPC ID được gọi trong mẻ (batch), phân cách bằng dấu phẩy. |
| `source-path` | `%2F` hoặc `%2Fproject%2F22d33...` | Đường dẫn trang hiện tại tại thời điểm phát lệnh gọi. |
| `bl` | `boq_labs-ai-sandbox-frontend_20261018.05_p0` | Build Label của frontend, lấy từ `WIZ_global_data.cfb2h`. |
| `f.sid` | `-4288118084493142723` | Mã định danh phiên làm việc client-server, lấy từ `WIZ_global_data.f_sid`. |
| `hl` | `vi` | Mã ngôn ngữ hiển thị (Host Language). |
| `_reqid` | `859592` | Số nguyên tăng dần ngẫu nhiên được sinh ra bởi client cho mỗi request để theo dõi. |
| `rt` | `c` | Response Type: `c` (Chunked/Streamed transfer encoding). |

---

## 2. Tiêu Đề Yêu Cầu (Request Headers)

```http
POST /_/AiSandboxAngularFrontend/data/batchexecute?... HTTP/2
Host: flow.google.com
Content-Type: application/x-www-form-urlencoded;charset=utf-8
X-Same-Domain: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...
Referer: https://flow.google.com/
Cookie: [REDACTED_SENSITIVE_AUTH]
```

- Header `X-Same-Domain: 1` là bắt buộc để vượt qua bộ lọc CSRF của máy chủ ESF.
- `Content-Type` luôn là `application/x-www-form-urlencoded;charset=utf-8`.

---

## 3. Cấu Trúc Thân Yêu Cầu (Request Body Format)

Thân request gồm 2 trường URL-encoded chính:
```
f.req=<URL_ENCODED_NESTED_ARRAY>&at=<CSRF_TOKEN>&
```

### Cấu trúc mảng lồng nhau của `f.req`:
Giải mã URL của `f.req` là một JSON Array đại diện cho danh sách các RPC calls được gộp chung:
```json
[
  [
    [
      "RPC_ID",
      "STRINGIFIED_INNER_PAYLOAD_JSON",
      null,
      "generic"
    ]
  ]
]
```

**Chi tiết từng phần tử trong mảng gọi:**
1. `Envelope Index 0` (`RPC_ID`): Chuỗi định danh RPC bị obfuscate của Google (Ví dụ: `"UpteDb"`, `"YhhmEf"`, `"HTrJv"`).
2. `Envelope Index 1` (`STRINGIFIED_INNER_PAYLOAD_JSON`): Payload của hàm, là một chuỗi JSON được serialize từ đối tượng Protobuf/JSPB (Ví dụ: `"[\"projects/*\",21,null,null,null,null,[1]]"`).
3. `Envelope Index 2`: Thường là `null`.
4. `Envelope Index 3`: Kiểu định tuyến RPC, hầu hết là `"generic"`.

---

## 4. Cấu Trúc Thân Phản Hồi (Response Body Format)

Phản hồi từ máy chủ luôn có tiêu đề an toàn chống XSSI (Cross-Site Script Inclusion) và truyền theo dạng các khối có độ dài xác định (length-delimited chunks).

```http
HTTP/2 200 OK
Content-Type: application/json; charset=utf-8
Content-Disposition: attachment; filename="response.bin"; filename*=UTF-8''response.bin
Content-Security-Policy: require-trusted-types-for 'script';report-uri /_/AiSandboxAngularFrontend/cspreport
Server: ESF
```

### Định dạng dữ liệu phản hồi:
```
)]}'

<chunk_byte_length>
[["wrb.fr","RPC_ID","STRINGIFIED_RESPONSE_PAYLOAD_JSON",null,null,null,"generic"],["di",<dispatch_id>],["af.httprm",<dispatch_id>,"<request_trace_id>",26]]
<next_chunk_byte_length>
[["e",4,null,null,<status_code>]]
```

### Quy tắc bóc tách dữ liệu phản hồi (Response Envelope Decoding):
1. Bỏ qua dòng đầu tiên: `)]}'\n`.
2. Đọc độ dài khối `<chunk_byte_length>`, theo sau là dòng dữ liệu JSON mảng.
3. Trong mảng phản hồi, tìm phần tử có định dạng:
   - `envelope[0] == "wrb.fr"` (Wiz Response Block - Function Result).
   - `envelope[1]`: Trùng với `RPC_ID` đã gửi.
   - `envelope[2]`: Chuỗi JSON chứa dữ liệu thực tế (Deserialized Protobuf Response).
4. `["di", <id>]`: Dispatch Index của request trong server pipeline.
5. `["af.httprm", ...]`: Metadata phân tán HTTP, chứa trace ID nội bộ của Google.
6. `[["e", 4, null, null, ...]]`: Báo cáo mã trạng thái kết thúc (Execution Status).

---

## 5. Cơ Chế Truyền Tải Dòng (Streaming / Chunked RPC)

Đối với các API xử lý thời gian thực hoặc sinh dữ liệu tuần tự:
- **Các API Streaming tiêu biểu:**
  - `StreamGenerateContent` (`L2jnw`) - Sinh video dạng dòng.
  - `StreamChat` (`xNyCid`) - Trò chuyện và điều khiển studio bằng Agent.
  - `RunAppletAgentSse` (`cNQB4b`) - Chạy công cụ tùy chỉnh Server-Sent Events.
- **Thuộc tính nội bộ:** Được gắn cờ `zU: "/google.internal.labs.aisandbox.proto.flow.v1.FlowService/StreamGenerateContent"` trong client registry.
- **Cơ chế:** Kết nối HTTP giữ mở, máy chủ liên tục flush các khối `wrb.fr` chứa các token sinh ra hoặc tiến độ render mà không đóng kết nối cho đến khi hoàn tất.

---

## 6. Phân Loại Idempotency & Caching (`Za` Flag)

Trong mã nguồn client, mỗi RPC được cấu hình một cờ boolean `Za`:
- `Za: true` (Read-only / Query): Cuộc gọi mang tính chất tra cứu thông tin (như `GetProjects`, `GetCredits`, `GetModels`). Nhiều query có thể được batch tự động trong một request HTTP duy nhất.
- `Za: false` (Mutation / Action): Cuộc gọi thay đổi trạng thái hoặc tiêu tốn tài nguyên (như `BatchAsyncGenerateVideoText`, `CreateProject`, `CancelTurn`). Yêu cầu token CSRF `at` và thường đi kèm xác thực Recaptcha Enterprise.
