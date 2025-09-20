import os

# Leer el archivo database.dbml
with open("database.dbml", "r") as f:
    dbml_content = f.readlines()

# Generar el diccionario de datos
output_path = "docs/dictionary.md"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    f.write("# Diccionario de Datos\n\n")
    for line in dbml_content:
        if line.startswith("Table"):
            table_name = line.split()[1]
            f.write(f"## Tabla: {table_name}\n\n")
            f.write("| Columna       | Tipo          |\n")
            f.write("|---------------|---------------|\n")
        elif line.strip() and not line.startswith("}"):
            col_name, col_type = line.strip().split()[:2]
            f.write(f"| {col_name} | {col_type} |\n")
        elif line.startswith("}"):
            f.write("\n")

print(f"Diccionario generado en {output_path}")