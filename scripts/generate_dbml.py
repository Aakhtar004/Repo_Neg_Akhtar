import pymysql
import os

# Conexión a la base de datos
connection = pymysql.connect(
    host=os.getenv("DB_HOST", "localhost"),  # Valor predeterminado: "localhost"
    user=os.getenv("DB_USER", "root"),      # Valor predeterminado: "root"
    password=os.getenv("DB_PASSWORD", ""),  # Valor predeterminado: cadena vacía
    database=os.getenv("DB_NAME", "test")   # Valor predeterminado: "test"
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