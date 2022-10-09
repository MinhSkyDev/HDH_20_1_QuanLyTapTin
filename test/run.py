from asyncio import start_server
from FAT32 import *
from RDET import *
from Partition import *
from SDET import *
from convert import *

idx = 1


class READING_FAT32:
    def __init__(self, diskName, startSector):
        self.partition = Partition(diskName, startSector)
        self.partition.printPartitionInfo()
        self.RDET = RDET(self.partition.getReservedSector() + self.partition.getNumOfFATs()
                         * self.partition.getSectorsPerFAT() + startSector, diskName)
        self.FATTable = FAT32Table(
            diskName, self.partition.getReservedSector() + startSector)
        # Danh sach tep tin va thu muc tren o dia
        self.Folder_File_Name = self.getFileNFolderList()
        self.startSector = startSector
        self.diskName = diskName

    # Doc danh sach tep tin va thu muc tren o dia
    def getFileNFolderList(self):
        return self.RDET.readAllEntry()

    # Lay danh sach thu muc tu 1 danh sach gom thu muc va file
    def getFolder(self, Folder_File_Name):
        FolderList = []
        for element in Folder_File_Name:
            if element['type'] == 'Subdirectory':
                if 'submainName' in element:
                    FolderList.append(
                        {'name': element['submainName'], 'clusterStart': element['clusterStart']})
                else:
                    FolderList.append(
                        {'name': element['name'], 'clusterStart': element['clusterStart']})
        return FolderList

    # Lay file SDET cua thu muc, truyen vao Cluster bat dau cua thu muc
    def getSDETOfFolder(self, clusterStartOfFolder):
        clusterList = self.FATTable.getClusterList(clusterStartOfFolder)
        data = (self.FATTable.getContentFromClusterList(clusterList, self.startSector, self.partition.getReservedSector(),
                                                        self.partition.getNumOfFATs(), self.partition.getSectorsPerFAT(), self.partition.getSectorsPerCluster()))
        # Tra ve mang 1 chieu gom cac cluster chua noi dung SDET
        handleData = []
        for sector in data:
            for i in sector:
                handleData.append(i)
        return handleData

    # Lay danh sach tep tin
    def getFile(self, Folder_File_Name):
        FileList = []
        for element in Folder_File_Name:
            if element['type'] == 'Archive':
                if 'submainName' in element:
                    FileList.append(
                        {'name': element['submainName'], 'clusterStart': element['clusterStart'], 'FileSize': element['size']})
                else:
                    FileList.append(
                        {'name': element['name'], 'clusterStart': element['clusterStart'], 'FileSize': element['size']})
        return FileList

    def getContentFile(self, fileName, Folder_File_Name):
        fileList = self.getFile(Folder_File_Name)
        selectedFile = None
        for file in fileList:
            if file['name'] == fileName:
                selectedFile = file
        fileSize = selectedFile['FileSize']
        if (fileSize == 0):
            return ""
        clusterList = self.FATTable.getClusterList(
            selectedFile['clusterStart'])
        content = self.FATTable.getContentFromClusterList(clusterList, self.startSector, self.partition.getReservedSector(),
                                                          self.partition.getNumOfFATs(), self.partition.getSectorsPerFAT(), self.partition.getSectorsPerCluster())
        data = self.FATTable.getASCIIContent(content)
        handleData = ''
        for i in range(fileSize):
            handleData += data[i]
        return handleData

    def printCurrentFolder(self, level, Name):
        print(level * '     ' + Name)

    def printTree(self, data, level):
        for item in data:
            if (item['type'] == 'Archive'):
                if 'submainName' in item:
                    self.printCurrentFolder(level, item['submainName'])
                else:
                    self.printCurrentFolder(level, item['name'])
        for item in data:
            if (item['type'] == 'Subdirectory'):
                if 'submainName' in item:
                    self.printCurrentFolder(level, item['submainName'])
                else:
                    self.printCurrentFolder(level, item['name'])
                s = SDET(self.getSDETOfFolder(item['clusterStart']))
                xdata = s.readAllEntry()
                self.printTree(xdata, level + 1)

    def aaa(self, data, level, list, parentId, rootId):
        global idx
        for item in data:
            item['id'] = idx
            item['parentId'] = parentId
            item['rootId'] = rootId
            idx += 1
            list.append(item)
        for item in data:
            if (item['type'] == 'Subdirectory'):
                # print(self.getSDETOfFolder(item['clusterStart']))
                s = SDET(self.getSDETOfFolder(item['clusterStart']))
                xdata = s.readAllEntry()
                self.aaa(xdata, level + 1, list, item['id'], rootId + 1)
        return list

    def printFileInFolder(self, folderName):
        listFile = self.aaa(self.Folder_File_Name, 1, [], 0, 1)
        id = -1
        for i in listFile:
            if "submainName" in i:
                if i['submainName'] == folderName:
                    id = i['id']
            else:
                if i['name'] == folderName:
                    id = i['id']
        if id == -1:
            print("No folder name!")
            return
        list = []
        for i in listFile:
            if i['parentId'] == id:
                list.append(i)
        return list


# a = READING_FAT32('PhysicalDrive1', 224)
# print(a.aaa(a.Folder_File_Name, 1, [], 0, 1))
# a.printTree(a.Folder_File_Name, 1)
# print(a.printTree(a.Folder_File_Name, 1))
# XU LI THU MUC
# b = a.getFolder()
# c = a.getSDETOfFolder(6)
# d = SDET(c)

# print(d.devideEntry(d.data))

# print(d.readAllEntry())
# XU LI TEP TIN
# x = a.getFile()
# print('*********************')
# print(y)
