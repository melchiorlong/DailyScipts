def add_param(a, b):
    return a + b
#
#
# def mult_param(func, a, b, c):
#     return func(a, b) * c
#
#
# a, b, c = 1, 2, 3
#
# r1 = add_param(a, b)
#
# r2 = mult_param(add_param, a, b, c)
#
# print(r1)
# print(r2)
#

def mult_dict(func, c, **params):
    return func(**params) * c


r3 = mult_dict(add_param, c, a=1, b=2)
print(r3)
