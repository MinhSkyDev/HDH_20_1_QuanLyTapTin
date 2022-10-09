from tracemalloc import start


"""
Ham chuyen tu HEX dang Little Endian sang DEC:
Vi du: 00 02 => 02 00(h) => 512(d)
Input: Hex Array (little Endian). Ex: h = ["00", "02"]
Output: Ket qua thap phan
"""
def convertHexLittleEndianStringToInt(hexArray):
    hexArray.reverse()
    hexStr = ""
    for i in range(len(hexArray)):
        hexStr += hexArray[i]
    i = int(hexStr, 16)
    return i


'''Ham chuyen tu mot mang Hex sang chuoi ASCII String
Input: Mang Hex: Ex: H = ['20', '32', '48']
Output: Chuoi ASCII. Ex: FAT32
'''
def convertHexStringToASCIIString(hexArray):
    ASCII_String = ""
    for i in hexArray:
        ASCII_String += chr(int(i, 16))
    return ASCII_String



'''
    Hàm chuyển từ một số Hex -> số bù 2 -> |Số Nguyên|
    Hàm được implement riêng để tính kích thước một MFT Entry
    MFT_entry_size = 2^ (kết quả trả về của hàm này)
    !!!KHÔNG CÓ TÁC DỤNG DÙNG CHUNG VỚI CÁC LOẠI KHÁC!!!
'''
def convertHexToTwoComplementBinary(hex):
    result = bin(int(hex,16))
    twoComplement = result[2:]
    size = len(twoComplement)
    result = 0
    for i in range(0,size):
        result += int(twoComplement[i]) * (2**(size-i-1))
        if(i == 0):
            result *=-1
    if(result <0):
        result *=-1
    return result
