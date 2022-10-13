from tracemalloc import start
import numpy as np
import json
from Partition import *
from convert import *


sizeOfEntry = 32


class RDET:
    # Đầu vào là giá trị index(giá trị bắt đầu của RDET)
    def __init__(self, index, filePath):
        self.index = index
        self.Entry = []
        self.filePath = filePath
    # Hàm đọc data đọc 512byte 1 lần
    # hàm trả về [[],[],[]] chưa phân định được Entry phụ của Entry chính nào

    def readData(self):
        hexData = self.read512bytes(0)
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
                hexData = self.read512bytes(count)
                count += 1
                start = 0
                end = 32
                continue
            Entry.append(temp)
            start = end
            end += 32
        return Entry

    def read512bytes(self, start):
        filePath = r"\\.\{0}".format(self.filePath)
        with open(filePath, 'rb') as disk_fd:
            disk_fd.seek(self.index * 512 + start*512)
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

    def Reverse(self, lst):
        new_lst = lst[::-1]
        return new_lst
    # Hàm này sẽ xác định Entry phụ thuộc Entry chính nào

    def devideEntry(self, data):
        listEntry = []
        i = 0
        while i < len(data):
            temp = []
            if data[i][0] == 'e5':
                i = i + 1
            elif data[i][11] != "0f":
                listEntry.append(data[i])
                i += 1
            else:
                while data[i][11] == "0f":
                    temp.append(data[i])
                    i += 1
                temp.append(data[i])
                listEntry.append(temp)
                i += 1
        return listEntry

    def readSubEntry(self, data):
        # offset 1 => 10 byte:
        # offset E => lấy 14 byte
        # 28d => lấy 4
        name1 = convertHexStringToASCIIString((data[1:11]))
        name2 = convertHexStringToASCIIString((data[14:26]))
        name3 = convertHexStringToASCIIString((data[28:32]))
        return name1+name2+name3
    # Xác định dạng file

    def defineType(self, data):
        if data == '0x01':
            return "Read only"
        elif data == "0x02":
            return "Hidden"
        elif data == "System":
            return "System"
        elif data == "0x08":
            return "Volume Label"
        elif data == '0x10':
            return "Subdirectory"
        elif data == "0x20":
            return "Archive"
        elif data == "0x40":
            return "Device"
        else:
            return "Unused"

    def readMainEntry(self, data):
        # Tên chính/ tên ngắn Offet: 0 lấy 8byte
        # Tên mở rộng offset 8 lấy 3 byte
        # Loại: offset B 1 byte
        # Kích thước tập tin 1C lấy 4byte
        # cluster bắt đầu 14(2byte) 1A(2byte)
        mainName = convertHexStringToASCIIString(data[0:8])
        wideName = convertHexStringToASCIIString(data[8:11])
        typ = self.defineType(hex(int(data[11], 16)))
        size = convertHexLittleEndianStringToInt(data[28:32])
        cluster14 = self.Reverse(data[20:22])
        cluster1A = self.Reverse(data[26:28])
        cluster = cluster14 + cluster1A
        hexStr = ""
        for i in range(len(cluster)):
            hexStr += cluster[i]
        clusterStart = int(hexStr, 16)
        if typ == 'Subdirectory':
            return {
                "name": f"{mainName.strip()}",
                "type": typ,
                "size": size,
                "clusterStart": clusterStart
            }
        else:
            return {
                "name": f"{mainName.strip()}.{wideName.strip()}",
                "type": typ,
                "size": size,
                "clusterStart": clusterStart
            }
    # Đọc tất cã các Entry có trong data

    def readAllEntry(self):
        self.data = self.devideEntry((self.readData()))
        # data ở đây là các Entry đạ được chia ra. Có dạng [[Entry chính],[[Entry phụ 1],[Entry phụ 2],[Entry chính]]]
        for i in range(0, len(self.data)):
            if len(self.data[i]) == 32:  # 1 Entry chính
                mainEntry = self.readMainEntry(self.data[i])
                if mainEntry["type"] == 'Unused':
                    continue
                self.Entry.append(mainEntry)
            else:
                temp = []
                data = self.data[i]
                k = 0
                while data[k][11] == '0f':
                    temp.append(self.readSubEntry(data[k]))
                    k += 1
                temp.append(self.readMainEntry(data[k]))
                mainEntry = self.readMainEntry(data[k])
                if mainEntry["type"] == 'Unused':
                    continue
                i += 1
                self.Entry.append(temp)
        newEntry = []
        # cái này dùng để cộng các tên Entry phụ lại với nhau
        for i in self.Entry:
            if type(i) is list:
                i.reverse()
                newName = ""
                tmp = []
                for k in range(0, len(i)):
                    if k == 0:
                        tmp.append(i[0])
                        continue

                    newName += i[k]
                tmp[0]["submainName"] = newName
                newEntry.append(tmp)
            else:
                newEntry.append(i)

        rs = self.getOnlyFile(newEntry)
        return ((rs))
    # Lọc các file dư

    def getOnlyFile(self, data):
        rs = []
        for i in data:
            if type(i) is list:
                rs.append(i[0])
            else:
                rs.append(i)

        existing_dicts = set()
        filtered_list = []
        for d in rs:
            if (d['name']) not in existing_dicts:
                existing_dicts.add((d['name']))
                filtered_list.append(d)
        return filtered_list
