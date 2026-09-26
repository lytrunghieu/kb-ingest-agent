# Phân rã Task - Kế hoạch Thực thi (OptiBot Mini-Clone)

Dưới đây là danh sách các Task nguyên tử (Atomic Tasks) để triển khai dự án với kiến trúc **Zendesk API**.

## Task 1: Khởi tạo Project & Cài đặt Thư viện
- [x] Thiết lập môi trường Python (`requirements.txt`).
- [x] Khai báo các thư viện cần thiết: `requests`, `markdownify`, `google-generativeai`, `python-dotenv`.
- [x] Tạo file `.env.sample` (chứa biến `GEMINI_API_KEY`).
- [x] Tạo cấu trúc thư mục dự án (thư mục `output` để chứa file markdown, thư mục `src` chứa code).

## Task 2: Data Ingestion (Zendesk API => Markdown)
- [x] Viết hàm gọi HTTP GET đến `https://support.optisigns.com/api/v2/help_center/en-us/articles.json` (phân trang nếu cần để lấy đủ $\ge$ 30 bài).
- [x] Lặp qua danh sách bài viết, trích xuất thuộc tính `title`, `body` (HTML) và `updated_at`.
- [x] Dùng thư viện `markdownify` chuyển đổi trường `body` thành Markdown.
- [x] Lưu nội dung ra thư mục `output` với định dạng `<id-slug>.md` (giữ nguyên headings, code blocks, links).
- [x] **Nghiệm thu:** Chạy thử và xác nhận có ít nhất 30 file Markdown sạch sẽ trong thư mục `output`.

## Task 3: Quản lý Trạng thái & Delta Logic (Last-Modified)
- [x] Viết hàm đọc/ghi thời gian chạy cuối cùng (`last_run_timestamp`) vào file `sync_state.json`.
- [x] Bổ sung logic lọc vào Task 2: Chỉ tải về và ghi đè những file Markdown có `updated_at` (từ API) lớn hơn `last_run_timestamp`.
- [x] **Nghiệm thu:** Chạy lần 1 báo 30 New. Chạy lần 2 báo 30 Skipped. Sửa `sync_state.json` lùi về quá khứ, chạy lần 3 báo Updated chính xác.

## Task 4: Tích hợp Google Gemini (Vector Store / File API)
- [x] Viết hàm gọi Gemini API để upload các file (chỉ upload các file được tải về/cập nhật ở Task 3).
- [x] Viết cấu hình tạo Agent/ChatSession với System Prompt quy định (giọng điệu, trả lời dựa trên file, bullet points).
- [x] Thống kê và in ra console tổng số file/chunk đã upload: added, updated, skipped.
- [x] **Nghiệm thu:** Script chạy mượt mà, không upload lại file cũ. Test thử đặt câu hỏi qua API và nhận câu trả lời.

## Task 5: Đóng gói Docker
- [x] Tạo `Dockerfile`.
- [x] Thiết lập base image Python, copy source, cài dependencies.
- [x] Thiết lập `CMD` mặc định chạy `main.py` (code tổng hợp các task trên).
- [x] **Nghiệm thu:** Chạy lệnh `docker run -e GEMINI_API_KEY=... <image>` thành công (thực thi xong và exit 0).

## Task 6: Thiết lập Job Automation (GitHub Actions)
- [x] Tạo file `.github/workflows/daily-job.yml`.
- [x] Cấu hình cron schedule chạy 1 lần / ngày.
- [x] Thêm bước lấy lại (restore) cache cho `sync_state.json`.
- [x] Chạy Docker image và lưu lại cache trạng thái mới.
- [x] **Nghiệm thu:** Push code lên GitHub, test trigger manual thành công.

## Task 7: Tài liệu hóa & Sanity Check (Deliverables)
- [x] Chạy Sanity check (qua Script hoặc AI Studio): Hỏi *"How do I add a YouTube video?"*, chụp ảnh màn hình có chứa trích dẫn URL.
- [x] Viết `README.md` (Hướng dẫn setup, lệnh chạy local, giải thích lý do không chia nhỏ chunk mà nhúng toàn file, link Github Actions logs).
- [x] **Nghiệm thu:** Kiểm tra 100% các tiêu chí chấm điểm của đề bài.

---
*Lưu ý: Bắt đầu code theo tuần tự từ Task 1. Hãy ra lệnh "Làm Task 1" để bắt đầu.*
