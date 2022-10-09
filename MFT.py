from converter import *
import binascii

class MFT:
    '''
    Constructor của class MFT
    Nhận input đầu vào là sector bắt đầu của MFT, một MFT entry sẽ là bao nhiêu byte, kích thước của MFT, số byte trên một sector,
    số sector của một cluster
    '''
    def __init__(self,startSector,entry_size,bytesPerSector,sectorsPerCluster,diskName):
        self.startSector = startSector
        self.entry_size = entry_size
        self.bytesPerSector = bytesPerSector
        self.sectorsPerCluster = sectorsPerCluster
        self.diskName = diskName


        self.id_isFile = []
        self.id_File = set()
        self.parent_id = []

        self.__readFirstMFTEntry()


    '''---------------PRIVATE METHOD--------------- '''


    '''Process only for entry'''
    def __isEntryAFile(self,entry):
        return (
                entry[0] == '46' and
                entry[1] == '49' and
                entry[2] == '4c' and
                entry[3] == '45'
        )


    def __getEnd_StandardInfo_entry(self,entry):
        standardInfo_start = convertHexLittleEndianStringToInt(entry[20:22])
        standardInfo_len = convertHexLittleEndianStringToInt(entry[standardInfo_start + 4 : standardInfo_start +8])
        return standardInfo_len + standardInfo_start



    def __createFileID(self,MFT_size):
        for i in range(0,MFT_size):
            id = []
            self.parent_id.append(id)

    def __getIdOfAnEntry(self, entry):
        id = convertHexLittleEndianStringToInt(entry[44:48])
        return id

    def __getDataFromDataAttribute_ASCII(self,entry,data_start):
        data = []
        while(entry[data_start] != 'ff'):
            data.append(entry[data_start])
            data_start += 1

        data_string = ""
        for ele in data:
            data_string += ele
        ascii_string = binascii.unhexlify(data_string)
        return ascii_string



    def __processEntry(self, entry,MFT_size):

        id = self.__getIdOfAnEntry(entry)
        self.id_isFile.append(id)
        ## Move To Attribute FileName
        ## Move to Standard Information
        standardInfo_endPos = self.__getEnd_StandardInfo_entry(entry)
        fileName_startPos = standardInfo_endPos
        parent_id = convertHexLittleEndianStringToInt(entry[
                fileName_startPos + 24 : fileName_startPos + 30
        ])
        if(parent_id >= MFT_size):
            return
        self.parent_id[parent_id].append(id)

        ##Get to data attribute
        current_attribute_start = fileName_startPos
        current_attribute_type = entry[current_attribute_start]


        print("***************")
        print("Entry id: ",id)
        while(current_attribute_start < self.entry_size and entry[current_attribute_start] !='ff' and current_attribute_type != '80'):
            current_attribute_len = convertHexLittleEndianStringToInt(entry[
                                current_attribute_start +4 : current_attribute_start +8])
            next_attribute_start = current_attribute_start + current_attribute_len
            current_attribute_start = next_attribute_start
            current_attribute_type = entry[current_attribute_start]

        if(current_attribute_start >= self.entry_size or entry[current_attribute_start] =='ff'):
            return

        ##Da den duoc data
        ##print("Data attribute {0} start: ".format(id), current_attribute_start)
        data_offset = convertHexLittleEndianStringToInt(entry[current_attribute_start + 10 : current_attribute_start + 12])
        data_start = current_attribute_start + data_offset
        data = self.__getDataFromDataAttribute_ASCII(entry,data_start)
        print(data)




    def __getAllEntryInfo(self,MFT_size):
        Entry_start_sector = self.startSector
        Entry_start_byte = Entry_start_sector * self.bytesPerSector + self.entry_size ##exclude MFT entry
        self.__createFileID(MFT_size)
        filePath = r"\\.\{0}".format(self.diskName)
        f_read = open(filePath, 'rb')
        f_read.seek(Entry_start_byte)
        for i in range(1,MFT_size+1):
            entry_read = f_read.read(self.entry_size)
            entry = self.__standardizeData(entry_read)
            if(self.__isEntryAFile(entry)):
                self.__processEntry(entry,MFT_size)

        print(self.parent_id)
        f_read.close()


    def __standardizeData(self,data):
        arr = []
        for i in range(0, len(data)):
            data_toHex = hex(data[i]) ##giá trị data[i] hiện tại ở dạng số từ 0 -> 255, convert về hex
            data_toHex_standardize = data_toHex[2:] ##trả về ở lệnh trên ở dạng 0xMãHex, lệnh này để lọc bớt đi 0x
            if (len(data_toHex_standardize) != 2):
                data_toHex_standardize = "0" + data_toHex_standardize
            arr.append(data_toHex_standardize)
        return arr

    def __getStartAttribute_startByte(self):
        attribute_start_byte = self.MFT_first_entry[20:22]
        return convertHexLittleEndianStringToInt(attribute_start_byte)


    def __indexMFT(self,len_MFT,MFT_start_byte):
        filePath = r"\\.\{0}".format(self.diskName)
        f_read = open(filePath, 'rb')

        entry_start_byte = MFT_start_byte + self.entry_size
        f_read.seek(entry_start_byte)
        for i in range(1,len_MFT+1):
            entry = f_read(self.entry_size)


    '''
    Hàm này đọc entry bắt đầu của MFT, tức là đọc entry $MFT$
    Mục đích của hàm này là chúng ta có thể lấy được kích thước MFT vì entry này đại diện cho $MFT tức là thư mục chứa tất cả các file
    trong ổ đĩa
    '''
    def __readFirstMFTEntry(self):
        filePath = r"\\.\{0}".format(self.diskName)
        f_read = open(filePath, 'rb')
        MFT_start_byte = self.startSector * self.bytesPerSector
        f_read.seek(MFT_start_byte)

        ##Đọc số byte của một entry lên , tức là đọc entry bắt đầu của MFT
        MFT_first_entry_temp = f_read.read(self.entry_size)
        self.MFT_first_entry = self.__standardizeData(MFT_first_entry_temp)

        f_read.close()

        ##Note: T biết những dòng dưới này nhìn rất là nguyền rủa tuy nhiên rằng t sẽ cố gắng sửa lại sao cho nó clean code nhất có thể
        ##Nhiệm vụ của những dòng code dưới đây chỉ là để lấy số file mà $MFT có - Quang Minh
        MFT_firstEntry_standardInformation = self.__getStartAttribute_startByte()

        print("Vị trí bắt đầu của attribute: ",MFT_firstEntry_standardInformation)

        MFT_firstEntry_standardInformation_len = convertHexLittleEndianStringToInt(self.MFT_first_entry[
            MFT_firstEntry_standardInformation+4 : MFT_firstEntry_standardInformation +8
        ])

        MFT_firstEntry_FileName = MFT_firstEntry_standardInformation + MFT_firstEntry_standardInformation_len
        print("Vị trí bắt đầu của attribute filename:",MFT_firstEntry_FileName)

        MFT_firstEntry_FileName_len = convertHexLittleEndianStringToInt(self.MFT_first_entry[
            MFT_firstEntry_FileName+4 : MFT_firstEntry_FileName +8
        ])

        MFT_firstEntry_Data = MFT_firstEntry_FileName + MFT_firstEntry_FileName_len

        print("Vị trí bắt đầu của attribute data: ",MFT_firstEntry_Data)

        len_MFT = convertHexLittleEndianStringToInt(self.MFT_first_entry[
            MFT_firstEntry_Data + 24 : MFT_firstEntry_Data + 32
        ])

        print("Kích thước của MFT là: ",len_MFT)
        ##Sau khi có kích thước của MFT theo dạng số entry mà MFT có sở hữu thì chúng ta sẽ lần lượt đọc qua các entry đó:
        self.__getAllEntryInfo(len_MFT)





    '''---------------PUBLIC METHOD--------------- '''
    '''
    Class này có nhiệm vụ chỉ là in ra được cây thư mục
    '''
    def printTreeFolder(self):
        pass
