import re
from .dbcbase import signal

class dbcSignal(signal):
    
    def __init__(self, dbcSignalStr):
        super(dbcSignal, self).__init__()
        self.dbcSignalStrInput = dbcSignalStr.strip()
        self.parsed = False
        self.comment = ""

    '''
    dbc signal format:
        SG_ signal_name multiplexer_indicator : start_bit|signal_size@byte_order+value_type (factor,offset) [mininum|maxinum] "unit" receiver
    '''
    def parse(self):
        if self.parsed == True:
            return True
        
        if self.dbcSignalStrInput == "":
            return False

        res = re.search(r'SG_\s(?P<signalName>\w+)\s+(?P<multiplexerIndicator>\w*)\s*'+
        r'[:]\s+(?P<startBit>\d+)[|](?P<signalSize>\d+)[@](?P<byteOrder>[01])(?P<valueType>[+-])\s+'+
        r'[(](?P<factor>[-]?(0|\d+)(\.[\d, E]+)?)[,](?P<offset>[-]?(0|\d+)(\.[\d, E]+)?)[)]\s+'+
        r'\[(?P<min>[-]?(0|\d+)(\.[\d, E]+)?)[|](?P<max>[-]?(0|\d+)(\.[\d, E]+)?)\]\s+'+
        r'["](?P<unit>\w*)["]\s+(?P<receiver>\w*)\s*', self.dbcSignalStrInput)


        if res == None:
            return False
        else:
            matchGroup = res.groupdict()
            self.signalName = matchGroup['signalName']
            self.multiplexerIndicator = matchGroup['multiplexerIndicator']
            self.startBit = int(matchGroup['startBit'])
            self.signalLength = int(matchGroup['signalSize'])
            self.byteOrder = int(matchGroup['byteOrder'])
            self.valueType = matchGroup['valueType']
            self.factor = float(matchGroup['factor'])
            self.offset = float(matchGroup['offset'])
            self.min = float(matchGroup['min'])
            self.max = float(matchGroup['max'])
            self.unit = matchGroup['unit']
            self.receiver = matchGroup['receiver']
            self.parsed = True
            return True
            #print(matchGroup)

    def printSignalInfo(self):
        if self.parsed == False:
            ret = self.parse()
            if ret == False:
                print("dbcSignalStrInput format error")

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
        mininum: {8}; maxnum: {9}; unit: {10}; receiver: {11};
        comment: {12};\n'''.format(self.signalName, \
            self.multiplexerIndicator, self.startBit, self.signalLength, \
            byteOrder, value_type, self.factor, self.offset, self.min, \
            self.max, self.unit, self.receiver, self.comment))


if __name__ == '__main__':
    for line in open("./test.dbc", 'r'):
        if re.match('SG_', line) != None:
            strInput = line
            s = dbcSignal(strInput)
            ret = s.parse()
            if ret == False:
                print("error: ", line)
            s.printSignalInfo()
        