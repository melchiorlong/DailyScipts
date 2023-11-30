import re

s1 = '123嗷1嗷12'

print(re.sub('^\d*', '', s1))
