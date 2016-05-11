import sys

try:
    for line in sys.stdin.read():
        sys.stdout.writelines(line)
except EOFError:
    pass




