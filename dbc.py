from dbcAnalyse.dbcbase import message
import re
from . import dbcMessage
from . import dbcSignal


class dbcMsgSigs():
    def __init__(self, message = None, signalList = None):
        self.message = message
        self.signalList = signalList

class dbc():
    
    def __init__(self, dbcFilePath):
        self.dbcFilePathInput = dbcFilePath
        self.dbcVersion = ""
        self.nodeList = []
        self.messageAndSignalsDict = {} # {'ID': dbcMsgSigs()}
        self.parsed = False


    def parse(self):
        if self.parsed == True:
            return True

        mAndS = dbcMsgSigs()
        messageTmp = dbcMessage.dbcMessage()
        messageFlag = False

        signalList = []
        for line in open(self.dbcFilePathInput, 'r'):
            lineStr = line.strip()


            # VERSION
            res = re.match(r'VERSION\s+["](?P<version>.+)["]', lineStr)
            if res != None:
                self.dbcVersion = res.groupdict()["version"]
                continue

            # BU_
            res = re.match(r'BU_: \w+', lineStr)
            if res != None:
                self.nodeList = lineStr.split(" ")[1:]
                continue
            # BO_
            res = re.match(r'BO_ ', lineStr)
            if res != None:
                messageTmp = dbcMessage.dbcMessage(lineStr)
                messageTmp.parse()
                messageFlag = True
                continue

            # SG_
            res = re.match(r'SG_ ', lineStr)
            if res != None:
                signal = dbcSignal.dbcSignal(lineStr)
                signal.parse()
                signalList.append(signal)
                continue

            # null
            if lineStr == '' and messageFlag == True:
                mAndS = dbcMsgSigs(messageTmp, signalList)
                self.messageAndSignalsDict[messageTmp.messageId] = mAndS
                #self.messageAndSignalsDict[messageTmp.messageId].message.printMessageInfo()
                messageFlag = False
                signalList = []
                continue

            # CM_
            res = re.match(r'CM_ ', lineStr)
            if res != None:
                # CM_ BO_ ID "Comment"
                ret = re.match(r'CM_\s+BO_\s+(?P<ID>\w+)\s+["](?P<Comment>.+)["]', lineStr)
                if ret != None:
                    id = int(ret.groupdict()["ID"])
                    comment = ret.groupdict()["Comment"]
                    if id in self.messageAndSignalsDict:
                        self.messageAndSignalsDict[id].message.comment = comment
                        continue
                # CM_ SG_ ID SIGNAME "Comment"
                ret = re.match(r'CM_\s+SG_\s+(?P<ID>\w+)\s+(?P<Sig>\w+)\s+["](?P<Comment>.+)["]', lineStr)
                if ret != None:
                    id = int(ret.groupdict()["ID"])
                    signalName = ret.groupdict()["Sig"]
                    comment = ret.groupdict()["Comment"]
                    if id in self.messageAndSignalsDict:
                        for i in range(len(self.messageAndSignalsDict[id].signalList)):
                            if self.messageAndSignalsDict[id].signalList[i].signalName == signalName:
                                self.messageAndSignalsDict[id].signalList[i].comment = comment
                                continue

                    continue

        
        if messageFlag == True:
            mAndS = dbcMsgSigs(messageTmp, signalList)
            self.messageAndSignalsDict[messageTmp.messageId] = mAndS
            messageFlag = False
            signalList = []
                

        self.parsed = True

        return self.parsed


    def printdbcInfo(self):
        if self.parsed == False:
            self.parse()

        print("version: {0}".format(self.dbcVersion))
        print("node list: {0}".format(self.nodeList))
        print("message and signals:")
        for key, value in self.messageAndSignalsDict.items():
            print("id: {0}; signalNum: {1}".format(key, len(value.signalList)))
            value.message.printMessageInfo()
            for sig in value.signalList:
                sig.printSignalInfo()

if __name__ == '__main__':

    d = dbc("./test.dbc")
    d.parse()
    d.printdbcInfo()
    
    '''
    for line in open('./tmp.dbc', 'r'):
        if re.search('BO_', line) != None:
            msg = dbcMessage.dbcMessage(line)
            msg.printMessageInfo()
        elif re.search('SG_', line) != None:
            msg = dbcSignal.dbcSignal(line)
            msg.printSignalInfo()
    '''
        