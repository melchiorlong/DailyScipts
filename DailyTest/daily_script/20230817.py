s = ""
a = [3, 8, 5, 1, 8, 5, 3, 2, 7]

i = 0
while i < len(a):
	if a[i] % 2 != 0:
		s += str(a[i] + a[a[i]])
		i += 2
	else:
		i -= 1

print(s)
