from converter import *
import binascii
import os

class MFT:
    '''
    Constructor của class MFT
    Nhận input đầu vào là sector bắt đầu của MFT, một MFT entry sẽ là bao nhiêu byte, kích thước của MFT, số byte trên một sector,
    số sector của một cluster
    '''

    path_st = []


    def __init__(self,startSector,entry_size,bytesPerSector,sectorsPerCluster,diskName):
        self.startSector = startSector
        self.entry_size = entry_size
        self.bytesPerSector = bytesPerSector
        self.sectorsPerCluster = sectorsPerCluster
        self.diskName = diskName


        ''''ở đây tổ chức dạng Dictionary Key -> Value
            Key: Id của Entry
            Value: Tuple chứa (Tên file,Data)
        '''
        self.id_File = {}


        self.id_isFile = []


        '''Ứng với mỗi id ở vị trí index thì sẽ có các file con của nó (Giống cấu trúc cây)
            Biến này dùng để lưu đồ thị cây thư mục ở dạng danh sách kề
        '''
        self.parent_id = []

        self.fileName_id = {}
        self.id_fileName = {}

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

        data_string = convertHexStringToASCIIString(data)

        return data_string


    def __getFilenameOfEntry(self,entry,fileName_startPos):
        result = []
        fileName_size_pos = fileName_startPos + 24 + 64
        fileName_size = int(entry[fileName_size_pos],16)
        fileName_namespace_temp = []
        fileName_namespace_temp.append(entry[fileName_size_pos+1])
        fileName_namespace = convertHexStringToASCIIString(fileName_namespace_temp)
        '''
        Lý do có biến fileName_size_double là vì phần tử trong fileName được ngăn cách với nhau bởi byte 00
        '''
        fileName_size_double = fileName_size *2
        file_name_start = fileName_size_pos +1


        for i in range(0,fileName_size_double):
            if i % 2 == 1:
                result.append(entry[file_name_start+i])

        print(result)
        return convertHexStringToASCIIString(result)



    '''
    Input: Mảng có kích thước bằng entry_size là chứa các byte thông tin của một entry, số lượng entry trong ổ đĩa
    Output: Thông tin của thể của một Entry
    '''
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


        fileName = self.__getFilenameOfEntry(entry,fileName_startPos)
        data = ''
        self.id_File[int(id)] = (fileName,data)
        self.fileName_id[fileName] = id
        self.id_fileName[id] = fileName
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
        self.id_File[int(id)] = (fileName,data)



    '''
    Input : số lượng entry mà $MFT đang quản lý
    Output: Thông tin tất cả các Entry đó
    '''
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
    Hàm này đọc entry bắt đầu của MFT, tức là đọc entry $MFT
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



    def __getCurrentPathFolder(self):
        path = ""
        for i in range(0, len(self.path_st)):
            if(i == len(self.path_st) -1):
                path += self.id_fileName[(self.path_st[i])]
            else:
                path += self.id_fileName[(self.path_st[i])] +"/"

        return path + ">"


    '''---------------PUBLIC METHOD--------------- '''
    '''
    Hàm này có nhiệm vụ chỉ là in ra được cây thư mục
    '''
    def printTreeFolder(self,root):
        ## Thực hiện thuật toán DFS ngay tại root gốc
        print("***********************Cây Thư Mục***********************")
        ##Chuẩn bị cấu trúc dữ liệu
        st = [] ##Stack
        isVisted = []
        tab = [] ##T Tính ra số lần tab
        for i in range(0,len(self.parent_id)):
            isVisted.append(False)
            tab.append(0)

        #Bỏ root vào trong stack
        st.append(root)
        isVisted[root] = True
        tab[root] = 0
        while(len(st) != 0):

            ## pop stack
            current = int(st.pop())
            isVisted[current] = True
            tab_time = tab[current]

            for i in range(0,tab_time):
                print('  ',end = ' ')

            if(current == 5):
                print("Root")
            if current in self.id_File:
                tuple_fileName_data = self.id_File[current]
                print(tuple_fileName_data[0])

            for i in range(0,len(self.parent_id[current])):
                v = self.parent_id[current][i]
                if( isVisted[v] == False):
                    ##Push vao stack va tang tab[ len + 1]
                    st.append(v)
                    tab[v] += tab[current] + 1



    def indexFolder(self):
        while(True):
            os.system('cls')
            current_id = self.path_st[-1]
            current_folder_name = ''
            if(current_id == 5):
                current_folder_name = "Root"
            else:
                if current_id in self.id_File:
                    current_folder_name = self.id_File[current_id][0]

            print("Các folder hiện tại của {0}".format(current_folder_name))
            current_parent_id = self.parent_id[current_id]
            for i in range (0,len(current_parent_id)):
                child_id = current_parent_id[i]
                child_name = ''
                if child_id in self.id_File:
                    tuple_name = self.id_File[child_id]
                    child_name = tuple_name[0]
                print("{0}".format(child_name))

            print("\n\n\nCác lệnh có thể thực hiện: ")
            print("cd TênThưMục ---> Di chuyển tới thư mục con")
            print("cd ..   ---> Quay lại folder trước")
            print("TênThưMục.TênMởRộng ---> Mở tập tin con trong thư mục hiện hành")
            print("exit ---> Thoát ra khỏi chức năng\n\n")

            path = self.__getCurrentPathFolder()
            choice_temp =input(path)
            choice = choice_temp.split(' ')

            if(choice[0] == 'cd'):
                if(choice[1] == '..'):
                    self.path_st.pop()
                else:
                    str_pathName = ""
                    for i in range(1,len(choice)):
                        if(i == len(choice)-1):
                            str_pathName += choice[i]
                        else:
                            str_pathName += choice[i] +' '
                    self.path_st.append(self.fileName_id[str_pathName])
                    print(str_pathName)
            elif (choice[0] == 'exit'):
                break
            elif(choice[0] in self.fileName_id):
                id = self.fileName_id[choice[0]]
                name = self.id_File[id][0]
                data = self.id_File[id][1]
                if(data == ''):
                    print("Tập tin này có thể là thư mục hoặc không đọc được")
                else:
                    print("Dữ liệu của tập tin {0} là:\n{1}".format(name,data))
                    input("\nBấm Enter để tiếp tục")
            else:
                input("Nhập sai, bấm enter để reset: ")





    def printAllEntry(self):
        for key in self.id_File:
            print("-----------------------Entry {0}-----------------------".format(key))
            current = self.id_File[key]
            print("Name : {0}".format(current[0]))
            print("Data: {0}".format(current[1]))
