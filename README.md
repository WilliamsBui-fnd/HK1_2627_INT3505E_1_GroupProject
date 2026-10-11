# Tasks API — Bài tập B4

Đây là REST API đơn giản để quản lý công việc, được xây dựng bằng Flask và mô tả bằng OpenAPI 3.0.3. Dự án có sẵn Swagger UI để xem tài liệu và thử API trực tiếp trên trình duyệt.

## Chức năng chính

- Thêm, xem, cập nhật và xóa task.
- Lọc task theo trạng thái và giới hạn số lượng kết quả.
- Xác thực các endpoint bằng Bearer token.
- Kiểm tra dữ liệu đầu vào theo schema trong `openapi.yaml`.
- Trả lỗi theo định dạng `application/problem+json`.

## Cấu trúc thư mục

```text
tasks-api/
├── app.py
├── openapi.yaml
├── templates/docs.html
├── requirements.txt
├── requirements-dev.txt
├── test_app.py
├── .gitignore
└── README.md
```

## Cài đặt và chạy

Yêu cầu Python 3.10 trở lên.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python app.py
```

Sau khi chạy, truy cập:

- Swagger UI: http://127.0.0.1:5000/docs
- OpenAPI JSON: http://127.0.0.1:5000/openapi.json

Nếu cổng `5000` đang được sử dụng, có thể đổi sang cổng khác:

```sh
python -m flask --app app run --port 5001
```

## Thử API bằng Swagger UI

Nhấn **Authorize** và nhập token `demo-token` (không cần thêm chữ `Bearer`). Sau đó có thể thử lần lượt các endpoint ngay trên Swagger UI.

Ví dụ body để tạo task:

```json
{
  "title": "Hoàn thành bài tập B4",
  "priority": "high",
  "dueDate": "2026-10-18"
}
```

Token mặc định có thể thay đổi bằng biến môi trường:

```sh
export TASKS_API_TOKEN='token-rieng-cua-ban'
python app.py
```

Không đưa token riêng lên GitHub. Hai đường dẫn `/docs` và `/openapi.json` không yêu cầu xác thực.

## Các endpoint

| Method | Path | Thành công | Chức năng |
|---|---|---|---|
| GET | `/tasks` | 200 | Lấy danh sách task |
| POST | `/tasks` | 201 | Tạo task mới |
| GET | `/tasks/{taskId}` | 200 | Lấy chi tiết một task |
| PATCH | `/tasks/{taskId}` | 200 | Cập nhật một phần task |
| DELETE | `/tasks/{taskId}` | 204 | Xóa task |

Mỗi task gồm `id`, `title`, `status`, `priority` và hai trường không bắt buộc là `dueDate`, `assigneeId`.

- `status`: `open` hoặc `done`, mặc định là `open`.
- `priority`: `low`, `normal` hoặc `high`, mặc định là `normal`.
- `dueDate`: ngày theo định dạng `YYYY-MM-DD`.
- `assigneeId`: chuỗi UUID.

`GET /tasks` hỗ trợ hai query parameter là `status` và `limit`. Giá trị `limit` nằm trong khoảng từ 1 đến 100, mặc định là 10.

## Một số lựa chọn thiết kế

### Tách schema tạo và cập nhật task

Khi tạo task, trường `title` là bắt buộc. Khi cập nhật bằng `PATCH`, người dùng chỉ cần gửi những trường muốn thay đổi. Vì vậy dự án dùng hai schema riêng là `CreateTaskInput` và `UpdateTaskInput` thay vì dùng chung một schema cho cả hai trường hợp.

Các thành phần dùng lại như `Task`, parameter và response được khai báo trong `components` của OpenAPI để tránh lặp lại nội dung.

### Dùng `openapi.yaml` làm đặc tả chung

Ứng dụng đọc trực tiếp `openapi.yaml` để trả về `/openapi.json`, hiển thị Swagger UI và kiểm tra dữ liệu đầu vào. Cách này giúp phần mô tả API và phần xử lý trong ứng dụng thống nhất với nhau.

## Kiểm thử

Chạy test và kiểm tra file OpenAPI bằng các lệnh sau:

```sh
python -m unittest -v
python -m openapi_spec_validator openapi.yaml
```

Bộ test kiểm tra các thao tác CRUD, lọc danh sách, giới hạn kết quả, Bearer token, dữ liệu không hợp lệ và cấu trúc response theo đặc tả OpenAPI.
