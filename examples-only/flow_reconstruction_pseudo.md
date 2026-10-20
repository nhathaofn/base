# Thiết Kế Kiến Trúc Hệ Thống: Modular, Dynamic, Zero-Hardcode (Reconstruction Blueprint)

[CHÚ Ý: TÀI LIỆU NÀY LÀ BẢN THIẾT KẾ KIẾN TRÚC THAM KHẢO & PSEUDOCODE - KHÔNG PHẢI MÃ NGUỒN CHÍNH THỨC CỦA HỆ THỐNG]

Tài liệu này định hình thiết kế cho một hệ thống client/SDK độc lập trong tương lai có khả năng tương tác với hạ tầng Google Flow mà **hoàn toàn không hardcode** bất kỳ định danh, tham số, token hay danh mục mô hình nào.

---

## 1. Nguyên Tắc Cốt Lõi Của Kiến Trúc "Zero-Hardcode"

1. **Dynamic RPC Resolver (Bộ giải mã RPC động):**
   - Không gán cứng `"UpteDb"` hay `"YhhmEf"`.
   - Client tự động phân tích tệp script của Google tại thời điểm khởi động (AST Pattern Matching) hoặc tải registry từ tệp cấu hình động để ánh xạ tên phương thức chuẩn (ví dụ: `FlowService.GetProjects`) sang mã obfuscated tương ứng của phiên bản build hiện hành.
2. **Dynamic Session & CSRF Extractor (Bộ bóc tách phiên động):**
   - Không gán cứng token `SNlM0e` hay `cfb2h`.
   - Client tải trang gốc `https://flow.google.com/`, bóc tách đối tượng `window.WIZ_global_data` để lấy token CSRF, session ID và site key thời gian thực.
3. **Dynamic Model & Capability Discovery (Tự khám phá mô hình):**
   - Danh sách mô hình AI (Veo 3.1, Nano Banana, Abra), tỉ lệ khung hình và độ dài video được truy vấn trực tiếp từ `FlowService.GetModels` (`HTrJv`) và `FlowService.ListModelStatuses` (`yBhWQ`) khi người dùng mở ứng dụng.
4. **Adaptive BatchExecute Enveloping (Bộ đóng gói linh hoạt):**
   - Lớp transport xử lý trừu tượng việc đóng gói `f.req` lồng nhau, mã hóa URL, thêm header `X-Same-Domain`, và tự động bóc tách các khối `wrb.fr` chống XSSI (`)]}'`).

---

## 2. Mã Giả Kiến Trúc (Pseudocode Blueprint)

```typescript
// 1. Module trích xuất ngữ cảnh máy chủ động
interface FlowSessionContext {
  csrfToken: string;       // Lấy từ WIZ_global_data.SNlM0e
  buildLabel: string;      // Lấy từ WIZ_global_data.cfb2h
  sessionId: string;       // Lấy từ WIZ_global_data.f_sid
  recaptchaKey: string;    // Lấy từ WIZ_global_data.xZbWve
  accountEmail: string;    // Lấy từ WIZ_global_data.oPEP7c
}

class DynamicFlowContextManager {
  async bootstrapSession(): Promise<FlowSessionContext> {
    const html = await fetch("https://flow.google.com/", { credentials: "include" }).then(r => r.text());
    const wizData = this.parseWizGlobalData(html);
    return {
      csrfToken: wizData["SNlM0e"],
      buildLabel: wizData["cfb2h"],
      sessionId: wizData["f_sid"],
      recaptchaKey: wizData["xZbWve"],
      accountEmail: wizData["oPEP7c"]
    };
  }
}

// 2. Module ánh xạ RPC động (Zero-Hardcode RPC Registry)
class DynamicRpcResolver {
  private rpcMap: Map<string, string> = new Map();

  async loadFromBundle(bundleUrl: string): Promise<void> {
    const code = await fetch(bundleUrl).then(r => r.text());
    // Khai thác regex: {Wa: "RPC_ID", hb: "/Service.Method"}
    const regex = /\{Wa:\s*"([^"]+)",\s*hb:\s*"([^"]+)"/g;
    let match;
    while ((match = regex.exec(code)) !== null) {
      const [_, rpcId, serviceMethod] = match;
      this.rpcMap.set(serviceMethod.replace("/", ""), rpcId);
    }
  }

  getRpcId(serviceMethod: string): string {
    const id = this.rpcMap.get(serviceMethod);
    if (!id) throw new Error(`RPC Method ${serviceMethod} not found in active build`);
    return id;
  }
}

// 3. Bộ truyền tải BatchExecute tổng quát (Generic Transport)
class BatchExecuteTransport {
  constructor(
    private session: FlowSessionContext,
    private resolver: DynamicRpcResolver
  ) {}

  async callRpc<TRequest, TResponse>(serviceMethod: string, payload: TRequest): Promise<TResponse> {
    const rpcId = this.resolver.getRpcId(serviceMethod);
    const serializedPayload = JSON.stringify(payload);
    
    // Đóng gói theo chuẩn mảng lồng nhau của Boq
    const fReq = JSON.stringify([[[rpcId, serializedPayload, null, "generic"]]]);
    
    const body = new URLSearchParams();
    body.set("f.req", fReq);
    body.set("at", this.session.csrfToken);

    const url = new URL("https://flow.google.com/_/AiSandboxAngularFrontend/data/batchexecute");
    url.searchParams.set("rpcids", rpcId);
    url.searchParams.set("bl", this.session.buildLabel);
    url.searchParams.set("f.sid", this.session.sessionId);
    url.searchParams.set("rt", "c");

    const response = await fetch(url.toString(), {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "X-Same-Domain": "1"
      },
      body: body.toString(),
      credentials: "include"
    });

    const rawText = await response.text();
    return this.unwrapResponse<TResponse>(rawText, rpcId);
  }

  private unwrapResponse<T>(rawText: string, expectedRpcId: string): T {
    const lines = rawText.split("\n");
    for (const line of lines) {
      if (line.startsWith("[[") && line.includes("wrb.fr")) {
        const envelope = JSON.parse(line);
        for (const item of envelope) {
          if (item[0] === "wrb.fr" && item[1] === expectedRpcId) {
            return JSON.parse(item[2]) as T;
          }
        }
      }
    }
    throw new Error(`RPC ${expectedRpcId} returned no valid wrb.fr payload`);
  }
}
```
