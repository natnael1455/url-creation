# python code to demonstrate working of reduce()

# importing functools for reduce()
import functools

# initializing list
lis = [
    1,
    3,
    5,
    6,
    2,
]

# using reduce to compute sum of list
print("The sum of the list elements is : ", end="")

print(list(functools.reduce(lambda a, b: a + 2, lis)))
