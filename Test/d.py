from audioop import reverse
import binascii

data = [['73', '73', '20', '61', '6e', '79', '20', '6b', '65', '79', '20', '74', '6f', '20', '72', '65'], ['73', '74', '61', '72', '74', 'd', 'a', '0', '0', '0', '0', '0', '0', '0',
                                                                                                           '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'ac', '1', 'b9', '1', '0', '0']]

data1 = ['73', '73', '20', '61', '6e', '79', '20', '6b',
         '65', '79', '20', '74', '6f', '20', '72', '65']
temp = ""
for i, e in reversed((list(enumerate(data1)))):
    if i <= 11 and i >= 8:
        temp += e
# newTmp = "0x" + temp
# an_integer = int(newTmp, 16)
res = (int(temp, 16))
print(hex(res*512))


def toBigIndian(data, start, end):
    temp = ""
    for i, e in reversed((list(enumerate(data)))):
        if i <= end and i >= start:
            temp += e
    return temp


def findAddressBootsector(data):
    temp = ""
    for i, e in reversed((list(enumerate(data)))):
        if i <= 11 and i >= 8:
            temp += e
    res = (int(temp, 16))
    return hex(res*512)
