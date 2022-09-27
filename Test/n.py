import os
disk_fd = os.open(r"\\.\D:", os.O_RDONLY | os.O_BINARY)
data = os.read(disk_fd, 512)
print(data)
os.close(disk_fd)
