from BootSector import *
from readMBR import *
from FAT32 import *
from NTFS import *
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

        if(disk_fileSystem == 'NTFS'):
            input("\nBấm enter để tiếp tục")
            os.system('cls')
            # try:
            print("-------------------------NTFS-------------------------")
                    ##Bỏ phần NTFS vô đây
            partition1 = NTFS(mbr.getStartSector_Partition1(),PhysicalDrive_name_notPath)
            partition1.Menu()
            

        elif(dis_fileSystem == 'FAT32'):
            input("\nBấm enter để tiếp tục:")
            try:
                os.system('cls')
                print("-------------------------FAT32-------------------------")
                ##Bỏ phần FAT32 vô đây
            except:
                print("Ổ đĩa không phải là loại MBR")





def main():

    menu = Menu()
    menu.startMenu()

if __name__ == "__main__":
    main()
