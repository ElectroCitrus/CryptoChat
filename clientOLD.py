import socket, pyAesCrypt, time

password = "test"
bufferSize = 512*1024

# input plaintext binary stream
fIn = io.BytesIO(pbdata)

# initialize ciphertext binary stream
fCiph = io.BytesIO()

# initialize decrypted binary stream
fDec = io.BytesIO()

def c2s(addr="127.0.0.1", port=4000):
    CONN = socket.socket()
    CONN.connect((addr, port))

name = input("Имя: ")

while True:
    message = bytes(input())
    
    # encrypt stream
    pyAesCrypt.encryptStream(fIn, fCiph, password, bufferSize)

    conn = socket.socket()
    conn.connect(("127.0.0.1", 4000))

    if message != "/close":
        conn.send(bytes(name + " " + message, "utf-8"))
        print(">: " + message)
    else:
        conn.send(bytes(name + " вышел", "utf-8"))
        break


# data = b""
# tmp = conn.recv(1024)
# while tmp:
#     data += tmp
#     tmp = conn.recv(1024)

# print(data.decode("utf-8"))

"""
    import pyAesCrypt
import io

bufferSize = 64 * 1024
password = "foopassword"

# binary data to be encrypted
pbdata = b"This is binary plaintext \x00\x01"

# input plaintext binary stream
fIn = io.BytesIO(pbdata)

# initialize ciphertext binary stream
fCiph = io.BytesIO()

# initialize decrypted binary stream
fDec = io.BytesIO()

# encrypt stream
pyAesCrypt.encryptStream(fIn, fCiph, password, bufferSize)

# print encrypted data
print("This is the ciphertext:\n" + str(fCiph.getvalue()))

# get ciphertext length
ctlen = len(fCiph.getvalue())

# go back to the start of the ciphertext stream
fCiph.seek(0)

# decrypt stream
pyAesCrypt.decryptStream(fCiph, fDec, password, bufferSize, ctlen)

# print decrypted data
print("Decrypted data:\n" + str(fDec.getvalue()))
"""

conn.close()