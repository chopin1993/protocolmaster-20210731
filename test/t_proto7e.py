from tools.esloging import log_init
log_init(".")
from tools.converter import hexstr2bytes
from protocol.smart7e_protocol import Smart7eProtocol

def t_protocol():
    input = '7e73de8700692300002802050604'
    input = "7e73de8700ff700a002802050604"
    bytes_data = hexstr2bytes(input)
    proto = Smart7eProtocol()
    ret = proto.store_and_find_frame(bytes_data)
    print(str(ret))

if __name__ == "__main__":
    t_protocol()