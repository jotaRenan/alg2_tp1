import sys
import re
import shutil
import getopt

from io import StringIO
from struct import unpack

Txt = "txt"
Byte_Offset = 4


def main():

    try:
        (opts, args) = getopt.getopt(sys.argv[3:], "o:")
    except getopt.GetoptError:
        print("main.py -c <arquivo_entrada> [-o <arquivo_saida>]")

    file_extension, in_filename, out_filename = get_output_filename(opts)
    if file_extension == Txt:
        compress(in_filename, out_filename)
    elif file_extension == "z78":
        decompress(in_filename, out_filename)


def get_output_filename(optional_args):
    arg_output_file = None
    for opt, arg in optional_args:
        if opt in ["-o"]:
            arg_output_file = arg

    in_filename = sys.argv[2]
    file_extension = in_filename.split(".")[-1]
    file_name = in_filename.split(".")[0]
    if file_extension == Txt:
        arg_output_file = arg_output_file or file_name + ".z78"
    elif file_extension == "z78":
        arg_output_file = arg_output_file or file_name + ".txt"
    else:
        raise ValueError("Invalid file extension")
    return (file_extension, in_filename, arg_output_file)


class TrieDictionary:
    dic = {}
    next_code = 0

    def contains(self, possible_key):
        return possible_key in self.dic

    def lookup(self, key):
        return self.dic[key]

    def put(self, key):
        self.dic[key] = self.next_code
        self.next_code += 1


def compress(FileIn, FileOut):
    with open(FileIn, mode="r") as input_file:
        text = input_file.read()
    dic = TrieDictionary()

    dic.put("")
    string = ""
    with open(FileOut, mode="wb") as f:
        for char in text:
            if dic.contains(string + char):
                string = string + char
            else:
                f.write(dic.lookup(string).to_bytes(Byte_Offset, byteorder="big"))
                f.write(char.encode("utf-8"))
                dic.put(string + char)
                string = ""
        if char:
            f.write(dic.lookup(string).to_bytes(Byte_Offset, byteorder="big"))
            f.write(" ".encode("utf-8"))


def decompress(FileIn, FileOut):
    with open(FileIn, mode="rb") as f:
        binary = f.read()

    dic = {}
    dic[0] = ""
    buf = StringIO()
    size = 1

    for i in range(0, len(binary), Byte_Offset + 1):
        k = int.from_bytes(binary[i : i + Byte_Offset], byteorder="big")
        v = "".join(map(chr, [binary[i + Byte_Offset]]))
        cur_string = dic[k] + v
        dic[size] = cur_string
        if i + Byte_Offset + 1 >= len(binary):
            buf.write(cur_string[:-1])
        else:
            buf.write(cur_string)
        size += 1

    with open(FileOut, mode="w") as f:
        buf.seek(0)
        shutil.copyfileobj(buf, f)


if __name__ == "__main__":
    main()
