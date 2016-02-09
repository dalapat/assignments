import sys

'''try:
    for line in sys.stdin:
        print line
except EOFError:
    pass'''
try:
    for line in sys.stdin.read():
        sys.stdout.writelines(line)
except EOFError:
    pass

'''try:
    sys.stdout = open("output.txt", "w")
    for line in sys.stdin.readlines():
        sys.stdout.writelines(line)
except EOFError:
    pass
finally:
    sys.stdout.close()'''



