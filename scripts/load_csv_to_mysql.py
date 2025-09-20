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

# Conectar a la base de datos
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = connection.cursor()

# Insertar los datos en la tabla
for _, row in data.iterrows():
    query = """
    INSERT INTO crimes (DR_NO, Date_Rptd, DATE_OCC, TIME_OCC, AREA, AREA_NAME, Rpt_Dist_No, Part_1_2, Crm_Cd, Crm_Cd_Desc, Vict_Age, Vict_Sex, Vict_Descent, Premis_Cd, Premis_Desc, Status, Status_Desc, LOCATION, LAT, LON)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        row["DR_NO"], row["Date Rptd"], row["DATE OCC"], row["TIME OCC"], row["AREA"], row["AREA NAME"],
        row["Rpt Dist No"], row["Part 1-2"], row["Crm Cd"], row["Crm Cd Desc"], row["Vict Age"],
        row["Vict Sex"], row["Vict Descent"], row["Premis Cd"], row["Premis Desc"], row["Status"],
        row["Status Desc"], row["LOCATION"], row["LAT"], row["LON"]
    )
    cursor.execute(query, values)

connection.commit()
cursor.close()
connection.close()

print("Datos cargados exitosamente.")