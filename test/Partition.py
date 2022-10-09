from convert import *

'''Class co chuc nang doc bang phan vung'''


class Partition:
    # Khoi tao. Truyen vao 2 tham so:
    # 1. Ten o dia
    # 2. Sector bat dau cua phan vung
    def __init__(self, diskName, startSector):
        # Doc du lieu Partition vao data
        def readOneSector(diskName, i):
            filePath = r"\\.\{0}".format(diskName)
            with open(filePath, 'rb') as disk_fd:
                disk_fd.seek(i * 512)
                data = disk_fd.read(512)
                hexData = []
                for i in range(0, 512):
                    # giá trị data[i] hiện tại ở dạng số từ 0 -> 255, convert về hex
                    data_toHex = hex(data[i])
                    # trả về ở lệnh trên ở dạng 0xMãHex, lệnh này để lọc bớt đi 0x
                    data_toHex_remove0x = data_toHex[2:]
                    if (len(data_toHex_remove0x) != 2):
                        data_toHex_remove0x = "0" + data_toHex_remove0x
                    hexData.append(data_toHex_remove0x)
            return hexData
        self.data = readOneSector(diskName, startSector)
        self.getPartitionInfo()

    # ham doc cac thong so quan trong cua phan vung

    def getPartitionInfo(self):
        # So Byte tren 1 sector
        self.bytesPerSector = convertHexLittleEndianStringToInt(
            self.data[11:13])
        # So sector cua moi Cluster
        self.sectorsPerCluster = convertHexLittleEndianStringToInt(
            self.data[13:14])
        # So sector truoc bang FAT (la so sector cua vung BootSector)
        self.ReservedSector = convertHexLittleEndianStringToInt(
            self.data[14:16])
        self.numOfFATs = convertHexLittleEndianStringToInt(
            self.data[16:17])
        self.totalSectors = convertHexLittleEndianStringToInt(
            self.data[32:36])
        self.sectorsPerFAT = convertHexLittleEndianStringToInt(
            self.data[36:40])
        self.rootClusterAddress = convertHexLittleEndianStringToInt(
            self.data[44:48])
        self.typeOfFAT = convertHexStringToASCIIString(self.data[82:90])

    def printPartitionInfo(self):
        print('Số Byte trên 1 sector:', self.bytesPerSector)
        print('Số Sector trên mỗi Cluster:', self.sectorsPerCluster)
        print('Số Sector vùng BootSector:', self.ReservedSector)
        print('Số bảng FAT:', self.numOfFATs)
        print('Kích thước Volume:', self.totalSectors*512/(1024**3), 'GB')
        print('Số Sector mỗi bảng FAT:', self.sectorsPerFAT)
        print('Địa chỉ bắt đầu của Cluster:', self.rootClusterAddress)
        print('Loại FAT:', self.typeOfFAT)
    # GETTER

    def getBytesPerSector(self):
        return self.bytesPerSector

    def getSectorsPerCluster(self):
        return self.sectorsPerCluster

    def getReservedSector(self):
        return self.ReservedSector

    def getNumOfFATs(self):
        return self.numOfFATs

    def getTotalSector(self):
        return self.totalSectors

    def getSectorsPerFAT(self):
        return self.sectorsPerFAT

    def getRootClusterAddress(self):
        return self.rootClusterAddress

    def getTypeOfFAT(self):
        return self.typeOfFAT
