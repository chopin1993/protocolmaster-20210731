name = """
  1
  2dddd
  3
"""

name = "eastsoft"
print(name)
byte1 = bytearray()
[byte1.append(ord(c)) for c in name]
print(byte1)
print(byte1[1])
print([name[1]])