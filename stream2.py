import sys
import time
param1 = sys.argv[1]
param2 = sys.argv[2]
param3 = sys.argv[3]
if len(sys.argv) != 4:
    print("Usage: script.py <param1> <param2> <param3>")
    sys.exit(1)
else:
    print('ID = 4')
    for i in range(3):
        time.sleep(1)
        print('naem:',param1)
        print()
        time.sleep(1)
        print('account:',param2)
        print()
        time.sleep(1)
        print('password:',param3)
        print()
        print('---------------------------------------------------')
