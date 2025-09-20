import os
import pandas as pd
import mysql.connector

# Obtener las credenciales desde las variables de entorno
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Leer el archivo CSV
csv_file = "crimes_2020.csv"
data = pd.read_csv(csv_file, delimiter=";")  
data = data.where(pd.notnull(data), None)  # Reemplazar NaN por None

# Detectar dinámicamente las columnas del archivo CSV
columns = data.columns.tolist()
print(f"Columnas detectadas en el archivo CSV: {columns}")

# Generar la consulta SQL dinámicamente
table_name = "crimes"  # Cambia esto al nombre de tu tabla
placeholders = ", ".join(["%s"] * len(columns))
columns_sql = ", ".join([f"`{col}`" for col in columns])
query = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"

# Conectar a la base de datos
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = connection.cursor()

# Insertar los datos en bloque
values = [tuple(row[col] for col in columns) for _, row in data.iterrows()]
cursor.executemany(query, values)

connection.commit()
cursor.close()
connection.close()

print("Datos cargados exitosamente.")
