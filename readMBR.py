import os
from converter import *
# Class này có constructor nhận vào fileName và đọc lên MBR tương ứng


class MasterBootRecord:

    # Hàm khởi tạo sẽ có 1 tham số
    # 1: Tên ổ đĩa, nếu không truyền tham số thì sẽ mặc định là truyền địa chỉ usb
    def __init__(self, fileName="PhysicalDrive1"):
        self.size = 512
        filePath = r"\\.\{0}".format(fileName)
        disk_fd = open(filePath, mode="rb")
        print('a')
        data = disk_fd.read(self.size)
        self.data = []
        # Chuẩn hóa dữ liệu về dạng chuẩn thông thường
        self.__standardizeMBR(data)

        # Thuộc tính chứa mô tả 4 phân vùng
        self.partitions = []
        self.__getPartitions()

        # Mảng 1 chiều chứa 4 phần tử chứa thông tin về sector bắt đầu của ổ đĩa
        self.startSectors = []
        self.__setStartSector()

        # Dùng để xác định loại ổ đĩa
        self.partitionType_dictionary = {
            "0B": "FAT32",
            "07": "NTFS",
            "00": "Empty"
        }

    '''---------------GETTER--------------- '''

    def getSize(self):
        return self.size

    def getMBR(self):
        return self.data
        # Lấy các sector bắt đầu của chương trình

    def getStartSector_Partition1(self):
        return self.startSectors[0]

    def getStartSector_Partition2(self):
        return self.startSectors[1]

    def getStartSector_Partition3(self):
        return self.startSectors[2]

    def getStartSector_Partition4(self):
        return self.startSectors[3]

    # Các hàm này dùng để xác định loại ổ đĩa cho từng phân vùng
    # Trả về chuỗi tương ứng với loại ổ đĩa
    # Ví dụ phân vùng 1 là loại FAT32 => Trả về FAT32
    def getStatusPartition1(self):
        return self.__getStatus(0)

    def getStatusPartition2(self):
        return self.__getStatus(1)

    def getStatusPartition3(self):
        return self.__getStatus(2)

    def getStatusPartition4(self):
        return self.__getStatus(3)

    '''---------------PRIVATE METHOD--------------- '''

    def __standardizeMBR(self, data):
        for i in range(0, self.size):
            # giá trị data[i] hiện tại ở dạng số từ 0 -> 255, convert về hex
            data_toHex = hex(data[i])
            # trả về ở lệnh trên ở dạng 0xMãHex, lệnh này để lọc bớt đi 0x
            data_toHex_standardize = data_toHex[2:]
            if (len(data_toHex_standardize) != 2):
                data_toHex_standardize = "0" + data_toHex_standardize
            self.data.append(str(data_toHex_standardize))

    # Lấy được địa chỉ 4 sector bắt đầu của phân vùng
    def __getPartitions(self):
        partition_1 = self.data[446:462]
        partition_2 = self.data[462:478]
        partition_3 = self.data[478:494]
        partition_4 = self.data[494:510]
        self.partitions.append(partition_1)
        self.partitions.append(partition_2)
        self.partitions.append(partition_3)
        self.partitions.append(partition_4)
        for i in range(0, 4):
            print("Thông tin phân vùng ", i, ": ", self.partitions[i])

    # Tính toán sector bắt đầu của từng phân vùng
    def __setStartSector(self):
        for i in range(0, 4):
            startSector = convertHexLittleEndianStringToInt(
                self.partitions[i][8:12])
            print("Sector bắt đầu của phân vùng ", i, ": ", startSector)
            self.startSectors.append(startSector)

    def __getStatus(self, partition_id):
        id = self.partitions[partition_id][0]
        status = self.partitionType_dictionary[id]
        return status

    '''---------------PUBLIC METHOD--------------- '''
    # Duyệt xem MBR có gì

    def indexMBR(self):
        for i in range(0, self.size):
            if (i % 16 == 0):
                print("\n")
            else:
                print(self.data[i], end=" ")
