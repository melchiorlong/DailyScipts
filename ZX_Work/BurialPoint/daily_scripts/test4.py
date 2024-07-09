import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where
from sqlparse.tokens import Keyword, DML
from sqllineage.runner import LineageRunner
from sqllineage import run_l

# 定义 SQL 脚本
sql_script = """
CREATE TABLE result_table AS
SELECT a.id, b.name, c.value
FROM table_a a
JOIN table_b b ON a.id = b.id
LEFT JOIN table_c c ON b.id = c.id;
RIGHT JOIN table_d d ON c.id = d.id;

INSERT INTO another_table (id, name)
SELECT id, name
FROM result_table;
"""

# 使用 sqlparse 分割 SQL 脚本为独立的语句
statements = sqlparse.split(sql_script)

# 分析每个 SQL 语句
for statement in statements:
    if statement.strip():  # 确保语句不为空
        print(f"\nAnalyzing SQL: {statement}")
        # 使用 SQLLineage 进行分析
        result = SQLLineage(statement)

        # 输出源表和目标表
        print("Source Tables:", [str(table) for table in result.source_tables])
        print("Target Tables:", [str(table) for table in result.target_tables])

        # 使用 sqlparse 进行深入解析以获取字段和 JOIN 信息
        parsed = sqlparse.parse(statement)[0]
        select_columns = []
        joins = []

        # 遍历 tokens 来获取 SELECT 中的字段和 JOIN 信息
        for token in parsed.tokens:
            if isinstance(token, sqlparse.sql.IdentifierList):
                for identifier in token.get_identifiers():
                    select_columns.append(str(identifier))
            elif isinstance(token, sqlparse.sql.Identifier):
                select_columns.append(str(token))
            elif token.ttype is sqlparse.tokens.Keyword and 'JOIN' in token.value.upper():
                joins.append(token.value)

        # 输出 SELECT 的字段
        print("Columns Selected:", select_columns)
        # 输出 JOIN 信息
        if joins:
            print("Join Operations:", joins)
        else:
            print("No join operations in this SQL.")
