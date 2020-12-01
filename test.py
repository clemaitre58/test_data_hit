
from struct import *

filename = "log_manip_1k_centrale_petit.txt"
with open(filename, mode='rb') as file:
    filecontent = file.read()

pattern = 'BhhhBBB'
siz = calcsize(pattern)
end = len(filecontent) -siz
offset = 0
record = []
while offset < end:
    data = unpack_from(pattern,filecontent,offset)
    if data[-1] == 0xA and data[-2] == 0xAB and data[-3] == 0xAB:
        record.append(data[:4])
        offset += siz
    else:
        offset += 1
        