#encoding:utf-8
class TestCaseInfo(object):
    def __init__(self, name, func, brief):
        self.name = name
        self.infos = []
        self.passed = True
        self.errors = []
        self.subcases = []
        self.func = func
        self.brief = brief

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
            total = len(self.subcases)
            fails = [sub for sub in self.subcases if not sub.is_passed()]
            passed_cnt = total - len(fails)
        else:
            total = 1
            passed_cnt = 1 if self.passed else 0
            fails =[] if self.passed else [self]
        return total, passed_cnt,fails

    def write_doc(self, doc_engine, group=False):
        if len(self.subcases) > 0:
            doc_engine.start_group(self.name, self.brief)
            for case in self.subcases:
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
        for case in self.subcases:
            row_cells = table.add_row().cells
            row_cells[0].text = self.name
            row_cells[1].text = case.name
            if case.is_passed():
                row_cells[2].text = "通过"
            else:
                row_cells[2].text = "失败"
