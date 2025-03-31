# Hướng dẫn đóng góp

Cảm ơn bạn đã quan tâm đến việc đóng góp cho dự án Dịch vụ Phân tích Cảm xúc. Dưới đây là hướng dẫn để giúp bạn đóng góp hiệu quả.

## Quy trình đóng góp

1. Fork repository và tạo branch mới từ `main`
2. Đặt tên branch theo format: `feature/ten-tinh-nang` hoặc `fix/ten-loi`
3. Thực hiện các thay đổi và commit theo quy ước commit
4. Đảm bảo code đáp ứng các tiêu chuẩn chất lượng và pass tất cả tests
5. Tạo Pull Request đến branch `main` của repository chính

## Quy ước commit

Vui lòng sử dụng các tiêu đề commit ngắn gọn, rõ ràng và mô tả được nội dung thay đổi. Ví dụ:

- `feat: Thêm endpoint thống kê xu hướng cảm xúc theo tuần`
- `fix: Sửa lỗi không phân tích được văn bản có ký tự đặc biệt`
- `docs: Cập nhật tài liệu API`
- `test: Thêm test case cho phân tích batch`
- `refactor: Cải thiện hiệu suất tính toán xu hướng`

## Tiêu chuẩn code

- Tuân thủ PEP 8 cho Python code
- Sử dụng docstrings cho tất cả các class và method
- Viết test cho các tính năng mới
- Đảm bảo code coverage ít nhất 80%

## Kiểm thử

Khi thêm tính năng mới hoặc sửa lỗi, vui lòng thêm test case tương ứng.

```bash
# Chạy tất cả tests
python -m pytest tests/

# Kiểm tra code coverage
python -m pytest --cov=src tests/
```

## Tài liệu

Vui lòng cập nhật tài liệu khi:
- Thêm API endpoint mới
- Thay đổi cấu trúc dữ liệu
- Thêm tính năng mới
- Thay đổi quy trình cài đặt hoặc cấu hình

## Các vấn đề thường gặp

### Cải thiện mô hình phân tích cảm xúc

Khi làm việc với mô hình phân tích cảm xúc, vui lòng lưu ý:

1. Luôn đo lường hiệu suất trước và sau khi thay đổi
2. Lưu trữ dữ liệu huấn luyện và kiểm thử trong thư mục `ml-service/datasets`
3. Cung cấp notebook minh họa quá trình phát triển và đánh giá mô hình

### Gửi lỗi và đề xuất

Khi gặp lỗi hoặc có đề xuất, vui lòng sử dụng Issues với format:

```
## Mô tả vấn đề
[Mô tả chi tiết vấn đề]

## Cách tái hiện
1. [Bước 1]
2. [Bước 2]
...

## Kết quả mong đợi
[Mô tả kết quả mong đợi]

## Môi trường
- Phiên bản Python:
- Hệ điều hành:
```

## Liên hệ

Nếu có câu hỏi hoặc cần hỗ trợ, vui lòng liên hệ với nhóm phát triển qua email: [thangdz1501@gmail.com] 