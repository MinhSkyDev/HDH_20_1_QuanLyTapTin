from tracemalloc import start
from converter import *
import os

'''Class có chức năng đọc bảng phân vùng BootSector của FAT32'''


class BootSector:
    # Khoi tao. Truyen vao 2 tham so:
    # 1. Ten o dia
    # 2. Sector bat dau cua phan vung
    def __init__(self, diskName, startSector):
        # Doc du lieu Partition vao data
        self.data = self.__getBootSector(diskName, startSector)
        self.__getPartitionInfo()

    # Khoi tao overloading. Truyen vao 1 tham so:
    # 2. Sector bắt đầu của phân vùng, tên ổ đĩa mặc định là PhysicalDrive1 (USB)
    # def __init__(self, startSector):
    #     diskName = "PhysicalDrive1"
    #     self.data = self.__getBootSector(diskName, startSector)
    #     self.__getPartitionInfo()

    # Hàm đọc du lieu cua sector dau tien cua phan vung (chua cac thong tin can thiet)
    def __getBootSector(self, diskName, startSector):
        filePath = r"\\.\{0}".format(diskName)
        disk_fd = open(filePath, mode="rb")
        startByte = startSector * 512  # Phải chuyển từ sector sang byte
        disk_fd.seek(startByte)
        self.size = 512
        data = disk_fd.read(self.size)
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

    # Ham tach cac thanh phan trong BootSector
    def __getPartitionInfo(self):
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

    # Ham xuat cac thanh phan trong BootSector
    def printPartitionInfo(self):
        print('So Byte tren 1 sector:', self.bytesPerSector)
        print('So Sector tren moi Cluster:', self.sectorsPerCluster)
        print('So sector vung BootSector:', self.ReservedSector)
        print('So bang FAT:', self.numOfFATs)
        print('Kich thuoc volume:', self.totalSectors*512/(1024**3), 'GB')
        print('So Sector moi bang FAT:', self.sectorsPerFAT)
        print('Dia chi bat dau cua RDET:', self.rootClusterAddress)
        print('Loai FAT:', self.typeOfFAT)

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
