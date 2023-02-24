#! /usr/bin/python3.11
# imports
from random import choice
# constructing a sample space
sample_space = [i+1 for i in range(0, 10)]
# choosing between 0 and 1
print(f"choice between 0 and 1 is {choice([0, 1])}")
# choosing between 1 and 10
for i in sample_space: print(f"choice between 1 and 10 is {choice(sample_space)}")
i = {}
