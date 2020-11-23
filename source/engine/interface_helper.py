import re
from engine.public_case import FunCaseAdapter
from tools.filetool import get_file_list
import importlib
import time
from .test_engine import TestEngine
import os

def set_output_dir(path):
    import os
    def to_source_dir(path):
        ret = re.search(r"(.*)autotest.*",path)
        if ret is None:
            return None
        return ret.group(1)
    source_path = to_source_dir(path)
    if source_path is not None:
        os.chdir(source_path)
    TestEngine.instance().set_output_dir(path)

def _parse_doc_string(doc_string):
    if doc_string is None:
        doc_string = "默认"
    doc_string = doc_string.strip()
    names = doc_string.split("\n")
    brief = None
    if len(names) >= 2:
        briefs = [data.lstrip() for data in names[1:]]
        brief = "\n".join(briefs)
    return names[0],brief


def gather_all_test(variables):
    tests = []
    for key, value in variables.items():
        if key.startswith("test"):
            tests.append(value)
    return tests


def parse_func_testcase():
    public_dir = os.path.join(TestEngine.instance().output_dir, "测试用例")
    files = get_file_list(public_dir)
    for name in files:
        name = os.path.splitext(name)[0]
        if name.startswith("__"):
            continue
        file = os.path.split(TestEngine.instance().output_dir)[-1]
        mod = importlib.import_module("autotest." + file +".测试用例." + name)
        group_brief = getattr(mod, "测试组说明", None)
        tests = gather_all_test(mod.__dict__)
        TestEngine.instance().group_begin(name, None, group_brief)
        for test in tests:
            case_name, case_brief = _parse_doc_string(test.__doc__)
            test = FunCaseAdapter(test)
            TestEngine.instance().test_begin(case_name, test, case_brief)


def parse_public_test_case():
    public_dir = os.path.join(TestEngine.instance().output_dir, "..", "公共用例")
    files = get_file_list(public_dir)
    for name in files:
        name = os.path.splitext(name)[0]
        if name.startswith("__"):
            continue
        mod = importlib.import_module("autotest.公共用例." + name)
        group_brief = getattr(mod, "测试组说明", None)
        tests = gather_all_test(mod.__dict__)
        TestEngine.instance().group_begin(name, None, group_brief)
        for test in tests:
            case_name, case_brief = _parse_doc_string(test.__doc__)
            test = FunCaseAdapter(test)
            TestEngine.instance().test_begin(case_name, test, case_brief)
