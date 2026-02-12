import pandas
import unicodedata


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

df12.drop(columns=['AREAG', 'GETHOM', 'GETMUJ', 'OCUHOM', 'OCUMUJ'], inplace=True)
df13.drop(columns=['AREAGOCU', 'CIUOHOM', 'CIUOMUJ', 'PUEHOM', 'PUEMUJ'],inplace=True)
df14.drop(columns=['AREAGOCU', 'CIUOHOM', 'CIUOMUJ', 'PUEHOM', 'PUEMUJ'],inplace=True)
df15.drop(columns=['AREAGOCU', 'CIUOHOM', 'CIUOMUJ', 'NUNUHO', 'NUNUMU', 'PUEHOM', 'PUEMUJ'],inplace=True)
df16.drop(columns=['AREAGOCU' ,'CIUOHOM', 'CIUOMUJ', 'NUNUHO', 'NUNUMU', 'PUEHOM', 'PUEMUJ'],inplace=True)
df17.drop(columns=['AREAGOCU','CIUOHOM', 'CIUOMUJ', 'NUNUHO', 'NUNUMU', 'PUEHOM', 'PUEMUJ'],inplace=True)
df18.drop(columns=['CIUOHOM', 'CIUOMUJ', 'NUNUHO', 'NUNUMU', 'PUEHOM', 'PUEMUJ'],inplace=True)
df19.drop(columns=['CIUOHOM', 'CIUOMUJ', 'NUNUHO', 'NUNUMU', 'PUEHOM', 'PUEMUJ'],inplace=True)
df20.drop(columns=['CIUOHOM', 'CIUOMUJ', 'NUNUHO', 'NUNUMU', 'PUEHOM', 'PUEMUJ'],inplace=True)
df21.drop(columns=['CIUOHOM', 'CIUOMUJ', 'NUNUHO', 'NUNUMU', 'PUEHOM', 'PUEMUJ'],inplace=True)
df22.drop(columns=['CIUOHOM', 'CIUOMUJ', 'NUNUHO', 'NUNUMU', 'PUEHOM', 'PUEMUJ'],inplace=True)


df12['AÑOOCU'] = 2012
df13['AÑOOCU'] = 2013
df14['AÑOOCU'] = 2014
df15['AÑOOCU'] = 2015
df16['AÑOOCU'] = 2016
df17['AÑOOCU'] = 2017
df18['AÑOOCU'] = 2018

#Verificación de la cantidad de variables dentro de cada dataframe
#Todas se comparan en base a la primera (2012)
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

#Concatenar todos los df individuales
df_final = pandas.concat(dataframes.values(), ignore_index=True)


#LIMPIEZA

def normalizar_texto(s):
    if pandas.isna(s):
        return s
    s = str(s).strip().lower()
    s = ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )
    return s

## se percató que existen incongruencias en las columnas de ESCHOM y ESCMUJ, ya que existían valores como "post grado", "post Grado", "postgrado"
mapa_escolaridad = {
    'primaria': 'Primaria',
    'basico': 'Básico',
    'diversificado': 'Diversificado',
    'universitario': 'Universitario',
    'ninguno': 'Ninguno',
    'ninguna': 'Ninguno',
    'ignorado': 'Ignorado',
    'post grado': 'Postgrado',
    'postgrado': 'Postgrado'
}


for col in ['ESCHOM', 'ESCMUJ']:
    df_final[col] = (
        df_final[col]
        .apply(normalizar_texto)
        .map(mapa_escolaridad)
        .astype('category')
    )




mapa_departamentos = {
    'alta verapaz': 'Alta Verapaz',
    'baja verapaz': 'Baja Verapaz',
    'chimaltenango': 'Chimaltenango',
    'chiquimula': 'Chiquimula',
    'el progreso': 'El Progreso',
    'escuintla': 'Escuintla',
    'guatemala': 'Guatemala',
    'huehuetenango': 'Huehuetenango',
    'izabal': 'Izabal',
    'jalapa': 'Jalapa',
    'jutiapa': 'Jutiapa',
    'peten': 'Petén',
    'quetzaltenango': 'Quetzaltenango',
    'quiche': 'Quiché',
    'retalhuleu': 'Retalhuleu',
    'sacatepequez': 'Sacatepéquez',
    'san marcos': 'San Marcos',
    'santa rosa': 'Santa Rosa',
    'solola': 'Sololá',
    'suchitepequez': 'Suchitepéquez',
    'totonicapan': 'Totonicapán',
    'zacapa': 'Zacapa'
}

for col in ['DEPREG', 'DEPOCU']:
    df_final[col] = (
        df_final[col]
        .apply(normalizar_texto)   # quita tildes + lower
        .map(mapa_departamentos)   # nombre oficial
        .astype('category')
    )

cols_cat = [
    'DEPREG', 'MUPREG', 'CLAUNI',
    'NACHOM', 'NACMUJ',
    'ESCHOM', 'ESCMUJ',
    'DEPOCU', 'MUPOCU',
    'DIAOCU'
]
df_final[cols_cat] = df_final[cols_cat].astype('category')

meses_map = {
    'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6,
    'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
}
df_final['MESOCU'] = df_final['MESOCU'].map(meses_map)
df_final['MESREG'] = df_final['MESREG'].map(meses_map)

cols_num = [
    'MESREG', 'AÑOREG',
    'EDADHOM', 'EDADMUJ',
    'MESOCU', 'AÑOOCU'
]
for col in cols_num:
    df_final[col] = pandas.to_numeric(df_final[col], errors='coerce').astype('float64')

#b------------------------

resumen = pandas.DataFrame({
    'dtype': df_final.dtypes,
    'n_unicos': df_final.nunique()
})
# print(resumen)


# # Se verificaron los datos atípicos; según el excel guía del INE, los datos de 999 eran para datos ignorados, por ende, esos fueron los que se eliminaron
# # Se consideró que los otros máximos (97-98 años) sí podrían llegar a ser realistas, por lo que se conservaron
## si se quiere ver el proceso o cantidad de atípicos, descomentar las siguientes líneas:
# Q1 = df_final['EDADMUJ'].quantile(0.25) #cambiar MUJ por HOM segun ayude
# Q3 = df_final['EDADMUJ'].quantile(0.75)
# IQR = Q3 - Q1
# limite_inferior = Q1 - 1.5 * IQR
# limite_superior = Q3 + 1.5 * IQR
# outliers = df_final[(df_final['EDADMUJ'] < limite_inferior) | (df_final['EDADMUJ'] > limite_superior)]
# print(f"Número de outliers en EDADMUJ: {len(outliers)}")
# print(outliers['EDADMUJ'].describe())
df_final = df_final[df_final['EDADHOM'] != 99]
df_final = df_final[df_final['EDADMUJ'] != 99]
