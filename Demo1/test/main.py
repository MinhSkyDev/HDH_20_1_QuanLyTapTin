from run import *
from MBR import *


def ReadPartition(diskName, startSector):

    print('-----------Thông tin của phân vùng: -------------')
    FAT32 = READING_FAT32(diskName, startSector)
    # Xuat cay thu muc goc
    print('-----------------------------------------')
    print('Xuất cây thư mục gốc: \n')
    root = FAT32.aaa(FAT32.Folder_File_Name, 1, [], 0, 1)
    partition = FAT32.partition
    for item in root:
        if (item['rootId'] == 1):
            size = item['size']
            clusterStart = item['clusterStart']
            if clusterStart != 0:
                FATTBLE = FAT32.FATTable

                clusterList = FATTBLE.getClusterList(clusterStart)

                firstSector = partition.getReservedSector() + partition.getSectorsPerFAT() * \
                    partition.getNumOfFATs() + startSector + \
                    partition.getSectorsPerCluster() * (clusterStart - 2)
                lengthOfClusterList = len(clusterList)
                lastSector = firstSector + partition.getSectorsPerCluster() * lengthOfClusterList
            if 'submainName' in item:
                if size != 0:
                    print(
                        f"Name: {item['submainName']}, Size: {item['size']}, Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")
                else:
                    print(
                        f"Name: {item['submainName']}, Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")
            else:
                if size == 0:
                    print(
                        f"Name: {item['name']}, Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")
                else:
                    print(
                        f"Name: {item['name']}, Size: {item['size']},Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")

    stack = []
    rootId = 1
    while (True):
        checkExist = False
        print()
        print('1. Đọc tệp tin/ thư mục con')
        print('2. Quay lại thư mục cha')
        print('3. Thoát')
        select = int(input("Mời bạn chọn: "))
        if (select == 1):
            subName = str(input("Nhập tệp tin/ thư mục cần đọc:"))
            print('-----------------------------------------')
            if (len(stack) == 0):
                subList = root
            elif ('submainName' in stack[-1]):
                subList = FAT32.printFileInFolder(stack[-1]['submainName'])
            else:
                subList = FAT32.printFileInFolder(stack[-1]['name'])
            for item in subList:
                # Nếu tồn tại thư mục / tệp tin
                if ('submainName' in item):
                    if item['submainName'] == subName:
                        stack.append(item)
                        rootId += 1
                        checkExist = True
                        if item['type'] == 'Archive':
                            tail = subName[len(subName) - 3:len(subName)]
                            if tail == 'TXT' or tail == 'txt':
                                print('Nội dung File ' + subName + ':\n')
                                print(FAT32.getContentFile(subName, subList))
                            else:
                                print(
                                    'Không phải file text. Hãy dùng phần mềm khác để đọc!')
                        elif item['type'] == 'Subdirectory':
                            print('Thư mục hiện tại: \n')
                            content = FAT32.printFileInFolder(subName)
                            for item in content:
                                size = item['size']
                                if 'submainName' in item:

                                    if size != 0:
                                        print(
                                            f"Name: {item['submainName']}, Size: {item['size']}, Type: {item['type']}, List Sector: {firstSector} ===> {lastSector},")
                                    else:
                                        print(
                                            f"Name: {item['submainName']}, Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")
                                else:
                                    if size == 0:
                                        print(
                                            f"Name: {item['name']}, Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")
                                    else:
                                        print(
                                            f"Name: {item['name']}, Size: {item['size']},Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")
                else:
                    if item['name'] == subName:
                        stack.append(item)
                        rootId += 1
                        checkExist = True
                        if item['type'] == 'Archive':
                            tail = subName[len(subName) - 3:len(subName)]
                            if tail == 'TXT' or tail == 'txt':
                                print('Nội dung File ' + subName + ':\n')
                                print(FAT32.getContentFile(subName, subList))
                            else:
                                print(
                                    'Không phải file text. Hãy dùng phần mềm khác để đọc!')
                        elif item['type'] == 'Subdirectory':
                            print('Thư mục hiện tại: \n')
                            content = FAT32.printFileInFolder(subName)
                            for item in content:
                                size = item['size']
                                if 'submainName' in item:

                                    if size != 0:
                                        print(
                                            f"Name: {item['submainName']}, Size: {item['size']}, Type: {item['type']}, List Sector: {firstSector} ===> {lastSector},")
                                    else:
                                        print(
                                            f"Name: {item['submainName']}, Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")
                                else:
                                    if size == 0:
                                        print(
                                            f"Name: {item['name']}, Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")
                                    else:
                                        print(
                                            f"Name: {item['name']}, Size: {item['size']},Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")
            if (checkExist == False):
                print('Không tồn tại thư mục/ tệp tin này!')
                # Nếu là tệp tin thì xuất thông tin tệp tin ra
        elif (select == 2):
            print('-----------------------------------------')
            print('Thư mục hiện tại: \n')
            if (len(stack) == 0):
                subList = root
                rootId = 1
            else:
                stack.pop()
                if (len(stack) == 0):
                    subList = root
                    rootId = 1
                else:
                    rootId = rootId - 1
                    if 'submainName' in stack[-1]:
                        subList = FAT32.printFileInFolder(
                            stack[-1]['submainName'])
                    else:
                        subList = FAT32.printFileInFolder(stack[-1]['name'])
            for item in subList:
                if item['rootId'] == rootId:
                    size = item['size']
                    # Nếu tồn tại thư mục / tệp tin
                    if 'submainName' in item:

                        if size != 0:
                            print(
                                f"Name: {item['submainName']}, Size: {item['size']}, Type: {item['type']}, List Sector: {firstSector} ===> {lastSector},")
                        else:
                            print(
                                f"Name: {item['submainName']}, Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")
                    else:
                        if size == 0:
                            print(
                                f"Name: {item['name']}, Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")
                        else:
                            print(
                                f"Name: {item['name']}, Size: {item['size']},Type: {item['type']}, List Sector: {firstSector} ===> {lastSector}")

        elif (select == 3):
            break
        else:
            print('Không tồn tại lựa chọn này!')


def Main():
    print('Đọc MBR của ổ đĩa (Physical Drive 1): ')
    diskName = "PhysicalDrive2"
    MBR = MasterBootRecord(diskName)
    MBR.printPartitionInfo()
    startSector = 0
    while True:
        select = int(
            input('Hãy chọn phân vùng cần đọc thông tin (Nhập -1 để thoát): '))
        if (select == 1):
            if (MBR.getStartSector_Partition1() == 0):
                print('Không đọc được phân vùng này!')
            else:
                startSector = MBR.getStartSector_Partition1()
                ReadPartition(diskName, startSector)
        elif (select == 2):
            if (MBR.getStartSector_Partition2() == 0):
                print('Không đọc được phân vùng này!')
            else:
                startSector = MBR.getStartSector_Partition2()
                ReadPartition(diskName, startSector)
        elif (select == 3):
            if (MBR.getStartSector_Partition3() == 0):
                print('Không đọc được phân vùng này!')
            else:
                startSector = MBR.getStartSector_Partition3()
                ReadPartition(diskName, startSector)
        elif (select == 4):
            if (MBR.getStartSector_Partition4() == 0):
                print('Không đọc được phân vùng này!')
            else:
                startSector = MBR.getStartSector_Partition4()
                ReadPartition(diskName, startSector)
        elif (select == -1):
            break
        else:
            print('Không tồn tại phân vùng này!')


Main()
