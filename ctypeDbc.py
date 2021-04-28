import re
from .dbcbase import message, signal


'''
typedef struct  {
    uint32_t ID;                    /*!< CAN message id */
    uint8_t DLC;                    /*!< CAN message data length code */
    uint32_t repetition_time;       /*!< CAN message cycle time */
    uint32_t repetition_phase;      /*!< CAN message startup (first send) offset */
    can_callback_funcPtr cbk_func;  /*!< CAN message callback after message is sent or received */
} CAN_MSG_TX_TYPE_s;

CAN_MSG_TX_TYPE_s foxbms_tx[] = {
    { 0x110, 8, 100, 0, NULL_PTR },  /*!< BMS system state 0 */
    { 0x111, 8, 100, 0, NULL_PTR },  /*!< BMS system state 1 */
    { 0x112, 8, 100, 0, NULL_PTR },  /*!< BMS system state 2 */
    { 0x115, 8, 100, 0, NULL_PTR },  /*!< BMS slave state 0 */
    { 0x116, 8, 100, 0, NULL_PTR },  /*!< BMS slave state 1 */
    { 0x130, 8, 100, 30, NULL_PTR },  /*!< Maximum allowed current */
}
'''
class ctypeMessage(message):
    __idIndex = 0
    __dlcIndex = 1
    __cycleTimeIndex = 2

    def __init__(self, ctypeMessageInput = "", messageName = "", transmitter = ""):
        super(ctypeMessage, self).__init__()
        self.ctypeMessageInput = ctypeMessageInput
        self.parsed = False

        self.cycleTime = 0 # ms
        self.transmitter = transmitter
        self.messageName = messageName
        self.comment = ""

    def parse(self):
        if self.parsed == True:
            return True
        
        if self.ctypeMessageInput == "":
            return False

        res = re.search(r'\{(?P<messageInfo>.+)\}[,]\s+.+[<](?P<comment>.+)[*]', self.ctypeMessageInput)
        if res != None:
            matchGroup = res.groupdict()
            messageInfoList = matchGroup['messageInfo'].strip().split(',')
            self.messageId = int(messageInfoList[ctypeMessage.__idIndex], 16)
            self.comment = matchGroup['comment'].strip()
            self.messageLength = int(messageInfoList[ctypeMessage.__dlcIndex])
            self.cycleTime = int(messageInfoList[ctypeMessage.__cycleTimeIndex])
            self.parsed = True

        return self.parsed


    def __checkParsed(self):
        if self.parsed == False:
            ret = self.parse()
            if ret == False:
                print("ctypeMessageInput format error")

    def printMessageInfo(self):
        self.__checkParsed()

        print('''\tmessage_id: {0}; message_name: {1};
        message_size: {2}; transmitter: {3}; cycle_time: {4};
        message_comment: {5}\n'''.format(self.messageId, \
            self.messageName, self.messageLength, self.transmitter, self.cycleTime, self.comment))

    # BO_ message_id message_name: message_size transmitter
    def getDbcFormat(self):
        self.__checkParsed()

        dbcStr = "BO_ {0} {1}: {2} {3}".format(self.messageId, self.messageName, self.messageLength, self.transmitter)
        return dbcStr
