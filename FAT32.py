from converter import *


class FAT32Table:
    # Khoi tao. Truyen vao 2 tham so:
    # 1. Ten o dia
    # 2. Sector bat dau cua phan vung

    def __init__(self, diskName, startSector):
        # Doc du lieu Partition vao data
        self.data = self.readFullFATTable(diskName, startSector)
        self.diskName = diskName

    def readOneSector(self, diskName, i):
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
    # Doc toan bo bang FAT, luu data vao mang 1 chieu data (luu y: da bo 8byte dau khong su dung)

    def readFullFATTable(self, diskName, startFATSector):
        count = 1
        data = []
        temp = self.readOneSector(diskName, startFATSector)
        data.append(temp)
        while (temp[len(temp) - 1] != '00'):
            temp = self.readOneSector(diskName, startFATSector + count)
            count = count + 1
            data.append(temp)
        handleData = []
        for sector in data:
            for element in sector:
                handleData.append(element)
        for i in range(0, 8):
            handleData.pop(0)
        return handleData
    # Chuyen ve duoi dang 1 list cac Cluster

    def convertFATElementToCluster(self):
        data = self.data
        clusterList = [None, None]
        i = 0
        for i in range(0, len(data) - 4, 4):
            if (data[i + 3]) == '0f':
                clusterList.append(-1)
            else:
                temp = []
                temp.append(data[i])
                temp.append(data[i + 1])
                temp.append(data[i + 2])
                temp.append(data[i + 3])
                x = convertHexLittleEndianStringToInt(temp)
                if (x == 0):
                    break
                clusterList.append(x)
        return clusterList

    # Ham nay co chuc nang tim danh sach cluster tu 1 cluster bat dau
    def getClusterList(self, initCluster):
        data = self.convertFATElementToCluster()
        list = []
        curCluster = initCluster
        list.append(curCluster)
        while (data[curCluster] != -1):
            curCluster = data[curCluster]
            list.append(curCluster)
        return list

    # Ham nay co chuc nang lay noi dung file
    # va tra ve duoi dang chuoi (string)
    def getContentFromClusterList(self, clusterList, partitionFirstSector, reservedSectors, numOfFATs,
                                  sectorsPerFAT, sectorsPerCluster):
        list = []
        rootIndex = partitionFirstSector + reservedSectors + sectorsPerFAT * numOfFATs
        for cluster in clusterList:
            index = rootIndex + sectorsPerCluster * (cluster - 2)
            for i in range(sectorsPerCluster):
                list.append(self.readOneSector(self.diskName, index + i))
        return list

    def getASCIIContent(self, list):
        content = ""
        for sector in list:
            temp = convertHexStringToASCIIString(sector)
            content += temp
        return content


# a = FAT32Table('D:', 2664)
# data = a.getContentFromClusterList(a.getClusterList(6), 0, 2664, 2, 15052, 32)
# print(data)
