
class Animal(object):
    def __init__(self):
        self._age = 1

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age
        print("anaial set  age")


class Dog(Animal):
    def __init__(self):
        self._age = 2

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self.age = age
        print("dog set age")

def test_describe():
    an = Animal()
    an.age = 14
    print("anmial age", an.age)

    dog = Dog()
    Animal.age = 16
    print("dog age",dog.age)