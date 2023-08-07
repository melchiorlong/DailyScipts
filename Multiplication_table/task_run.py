import random
from random import choice

questions = 100
number_max = 99
methods = ['+', '-', ]

task_number = 0
while task_number <= questions:
	number_a = random.randint(0, number_max)
	number_b = random.randint(0, number_max)
	method = choice(methods)
	if method == '-':
		if number_a < number_b:
			continue
	# if method == '+':
	# 	if number_a + number_b >= 100:
	# 		continue
	if method == '/':
		if number_b == 0:
			continue
		if number_a % number_b != 0:
			continue
	ques_str = str(number_a) + " " + method + " " + str(number_b) + " = "
	print(ques_str)
	task_number += 1
