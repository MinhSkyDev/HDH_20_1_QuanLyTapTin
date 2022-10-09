from converter import *
from MFT import*

class NTFS:

    def __init__(self,startSector):
        self.driveName = "PhysicalDrive1"
        self.sizeVBR = 512
        self.VBR = []
        self.__getVBR(startSector)


        self.sectorsPerCluster = int(self.VBR[13],16)
        self.MFT_start_cluster = self.__getStart_MFT_Cluter()
        self.MFT_Entry_size = 2**(self.__getMFT_Entry_size())

        self.sectorLogicalDisk_start = convertHexLittleEndianStringToInt(self.VBR[28:32])

        self.MFT = MFT(self.MFT_start_cluster*self.sectorsPerCluster + self.sectorLogicalDisk_start,
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
    Mục đích hàm này sinh ra là để debug
    '''
    def printBPB(self):
        print("Sectors per cluster", self.sectorsPerCluster)
        print("Cluster bắt đầu của MFT: ",self.MFT_start_cluster)
        print("Sector bắt đầu của ổ đĩa logic: ", self.sectorLogicalDisk_start)
        print("Số byte một Entry: ",self.MFT_Entry_size)
        print("Sector bắt đầu của MFT", self.MFT_start_cluster)
        print("Entry size: ",self.MFT_Entry_size)

    def printFolderTree():
        pass
