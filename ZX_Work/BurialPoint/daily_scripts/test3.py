import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Function, Token
from sqlparse.tokens import Keyword, DML, Punctuation


def extract_tables_and_columns(parsed):
    tables = set()
    columns = set()
    joins = []
    where_conditions = []

    def extract_from_part(parsed):
        from_seen = False
        join_seen = False
        where_seen = False
        join_clause = None

        for item in parsed.tokens:
            if from_seen:
                if is_subselect(item):
                    for x in extract_from_part(item):
                        yield x
                elif item.ttype is Keyword and 'JOIN' in item.value.upper():
                    join_seen = True
                    if join_clause:
                        joins.append(join_clause)
                    join_clause = {'type': item.value.upper(), 'condition': ''}
                elif join_seen and item.ttype is Keyword and item.value.upper() == 'ON':
                    join_seen = False
                    join_clause['condition'] = ''
                elif join_clause and join_clause['condition'] is not None:
                    if item.ttype in (None, Keyword, Identifier, Token):
                        join_clause['condition'] += item.value
                elif isinstance(item, IdentifierList):
                    for identifier in item.get_identifiers():
                        tables.add(identifier.get_real_name())
                elif isinstance(item, Identifier):
                    tables.add(item.get_real_name())
                elif item.ttype is Keyword and item.value.upper() == 'WHERE':
                    where_seen = True
                elif where_seen:
                    where_conditions.append(item.value.strip())
            elif item.ttype is Keyword and item.value.upper() == 'FROM':
                from_seen = True

        if join_clause:
            joins.append(join_clause)

    def extract_columns(parsed):
        select_seen = False
        case_when = False
        case_expr = ""
        current_column = ""

        for item in parsed.tokens:
            if select_seen:
                if isinstance(item, IdentifierList):
                    for identifier in item.get_identifiers():
                        columns.add(str(identifier))
                elif isinstance(item, Function):
                    columns.add(str(item))
                elif isinstance(item, Identifier):
                    if item.get_real_name() not in tables:
                        columns.add(str(item))
                elif item.ttype is Keyword and item.value.upper() == 'CASE':
                    case_when = True
                    case_expr = item.value
                elif case_when:
                    case_expr += item.value
                    if item.ttype is Keyword and item.value.upper() == 'END':
                        case_when = False
                        columns.add(case_expr.strip())
                        case_expr = ""
                elif item.ttype in (Punctuation,) and item.value == ',':
                    if current_column:
                        columns.add(current_column.strip())
                        current_column = ""
                elif item.ttype not in (Keyword, DML):
                    current_column += item.value.strip()
            elif item.ttype is DML and item.value.upper() == 'SELECT':
                select_seen = True

        if current_column:
            columns.add(current_column.strip())

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

    return tables, columns, joins, where_conditions


# 示例 SQL 脚本解析
def parse_sql_script(script):
    statements = sqlparse.split(script)
    for statement in statements:
        statement = statement.strip()
        if statement:
            parsed = sqlparse.parse(statement)[0]
            tables, columns, joins, where_conditions = extract_tables_and_columns(parsed)

            print("SQL语句:")
            print(statement)
            print("源表: ", tables)
            print("SELECT字段: ", columns)
            print("关联关系: ", joins)
            print("WHERE条件: ", where_conditions)
            print("\n")


# 示例 SQL 脚本
sql_script = """
CREATE TABLE result_table AS
SELECT a.id, b.name, c.value,
       CASE WHEN a.type = 'A' THEN 'Type A'
            WHEN a.type = 'B' THEN 'Type B'
            ELSE 'Other' END as type_description,
       SUM(a.amount) as total_amount
FROM table_a a
JOIN table_b b ON a.id = b.id
LEFT JOIN table_c c ON b.id = c.id
WHERE a.status = 'active' AND b.amount > 1000
GROUP BY a.id, b.name, c.value, a.type;

INSERT INTO another_table (id, name)
SELECT id, name
FROM result_table
WHERE id > 10;
"""

# 解析 SQL 脚本
parse_sql_script(sql_script)
