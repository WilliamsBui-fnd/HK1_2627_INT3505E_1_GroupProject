# B8 — Analysis note: GET /tasks

## Endpoint và cách đo

Chọn `GET /tasks?limit=10` vì đây là chức năng xem danh sách công việc chính của Tasks API. Request dùng Bearer token hợp lệ. Theo OpenAPI, response thành công là HTTP 200 với `items` và `total`.

Thử nghiệm ngày 17/11/2026 trên bản sao repo nhóm tại commit `7f0446c`, dùng Flask development server trên máy cá nhân. Ứng dụng lưu task trong bộ nhớ, không dùng cơ sở dữ liệu. Chuẩn bị 10 task trước khi đo; trong lúc đo chỉ đọc danh sách.

Locust chạy **10 users, spawn rate 2 user/s, 30 giây**, mỗi user chờ ngẫu nhiên 1–3 giây giữa các request. Không giả lập lỗi. Bearer token được gửi trong mỗi request.

## Kết quả thực tế

| Requests | Failures | Failure rate | RPS | Trung bình | p95 | Lớn nhất |
|---:|---:|---:|---:|---:|---:|---:|
| 141 | 0 | 0% | 4.77 | 3.95 ms | 6 ms | 14 ms |

Nguồn: [báo cáo Locust](../reports/tasks-load.html). Lượt chạy đạt đủ 10 users và không ghi nhận exception. RPS khoảng 4.77 phù hợp với thời gian chờ của 10 users; đây không phải thông lượng tối đa của API.

## SLO đề xuất và giải thích

Đề xuất ban đầu cho thao tác xem danh sách: **p95 < 300 ms và failure rate < 1%**, kiểm tra ở mức tải 10 users như trên. p95 < 300 ms nghĩa là ít nhất khoảng 95% request phải hoàn thành dưới 300 ms. Ngưỡng này dành cho một thao tác đọc ngắn, giúp phản hồi danh sách nhanh và có khoảng dự phòng so với kết quả local. Failure rate < 1% đặt mục tiêu ít nhất 99% request hợp lệ được phục vụ thành công. Đây là mục tiêu đề xuất cho đồ án, chưa phải cam kết đã thống nhất với người dùng.

Lượt đo có p95 = 6 ms và failure rate = 0%, nên **đạt hai ngưỡng đề xuất trong điều kiện thử nghiệm này**. Không có lỗi HTTP hoặc lỗi giả lập được ghi nhận; với token hợp lệ, kết quả mong đợi của endpoint là HTTP 200.

## Giới hạn và kết luận

Mới đo một lần trong 30 giây, chỉ có 141 request và 10 task. Locust và API cùng chạy trên một máy nên chưa phản ánh mạng thực, dữ liệu lớn hoặc tài nguyên production. Thời gian đo từ client Locust không bao gồm thời gian giao diện hiển thị kết quả. Lưu trữ trong bộ nhớ cũng không phản ánh chi phí truy cập database khi dự án bổ sung sau này.

Vì vậy, kết quả là baseline ban đầu cho `GET /tasks`, chưa chứng minh SLO dài hạn hay khả năng chịu tải tối đa. Trước khi áp dụng ở production, cần đo lặp lại trên môi trường triển khai, với dữ liệu và tải dự kiến; sau đó xác nhận hoặc điều chỉnh SLO.
