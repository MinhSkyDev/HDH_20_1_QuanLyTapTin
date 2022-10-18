from converter import *
from MFT import*
import os


class NTFS:

    def __init__(self,startSector,diskName):
        self.driveName = diskName
        self.sizeVBR = 512
        self.VBR = []
        self.__getVBR(startSector)


        self.sectorsPerCluster = int(self.VBR[13],16)
        self.MFT_start_cluster = self.__getStart_MFT_Cluter()
        self.MFT_Entry_size = 2**(self.__getMFT_Entry_size())

        self.sectorLogicalDisk_start = convertHexLittleEndianStringToInt(self.VBR[28:32])

        MFT_start_byte = self.MFT_start_cluster*self.sectorsPerCluster + self.sectorLogicalDisk_start
        self.MFT = MFT(MFT_start_byte,
                       self.MFT_Entry_size,
                       512, self.sectorsPerCluster,self.driveName)




    '''---------------GETTER--------------- '''
    def getMFTStartCluster(self):
        return self.MFT_start_cluster * self.sectorsPerCluster + self.sectorLogicalDisk_start


    '''---------------PRIVATE METHOD--------------- '''

    def __getVBR(self,startSector):
        startByte_VBR = startSector * 512
        filePath = r"\\.\{0}".format(self.driveName)
        f_read = open(filePath,'rb')
        f_read.seek(startByte_VBR)
        data = f_read.read(512)
        self.__standardizeVBR(data)
        f_read.close()

    def __standardizeVBR(self,data):
        for i in range(0,self.sizeVBR):
            data_toHex = hex(data[i]) ##giá trị data[i] hiện tại ở dạng số từ 0 -> 255, convert về hex
            data_toHex_standardize = data_toHex[2:] ##trả về ở lệnh trên ở dạng 0xMãHex, lệnh này để lọc bớt đi 0x
            if (len(data_toHex_standardize) != 2):
                data_toHex_standardize = "0" + data_toHex_standardize
            self.VBR.append(str(data_toHex_standardize))

    def __getStart_MFT_Cluter(self):
        startSector = convertHexLittleEndianStringToInt(self.VBR[48:56])
        return startSector

    def __getMFT_Entry_size(self):
        MFT_entry_size_byte_hex = self.VBR[64]
        result = convertHexToTwoComplementBinary(MFT_entry_size_byte_hex)
        return result



    '''---------------PUBLIC METHOD--------------- '''


    '''
    Đọc một vài thông tin quan trọng trong Partition Boot Sector của NTFS
    '''
    def printBPB(self):
        os.system('cls')
        print("Sectors per cluster", self.sectorsPerCluster)
        print("Cluster bắt đầu của MFT: ",self.MFT_start_cluster)
        print("Sector bắt đầu của ổ đĩa logic: ", self.sectorLogicalDisk_start)
        print("Số byte một Entry: ",self.MFT_Entry_size)
        print("Sector bắt đầu của MFT", self.MFT_start_cluster)
        input("Bấm enter để về màn hình menu: ")

    def printFolderTree(self):
        self.MFT.printTreeFolder(5)
        ##All file starts with


    def printAllEntry(self):
        self.MFT.printAllEntry()

    def indexFolder(self):
        self.MFT.path_st.append(5)
        self.MFT.indexFolder()

    def Menu(self):
        while(True):
            os.system('cls')
            print("-------------------Các chức năng-------------------")
            print("1. Đọc các thông số cơ bản của NTFS ")
            print("2. In ra cây thư mục của hệ thống tập tin NTFS")
            print("3. Chọn tập tin và in,đọc các thư mục con của nó")
            print("4. Hiện tất cả các entry trong MFT")
            print("0. Thoát chương trình")

            choice = int(input("Xin mời nhập lựa chọn của bạn: "))

            if(choice == 1):
                self.printBPB()
            elif (choice ==2 ):
                os.system('cls')
                self.printFolderTree()
                input("Bấm enter để tiếp tục: ")
            elif (choice == 3):
                os.system('cls')
                self.indexFolder()
            elif(choice == 0):

                break
            elif(choice == 4):
                os.system('cls')
                self.printAllEntry()
                input("Bấm enter để tiếp tục: ")
