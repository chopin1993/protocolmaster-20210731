#encoding:utf-8
import re
from pprint import pprint
import os
from copy import deepcopy
import io
import sys

def trim_code(code):
    code = code.strip()
    lines = code.split("\n")
    lines = [line.lstrip() for line in lines]
    return "\n".join(lines)

def to_output(code, result):
    result = str(result)
    code +="\n```\n" + result +"\n```\n"
    return code

def render(file_name):
    outputs = []
    with open(file_name,"r", encoding="utf-8") as handle:
        content = handle.read(-1)
        codes = re.findall(r"```(.*?)```", content, re.S)
        codes1 = re.findall(r"(```.*?```)", content, re.S)
        assert len(codes1) == len(codes)
        if codes:
            for code,full_code in zip(codes,codes1):
                code = deepcopy(code)
                code = trim_code(code)
                print("-----start-------")
                print(code)
                print("-----end-------")
                save_std = sys.stdout
                sys.stdout = io.StringIO()
                exec(code)
                sys.stdout.seek(0)
                output = sys.stdout.read()
                sys.stdout = save_std
                outputs.append((full_code, output))

    for code, output in outputs:
        content = content.replace(code,to_output(code, output), 1)

    prefix, name = os.path.split(file_name)
    name,ext = os.path.splitext(name)
    name = name+"_render"+ ext
    file_name = os.path.join(prefix,name)
    with open(file_name,"w", encoding="utf-8") as handle:
        handle.write(content)


if __name__ == "__main__":
    render("python入门教程/2.基本数据类型和运算符.md")
