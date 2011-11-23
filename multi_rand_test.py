from numpy import random
from multiprocessing import Process

def printrand(number):
    rndn = random.random()
    print "n:",number,"r:",rndn

if __name__=='__main__':
    num = 1
    p_list = []
    for proc in range(10):
        p_list.append(Process(target=printrand, args=(proc,)))
        p_list[-1].start()


