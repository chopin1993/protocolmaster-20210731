from tools.imgtool import *


def test_gray2color():
    data = np.linspace(0,50,64)
    data = data.reshape((8,8))
    data = numpy2color(data)
    data = color2jpg(data)
    with open("test.jpg", mode="wb") as handle:
        handle.write(data)

def test_bytes_file():
    bytes_value = bytes([1,2,3,4,5])
    with open("test_file.bin", "wb") as handle:
        handle.write(bytes_value)

