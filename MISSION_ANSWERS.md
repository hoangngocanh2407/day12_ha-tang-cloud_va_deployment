# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. Vấn đề 1: API key hardcode trong code. Nếu push lên GitHub → key bị lộ ngay lập tức
2. Vấn đề 2: Không có config management
3. Vấn đề 3: Print thay vì proper logging
4. Vấn đề 4: Không có health check endpoint
5. Vấn đề 5: Port cố định — không đọc từ environment

### Exercise 1.3: Comparison table
| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config | Hardcode | Env vars | Bảo mật secrets (không lộ key) & cho phép thay đổi cấu hình ứng với từng môi trường mà không cần dùng code mới. |
| Health check | Không có | Có | Giúp hệ thống platform/container biết khi nào ứng dụng còn sống hoặc sẵn sàng xử lý traffic để restart/route hợp lý. |
| Logging | print() | JSON | Giúp máy và hệ thống quản lý log (như Datadog, ELK) dễ dàng parse log, tìm kiếm, lưu trữ có cấu trúc. |
| Shutdown | Đột ngột | Graceful | Chờ các requests và process đang chạy được hoàn thành nốt trước khi đóng ứng dụng để không làm mất kết nối bất ngờ với người dùng. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: python:3.11
2. Working directory: /app
3. Để Docker cache và không phải cài lại package mỗi lần sửa code
4. CMD = mặc định, dễ thay. ENTRYPOINT = chương trình chính

### Exercise 2.3: Image size comparison
- Develop: 1150 MB
- Production: 160 MB
- Difference: 86.1%

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: https://precious-spontaneity-production-66dd.up.railway.app/health
- Screenshot: Included in screenshots folder

## Part 4: API Security

### Exercise 4.1-4.3: Test results
- API key test return 200 HTTP code.
- JWT missing return 401 Unauthorized code.
- Rate limits triggered 429 using loop testing.

### Exercise 4.4: Cost guard implementation
Implemented using Redis. Every request calculates roughly estimated usage against daily user budget.

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
Deployed via Docker compose using independent Nginx Gateway and load balanced Agent instances.
