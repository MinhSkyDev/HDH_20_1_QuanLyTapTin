import os

oneSectorSize = 10248  # Kích thước của một Sector

# Nhận vào tên của thư mục muốn kiểm tra, trả về MBR của thư mục đó


# Output trả về là dạng mảng


def readOneSector(filename):
    filePath = r"\\.\{0}".format(filename)
    disk_fd = os.open(filePath, os.O_RDONLY | os.O_BINARY)
    data = os.read(disk_fd, oneSectorSize)
    # print(data)
    return data

# Duyệt sector


def readDisk(filename):
    filePath = r"\\.\{0}".format(filename)
    disk_fd = os.open(filePath, os.O_RDONLY | os.O_BINARY)
    data = os.read(disk_fd, 10248)
    # print(data)
    return data


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
    disk = readDisk(diskName)
    MBR = indexMBR(data)
    # print(MBR)
    print(disk)
    partition = readPartition(MBR)
    print(partition)


def findAddressBootsector(data):
    temp = ""
    for i, e in reversed((list(enumerate(data)))):
        if i <= 11 and i >= 8:
            temp += e
    res = (int(temp, 16))
    return hex(res*512)


main()
