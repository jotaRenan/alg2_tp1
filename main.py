import sys
import re
import shutil
from io import StringIO
from struct import unpack

Txt = "txt"

def main():
    in_filename = sys.argv[1]
    file_extension = in_filename.split(".")[-1]
    if file_extension == Txt:
        compress(in_filename, "output.tz8")
    elif file_extension == "tz8":
        decompress("output.tz8", "decoded.txt")


def compress(FileIn, FileOut):
    with open(FileIn, mode="r") as input_file:
        text = input_file.read()
    dic = {}
    size = 1
    dic[""] = 0
    string = ""
    with open(FileOut, mode="wb") as f:
        for char in text:
            if string + char in dic:
                string = string + char
            else:
                f.write(dic[string].to_bytes(2, byteorder="big"))
                f.write(char.encode("utf-8"))
                dic[string + char] = size
                size += 1
                string = ""
        if char:
            f.write(dic[string].to_bytes(2, byteorder="big"))
            f.write(" ".encode("utf-8"))


def decompress(FileIn, FileOut):
    dic = {}
    dic[0] = (0, "")
    buf = StringIO()
    size = 1
    with open(FileIn, mode="rb") as f:
        binary = f.read()

    for i in range(0, len(binary), 3):
        k = int.from_bytes(binary[i : i + 2], byteorder="big")
        v = "".join(map(chr, [binary[i + 2]]))
        dic[size] = (k, v)
        progress = getPrefix(size, dic)
        if i + 3 >= len(binary):
            buf.write(progress[:-1])
        else:
            buf.write(progress)
        size = size + 1

    with open(FileOut, mode="w") as f:
        buf.seek(0)
        shutil.copyfileobj(buf, f)


def getPrefix(idx, dic):
    if dic[idx][1] == "":
        return ""
    return getPrefix(dic[idx][0], dic) + dic[idx][1]


if __name__ == "__main__":
    main()
