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
