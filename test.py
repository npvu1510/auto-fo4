import time

# Lấy thời gian hiện tại bằng time.time()
timestamp = time.time()

# Chia thành phần trước và phần sau dấu chấm
seconds = int(timestamp)
milliseconds = int((timestamp - seconds) * 1000000)  # Chuyển phần thập phân thành microseconds

# Hiển thị kết quả
print(f"Phần trước dấu chấm: {seconds}")
print(f"Phần sau dấu chấm: {milliseconds}")
print(f"Kết quả cuối: {str(seconds) + str(milliseconds)}")


print(172421207094746 - 1724212065277909)