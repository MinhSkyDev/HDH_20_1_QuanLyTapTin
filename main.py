
from readMBR import *
from FAT32 import *
from NTFS import *

def main():
    mbr = MasterBootRecord()
    ##partition1 = FAT32(mbr.getStartSector_Partition1())

    ##partition1.printPartitionInfo()

    partition1 = NTFS(mbr.getStartSector_Partition1())
    print(mbr.getStatusPartition1())
    partition1.printBPB()

if __name__ == "__main__":
    main()
