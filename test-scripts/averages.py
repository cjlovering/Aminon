import time
import os
import sys

def main():
    tsum = 0
    tctr = 0
    
    with open('times.txt', 'r') as fi:
        for line in fi:
            tctr+=1
            tsum+=float(line.strip())

    avg = tsum / tctr
    print avg


if __name__=='__main__':
    main()
