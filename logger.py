import sys

CONSOLE = False

def clear_logs():
    file = open('log.txt', 'r+')
    file.truncate(0)
    file.close()

def logger(message, *options):
    if CONSOLE:
        print(message)
    print(message, file=open('log.txt', 'a'))

    for option in options:
        if CONSOLE:
            print(option)
        print(option, file=open('log.txt', 'a'))