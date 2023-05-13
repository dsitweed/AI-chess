Sử dụng thuật toán negamax - biến thể của minimax (nhưng cốt lõi vẫn dựa vào minimax) để lựa chọn đường đi
1. Anpha càng lớn càng có lợi cho trắng
2. Bepha càng nhỏ thì càng có lợi cho đen

WHITE đi với hệ số dương
BLACK đi với hệ số âm
1. Nếu trả về giá trị
- trả về 9999 Trắng thắng
- Trả về -9999 Trắng thua - đen thắng
2. a

4 Bước tinh toán các tham số để ra được tri thúc bổ sung heuristic
1. Firstly, let’s check if the game is still going on.
2. Secondly, we must calculate the total number of pieces so that we can pass it into our material function.
3. Third, let’s calculate the scores: material score and individual pieces score


Tạo 1 adapter chuyển sang nước đi kiểu chess board 
- tạo nước đi ngẫu nhiên cho nó tự oánh với nhau 