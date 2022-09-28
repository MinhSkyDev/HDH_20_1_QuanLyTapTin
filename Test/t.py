import os

oneSectorSize = 512  # Kích thước của một Sector

# Nhận vào tên của thư mục muốn kiểm tra, trả về MBR của thư mục đó


# Output trả về là dạng mảng


def readOneSector(filename):
    filePath = r"\\.\{0}".format(filename)
    disk_fd = os.open(filePath, os.O_RDONLY | os.O_BINARY)
    data = os.read(disk_fd)
    # print(data)
    return data

# Duyệt sector


def indexMBR(data):
    MBR = []
    for i in range(0, 512):
        if (i % 16 == 0):
            print("\n")
        # giá trị data[i] hiện tại ở dạng số từ 0 -> 255, convert về hex
        data_toHex = hex(data[i])
        # trả về ở lệnh trên ở dạng 0xMãHex, lệnh này để lọc bớt đi 0x
        data_toHex_remove0x = data_toHex[2:]
        MBR.append(data_toHex_remove0x)
    return MBR


def readPartition(MBR):

    partition = []

    for i in range(0, len(MBR)):
        if i >= 446 and i <= 509:
            partition.append(MBR[i])
    listPartition = []
    temp = []
    count = 0
    for i in range(0, len(partition)):
        count += 1
        temp.append(partition[i])
        if count == 16:
            listPartition.append(temp)
            temp = []
            count = 0

    return listPartition


def main():
    diskName = "D:"
    data = readOneSector(diskName)
    MBR = indexMBR(data)
    # print(MBR)
    partition = readPartition(MBR)
    print(partition)


main()
