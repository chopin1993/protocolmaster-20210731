import os
from database import EsDatabase
import numpy as np
from nose.tools import assert_equal

def test_database():
    name = "test.db"
    if os.path.exists(name):
        os.remove(name)
    database = EsDatabase(name)
    database.append_sample(0,"hello world","rev",np.zeros((3,3)))
    for sample in database.get_sample_images():
        sample = sample
    assert_equal(sample[0], 0)
    assert_equal(sample[1], "hello world")

