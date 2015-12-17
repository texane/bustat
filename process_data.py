#!/usr/bin/env python

def main():
    f = open('./data.o', 'r')
    while True:
        l = f.readline()
        if len(l) == 0: break
        if l[0] == '#': continue
        v = l.rstrip().split(' ')
        people = float(v[-3])
        bakers = float(v[-2])
        butchers = float(v[-1])
        if (people == 0) or (bakers == 0) or (butchers == 0): continue
        print(str(people) + ' ' + str(people / bakers) + ' ' + str(people / butchers))
    return

main()
