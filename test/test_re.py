import re


def to_tuple():
    pass


def test_re_findall():
    txt = r"（u32,wd,aid)(u16,wd,panid）(u16，wd,pw）(u32,wd,gid）(u16,wd,sid）"
    #txt = r"（u32,wd,aid)"
    matchs = re.findall(r"[(（](\w*)[,，](\w*)[,，](\w*)[)）]", txt)
    print(matchs)

    # txt = r"(u32,wd,aid)(u16,wd,panid)(u16,wd,pw)(u32,wd,gid)(u16,wd,sid)"
    # matchs = re.findall(r"[(（)）]", "（s，s，s）(（（（（）））", )
    # print(matchs)

def test_replce():
    x ="xxxxx:"
    y= x.replace(':','_')
    print(x,y)