'''
typedef union {
    CANS_messagesTx_e Tx;
    CANS_messagesRx_e Rx;
} CANS_messages_t;

typedef enum {
    littleEndian = 0,
    bigEndian = 1
} CANS_byteOrder_e;

typedef struct  {
    CANS_messages_t msgIdx;
    uint8_t bit_position;
    uint8_t bit_length;
    float min;
    float max;
    float factor;
    float offset;
    CANS_byteOrder_e byteOrder;
    can_callback_funcPtr callback;
} CANS_signal_s;

CANS_signal_s cans_CAN0_signals_tx[] = {
    { {CAN0_MSG_SystemState_0}, 0, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_general_error, */
    { {CAN0_MSG_SystemState_0}, 8, 8, 0, UINT8_MAX, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_current_state, */
    { {CAN0_MSG_SystemState_0}, 16, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_error_overtemp_charge, */
    { {CAN0_MSG_SystemState_0}, 24, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_error_undertemp_charge, */
    { {CAN0_MSG_SystemState_0}, 32, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_error_overtemp_discharge, */
    { {CAN0_MSG_SystemState_0}, 40, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_error_undertemp_discharge, */
    { {CAN0_MSG_SystemState_0}, 48, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_error_overcurrent_charge, */
    { {CAN0_MSG_SystemState_0}, 56, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_error_overcurrent_discharge, */
    }
'''
class ctypeSignal(signal):

    __messageIdIndex = 0
    __startBitIndex = 1
    __lengthIndex = 2
    __minIndex = 3
    __maxIndex = 4
    __factorIndex = 5
    __offsetIndex = 6
    __byteOrderIndex = 7

    __intelCtypeName = "littleEndian"
    __motorolaName = "bigEndian"

    __UINT8_MAX = 255
    __UINT16_MAX = 65535
    __UINT32_MAX = 4294967295
    __UINT64_MAX = 18446744073709551615

    def __init__(self, ctypeSignalInput = "", receiver = "Vector__XXX"):
        super(ctypeSignal, self).__init__()
        self.ctypeSignalInput = ctypeSignalInput.strip()
        self.parsed = False

        self.receiver = receiver
        self.messageIndex = ""

    def parse(self):
        if self.parsed == True:
            return True

        if self.ctypeSignalInput == "":
            return False


        res = re.match(r'\{(?P<signalInfo>.+)\}.+[<](?P<signalName>.+)[*]', self.ctypeSignalInput)

        if res != None:
            matchGroup = res.groupdict()
            signalInfoList = matchGroup['signalInfo'].strip().split(',')
            
            self.signalName = matchGroup['signalName'].strip().replace(',', '')
            self.startBit = int(signalInfoList[ctypeSignal.__startBitIndex])
            self.signalLength = int(signalInfoList[ctypeSignal.__lengthIndex])
            
            byteOrder = signalInfoList[ctypeSignal.__byteOrderIndex].strip()
            if byteOrder == ctypeSignal.__intelCtypeName:
                self.byteOrder = 1
            elif byteOrder == ctypeSignal.__motorolaName:
                self.byteOrder = 0
            else:
                self.byteOrder = -1

            self.min = float(signalInfoList[ctypeSignal.__minIndex])

            maxStr = signalInfoList[ctypeSignal.__maxIndex].strip()
            if maxStr == 'UINT8_MAX':
                self.max = ctypeSignal.__UINT8_MAX
            elif maxStr == 'UINT16_MAX':
                self.max = ctypeSignal.__UINT16_MAX
            elif maxStr == 'UINT32_MAX':
                self.max = ctypeSignal.__UINT32_MAX
            elif maxStr == 'UINT64_MAX':
                self.max = ctypeSignal.__UINT64_MAX
            else:
                self.max = float(maxStr)


            self.factor = float(signalInfoList[ctypeSignal.__factorIndex])
            self.offset = float(signalInfoList[ctypeSignal.__offsetIndex])

            if self.min < 0:
                self.valueType = '-'
            else:
                self.valueType = '+'

            self.messageIndex = signalInfoList[ctypeSignal.__messageIdIndex][1:-1]

            self.parsed = True

        return self.parsed

    def __checkParsed(self):
        if self.parsed == False:
            ret = self.parse()
            if ret == False:
                print("ctypeSignalInput format error")

    def printSignalInfo(self):
        self.__checkParsed()

        byteOrder = ""
        if self.byteOrder == 1:
            byteOrder = "Intel"
        elif self.byteOrder == 0:
            byteOrder = "Motorola"

        value_type = ""
        if self.valueType == "+":
            value_type = "unsigned"
        elif self.valueType == "-":
            value_type = "signed"

        print('''\tsignal_name: {0}; multiplexer_indicator: {1};
        start_bit: {2}; signal_length: {3}; byte_order: {4};
        value_type: {5}; factor: {6}; offset: {7};
        mininum: {8}; maxnum: {9}; unit: {10}; receiver: {11}
        message_index: {12}\n'''.format(self.signalName, \
            self.multiplexerIndicator, self.startBit, self.signalLength, \
            byteOrder, value_type, self.factor, self.offset, self.min, \
            self.max, self.unit, self.receiver, self.messageIndex))

    def getDbcFormat(self):
        self.__checkParsed()

        signalStr = "SG_ {0} {1}: {2}|{3}@{4}{5} ({6},{7}) [{8}|{9}] \"{10}\" {11}".format( \
            self.signalName, self.multiplexerIndicator, self.startBit, self.signalLength, \
            self.byteOrder, self.valueType, self.factor, self.offset, self.min, \
            self.max, self.unit, self.receiver)

        return signalStr


