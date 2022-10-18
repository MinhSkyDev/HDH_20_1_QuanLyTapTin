from BootSector import *
from readMBR import *
from FAT32 import *
from NTFS import *
from run import *
import os
import time
import subprocess

class Menu():

    def __processDiskDriveStatus(self,diskDrive):
        for i in range(1,len(diskDrive)):
            if(diskDrive[i] == ''):
                continue
            else:
                disk_Drive_parse = (diskDrive[i]).split('  ')
                removeBlankSpace(disk_Drive_parse)
                key = int(disk_Drive_parse[0])
                self.diskDrive_dict[key] = (disk_Drive_parse[1],disk_Drive_parse[2])




    def __init__(self):

        '''
        Tổ chức cấu trúc dữ liệu cho nhận dạng loại tập tin
        '''
        self.diskDrive_dict = {}


        command = "wmic diskdrive get name,index,size"
        output = subprocess.getoutput(command).split('\n')
        self.__processDiskDriveStatus(output)


    def __detectFileSystem(self,input_index):
        print("Đang tiến hành đọc ổ đĩa !!!!")
        f_write = open("scriptname.txt", 'w')
        line1 = "select disk {0}\n".format(input_index)
        line2 = "detail disk"
        f_write.write(line1)
        f_write.write(line2)
        f_write.close()

        command = "diskpart /s scriptname.txt > logfile.txt"
        os.system(command)
        ##Cho ngủ 3 giây để tránh trường hợp máy không viết kịp câu lệnh trên
        time.sleep(1)

        f_read = open("logfile.txt", 'r')
        for i in range(0,26):
            temp = f_read.readline()
        fileSystem_string = f_read.readline()
        f_read.close()
        fileSystem_parse = fileSystem_string.split('  ')


        fileSystem = ""
        for ele in fileSystem_parse:
            if ('NTFS' in ele):
                fileSystem = 'NTFS'
            elif ('FAT32' in ele):
                fileSystem = 'FAT32'
            else:
                pass



        print("Loại hệ thống tập tin được sử dụng trong ổ đĩa sau khi detect là: {0} \n".format(fileSystem))
        return fileSystem


    def __readingFAT32Partition(self,diskName, startSector):
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

    '''
    Hiện thông tin về các ổ đĩa có trong máy và cho người dùng nhập lựa chọn
    '''
    def startMenu(self):
        os.system('cls')
        print("---------------------------------------------------------------")
        print("   Các ổ đĩa đang có trong máy (Chỉ thích hợp với ổ đĩa MBR)   \n")
        print("Chỉ mục       Tên ổ đĩa                    Kích thước  ")

        for key in self.diskDrive_dict:
            print("{0}        {1}                {2}          ".format(key,self.diskDrive_dict[key][0],self.diskDrive_dict[key][1]))

        input_index = int(input("\nXin hãy nhập chỉ mục ổ đĩa mà bạn muốn khảo sát: "))
        while(input_index not in self.diskDrive_dict):
            input_index = int(input("Không hợp lệ, xin mời nhập lại: "))

        disk_fileSystem = self.__detectFileSystem(input_index)

        print("\n Thông tin phân vùng MBR của ổ đĩa: ")

        PhysicalDrive_name = "\\.\PhysicalDrive{0}".format(input_index)
        PhysicalDrive_name_notPath = "PhysicalDrive{0}".format(input_index)
        mbr = MasterBootRecord(PhysicalDrive_name)
        mbr.printPartitionInfo()
        input("\nBấm enter để tiếp tục")
        if(disk_fileSystem == 'NTFS'):
            try:
                os.system('cls')
                # try:
                print("-------------------------NTFS-------------------------")
                while True:
                    select = int(
                        input('Hãy chọn phân vùng cần đọc thông tin (Nhập -1 để thoát): '))
                    if (select == 1):
                        if (mbr.getStartSector_Partition1() == 0):
                            print('Không đọc được phân vùng này!')
                        else:
                            partition1 = NTFS(mbr.getStartSector_Partition1(),PhysicalDrive_name_notPath)
                            partition1.Menu()
                            os.system('cls')
                    elif (select == 2):
                        if (mbr.getStartSector_Partition2() == 0):
                            print('Không đọc được phân vùng này!')
                        else:
                            partition2 = NTFS(mbr.getStartSector_Partition2(),PhysicalDrive_name_notPath)
                            partition2.Menu()
                            os.system('cls')
                    elif (select == 3):
                        if (mbr.getStartSector_Partition3() == 0):
                            print('Không đọc được phân vùng này!')
                        else:
                            partition3 = NTFS(mbr.getStartSector_Partition3(),PhysicalDrive_name_notPath)
                            partition3.Menu()
                            os.system('cls')
                    elif (select == 4):
                        if (mbr.getStartSector_Partition4() == 0):
                            print('Không đọc được phân vùng này!')
                        else:
                            partition4 = NTFS(mbr.getStartSector_Partition4(),PhysicalDrive_name_notPath)
                            partition4.Menu()
                            os.system('cls')
                    elif (select == -1):
                        break
                    else:
                        print('Không tồn tại phân vùng này!')
            except:
                print("Đã xảy ra lỗi !")
                input()


        elif(disk_fileSystem == 'FAT32'):
            input("\nBấm enter để tiếp tục:")
            try:
                os.system('cls')
                print("-------------------------FAT32-------------------------")
                while True:
                    select = int(
                        input('Hãy chọn phân vùng cần đọc thông tin (Nhập -1 để thoát): '))
                    if (select == 1):
                        if (mbr.getStartSector_Partition1() == 0):
                            print('Không đọc được phân vùng này!')
                        else:
                            startSector = mbr.getStartSector_Partition1()
                            self.__readingFAT32Partition(PhysicalDrive_name_notPath, startSector)
                    elif (select == 2):
                        if (mbr.getStartSector_Partition2() == 0):
                            print('Không đọc được phân vùng này!')
                        else:
                            startSector = mbr.getStartSector_Partition2()
                            self.__readingFAT32Partition(PhysicalDrive_name_notPath, startSector)
                    elif (select == 3):
                        if (mbr.getStartSector_Partition3() == 0):
                            print('Không đọc được phân vùng này!')
                        else:
                            startSector = mbr.getStartSector_Partition3()
                            self.__readingFAT32Partition(PhysicalDrive_name_notPath, startSector)
                    elif (select == 4):
                        if (mbr.getStartSector_Partition4() == 0):
                            print('Không đọc được phân vùng này!')
                        else:
                            startSector = mbr.getStartSector_Partition4()
                            self.__readingFAT32Partition(PhysicalDrive_name_notPath, startSector)
                    elif (select == -1):
                        break
                    else:
                        print('Không tồn tại phân vùng này!')
            except:
                print("Đã xảy ra lỗi !")
                input()





def main():

    menu = Menu()
    menu.startMenu()
    os.system('cls')

if __name__ == "__main__":
    main()
