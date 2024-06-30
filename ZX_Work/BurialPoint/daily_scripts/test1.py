l1 = ['26428',
      '26429',
      '26431',
      '26478',
      '26656',
      '20657',
      '27409',
      '27410',
      '27411',
      '27413',
      '27414',
      '27415',
      '27416',
      '27417',
      '27418',
      '27419',
      '27420',
      '27422'
      ]

l2 = []
for num in l1:
    l2.append("'" + num + "'")
str2 = ','.join(l2)

l3 = ["'" + num + "'" for num in l1]


str1 = """
select 
*
from a
where 1=1 
and job_name in ({job_name},'') 
""".format(
    job_name=str2
)

print(l2)
print(l3)