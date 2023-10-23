import random


def str_space(a, b):
    return f'Hello World'


def desc_rand(pre):
    return f'{pre} {random.randint(1,10)}'


print(str_space("Hello", "World"))
print(desc_rand("Random number is"))
