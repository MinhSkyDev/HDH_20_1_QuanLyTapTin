
from readMBR import *
from FAT32 import *


def main():
    mbr = MasterBootRecord()
    partition1 = FAT32(mbr.getStartSector_Partition1())

    partition1.printPartitionInfo()
if __name__ == "__main__":
    main()
