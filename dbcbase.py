class signal:
    def __init__(self):
        self.signalName = ""
        self.multiplexerIndicator = ""
        self.startBit = 0
        self.signalLength = 0
        self.byteOrder = 0 # 0: Motorola, 1: Intel
        self.valueType = "" # +: unsigned, -: signed
        self.factor = 0.0
        self.offset = 0.0
        self.min = 0.0
        self.max = 0.0
        self.unit = ""
        self.receiver = ""


class message:
    def __init__(self):
        self.messageId = 0
        self.messageName = ""
        self.messageLength = 0
        self.transmitter = ""

