from dotenv import load_dotenv

import pymysql
import os

# Conexión a la base de datos
load_dotenv()  # carga variables de .env en local

# En local carga el env y en el servidor ya están en el entorno de secrets
connection = pymysql.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"]
)

cursor = connection.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# Generar el archivo database.dbml
with open("database.dbml", "w") as f:
    for table in tables:
        table_name = table[0]
        f.write(f"Table {table_name} {{\n")
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = cursor.fetchall()
        for column in columns:
            col_name, col_type, _, col_key, _, _ = column
            f.write(f"  {col_name} {col_type}")
            if col_key == "PRI":
                f.write(" [primary key]")
            f.write("\n")
        f.write("}\n\n")

cursor.close()
connection.close()