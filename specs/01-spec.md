# OptiSigns Take-Home Test - Specification

## 1. Tổng quan
Bài test gồm 2 phần, mỗi phần giới hạn trong khoảng 8 giờ làm việc tập trung (tổng cộng ~16 giờ). 
- **Part 1:** Coding - Xây dựng bản sao thu nhỏ của OptiBot (OptiBot Mini-Clone).
- **Part 2:** Planning - Lập kế hoạch xây dựng bản sao của hệ thống SCIO (Không yêu cầu code).

**Nguyên tắc chung:** Không làm lố thời gian dự kiến. Nếu không kịp, nộp những gì đã hoàn thành và báo cáo những phần đã cắt giảm.

---

## 2. Phân tích Yêu cầu - Part 1: OptiBot Mini-Clone

### 2.1. Functional Requirements (Yêu cầu tính năng)
1. **Scrape Web sang Markdown (Crawler):**
   - Lấy ít nhất 30 bài viết từ `support.optisigns.com`.
   - Chuyển đổi nội dung thành file Markdown sạch, lưu dưới định dạng `<slug>.md`.
   - **Yêu cầu bắt buộc:** Giữ nguyên các relative links, code blocks, headings. Loại bỏ navigation/ads.
   - *Gợi ý:* Có thể dùng Zendesk API để đọc bài viết.
2. **AI Assistant & Vector Store (Tự động hóa qua API):**
   - **Bắt buộc:** Upload file qua API (không dùng giao diện kéo thả UI).
   - Thiết lập AI Assistant bằng OpenAI hoặc Google Gemini theo System Prompt được cung cấp.
   - Script Python (`main.py`) thực hiện:
     - Upload file Markdown lên Vector Store / Knowledge Base của AI.
     - Xử lý Chunking (tùy chọn chiến lược, nhưng phải giải thích trong README).
     - Ghi log số lượng file và số chunks đã embed.
3. **Daily Job & Tối ưu hóa (Cronjob & Delta Upload):**
   - Cronjob chạy 1 lần/ngày.
   - Crawl lại (Re-scrape) và phát hiện bài viết mới/cập nhật (dựa vào hash, Last-Modified...).
   - Chỉ upload phần thay đổi (delta upload).
   - Ghi log thống kê: số lượng added, updated, skipped.

### 2.2. Non-functional Requirements (Hiệu năng, Công nghệ, Triển khai)
1. **Môi trường & Triển khai:**
   - Đóng gói bằng Docker (`Dockerfile`). Lệnh khởi chạy phải là: `docker run -e API_KEY=... main.py` chạy một lần rồi thoát (exit 0).
   - Triển khai lịch chạy (cron) trên nền tảng Cloud (Railway, Render, Fly.io, AWS, GCP, hoặc DigitalOcean).
2. **Bảo mật & Quản lý mã nguồn:**
   - Lưu trữ trên GitHub Repository với tên "bí ẩn" (không dùng từ khóa "optisigns").
   - Commit history rõ ràng.
   - Không hard-code các khóa API (sử dụng `.env.sample`).
3. **Tài liệu hóa (Deliverables):**
   - **README (<= 1 trang):** Hướng dẫn setup, chạy local, giải thích chiến lược chunking, link dẫn tới logs của Daily job.
   - **Screenshot:** Ảnh chụp màn hình trợ lý AI trả lời đúng câu hỏi "How do I add a YouTube video?" với các trích dẫn URL hợp lệ.

### 2.3. Out of Scope (Ngoài phạm vi)
- Xây dựng giao diện Chatbot UI (chỉ cần test trên Playground/AI Studio).
- Code cho Part 2 (Chỉ yêu cầu tài liệu Plan).

---

## 3. Phân tích Yêu cầu - Part 2: SCIO Clone Plan

### 3.1. Yêu cầu đầu ra
Lập một bản kế hoạch chi tiết (dành cho team hoặc cá nhân) để xây dựng lại hệ thống SCIO (Web management portal for digital signage) từ con số 0.

### 3.2. Nội dung bắt buộc trong Kế hoạch
- Sản phẩm sẽ xây dựng là gì, thứ tự làm các tính năng, thời gian hoàn thành, và lý do cho các quyết định đó.
- Quyết định quy mô đội ngũ (team size), nền tảng (platforms), phạm vi sản phẩm (in scope/out of scope).
- **Đặc biệt:** Phải nêu rõ **một điều ngoài dự kiến** khi trải nghiệm sản phẩm thật và nó đã làm thay đổi kế hoạch của bạn như thế nào.

---

## 4. Các điểm cần làm rõ (Clarification)
- *Đối với Vector Store:* Hiện tại OpenAI Assistants API (v2) hỗ trợ "Vector Stores", Google Gemini cũng có cơ chế tương đương. Bạn muốn ưu tiên sử dụng platform nào (OpenAI hay Gemini) cho dự án này?
- *Đối với Cloud Hosting:* Bạn có tài khoản sẵn ở nhà cung cấp Cloud nào để thiết lập Daily Job chưa (VD: Railway, Render, GCP, AWS)?
