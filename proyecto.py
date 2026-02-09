import pandas


print("Proyecto 1 - Mineria de datos")
print("Melisa Mendizabal - Renato Rojas")

#Importación de todos las bases de datos corresponientes a matrimonios
#en un rango de 11 años 
print("\n Cargando bases de datos...")
df12 = pandas.read_spss("matri2012.sav")
df13 = pandas.read_spss("matri2013.sav")
df14 = pandas.read_spss("matri2014.sav")
df15 = pandas.read_spss("matri2015.sav")
df16 = pandas.read_spss("matri2016.sav")
df17 = pandas.read_spss("matri2017.sav")
df18 = pandas.read_spss("matri2018.sav")
df19 = pandas.read_spss("matri2019.sav")
df20 = pandas.read_spss("matri2020.sav")
df21 = pandas.read_spss("matri2021.sav")
df22 = pandas.read_spss("matri2022.sav")



#Almacenamiento de dataframes en lista para optimizar el recorrido entre todos los df
dataframes = {
    2012: df12, 2013: df13, 2014: df14,
    2015: df15, 2016: df16, 2017: df17, 
    2018: df18, 2019: df19, 2020: df20, 
    2021: df21, 2022: df22
}

#Verificación de la cantidad de variables dentro de cada dataframe
#Todas se comparan en base a la primera (2015)
base_cols = df12.columns   

#Recorrido para compara que se tengan las mismas columnas entre los dataframes 
print("\n Compraración entre las variables de dataframes")
for year, df in dataframes.items():
    if base_cols.equals(df.columns):
        print("  - ",year, "columnas iguales")
    else:
        print("  - ", year, "columnas distintas")

        faltan = set(base_cols) - set(df.columns)
        sobran = set(df.columns) - set(base_cols)

        if faltan:
            print("    Faltan columnas: ", sorted(faltan))
        if sobran:
            print("    Columnas extra: ", sorted(sobran))

#Todas las columnas son iguales


