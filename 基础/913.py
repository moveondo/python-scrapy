#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Student(object):
    def __init__(self, name, score,age):
        self.name = name
        self.score = score
        self.age=age

    def get_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 60:
            return 'B'
        else:
            return 'C'
    def set_score(self, score):
        if 0 <= score <= 100:
            self.__score = score #私有变量  __
        else:
            raise ValueError('bad score')

lisa = Student('Lisa', 99,18)
bart = Student('Bart', 59,17)
print(lisa.name, lisa.get_grade(),lisa.age)
print(bart.name, bart.get_grade(),bart.age)


class Animal(object):
    def run(self):
         print('Animal is running...')


class Dog(Animal):
     def run(self):
        print('Dog is running...')

     def eat(self):
        print('Eating meat...')

class Cat(Animal):
    pass

dog = Dog()
dog.run()
dog.eat()

cat = Cat()
cat.run()