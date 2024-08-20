# import re
#
# # 示例SQL脚本
# sql_script = """
# SELECT * FROM table1;
# SELECT column1, column2 FROM table2;
# INSERT INTO table3 (column1, column2) VALUES ('value1', 'value2');
# UPDATE table4 SET column1 = 'value1' WHERE column2 = 'value2';
# DELETE FROM table5 WHERE column1 = 'value1';
# SELECT a.column1, b.column2 FROM table6 a JOIN table7 b ON a.id = b.id;
# """
#
# # 使用正则表达式提取表名
# table_names = re.findall(r'FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\s|;|,|$)', sql_script, re.IGNORECASE)
#
# # 去重并排序
# unique_table_names = sorted(set(table_names))
#
# print("Table names found in SQL script:")
# for table_name in unique_table_names:
#     print(table_name)


s1 = {1, 2, 3, 4}

s2 = {1, 5, 6, 7}
s3 = s1 | s2
print(s3)
