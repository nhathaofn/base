# Google Flow (flow.google.com) Reverse Engineering Documentation

Tài liệu nghiên cứu và phân tích cơ chế hoạt động thực tế (reverse-engineering) của nền tảng **Google Flow** (AI Creative Studio for Video, Images & Custom Tools).

## Cấu trúc thư mục (Research Directory Structure)

Hệ thống tài liệu được phân loại nghiêm ngặt theo mức độ kiểm chứng thực nghiệm:

```
flow-research/
├── verified/                       # Toàn bộ thông tin ĐÃ XÁC MINH có bằng chứng thực tế
│   ├── architecture/
│   │   ├── boq_platform_runtime.md                # Kiến trúc Boq, WIZ_global_data, runtime
│   │   ├── security_authentication_session.md     # Cookie rotation, CSRF token, Recaptcha
│   │   └── client_routing_navigation.md           # Toàn bộ bảng route SPA từ AST bundle
│   ├── api/
│   │   ├── rpc_protocol_specification.md          # Đặc tả wire format f.req, wrb.fr, streaming
│   │   ├── rpc_registry.json                      # Registry đầy đủ 227 RPC IDs -> Service.Method
│   │   ├── service_flow_service.md                # FlowService (69 methods: Video, Image, Studio)
│   │   ├── service_video_fx_service.md            # VideoFxService (22 methods: Veo, Credits)
│   │   ├── service_ai_sandbox.md                  # AiSandbox (28 methods: Project, Scene, Concat)
│   │   ├── service_flow_creation_agent.md         # FlowCreationAgentService (8 methods: Copilot)
│   │   ├── service_flow_applet_agent.md           # FlowAppletAgentService (28 methods: Custom Tools)
│   │   ├── service_flow_likeness_service.md       # FlowLikenessService (5 methods: Character)
│   │   └── service_flow_sharing_service.md        # FlowSharingService (3 methods: Chia sẻ/Remix)
│   ├── data_models/
│   │   ├── project_contract.md                    # Hợp đồng thực thể Project
│   │   ├── scene_contract.md                      # Hợp đồng thực thể Scene
│   │   ├── workflow_contract.md                   # Hợp đồng thực thể Workflow (Prompt, Seed, Model)
│   │   ├── media_asset_contract.md                # Quản lý tài sản CDN và 30 giọng đọc AI
│   │   ├── model_manifest_contract.md             # Kê khai 54 biến thể mô hình Veo & Nano Banana
│   │   └── value_classification.md                # Ma trận phân loại: Static, Dynamic, Derived, Server-generated
│   ├── workflows/
│   │   ├── video_generation_workflow.md           # Vòng đời tác vụ sinh video chi tiết
│   │   ├── async_polling_job_tracking.md          # Thuật toán polling 3s, timeout 120s, mã lỗi
│   │   └── scotty_media_upload.md                 # Giao thức tải lên tệp lớn Google Scotty
│   ├── state_management/
│   │   └── angular_query_state_architecture.md    # State management (Angular Query + Signals)
│   └── quotas_limits/
│       └── credits_quotas_rate_limiting.md        # Quota tín dụng, chu kỳ reset, Anti-abuse
├── observations/                   # Dữ liệu quan sát thực tế (Raw Network Captures, Bundles)
│   ├── raw_network/
│   │   ├── page_load.json                         # 78 network calls khi tải Dashboard
│   │   └── project_studio.json                    # 75 network calls khi tải Project Studio
│   ├── bundles/                                   # 6 tệp JS bundle tải về để phân tích AST (~7MB)
│   ├── models_raw.json                            # Payload gốc danh mục model từ backend
│   ├── project_contents_raw.json                  # Payload gốc toàn bộ scenes/workflows (61KB)
│   └── observed_behaviors.md                      # Quan sát hành vi UI và telemetry
├── unknowns/
│   └── unverified_limits_and_gaps.md              # Các điểm chưa thể quan sát hoặc thiếu dữ liệu kiểm chứng
├── examples-only/                  # Mẫu minh họa payload, schema tham khảo (không phải dữ liệu chuẩn)
│   ├── request_response_samples.md                # Mẫu payload request/response minh họa
│   └── flow_reconstruction_pseudo.md              # Thiết kế kiến trúc zero-hardcode client
└── scripts/                        # Công cụ tự động hóa khảo sát qua Chrome DevTools Protocol (CDP)
```

## Ma trận trạng thái xác minh (Verification Status)

- **VERIFIED**: Dữ liệu có bằng chứng trực tiếp từ network capture hoặc AST bundle analysis.
- **OBSERVED**: Hành vi quan sát được trên giao diện nhưng chưa giải mã toàn bộ mã nguồn bên dưới.
- **INFERRED**: Suy luận logic dựa trên quy chuẩn kiến trúc của Google Boq / Wiz.
- **UNKNOWN**: Giới hạn phân quyền hoặc backend logic nội bộ chưa thể xác nhận.
