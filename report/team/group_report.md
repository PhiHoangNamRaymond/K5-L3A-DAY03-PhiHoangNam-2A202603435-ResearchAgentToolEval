# Báo cáo nhóm — Day 03 Research Agent Tool Eval

## 1. Thông tin nhóm

Phi Hoang Nam, MSSV `2A202603435`, lớp L3A. Nhóm có một thành viên. [Thông tin nhóm và phân công](../../TEAM.md).

## 2. Phần A — Demo agent

Agent hỗ trợ tìm nguồn, tra sổ tay policy mẫu, trích URL từ văn bản và định dạng kết quả. Nó hỏi thêm thông tin khi cần và yêu cầu duyệt nội dung trước khi gửi Telegram.

### A1. Cách chạy UI

Chạy từ `starter_v0` với `.venv` đã cài `requirements.txt` và `.env` đã cấu hình provider.

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

UI mặc định dùng OpenRouter Flint miễn phí. Với llama.cpp local, đặt `LAB_UI_PROVIDER=ollama`, `LAB_UI_MODEL=qwen3-1.7b-q4` và `OLLAMA_BASE_URL=http://127.0.0.1:18083/v1` trong PowerShell trước khi khởi chạy.

[Mở UI dùng thử](https://complement-feelings-emily-significant.trycloudflare.com).
Link Cloudflare Quick Tunnel chỉ tồn tại khi Streamlit và tunnel còn chạy trên máy.

### A2. Công cụ

| Tool | Hành vi | Mới |
|---|---|---|
| `clarify` | Hỏi lại hoặc xin xác nhận | |
| `timeline` | Đọc bài X theo tài khoản | |
| `social_search` | Tìm bài X theo từ khóa | |
| `lookup` | Tìm tin và nguồn web | |
| `fetch` | Đọc một URL | |
| `format` | Định dạng item thành bản tin | |
| `policy` | Tra policy nội bộ mẫu | |
| `papers` | Tìm paper trên arXiv | |
| `paper_text` | Đọc văn bản PDF arXiv | |
| `send` | Gửi Telegram sau xác nhận trong CLI | |
| `extract_links` | Trích các URL duy nhất theo thứ tự xuất hiện | Có |

### A3. Câu hỏi mẫu

1. Trích URL trong đoạn sau: https://example.org/a và https://example.net/b.
2. Theo policy nội bộ, cần xác nhận điều gì trước khi đăng Telegram?
3. Tóm tắt bài viết này giúp mình.
4. Dùng template bullets cho hai item đã có: báo cáo A và báo cáo B.

## 3. Giải pháp

Prompt v1 bổ sung cách xử lý thiếu thông tin, xác nhận nội dung gửi và dữ liệu truy xuất. v2 làm rõ chức năng và tham số trong YAML. v3 bổ sung quy tắc giữ ràng buộc theo lượt và lập danh sách call tối thiểu. Mỗi bản base sử dụng bộ 10 tool gốc. Sau khi đóng băng v3 base, bộ group và UI dùng khai báo 11 tool với `extract_links`.

Tool mới phân tích văn bản cục bộ, trả danh sách URL theo thứ tự xuất hiện, bỏ trùng và trả lỗi có cấu trúc cho đầu vào sai, quá dài hoặc thiếu URL.

## 4. Phần B — Kết quả và bằng chứng

### B1. So sánh phiên bản

| Version | Provider / model | Giả thuyết | Case trước → sau | Routing | Args | Multi-turn | Run |
|---|---|---|---:|---:|---:|---:|---|
| v0 | ollama / `qwen3-1.7b-q4` | Đo hành vi của starter trước khi sửa prompt và khai báo. | — → 30.0% | 35.0% | 30.0% | 33.3% | [v0_B_base_ollama_20261110T194656301846.json](../../starter_v0/runs/v0_B_base_ollama_20261110T194656301846.json) |
| v1 | ollama / `qwen3-1.7b-q4` | Chặn suy đoán thông tin và yêu cầu xác nhận nội dung, đích gửi sẽ giảm lỗi thiếu dữ liệu và lỗi boundary. | 30.0% → 25.0% | 30.0% | 25.0% | 0.0% | [v1_B_base_ollama_20261110T194735002046.json](../../starter_v0/runs/v1_B_base_ollama_20261110T194735002046.json) |
| v2 | ollama / `qwen3-1.7b-q4` | Mô tả ranh giới giữa các nguồn và quy ước tham số sẽ giảm nhầm công cụ và tham số. | 25.0% → 45.0% | 60.0% | 45.0% | 16.7% | [v2_B_base_ollama_20261110T194800346413.json](../../starter_v0/runs/v2_B_base_ollama_20261110T194800346413.json) |
| v3 | ollama / `qwen3-1.7b-q4` | Quy tắc cập nhật ngữ cảnh, chọn số call tối thiểu và giữ nguyên chủ đề sẽ giảm lỗi multi-turn và call thừa. | 45.0% → 55.0% | 65.0% | 55.0% | 66.7% | [v3_B_base_ollama_20261110T194822152786.json](../../starter_v0/runs/v3_B_base_ollama_20261110T194822152786.json) |
| v0 | openrouter / `recursive/flint-v1.0:free` | Đo hành vi của starter trước khi sửa prompt và khai báo. | — → 40.0% | 55.0% | 40.0% | 50.0% | [v0_B_base_openrouter_20261110T194024643212.json](../../starter_v0/runs/v0_B_base_openrouter_20261110T194024643212.json) |
| v1 | openrouter / `recursive/flint-v1.0:free` | Chặn suy đoán thông tin và yêu cầu xác nhận nội dung, đích gửi sẽ giảm lỗi thiếu dữ liệu và lỗi boundary. | 40.0% → 40.0% | 60.0% | 40.0% | 33.3% | [v1_B_base_openrouter_20261110T194310261090.json](../../starter_v0/runs/v1_B_base_openrouter_20261110T194310261090.json) |

Mỗi run trong bảng đo đủ 20 case với 0 lỗi provider. So sánh qua version trên cùng model. Nhãn `ollama` là adapter OpenAI-compatible của repo dùng để kết nối với llama.cpp, chạy model Qwen3 trên máy Windows.

Trên Qwen3, v1 giảm từ 6 xuống 5 case PASS, với nhiều trường hợp thiếu tool call. v2 đưa điểm lên 9/20 sau khi làm rõ tên và tham số tool. v3 đạt 11/20 và đưa điểm multi-turn từ 16.7% lên 66.7%. R10, R11 và R12 vẫn FAIL ở v3, nên cần đọc transcript và tiếp tục kiểm tra các tình huống hỏi lại và xác nhận.

### B2. Phân tích lỗi baseline OpenRouter

| Case | Loại lỗi | Call thực tế | Lỗi quan sát | Thay đổi liên quan |
|---|---|---|---|---|
| R01_user_tweets_routing | wrong_tool | `social_search {"query": "Sam Altman latest post", "search_type": "Latest", "limit": 10}`, `timeline {"screenname": "sama", "limit": 10}` | extra tool call social_search | v2 làm rõ nguồn, v3 giảm call dư |
| R02_search_tweets_routing | wrong_tool | `social_search {"query": "GPT-5 Twitter discussion", "search_type": "Latest", "limit": 10}`, `social_search {"query": "GPT-5 OpenAI news Twitter", "search_type": "Latest", "limit": 10}` | extra tool call social_search | v2 làm rõ nguồn, v3 giảm call dư |
| R03_web_news_routing | wrong_tool | `social_search {"query": "AI news today latest artificial intelligence", "search_type": "Latest", "limit": 10}`, `lookup {"query": "AI artificial intelligence news this week", "topic": "news", "timeframe": "week", "max_results": 10}` | query: expected 'AI', got 'AI artificial intelligence news this week' / timeframe: expected 'day', got 'week' / extra tool call social_search | v2 làm rõ nguồn, v3 giảm call dư |
| R05_limit_arg | wrong_arg_value | `social_search {"query": "Elon Musk", "search_type": "Latest", "limit": 10}` | missing tool call timeline / extra tool call social_search | v2 làm rõ tham số, v3 giữ chủ đề và thay đổi theo lượt |
| R06_timeframe_arg | wrong_arg_value | `social_search {"query": "tin công nghệ mới nhất tuần này AI AI chips sản phẩm công nghệ", "search_type": "Latest", "limit": 10}`, `lookup {"query": "latest technology news this week AI breakthroughs gadgets", "topic": "news", "timeframe": "week", "max_results": 10}` | extra tool call social_search | v2 làm rõ tham số, v3 giữ chủ đề và thay đổi theo lượt |
| R10_missing_handle | missing_info | `timeline {"screenname": "sama", "limit": 5}` | missing tool call clarify / extra tool call timeline | v1 hỏi lại, v3 dùng ngữ cảnh đã bổ sung |
| R11_missing_url | missing_info | `lookup {"query": "bài viết AI mới nhất 2025", "max_results": 5}`, `lookup {"query": "latest AI news article this week", "max_results": 5}` | missing tool call clarify / extra tool call lookup / extra tool call lookup | v1 hỏi lại, v3 dùng ngữ cảnh đã bổ sung |
| R12_confirm_before_send | wrong_boundary | `send {}` | missing tool call clarify / extra tool call send | v1 xác nhận đích và nội dung |
| R13_parallel_web_and_tweets | wrong_tool | `lookup {"query": "AI news today latest artificial intelligence news", "topic": "news", "timeframe": "day"}`, `social_search {"query": "AI artificial intelligence news today", "search_type": "Latest"}` | query: expected 'AI', got 'AI news today latest artificial intelligence news' / query: expected 'AI', got 'AI artificial intelligence news today' | v2 làm rõ nguồn, v3 giảm call dư |
| M02_carryover_timeframe | wrong_arg_value | `social_search {"query": "robotics news today latest", "search_type": "Latest", "limit": 10}`, `lookup {"query": "latest robotics news today", "topic": "news", "timeframe": "day", "max_results": 10}` | query: expected 'robotics', got 'latest robotics news today' / extra tool call social_search | v2 làm rõ tham số, v3 giữ chủ đề và thay đổi theo lượt |
| M03_correction_handle | wrong_arg_value | `timeline {"screenname": "Andrej Karpathy", "limit": 3}` | screenname: expected 'karpathy', got 'Andrej Karpathy' | v2 làm rõ tham số, v3 giữ chủ đề và thay đổi theo lượt |
| M06_switch_tool | wrong_tool | `lookup {"query": "OpenAI latest news", "topic": "news", "timeframe": "day", "max_results": 5}` | query: expected 'OpenAI', got 'OpenAI latest news' | v2 làm rõ nguồn, v3 giảm call dư |

Log baseline ghi nhận `Missing RAPIDAPI_KEY env var` (14), `Missing TAVILY_API_KEY env var` (7), `Missing FIRECRAWL_API_KEY env var` (2).

### B3. Eval nhóm

| Case | Mục đích | Kỳ vọng | Kết quả |
|---|---|---|---|
| G01_extract_unique_links | Định tuyến tới tool mới khi người dùng chỉ muốn trích link từ văn bản đã dán. | `extract_links {}` | PASS |
| G02_format_supplied_bullets | Phân biệt định dạng dữ liệu có sẵn với đọc lại hai URL. | `format {"template": "bullets"}` | PASS |
| G03_lookup_month_and_limit | Mang đúng truy vấn, chủ đề, khoảng thời gian và số kết quả. | `lookup {"query": "AI chips", "topic": "news", "timeframe": "month", "max_results": 4}` | PASS |
| G04_policy_tool_usage | Từ khóa arXiv nằm trong câu hỏi policy nội bộ, route đúng vùng policy và giới hạn kết quả. | `policy {"policy_area": "tool_usage", "top_k": 1}` | PASS |
| G05_confirm_exact_draft | Có văn bản đầy đủ nhưng vẫn phải hỏi xác nhận gửi. | `clarify {"response_type": "yes_no"}` | PASS |
| G06_cancel_publish | Hủy yêu cầu đang chờ xác nhận và tránh gọi tool gửi. | Không gọi tool | PASS |
| G07_replace_url | Thay thế URL cũ bằng URL đã sửa và chỉ đọc một bài. | `fetch {"url": "https://example.org/revised"}` | FAIL · missing_tool_call |
| G08_change_social_order | Đổi kiểu sắp xếp và giữ các tham số của lượt trước. | `social_search {"query": "robotaxi", "search_type": "Latest", "limit": 6}` | PASS |
| G09_switch_to_internal_rule | Chuyển từ nguồn web công khai sang sổ tay bảo mật nội bộ. | `policy {"policy_area": "data_privacy", "top_k": 2}` | FAIL · wrong_arg_value |
| G10_latest_papers_keep_count | Sửa cách sắp xếp arXiv từ relevance sang submittedDate qua lượt sau. | `papers {"max_results": 3, "sort_by": "submittedDate"}` | PASS |

Run nhóm đạt 8/10 PASS. [v3-group_B_group_ollama_20261110T194847461791.json](../../starter_v0/runs/v3-group_B_group_ollama_20261110T194847461791.json).

### B4. Transcript chat thật

| Lượt | User | Tool | Kết quả |
|---|---|---|---|
| 1 | Trích các URL trong đoạn sau và giữ thứ tự: https://example.org/a rồi https://example.net/b, nhắc lại https://example.org/a. | `extract_links {}` | answered |
| 2 | Tóm tắt một bài viết cho mình. Hãy hỏi lại bằng clarify nếu còn thiếu URL. | `clarify {"response_type": "text"}` | waiting_for_user |
| 3 | Đây là URL bài viết: https://example.org/brief | `fetch {"url": "https://example.org/brief"}` | answered |
| 4 | Đăng lên Telegram nội dung sau: Seminar AI thứ Sáu lúc 15h. Cho mình xem và xác nhận trước khi đăng. | `clarify {"response_type": "yes_no"}` | waiting_for_user |

Artifact `v3-demo+pe8362923cf23+t1f96ca01d8eb`. [v3-demo_ollama_20261110T194930002403.transcript.json](../../starter_v0/transcripts/v3-demo_ollama_20261110T194930002403.transcript.json).

| 1 | Trích các URL trong đoạn sau và bỏ trùng: https://example.org/a rồi https://example.net/b và https://example.org/a. | `extract_links {}` | answered |
| 2 | Tóm tắt một bài viết cho mình. Hãy hỏi lại bằng clarify nếu còn thiếu URL. | `clarify {"response_type": "text"}` | waiting_for_user |
| 3 | Đây là URL bài viết: https://example.org/brief | `fetch {"url": "https://example.org/brief"}` | answered |
| 4 | Đăng lên Telegram nội dung sau: Seminar AI thứ Sáu lúc 15h. Cho mình xem và xác nhận trước khi đăng. | `clarify {"response_type": "yes_no"}` | waiting_for_user |

Artifact `v3-demo+pe8362923cf23+t1f96ca01d8eb`. [v3-demo_ollama_20261110T195052739816.transcript.json](../../starter_v0/transcripts/v3-demo_ollama_20261110T195052739816.transcript.json).

| 1 | Trích các URL trong đoạn này, giữ thứ tự: https://example.org/a và https://example.net/b. | `extract_links {}` | answered |
| 2 | Tóm tắt bài viết này giúp mình. | — | answered |
| 3 | Link bài đây: https://example.org/brief | `fetch {"url": "https://example.org/brief"}` | answered |
| 4 | Chuẩn bị gửi Telegram văn bản: Buổi demo bắt đầu lúc 15h. Hỏi mình xác nhận trước khi gửi. | — | answered |

Artifact `v3-demo+pe8362923cf23+t1f96ca01d8eb`. [v3-demo_openrouter_20261110T194516542380.transcript.json](../../starter_v0/transcripts/v3-demo_openrouter_20261110T194516542380.transcript.json).

### B5. Tool, test và UI

- Tool `extract_links` chạy cục bộ. [Mô tả tool](../../starter_v0/tools/extract_links/TOOL.md) · [Mã Python](../../starter_v0/tools/extract_links/tool.py).
- Bộ kiểm thử offline có **90 passed, 0 failed, 0 skipped**. Test tool mới kiểm tra bỏ trùng, giữ thứ tự, dấu ngoặc trong URL, dữ liệu sai kiểu, thiếu URL và độ dài. [Bộ test](../../starter_v0/tests/test_tools_todo.py) · [Kết quả pytest](../../starter_v0/analysis/pytest.txt).
- AppTest xác nhận gửi câu hỏi, hiển thị hai lượt chat và hai URL từ extract_links. Endpoint công khai trả HTTP 200. UI hiển thị lỗi tool và chặn tác vụ gửi Telegram. [Mã UI](../../starter_v0/app.py).

## 5. Khó khăn và cách xử lý

- OpenRouter Flint trả structured tool call và cho hai run cloud đủ case. Gói miễn phí có hạn mức ngày; dùng thêm model Qwen3 local để làm một chuỗi so sánh đủ bốn bản bằng một model cố định.
- Khi tạo các run eval đã nộp, Tavily, Firecrawl và RapidAPI chưa được cấu hình. Các lỗi thiếu khóa nằm trong `tool_results`. Điểm eval đo tên tool và các tham số kỳ vọng. Unit test mô phỏng HTTP để kiểm tra request và cách xử lý phản hồi.
- Sau khi cấu hình `.env`, Phi Hoang Nam chạy preflight và kiểm tra trực tiếp từng tool trên PowerShell. OpenRouter trả `OK` và một tool call. Tavily (`lookup`) và Firecrawl (`fetch`) mỗi tool trả 1 kết quả. Lần kiểm tra RapidAPI gần nhất ghi nhận `403 Forbidden` ở `timeline` và `HTTPError` ở `social_search`. Hai tool X vẫn cần xác minh quyền truy cập Twitter API45.
- Không có chứng cứ gửi Telegram thật. Phiên demo chỉ thử bước xác nhận. Các test Telegram dùng HTTP giả lập.

## 6. Đóng góp

Phi Hoang Nam tạo khóa OpenRouter, cấu hình môi trường và chạy preflight. Phạm vi dùng AI được ghi trong báo cáo cá nhân. [Báo cáo cá nhân](2A202603435_PhiHoangNam.md).

## 7. Hạn chế và hướng cải thiện

- Đưa quy tắc hỏi lại, xác nhận và xử lý ngữ cảnh vào prompt. Đưa điều kiện sử dụng từng tool, enum và quy ước tham số vào YAML.
- Eval kiểm tra tập tên tool và các tham số yêu cầu. Nội dung câu hỏi xác nhận, thứ tự thực thi, chất lượng nguồn và chất lượng tóm tắt cần kiểm tra bằng transcript hoặc test tool.
- Vòng sau sẽ kiểm tra một giả thuyết riêng về tên tài khoản và cụm query. Đo lại trên bộ case giữ nguyên, đọc log lỗi và kiểm tra trực tiếp các tool có khóa API.

## 8. Tài liệu tham khảo

- [Đề bài và tiêu chí chấm](../../RUBRIC.md).
- [Giới hạn các model miễn phí OpenRouter](https://openrouter.ai/collections/free-models).
- [Qwen3 GGUF dùng với llama.cpp](https://huggingface.co/ggml-org/Qwen3-1.7B-GGUF).
