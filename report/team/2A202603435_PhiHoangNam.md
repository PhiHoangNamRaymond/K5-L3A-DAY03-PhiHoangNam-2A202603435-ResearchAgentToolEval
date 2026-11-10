# Báo cáo cá nhân — Phi Hoang Nam

## 1. Thông tin thành viên

- Họ tên: Phi Hoang Nam
- MSSV: `2A202603435`
- Lớp: L3A
- GitHub: `PhiHoangNamRaymond`

## 2. Phần việc phụ trách

Nhóm có một thành viên, nên Phi Hoang Nam phụ trách toàn bộ bài lab: cấu hình môi trường, prompt và tool declaration v0–v3, tool mới `extract_links`, unit test, 10 case eval nhóm, UI Streamlit, live chat, báo cáo và nộp bài.

## 3. Đóng góp cụ thể

| Hạng mục | Việc đã làm | File |
|---|---|---|
| Setup | Tạo khóa OpenRouter, cấu hình `.env`, chạy preflight. Dựng llama.cpp với Qwen3-1.7B trên Windows để có một model cố định cho chuỗi v0–v3 | `starter_v0/.env.example`, `starter_v0/scripts/preflight_provider.py` |
| Baseline và tối ưu | Chạy v0, v1 (prompt: hỏi lại, xác nhận gửi), v2 (tools.yaml: ranh giới tool, quy ước args), v3 (prompt: ngữ cảnh multi-turn, số call tối thiểu). Trên Qwen3: 30% → 25% → 45% → 55% | `starter_v0/artifacts/`, `starter_v0/runs/`, `starter_v0/artifacts/version_log.csv` |
| Tool mới | `extract_links`: trích URL, bỏ trùng, giữ thứ tự, trả error dict khi input sai | `starter_v0/tools/extract_links/` |
| Unit test | 5 test cho `extract_links` và điền các stub TODO; toàn suite 90 passed, 0 skipped | `starter_v0/tests/test_tools_todo.py`, `starter_v0/analysis/pytest.txt` |
| Eval nhóm | 10 case (5 single, 5 multi turn), run group đạt 8/10 | `starter_v0/data/eval_group.json` |
| UI và demo | UI Streamlit, mở link qua Cloudflare Tunnel, chạy 3 transcript live | `starter_v0/app.py`, `starter_v0/transcripts/` |
| Kiểm tra API thật | Sau khi có đủ khóa: OpenRouter, Tavily (`lookup`), Firecrawl (`fetch`) chạy được; RapidAPI trả `403` | `report/team/group_report.md` mục 5 |

## 4. Bằng chứng

- Commit:
  - `4e457b6` — Complete Day 03 research agent lab (prompt, tools, tool mới, test, eval, UI, run, transcript).
  - `ea7d0ef` — Consolidate lab assistance disclosure.
  - `cbc1bf1` — Record live API checks before submission.
- Run hợp lệ (20/20 case, 0 lỗi provider): xem bảng B1 trong [báo cáo nhóm](group_report.md).
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: Trợ lý AI (Codex) hỗ trợ lên ý tưởng, chỉnh prompt, viết mã tool và UI, viết test, chạy eval và tổng hợp kết quả. Cách tự kiểm tra: đối chiếu từng metric trong báo cáo với `summary` của run JSON, so `prompt_hash`/`tools_hash` giữa các version, chạy lại `pytest`, thử các câu mẫu A3 trên UI và tự chạy kiểm tra từng tool có API key trên PowerShell.

## 5. Tự đánh giá

<!-- TODO (tự viết bằng lời của mình): -->
<!-- - Điều học được rõ nhất từ vòng lặp v0→v3 (vd: vì sao v1 giảm điểm, vì sao v2 tăng). -->
- Với model nhỏ, sửa mô tả tool trong tools.yaml (v2) có tác dụng hơn thêm rule vào prompt (v1).
- Thêm rule vào prompt có thể làm điểm giảm, nên phải đo lại sau mỗi lần sửa.
- Lỗi multi-turn chủ yếu do model không giữ được ngữ cảnh, và v3 đã sửa được phần lớn.
<!-- - Phần tự làm chắc nhất và phần còn phụ thuộc AI nhiều nhất. -->
Phần tự làm chắc nhất:
- Cấu hình môi trường, API key, llama.cpp.
- Đọc run JSON và hiểu vì sao case FAIL.
- Chạy demo UI và kiểm tra từng tool.
Phần còn dựa vào AI nhiều nhất:
- Viết code tool và test.
- Viết prompt và tools.yaml.
- Tổng hợp báo cáo.
<!-- - Điểm yếu còn lại: R10/R11/R12 vẫn FAIL ở v3, G07/G09 FAIL, transcript chạy khi chưa có khóa Firecrawl. -->
<!-- - Nếu làm lại sẽ đổi gì. -->
- Cấu hình đủ API key trước khi chạy eval.
- Chạy chuỗi v0–v3 trên model cloud.