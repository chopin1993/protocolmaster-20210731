import os
from database import EsDatabase
import numpy as np
from nose.tools import assert_equal,assert_almost_equal,assert_equals,assert_true



def test_database():
    name = "test.db"
    if os.path.exists(name):
        os.remove(name)
    database = EsDatabase(name)
    data = np.linspace(0,1,64,dtype=np.float32)
    data = data.reshape((4,16))
    database.append_sample(0,"hello world","rev",data,data)
    for sample in database.get_sample_images():
        sample = sample
    assert_equal(sample[0], 0)
    assert_equal(sample[1], "hello world")
    test_data =np.frombuffer(sample[3],np.float32)
    test_data = test_data.reshape((4,16))
    assert_true((test_data == data).any())
