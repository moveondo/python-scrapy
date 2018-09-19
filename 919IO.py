
# try:
#     f =  open('/Users/my/Documents/py/914.py', 'r')
#     print(f.read())
# finally:
#     if f:
#         f.close()

with open('/Users/my/Documents/py/hello.py', 'r') as f:
    #   f.write('Hello, python2!')
     print(f.read())

# from io import StringIO
# f = StringIO()
# f.write('hello')
# f.write(' ')
# f.write('world!')
# print(f.getvalue())

# from io import StringIO
# f = StringIO('Hello!\nHi!\nGoodbye!')
# while True:
#         s = f.readline()
#         if s == '':
#             break
#         print(s.strip())


# from io import BytesIO
# f = BytesIO()
# f.write('中文'.encode('utf-8'))
# print(f.getvalue())

import json

class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }

s = Student('Bob', 20, 88)
print(json.dumps(s, default=student2dict))