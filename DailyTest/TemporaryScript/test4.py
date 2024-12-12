import re

# 定义包含各种情况的数据列表
data_list = [
    "CREATE TEMP something AS (select * from tableA where xx.xx = (2) and yy.yy = (3))",
    "CREATE LOCAL TEMP another AS (select id, name from tableB where age = (25))",
    "CREATE TEMP invalid (no as clause)",
    "CREATE LOCAL TEMP test AS select * from tableC where yy.yy > 5;",
    "CREATE TEMP something AS select * from tableA where xx.xx = 2;"
]

# 正则表达式
pattern = r"CREATE\s+(LOCAL\s+)?TEMP.*?AS\s+(?:\((.*?)\)|(.+?));?$"

# 循环遍历列表并提取符合条件的内容
results = []
for item in data_list:
    match = re.search(pattern, item, re.IGNORECASE)
    if match:
        # 检查捕获组，括号内容在 group(2)，无括号的内容在 group(3)
        logic_content = match.group(2) or match.group(3)
        results.append(logic_content.strip())

# 输出结果
for i, result in enumerate(results, start=1):
    print(f"匹配结果 {i}: {result}")
