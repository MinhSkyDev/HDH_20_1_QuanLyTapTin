"""
Ham chuyen tu HEX dang Little Endian sang DEC:
Vi du: 00 02 => 02 00(h) => 512(d)
Input: Hex Array (little Endian). Ex: h = ["00", "02"]
"""


from lib2to3.pytree import convert
from tracemalloc import start
import numpy as np
import json


def convertHexLittleEndianStringToInt(hexArray):
    hexArray.reverse()
    hexStr = ""
    for i in range(len(hexArray)):
        hexStr += hexArray[i]
    i = int(hexStr, 16)
    return i


'''Ham chuyen tu mot mang Hex sang chuoi ASCII String
Input: Mang Hex: Ex: H = ['20', '32', '48']
Output: Chuoi ASCII. Ex: FAT32
'''


def convertHexStringToASCIIString(hexArray):
    ASCII_String = ""
    for i in hexArray:
        ASCII_String += chr((int(i, 16)))
    return ASCII_String


'''Class co chuc nang doc bang phan vung'''


class Partition:
    # Khoi tao. Truyen vao 2 tham so:
    # 1. Ten o dia
    # 2. Sector bat dau cua phan vung
    def __init__(self, diskName, startSector):
        # Doc du lieu Partition vao data
        self.sizeOfEntry = 32

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
            disk_fd.close()
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
        print('So Byte tren 1 sector:', self.bytesPerSector)
        print('So Sector tren moi Cluster:', self.sectorsPerCluster)
        print('So sector vung BootSector:', self.ReservedSector)
        print('So bang FAT:', self.numOfFATs)
        print('Kich thuoc volume:', self.totalSectors*512/(1024**3), 'GB')
        print('So Sector moi bang FAT:', self.sectorsPerFAT)
        print('Dia chi bat dau cua Cluster:', self.rootClusterAddress)
        print('Loai FAT:', self.typeOfFAT)


Partition1 = Partition('D:', 0)
# Partition1.printPartitionInfo()

sizeOfEntry = 32
index = Partition1.ReservedSector + Partition1.numOfFATs * Partition1.sectorsPerFAT
filePath = r"\\.\{0}".format('D:')


def read512bytes(start):
    with open(filePath, 'rb') as disk_fd:
        disk_fd.seek(index * 512 + start*512)
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
        disk_fd.close()
    return hexData


hexData = read512bytes(0)
Entry = []
start = 0
end = 32
count = 1
while True:
    temp = []
    temp = hexData[start:end]
    if temp[11] == "00":
        break
    if end >= 512:
        hexData = read512bytes(count)
        count += 1
        start = 0
        end = 32
        continue
    Entry.append(temp)
    start = end
    end += 32

# Đảo ngược list


def Reverse(lst):
    new_lst = lst[::-1]
    return new_lst

# Chia thành các entry chính và entry phụ


def devideEntry(data):
    flag = False
    listEntry = []
    for i in range(0, len(data)):
        temp = []
        if data[i][11] != "0f" and flag == False:
            listEntry.append(data[i])
        else:
            while data[i][11] == "0f":
                temp.append(data[i])
                i += 1
            temp.append(data[i])
            listEntry.append(temp)
            i += 1
    return listEntry


# print(devideEntry(Entry))
# file1 = open('myfile.txt', 'w')
# file1.write(json.dumps(devideEntry(Entry)))


class RDET:
    def __init__(self, data):
        self.data = data
        self.Entry = []

    def readSubEntry(self, data):
        # offset 1 => 10 byte:
        # offset E => lấy 14 byte
        # 28d => lấy 4
        name1 = convertHexStringToASCIIString((data[1:11]))
        name2 = convertHexStringToASCIIString((data[14:26]))
        name3 = convertHexStringToASCIIString((data[28:32]))

        return {
            "name1": name1,
            "name2": name2,
            "name3": name3
        }

    def readMainEntry(self, data):
        # Tên chính/ tên ngắn Offet: 0 lấy 8byte
        # Tên mở rộng offset 8 lấy 3 byte
        # Loại: offset B 1 byte
        # Kích thước tập tin 1C lấy 4byte
        # cluster bắt đầu 14(2byte) 1A(2byte)
        mainName = convertHexStringToASCIIString(data[0:8])
        wideName = convertHexStringToASCIIString(data[8:11])
        typ = bin(int(data[11], 16))
        size = convertHexLittleEndianStringToInt(data[28:32])
        cluster14 = Reverse(data[20:22])
        cluster1A = Reverse(data[26:28])
        cluster = cluster14 + cluster1A
        hexStr = ""
        for i in range(len(cluster)):
            hexStr += cluster[i]
        clusterStart = int(hexStr, 16)
        return {
            "mainName": mainName,
            "wideName": wideName,
            "type": typ,
            "size": size,
            "clusterStart": clusterStart
        }

    def readAllEntry(self):

        for i in range(0, len(self.data)):
            if len(self.data[i]) == 32:  # 1 Entry chính
                self.Entry.append(self.readMainEntry(self.data[i]))
            else:
                temp = []
                data = self.data[i]
                k = 0
                while data[k][11] == '0f':
                    temp.append(self.readSubEntry(data[k]))
                    k += 1
                temp.append(self.readMainEntry(data[k]))
                i += 1
                self.Entry.append(temp)
        return self.Entry


a = RDET(devideEntry(Entry))

# print(a.readMainEntry(["55", "42", "55", "4e", "54", "55", "20", "32", "30", "5f", "30", "08", "00", "00", "00",
#                        "00", "00", "00", "00", "00", "00", "00", "43", "a2", "3b", "55", "00", "00", "00", "00", "00", "00"]))

# print(a.readSubEntry(["42", "20", "00", "49", "00", "6e", "00", "66", "00", "6f", "00", "0f", "00", "72",
#       "72", "00", "6d", "00", "61", "00", "74", "00", "69", "00", "6f", "00", "00", "00", "6e", "00", "00", "00"]))

print(a.readAllEntry())
