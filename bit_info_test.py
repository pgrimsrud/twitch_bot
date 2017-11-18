import sys
import json

bitInfo = {'link_7777_total_bits': 0}

def UpdateBits(epoch, user, count):
    if user in bitInfo:
        bitInfo[user] += count
    else:
        bitInfo[user] = count
    bitInfo['link_7777_total_bits'] += count
    LogBits(epoch, user, str(count))
    SaveBitInfo()

def SaveBitInfo():
    bitInfoFile = open("bit_info.json", 'w')
    json.dump(bitInfo, bitInfoFile)
    bitInfoFile.close()

def LoadBitInfo():
    global bitInfo
    bitInfoFile = open("bit_info.json", 'r')
    bitInfo = json.load(bitInfoFile)
    bitInfoFile.close()

def LogBits(epoch, user, count):
    bitLog = open("bit_log.txt", 'a')
    bitLog.write(epoch + ", " + user + ", " + count + "\n")
    bitLog.close()

LoadBitInfo()
print(bitInfo['link_7777_total_bits'])
UpdateBits('1494830731290', 'ev_brak', 100)
