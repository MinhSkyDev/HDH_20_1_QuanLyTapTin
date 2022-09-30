"""
Ham chuyen tu HEX dang Little Endian sang DEC:
Vi du: 00 02 => 02 00(h) => 512(d)
Input: Hex Array (little Endian). Ex: h = ["00", "02"]
Output: Ket qua thap phan
"""


from tracemalloc import start


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
        ASCII_String += chr(int(i, 16))
    return ASCII_String


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
        print('So Byte tren 1 sector:', self.bytesPerSector)
        print('So Sector tren moi Cluster:', self.sectorsPerCluster)
        print('So sector vung BootSector:', self.ReservedSector)
        print('So bang FAT:', self.numOfFATs)
        print('Kich thuoc volume:', self.totalSectors*512/(1024**3), 'GB')
        print('So Sector moi bang FAT:', self.sectorsPerFAT)
        print('Dia chi bat dau cua Cluster:', self.rootClusterAddress)
        print('Loai FAT:', self.typeOfFAT)
