import sqlite3 as sql
from pathlib import Path


def initialize_database(database_file, sql_paths: list[Path]):
    # Connect to SQLite database (creates a new file if it doesn't exist)
    connection = sql.connect(database_file)

    # Create a cursor object to execute SQL commands
    cursor = connection.cursor()

    # Read and execute the SQL commands from the .sql file
    for sql_path in sql_paths:
        with sql_path.open(mode="r", encoding="utf-8") as sql_file:
            print(sql_path)
            sql_script = sql_file.read()
            cursor.executescript(sql_script)

    # Commit the changes and close the connection
    connection.commit()
    connection.close()


def query(qstr: str, conn: sql.Connection = None, db_path: Path = None) -> list:
    q = qstr.strip()
    if conn is not None:
        cur = conn.cursor()
        r = cur.execute(q)
        return r.fetchall()

    if db_path is not None:
        with sql.connect(db_path) as conn:
            cur = conn.cursor()
            r = cur.execute(q)
            return r.fetchall()


def list_table_schemas(database_file: str):
    # Connect to SQLite database
    with sql.connect(database_file) as conn:
        cursor = conn.cursor()

        # Query to retrieve table names and their schema
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()

        # Iterate through tables and print their schema
        for table in table_names:
            table_name = table[0]
            print(f"Table: {table_name}")

            # Query to retrieve the schema of each table
            cursor.execute(f"PRAGMA table_info({table_name});")
            schema_info = cursor.fetchall()

            # Print the schema information
            for column in schema_info:
                column_name = column[1]
                column_type = column[2]
                print(f"  {column_name}: {column_type}")

            print("\n")


# region binary split insertion for tricky records


def insert_records(rows: list[str], table: str, db_con: sql.Connection) -> bool:
    try:
        cur = db_con.cursor()
        istr = ",".join(rows)
        cur.execute(f"INSERT INTO `{table}` VALUES {istr};")
        db_con.commit()
    except sql.OperationalError as er:
        return False
    return True


def smart_insert(db_path: Path, rows: list[str], step: int) -> list[str]:
    # try to insert 1000 rows

    conn = sql.connect(db_path)
    # bad_rows = []
    stack = [(0, step)]
    while stack:
        i, j = stack.pop()
        if i + 5 >= j:  # base case
            # bad_rows += rows[i:j]
            return rows[i:j]
            # continue

        if not insert_records(rows[i:j], "pokemon_moves", conn):
            k = int((i + j) / 2)  # midpoint
            stack.append((i, k))
            stack.append((k, j))

    conn.close()


# path = Path("resources/sql_scripts/pokemon_db/pokemon_moves_G6.sql")
# with path.open(encoding="utf-8") as fp:
#     data = fp.readlines()

# rows = [d+")" for d in data[0].split("),")]

# i, x = 0, None
# step = 1000
# while i < len(rows) and x is None:
#     x = smart_insert("resources/pokemon.db", rows[i:], step)
#     i += step


# endregion binary split insert
