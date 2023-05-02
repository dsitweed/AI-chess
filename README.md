## Các tri thức bổ sung
### 1. Mỗi con cờ có 1 giá trị khác nhau


## Suy nghĩ cải tiến chương trình
### 1. Thêm thư viện python-chess để sinh ra các nước đi, xác thực các nước đi, lưu trữ tập các kết thúc có giá trị cho phần phân tích AI
### 2. Thêm timer = pygame.time.Clock()
### 3. Thêm màn hình start - thêm màn hình chiến thắng [Git hướng dẫn](https://github.com/mandrelbrotset/pygame-chess/tree/master)
### 4. Thêm hướng dẫn ở chân bàn cờ, thêm cột bên phải để chứa các quân cờ đã ăn [Hướng dẫn trên youtube - phần đầu](https://www.youtube.com/watch?v=X-e0jk4I938)

## Luồng chạy của chương trình
1. Khi chọn con cờ lưu trữ các nước đi hợp lệ của nó vào attribute của instance đó 


## BUG
1. Nhấn vào thì tính các đường đi hợp lệ
2. Nếu quân ta đi vào những vị trí đã hợp lệ từ trước thì không phân biệt được quân ta và quân địch
3. Nguyên nhân: - khi di chuyển chưa cập nhật vị trí của quân. Hàm calculate có vấn đề