class ctypeMsgSigs():
    def __init__(self, ctypeMessage = None, ctypeSignalList = None):
        self.ctypeMessage = ctypeMessage
        self.ctypeSignalList = ctypeSignalList

'''
can_cfg.c format:

typedef enum{
    CAN0_MSG_SystemState_0,  /*!< BMS general state 0 */
    CAN0_MSG_SystemState_1,  /*!< BMS general state 1 */
    CAN0_MSG_SystemState_2,  /*!< BMS general state 2 */
    CAN0_MSG_SlaveState_0,    /*!< Slave state 0 */
    CAN0_MSG_SlaveState_1,    /*!< Slave state 1 */
    ...
}CANS_messagesTx_e；

CAN_MSG_TX_TYPE_s foxbms_tx[] = {
    { 0x110, 8, 100, 0, NULL_PTR },  /*!< BMS system state 0 */
    { 0x111, 8, 100, 0, NULL_PTR },  /*!< BMS system state 1 */
    { 0x112, 8, 100, 0, NULL_PTR },  /*!< BMS system state 2 */

    { 0x115, 8, 100, 0, NULL_PTR },  /*!< BMS slave state 0 */
    { 0x116, 8, 100, 0, NULL_PTR },  /*!< BMS slave state 1 */
};

CANS_signal_s cans_CAN0_signals_tx[] = {
    { {CAN0_MSG_SystemState_0}, 0, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_general_error, */
    { {CAN0_MSG_SystemState_0}, 8, 8, 0, UINT8_MAX, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_current_state, */
    { {CAN0_MSG_SystemState_0}, 16, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_error_overtemp_charge, */
    { {CAN0_MSG_SystemState_0}, 24, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_error_undertemp_charge, */
    { {CAN0_MSG_SystemState_0}, 32, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_error_overtemp_discharge, */
    { {CAN0_MSG_SystemState_0}, 40, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_error_undertemp_discharge, */
    { {CAN0_MSG_SystemState_0}, 48, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_error_overcurrent_charge, */
    { {CAN0_MSG_SystemState_0}, 56, 3, 0, 7, 1, 0, littleEndian, &cans_getcanerr },  /*!< CAN0_SIG_GS0_error_overcurrent_discharge, */
};
'''
class ctypeDbc():

    __parseIdleState = 0
    __parseMessageIndexState = 1
    __parseMessageState = 2
    __parseSignalState = 3

    def __init__(self, ctypeFilePath = ""):
        self.ctypeFilePath = ctypeFilePath
        self.parsed = False
        self.state = ctypeDbc.__parseIdleState

        self.messageIndexList = []
        self.transmitter = ""
        self.messageAndSignalsDict = {} # {'messageIndex': ctypeMsgSigs()}

    def parse(self):
        if self.parsed == True:
            return True

        if self.ctypeFilePath == "":
            return False

        messageNum = 0
        for line in open(self.ctypeFilePath, 'r'):
            lineStr = line.strip()

            if not len(lineStr):
                continue

            if self.state == ctypeDbc.__parseIdleState:
                res = re.match('typedef enum {', lineStr)
                if res != None:
                    self.state = ctypeDbc.__parseMessageIndexState
                    continue

                res = re.match(r'CAN_MSG_TX_TYPE_s (?P<transmitter>.+)_tx\[\]', lineStr)
                if res != None:
                    self.transmitter = res.groupdict()['transmitter']
                    self.state = ctypeDbc.__parseMessageState
                    continue

                res = re.match(r'CANS_signal_s', lineStr)
                if res != None:
                    self.state = ctypeDbc.__parseSignalState
                    continue

            elif self.state == ctypeDbc.__parseMessageIndexState:
                res = re.match('} CANS_messagesTx_e;', lineStr)
                if res != None:
                    self.state = ctypeDbc.__parseIdleState
                    continue

                res = re.match(r'(?P<msgIdx>.+)[,]', lineStr)
                if res != None:
                    messageIndex = res.groupdict()['msgIdx']
                    self.messageIndexList.append(messageIndex)
                    continue

            elif self.state == ctypeDbc.__parseMessageState:
                res = re.match(r'\};', lineStr)
                if res != None:
                    if messageNum != len(self.messageIndexList):
                        print("message num error, message num = {0}, len(messageIndexList) = {1}".format(messageNum, len(self.messageIndexList)))
                        return False
                    self.state = ctypeDbc.__parseIdleState
                    continue

                message = ctypeMessage(lineStr, self.messageIndexList[messageNum], self.transmitter)
                ret = message.parse()
                if ret == True:
                    ctypSignalList = []
                    msgSig = ctypeMsgSigs(message, ctypSignalList)
                    self.messageAndSignalsDict[self.messageIndexList[messageNum]] = msgSig
                    messageNum += 1
                    continue

            elif self.state == ctypeDbc.__parseSignalState:
                res = re.match(r'\};', lineStr)
                if res != None:
                    self.state = ctypeDbc.__parseIdleState
                    self.parsed = True
                    continue

                signal = ctypeSignal(lineStr)
                ret = signal.parse()
                if ret == True:
                    messageIndex = signal.messageIndex
                    msgSig = self.messageAndSignalsDict[messageIndex]
                    msgSig.ctypeSignalList.append(signal)
                else:
                    print("parse signal Error: {0}".format(lineStr))

                
        return self.parsed

            

    def printCtypeInfo(self):
        if self.parsed == False:
            self.parse()
        
        for messageIndex in self.messageIndexList:
            msgSig = self.messageAndSignalsDict[messageIndex]
            msgSig.ctypeMessage.printMessageInfo()
            for signal in msgSig.ctypeSignalList:
                signal.printSignalInfo()
           

    def outputDbcFile(self, dbcFilePath = "out.dbc"):
        if self.parsed == False:
            self.parse()


        with open(dbcFilePath, 'w+') as f:
            # BO_ AND SG_
            for messageIndex in self.messageIndexList:
                msgSig = self.messageAndSignalsDict[messageIndex]
                messageStr = msgSig.ctypeMessage.getDbcFormat() + "\n"
                f.write(messageStr)
                
                signalList = msgSig.ctypeSignalList
                for signal in signalList:
                    signalStr = " " + signal.getDbcFormat() + "\n"
                    f.write(signalStr)

                f.write("\n")

            # CM_ BO_ message_id "comment"
            for messageIndex in self.messageIndexList:
                message = self.messageAndSignalsDict[messageIndex].ctypeMessage
                messageCommentStr = "CM_ BO_ {0} \"{1}\";".format(message.messageId, message.comment) + "\n"
                f.write(messageCommentStr)

            f.write("\n")        

        



if __name__ == '__main__':
    c = ctypeDbc("./can_cfg.c")
    c.parse()
    c.outputDbcFile("test.dbc")
    c.printCtypeInfo()
    '''
    for line in open("cansignal_cfg.c", 'r'):
        res = re.match(r'\{', line.strip())
        if res != None:
        #c = ctypeMessage("    { 0x110, 8, 100, 0, NULL_PTR },  /*!< BMS system state 0 */", "foxbms")
            c = ctypeSignal(line)
            c.parse()
            c.printSignalInfo()
        #print(float('12.123'))
        #c.printMessageInfo()
    '''
