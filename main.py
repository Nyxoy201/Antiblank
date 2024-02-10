from zipfile import ZipFile
import os, base64, zlib, shutil, string, codecs, lzma
from Crypto.Cipher import AES
import sys

if len(sys.argv) != 2:
    print("Usage: python main.py <Executable_Path>")
    quit()

executable = sys.argv[1]
os.system("py extract.py " + executable + " >nul")
try:
    os.chdir(f"{os.path.basename(executable)}_extracted")
except:
    print("Please input a valid file")
    quit()

try:
    shutil.copyfile("./blank.aes", "../blank.aes")
except:
    print("This is not a blank grabber file")
    quit()

try:
    f = open("loader-o.pyc", "rb")
    data = f.read()
    f.close()
except:
    for i in os.listdir():
        if len(i) >= 40 and i.endswith(".pyc"):
            f = open(i, "rb")
            data = f.read()
            f.close()

os.chdir("..")

data = data.split(b"stub-oz,")[-1].split(b"\x63\x03")[0].split(b"\x10")

try:
    key = base64.b64decode(data[0].split(b"\xDA")[0])
    iv = base64.b64decode(data[-1])
    zipfile = os.path.join('./blank.aes')
except:
    print("Invalid file")

def decrypt(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted

if os.path.isfile(zipfile):
    with open(zipfile, "rb") as f:
        ciphertext = f.read()
    decrypted = decrypt(key, iv, zlib.decompress(ciphertext[::-1]))
    with open("stub.zip", "wb") as f:
        f.write(decrypted)
    try:
        with ZipFile('stub.zip', 'r') as f:
            f.extractall()
    except:
        print("An error occurred while decrypting the file, please contact on discord: lululepu.")

f = open("stub-o.pyc", "rb")
data = f.read()
a = b"\xFD\x37\x7A\x58\x5A\x00" + data.split(b"\xFD\x37\x7A\x58\x5A\x00")[-1]
last = lzma.decompress(a).decode()

l = last.split(";")[:-1]
for i in range(len(l)):
    l[i] = l[i] + ";"
exec("".join(l))

with open("last.pyc", "wb") as f:
    try:
        f.write(base64.b64decode(codecs.decode(____, "rot13") + _____ + ______[::-1] + _______))
    except:
        print("Error occurred while deobfuscating, please contact on discord: lululepu.")

def strings(filename, min=4):
    with open(filename, errors="ignore") as f:
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                yield result
            result = ""
        if len(result) >= min:
            yield result

webhook = ""
for i in strings("last.pyc"):
    i = bytes(i, encoding="utf8")
    try:
        a = base64.b64decode(i)
        if "discord.com/api/webhooks/" in a.decode():
            webhook = a.decode()
    except:
        pass

with open("webhook.txt", "w") as f:
    f.write(webhook)

os.remove("stub.zip")
os.remove("stub-o.pyc")
os.remove("last.pyc")
os.remove("blank.aes")
shutil.rmtree(f"{os.path.basename(executable)}_extracted")