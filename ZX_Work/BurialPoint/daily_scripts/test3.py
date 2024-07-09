import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML
from sqllineage.runner import LineageRunner


def extract_tables_and_columns(parsed):
    tables = set()
    columns = set()
    join_clauses = []

    def extract_from_part(parsed):
        from_seen = False
        for item in parsed.tokens:
            if from_seen:
                if is_subselect(item):
                    for x in extract_from_part(item):
                        yield x
                elif item.ttype is Keyword:
                    return
                elif item.ttype is None:
                    for x in extract_from_part(item):
                        yield x
                else:
                    yield item
            elif item.ttype is Keyword and item.value.upper() == 'FROM':
                from_seen = True

    def extract_columns(parsed):
        select_seen = False
        for item in parsed.tokens:
            if select_seen:
                if isinstance(item, IdentifierList):
                    for identifier in item.get_identifiers():
                        columns.add(identifier.get_real_name())
                elif isinstance(item, Identifier):
                    columns.add(item.get_real_name())
            elif item.ttype is DML and item.value.upper() == 'SELECT':
                select_seen = True

    def is_subselect(parsed):
        if not parsed.is_group:
            return False
        for item in parsed.tokens:
            if item.ttype is DML and item.value.upper() == 'SELECT':
                return True
        return False

    for item in extract_from_part(parsed):
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                tables.add(identifier.get_real_name())
        elif isinstance(item, Identifier):
            tables.add(item.get_real_name())

    extract_columns(parsed)

    for token in parsed.tokens:
        if isinstance(token, IdentifierList):
            for sub_token in token.get_identifiers():
                if 'JOIN' in sub_token.value.upper():
                    join_clauses.append(sub_token.value)
        elif isinstance(token, Identifier):
            if 'JOIN' in token.value.upper():
                join_clauses.append(token.value)
        elif 'JOIN' in token.value.upper():
            join_clauses.append(token.value)

    return tables, columns, join_clauses


def parse_sql_script(script):
    statements = sqlparse.split(script)
    for statement in statements:
        statement = statement.strip()
        if statement:
            runner = LineageRunner(statement)
            source_tables = runner.source_tables
            target_tables = runner.target_tables

            parsed = sqlparse.parse(statement)[0]
            tables, columns, joins = extract_tables_and_columns(parsed)

            print("SQL语句:")
            print(statement)
            print("源表: ", source_tables)
            print("目标表: ", target_tables)
            print("SELECT字段: ", columns)
            print("关联关系: ", joins)
            print("\n")


# 示例 SQL 脚本
sql_script = """
CREATE TABLE result_table AS
SELECT a.id, b.name, c.value
FROM table_a a
JOIN table_b b ON a.id = b.id
LEFT JOIN table_c c ON b.id = c.id;

INSERT INTO another_table (id, name)
SELECT id, name
FROM result_table;
"""

# 解析 SQL 脚本
parse_sql_script(sql_script)
