#!/usr/local/bin/python
print('Welcome to The Ultimate Math Challenge!')
print('My name is Franciscus Vieta and this is my challenge.')
print('If you answer all 100 of my questions correctly, I will give you the flag.\n')
from random import randint
def gen_q():
    #1.sum of roots
    #2.sum of reciprocals of roots
    #3.sum of squares of roots
    l=[1] + [randint(-100,100) for _ in range(randint(10,20))]
    choice = randint(1,3)
    if choice == 1:
        print('Find the sum of the roots of the given polynomial: ')
        return l,-1*l[1]
    elif choice == 2:
        print('Find the sum of the reciprocals of the roots of the given polynomial: ')
        ans = randint(-100,100)
        l[-2]=-1*ans*l[-1]
        return l,ans
    elif choice==3:
        print('Find the sum of the squares of the roots of the given polynomial: ')
        return l,l[1]**2-2*l[2]
for _ in range(100):
    l,ans = gen_q()
    for i in range(len(l)):
        start = '+'
        if l[i] < 0 :
            start = '-'
        start += ' '+str(abs(l[i]))
        if i==0:
            start=''
        print(start+'x^'+str(len(l)-i-1),end=' ')
    print()
    x = input('What is the answer: ')
    try:
        x = int(x)
        assert x == ans
    except:
        print('Invalid input. Exiting...')
        quit()
    print('Correct Answer!')
print('Here is your flag: flag{Viet4s_f0r_th3_win}')
