from converter import *


class NTFS:

    def __init__(self,startSector):
        self.driveName = "PhysicalDrive0"
        self.sizeVBR = 512
        self.VBR = []
        self.__getVBR(startSector)
        self.MFT_start_cluster = self.__getStart_MFT_Cluter()

    '''---------------GETTER--------------- '''
    def getMFTStartCluster(self):
        return self.MFT_start_cluster

    '''---------------PRIVATE METHOD--------------- '''

    def __getVBR(self,startSector):
        startByte_VBR = startSector * 512
        filePath = r"\\.\{0}".format(self.driveName)
        f_read = open(filePath,'rb')
        f_read.seek(startByte_VBR)
        data = f_read.read(512)
        self.__standardizeVBR(data)

    def __standardizeVBR(self,data):
        for i in range(0,self.sizeVBR):
            data_toHex = hex(data[i]) ##giá trị data[i] hiện tại ở dạng số từ 0 -> 255, convert về hex
            data_toHex_standardize = data_toHex[2:] ##trả về ở lệnh trên ở dạng 0xMãHex, lệnh này để lọc bớt đi 0x
            if (len(data_toHex_standardize) != 2):
                data_toHex_standardize = "0" + data_toHex_standardize
            self.VBR.append(str(data_toHex_standardize))

    def __getStart_MFT_Cluter(self):
        startVector = convertHexLittleEndianStringToInt(self.VBR[48:57])
        return startVector



    '''---------------PUBLIC METHOD--------------- '''

    def printBPB(self):
        pass
