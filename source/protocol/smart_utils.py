from tools.esenum import EsEnum
from .data_container import DataStruct
from .codec import BinaryEncoder,BinaryDecoder
from tools.converter import str2hexstr
class CMD(EsEnum):
    NOTIFY = 0x0 #不可靠上报
    REPORT = 0x01 #可靠上报
    READ = 0x02
    SEARCH = 0x03
    FILE = 0x04
    UPDATE = 0x05 #升级
    UPDATE_PLC = 0x06 #大文件升级
    WRITE = 0x7

class ErrorCode(EsEnum):
    NO_ERROR = 0
    OTHER_ERROR= 0x0f
    LEN_ERROR = 0x01
    BUFFER_ERR = 0x02
    DATA_ERR = 0x03
    DID_ERROR = 0x04
    DEV_BUSY = 0x05
    NO_RETURN = 0x10

class GIDTYPE(EsEnum):
    BIT1 = 0
    U8 = 1
    U16 = 2

class GID(DataStruct):
    def __init__(self, type=None, gids=None, decoder=None, **kwargs):
        self.gids = []
        if decoder is None:
            self.type = GIDTYPE.to_enum(type)
            if isinstance(gids, int):
                gids = [gids]
            self.gids = gids
        else:
            self.decode(decoder)

    def encode(self, encoder):
        data_encoder = BinaryEncoder()
        if isinstance(self.gids, list):
            if self.type == GIDTYPE.U8:
                [data_encoder.encode_u8(addr) for addr in self.gids]
            elif self.type== GIDTYPE.U16:
                [data_encoder.encode_u16(addr) for addr in self.gids]
            else:
                cnt = (max(self.gids)+7)//8
                buffers = [0]*cnt
                for gid in self.gids:
                    gid -= 1
                    idx = gid//8
                    bit = gid%8
                    buffers[idx] |= 1<<bit
                [data_encoder.encode_u8(data) for data in buffers]
        else:
            data_encoder.encode_str(self.gids)
        address = data_encoder.get_data()
        encoder.encode_u8(self.type.value<<6|len(address))
        encoder.encode_str(address)

    def decode(self, decoder):
        data = decoder.decode_u8()
        self.type = GIDTYPE.to_enum(((data&0xc0)>>6))
        len_ = data&0x3f
        if self.type == GIDTYPE.U8:
            self.gids = [decoder.decode_u8()  for i in range(0,len_)]
        elif self.type == GIDTYPE.U16:
            self.gids = [decoder.decode_u16() for i in range(0, len_, 2)]
        else:
            self.gids = []
            for i,data in enumerate(decoder.decode_bytes(len_)):
                base = i*8+1
                for bits in range(0,8):
                    if data & (1<<bits):
                        self.gids.append(bits+base)

    def __eq__(self, other):
        if self.type == other.type and set(self.gids) == set(other.gids):
            return True
        else:
            return False

    def __str__(self):
        data = BinaryEncoder.object2data(self)
        txt = "gid:{} {}[{}] ".format(str(self.type), str(self.gids), str2hexstr(data))
        return txt