import re
from .dbcbase import message
class dbcMessage(message):

    def __init__(self, dbcMessageInput = ""):
        super(dbcMessage, self).__init__()
        self.dbcMessageInputStr = dbcMessageInput.strip()
        self.parsed = False

    # BO_ message_id message_name: message_size transmitter
    def parse(self):
        if self.parsed == True:
            return True

        if self.dbcMessageInputStr == "":
            return False

        res = re.search(r'BO_\s+(?P<MsgID>\d+)\s+(?P<MsgName>\w+)[:]\s+(?P<MsgLenth>\d+)\s+(?P<transmitter>\w+)', self.dbcMessageInputStr)
        if res == None:
            return False
        else:
            matchGroup = res.groupdict()
            self.messageId = int(matchGroup['MsgID'])
            self.messageName = matchGroup['MsgName']
            self.messageLength = int(matchGroup['MsgLenth'])
            self.transmitter = matchGroup['transmitter']
            self.parsed = True
            return True

    def __checkParsed(self):
        if self.parsed == False:
            ret = self.parse()
            if ret == False:
                print("dbcMessageStrInput format error")

    def printMessageInfo(self):
        self.__checkParsed()

        print('''\tmessage_id: {0}; message_name: {1};
        message_size: {2}; transmitter: {3}\n'''.format(self.messageId, \
            self.messageName, self.messageLength, self.transmitter))   


if __name__ == '__main__':
    for line in open("./test.dbc", 'r'):
        if re.match('BO_', line) != None:
            strInput = line
            s = dbcMessage(strInput)
            ret = s.parse()
            if ret == False:
                print("error: ", line)
            s.printMessageInfo()

            

            