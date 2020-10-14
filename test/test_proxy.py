import types

class Work1(object):
    def __init__(self):
        super(Work1, self).__init__()

    def work(self, ctx):
        print("i am work1, start xxxxxx")


class Work2(object):
    def __init__(self):
        super(Work2, self).__init__()

    def work(self, ctx):
        print("i am work2, start ooooooo")


class SwitchContext(object):
  def __init__(self, obj, method):
    self.obj = obj
    self.method = method

  def __call__(self, *args, **kws):
    print('Log: ' + str(self.obj) + ' call ' + self.method.__name__)
    ret = self.method(*args, **kws)
    print('Log: ' + str(self.obj) + ' call ' + self.method.__name__ + ' finished')
    return ret


class WorkProxy(object):
    def __init__(self):
        self.a = 1111
        self.worker = Work1()
        self.proxies = {}

    def __getattr__(self, attr):
        if hasattr(self.worker, attr):
            ret = getattr(self.worker, attr)
            if isinstance(ret, types.MethodType):
                if ret not in self.proxies:
                    self.proxies[ret] = SwitchContext(self, ret)
                return self.proxies[ret]
            raise ret
        else:
            raise NotImplemented


def test_get():
    ex = WorkProxy()
    ex.work(2)


def test_kwargs():
    def print_args(header,**kwargs):
        print(header)
        for key, value in kwargs:
            print(key, value)

    print_args("xx",ss="hello")