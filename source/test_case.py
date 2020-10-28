#encoding:utf-8
from autotest.resuse.basic_helper import PublicCase
class TestCaseInfo(object):
    def __init__(self, name, func, brief):
        self.name = name
        self.infos = []
        self.passed = True
        self.errors = []
        self.subcases = []
        self.func = func
        if brief is not None:
            brief = brief.strip()
        self.brief = brief
        self.enable = True

    def clear(self):
        self.errors = []
        self.passed =True
        self.infos = []

    def is_enable(self):
        return self.enable

    def set_enable(self, enable):
        self.enable = enable

    def add_fail_test(self,role, tag, msg):
        self.passed = False
        self.errors.append((role, tag, msg))

    def add_normal_operation(self, role, tag, msg):
        self.infos.append((role, tag, msg))

    def add_sub_case(self, name, func, brief):
        case = TestCaseInfo(name, func, brief)
        self.subcases.append(case)
        return case

    def is_passed(self):
        passed = True
        for sub in self.subcases:
            passed = passed and sub.is_passed()
        return passed and self.passed

    def summary(self):
        if len(self.subcases) > 0:
            valid_cases = self.get_valid_sub_cases()
            total = len(valid_cases)
            fails = [sub for sub in valid_cases if not sub.is_passed()]
            passed_cnt = total - len(fails)
        else:
            total = 1
            passed_cnt = 1 if self.passed else 0
            fails =[] if self.passed else [self]
        return total, passed_cnt,fails

    def write_doc(self, doc_engine, group=False):
        if len(self.subcases) > 0:
            doc_engine.start_group(self.name, self.brief)
            for case in self.get_valid_sub_cases():
                case.write_doc(doc_engine)
            doc_engine.end_group(self.name)
        else:
            if group:
                doc_engine.start_group(self.name, self.brief)
            else:
                doc_engine.start_test(self.name, self.brief)
            for body in self.infos:
                doc_engine.add_tag_msg(*body)
            for error in self.errors:
                doc_engine.add_tag_msg(*error)
            if group:
                doc_engine.end_group(self.name)
            else:
                doc_engine.end_test(self.name)

    def get_fail_msg(self):
        return self.errors[0][1]

    def write_fail_table(self, table):
        row_cells = table.add_row().cells
        row_cells[0].text = self.name
        row_cells[1].text = self.get_fail_msg()

    def write_summary_table(self, table):
        row_cells = table.add_row().cells
        row_cells[0].text = self.name
        row_cells[1].text = ""
        if self.is_passed():
            row_cells[2].text = "通过"
        else:
            row_cells[2].text = "失败"
        for case in self.get_valid_sub_cases():
            row_cells = table.add_row().cells
            row_cells[0].text = self.name
            row_cells[1].text = case.name
            if case.is_passed():
                row_cells[2].text = "通过"
            else:
                row_cells[2].text = "失败"

    def get_valid_sub_cases(self):
        valids = [case for case in self.subcases if case.is_enable()]
        return valids

    def config_dict(self):
        ret = {}
        ret["enable"] = self.enable
        if isinstance(self.func, PublicCase):
            ret["paras"] = self.func.get_config_value()
        else:
            ret["paras"] = {}
        subcase = {}
        for sub in self.subcases:
            subcase[sub.name] = sub.config_dict()
        ret["subcase"] = subcase
        return ret

    def load_config(self, config):
        self.enable = config['enable']
        if isinstance(self.func, PublicCase):
            self.func.load_config_value(config["paras"])
        subconfig = config['subcase']
        for sub in self.subcases:
            if sub.name in subconfig:
                sub.load_config(subconfig[sub.name])


    def get_para_widgets(self):
        if isinstance(self.func, PublicCase):
            return self.func.get_para_widgets()
        else:
            return []

