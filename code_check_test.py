#!/usr/bin/env python3
import sys
import time
from code_check import CodeCheck
def main():
    start = time.time()
    code_checker = CodeCheck("gobang.py", 15)
    if not code_checker.check_code():
        print(code_checker.errormsg)
    else:
        print('pass')
        print('Total time:', time.time()-start, 's')

if __name__ == '__main__':
    main()


