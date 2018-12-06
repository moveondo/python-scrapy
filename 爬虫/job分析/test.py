def fun():
    for i in range(20):
        x=yield i
        print('good', x,i)

if __name__ == '__main__':
    # for x in fun():
    #     print(x)
    a = fun()
    for i in range(20):
        x=a.__next__()
        print(x)
    # a.__next__()
    # x = a.send(5)
    # print(x)