#LECCION 1:generar datos base y guardarlos.
import numpy as np
np.random.seed(42)
id_cliente = np.arange(1, 51)
edad = np.random.randint(18, 65, size=50)
total_compras = np.random.randint(1, 15, size=50)
monto_total = np.random.randint(1000, 10000, size=50)
print("Promedio monto:", monto_total.mean())
print("Total compras:", total_compras.sum())
print("Cantidad clientes:", len(id_cliente))
datos = np.array([id_cliente, edad, total_compras, monto_total])
np.save("clientes_numpy.npy", datos)

#LECCION 2:Explorar y transformar los datos generados en la Lección 1, utilizando la estructura de DataFrame de Pandas.
import pandas as pd
datos = np.load("clientes_numpy.npy")
df_base = pd.DataFrame({
    "id_cliente": datos[0],
    "edad": datos[1],
    "total_compras": datos[2],
    "monto_total": datos[3]
})
print(df_base.head())
print(df_base.tail())
print(df_base.describe())
# Filtro
print(df_base[df_base["monto_total"] > 8000])
# Guardar CSV
df_base.to_csv("clientes_base.csv", index=False)

#LECCION 3: Integrar datos de diversas fuentes y unificarlos en un solo DataFrame para su posterior limpieza.
ruta= r"C:\Users\Papa\Desktop\bootcamp_data_science\clientes_ecommerce.csv"
ruta2= r"C:\Users\Papa\Desktop\bootcamp_data_science\clientes_ecommerce.xlsx"

df_csv = pd.read_csv(ruta)
print(df_csv.head())
df_excel = pd.read_excel(ruta2)
print(df_excel.head())

url = "https://www.w3schools.com/html/html_tables.asp"
tables = pd.read_html(url)
df_web = tables[0]  # primera tabla
print(df_web.head())

# Unificar columnas (asumiendo que ambas tablas tienen una columna "id" para unir)
df_csv.columns = df_csv.columns.str.lower()
df_excel.columns = df_excel.columns.str.lower()
df_total = df_csv.merge(df_excel, on="id", how="left", suffixes=("_csv", "_excel"))

print(df_total.head())

#LECCION 4: Aplicar técnicas de limpieza de datos, resolviendo problemas de valores nulos y datos atípicos.
print(df_total.isna().sum())
df_total["edad_csv"] = df_total["edad_csv"].fillna(df_total["edad_csv"].mean())
df_total["edad_excel"] = df_total["edad_excel"].fillna(df_total["edad_excel"].mean())
Q1 = df_total["monto_total_csv"].quantile(0.25)
Q3 = df_total["monto_total_csv"].quantile(0.75)
IQR = Q3 - Q1

df_total = df_total[
    (df_total["monto_total_csv"] >= Q1 - 1.5 * IQR) &
    (df_total["monto_total_csv"] <= Q3 + 1.5 * IQR)
]
df_total.to_csv("clientes_limpio.csv", index=False)

#LECCION 5: Transformar y enriquecer los datos mediante técnicas de manipulación avanzada.
# Eliminar duplicados
df_total = df_total.drop_duplicates()

# Convertir tipos (USANDO Int64 para evitar errores)
df_total["edad_csv"] = df_total["edad_csv"].astype("Int64")

# Nueva columna
df_total["ticket_promedio"] = (
    df_total["monto_total_csv"] / df_total["total_compras_csv"]
)

# Normalización
df_total["monto_norm"] = (
    df_total["monto_total_csv"] - df_total["monto_total_csv"].min()
) / (
    df_total["monto_total_csv"].max() - df_total["monto_total_csv"].min()
)
df_total.to_csv("clientes_wrangling.csv", index=False)

#LECCION 6: Agrupamiento y pivoteo de datos
resumen = df_total.groupby("ciudad_csv").agg({
    "monto_total_csv": "mean",
    "total_compras_csv": "sum"
})

print(resumen)
tabla_pivot = df_total.pivot_table(
    values="monto_total_csv",
    index="ciudad_csv",
    aggfunc="mean"
)

print(tabla_pivot)
tabla_larga = pd.melt(
    df_total,
    id_vars=["id"],
    value_vars=["monto_total_csv", "total_compras_csv"]
)

print(tabla_larga.head())
df_total.to_csv("clientes_final.csv", index=False)
df_total.to_excel("clientes_final.xlsx", index=False)
print("Datos exportados exitosamente.")
print(df_total.head())




