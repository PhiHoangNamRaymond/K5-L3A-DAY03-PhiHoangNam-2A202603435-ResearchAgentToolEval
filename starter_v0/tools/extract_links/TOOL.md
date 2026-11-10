---
name: extract_links
track: core
kind: local_formatter
requires_env: []
inputs: [text]
outputs: [items, count]
side_effect: false
---
# extract_links

Trích các URL HTTP(S) đã có trong văn bản, bỏ trùng và giữ thứ tự xuất hiện. Mỗi mục gồm URL và hostname. Tool hoạt động cục bộ và chỉ phân tích văn bản đầu vào.

Chấp nhận chuỗi tối đa 20.000 ký tự. Trả mã lỗi có cấu trúc khi đầu vào sai, quá dài hoặc thiếu URL.
