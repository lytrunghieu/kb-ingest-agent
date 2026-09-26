# Kiến trúc và Kế hoạch Thực thi (OptiBot Mini-Clone)

## 1. Lựa chọn Công nghệ Chốt
- **AI Platform:** Google Gemini (Gemini API & File API).
- **Môi trường Job Automation:** GitHub Actions (Cronjob).
- **Ngôn ngữ:** Python.
- **Containerization:** Docker (`Dockerfile`).

---

## 2. Kiến trúc Triển khai (Đã được thống nhất)
Chúng ta sẽ triển khai dự án dựa trên giải pháp tối ưu nhất cho nguồn dữ liệu từ Zendesk Help Center.

### Lõi Kiến trúc: Zendesk API + RAG Đơn giản hóa
Mục tiêu: Viết code sạch, tối ưu hiệu năng và đạt 100% yêu cầu chức năng.
- **Crawler (Data Ingestion):** 
  - Không cào DOM HTML tĩnh vì dễ gãy và vất vả dọn dẹp quảng cáo (nav/ads).
  - Sử dụng trực tiếp **Zendesk API** (`/api/v2/help_center/articles.json`) của trang `support.optisigns.com`. API này sẽ trả về thẳng file JSON, với trường `body` chứa 100% HTML nội dung chính xác của bài viết, tự động bỏ qua toàn bộ rác UI của trang web.
  - Sử dụng thư viện `markdownify` để chuyển `body` HTML này sang chuẩn Markdown.
- **Delta Upload (Trạng thái):** 
  - Thay vì băm MD5 toàn bộ file để phát hiện thay đổi, ta chỉ cần dựa vào thuộc tính `updated_at` (thời gian cập nhật) được trả về sẵn từ Zendesk API.
  - File `sync_state.json` sẽ lưu lại mốc thời gian chạy cronjob thành công cuối cùng (Last Run). Lần chạy tiếp theo chỉ lấy các bài viết có `updated_at` lớn hơn mốc này.
- **Xử lý Chunking:** Lợi dụng context window khổng lồ của Gemini, ta upload **nguyên cả file Markdown** qua File API của Google mà không cần chia nhỏ (chunking) phức tạp. Việc này giảm thiểu rủi ro mất ngữ cảnh và được chú thích rõ trong README như một chiến lược.
- **Ưu điểm:** Khẳng định tư duy nhạy bén của kỹ sư: "Best code is no code" - biết dùng API thay vì hì hục cào dữ liệu thủ công. Code chạy cực nhanh, tỷ lệ lỗi parse HTML bằng 0.

---
*Kế hoạch đã chốt, chuyển sang xem `03-tasks.md` để bắt tay vào công việc!*
