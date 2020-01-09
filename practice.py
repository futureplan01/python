from sys import argv

script, filename = argv

text = open(filename, 'r')
line = text.readline()

def hello(*args):
    hi,bye = args
    print(hi,bye)

hello("hi","bye")