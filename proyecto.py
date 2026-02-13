import pandas
import unicodedata
import numpy as np
from scipy import stats
from serieB import graficasNumericas, frecuenciaVSvariable, cajaBigotesPorGrupo, tendencia, frecuenciaCruzadaBarras, mapaCalorCruce, lineasCategoria, tendencia_categorica
from serieC import edad_por_tipo_union, boxplot_edad_tipo_union, grafico_dispersion, analisis_correlaciones, grafico_barras_categorica
from clustering import clustering
print("Proyecto 1 - Mineria de datos")
print("Melisa Mendizabal - Renato Rojas")
print("Este proyecto se basa en analizar 10 años de bases de datos sobre matrimonios en Guatemala")
#Importación de todos las bases de datos corresponientes a matrimonios
#en un rango de 11 años 
print("\n Cargando bases de datos...")
df12 = pandas.read_spss("matri2012.sav")
print("\n   Cargando matrimonios2012")
df13 = pandas.read_spss("matri2013.sav")
print("\n   Cargando matrimonios2013")
df14 = pandas.read_spss("matri2014.sav")
print("\n   Cargando matrimonios2014")
df15 = pandas.read_spss("matri2015.sav")
print("\n   Cargando matrimonios2015")
df16 = pandas.read_spss("matri2016.sav")
print("\n   Cargando matrimonios2016")
df17 = pandas.read_spss("matri2017.sav")
print("\n   Cargando matrimonios2017")
df18 = pandas.read_spss("matri2018.sav")
print("\n   Cargando matrimonios2018")
df19 = pandas.read_spss("matri2019.sav")
print("\n   Cargando matrimonios2019")
df20 = pandas.read_spss("matri2020.sav")
print("\n   Cargando matrimonios2020")
df21 = pandas.read_spss("matri2021.sav")
print("\n   Cargando matrimonios2021")
df22 = pandas.read_spss("matri2022.sav")
print("\n   Cargando matrimonios2022")



#Almacenamiento de dataframes en lista para optimizar el recorrido entre todos los df
dataframes = {
    2012: df12, 2013: df13, 2014: df14,
    2015: df15, 2016: df16, 2017: df17, 
    2018: df18, 2019: df19, 2020: df20, 
    2021: df21, 2022: df22
}

#Eliminación de columnas que no tienen en común para limpieza de datos
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


#Asignación de la variable de año de ocurrencia para normalizar los datos
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
print("Nota: se comprobó que las columnas fueran iguales, pero en algunos casos marcan que son distintas debido a que las variables no están en el mismo orden")
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
print("Uniendo data frames...")
df_final = pandas.concat(dataframes.values(), ignore_index=True)


#LIMPIEZA
print("Proceso de limpieza y normalización de datos")
def normalizar_texto(s):
    if pandas.isna(s):
        return s
    s = str(s).strip().lower()
    s = ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )
    return s

#se percató que existen incongruencias en las columnas de ESCHOM y ESCMUJ, ya que existían valores 
#como "post grado", "post Grado", "postgrado"
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


#del mismo modo los departamentos no se encontraban normalizados, por lo que se realizó la corrección
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
        .apply(normalizar_texto)   
        .map(mapa_departamentos)   # nombre oficial
        .astype('category')
    )

#Lista con las variables
cols_cat = [
    'DEPREG', 'MUPREG', 'CLAUNI',
    'NACHOM', 'NACMUJ',
    'ESCHOM', 'ESCMUJ',
    'DEPOCU', 'MUPOCU',
    'DIAOCU'
]
df_final[cols_cat] = df_final[cols_cat].astype('category')

#mapa de los meses unidos con el número asignado al mes
meses_map = {
    'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6,
    'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
}
df_final['MESOCU'] = df_final['MESOCU'].map(meses_map)
df_final['MESREG'] = df_final['MESREG'].map(meses_map)

#lista de variables numéricas volverlas float64 cambiando el valor anterior de tipo object
cols_num = ['MESREG', 'AÑOREG', 'EDADHOM', 'EDADMUJ','MESOCU', 'AÑOOCU']
for col in cols_num:
    df_final[col] = pandas.to_numeric(df_final[col], errors='coerce').astype('float64')



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

print("Proceso de limpieza finalizado")
menu = "1"
while menu != "0":
    print(" ")
    print("A continuación se muestran opciones para verificar el análisis de datos:")
    print("1. Estadística descriptiva y forma de distribución")
    print("2. Gráficos Numéricos")
    print("3. Graficos de barras vaiables categoricas")
    print("4. Cruce de variables")
    print("5. Graficos de dispersión")
    print("6. Matriz de correlacion")
    print("7. Clustering")
    print("0. Salir")

    menu = input("Seleccione una opción: ")

    if menu == "1":
        resumen = pandas.DataFrame({
            'dtype': df_final.dtypes,
            'n_unicos': df_final.nunique()
        })
        print(resumen)

        #Estadística descriptiva y forma de distribución
        print("Asimetría: ")
        print(df_final[['EDADHOM', 'EDADMUJ']].skew())
        print("Curtosis: ")
        print(df_final[['EDADHOM', 'EDADMUJ']].kurt())


        data = df_final['EDADMUJ'].dropna() #Se hace para mujer, ya que es muy similar a los datos de hombre, por lo que aplica para ambos
        distributions = {
            "Normal": stats.norm,
            "Gamma": stats.gamma,
            "Lognormal": stats.lognorm,
            "Exponential": stats.expon,
            "Weibull": stats.weibull_min
        }
        results = []
        for name, dist in distributions.items():
            params = dist.fit(data)
            loglik = np.sum(dist.logpdf(data, *params))
            k = len(params)
            aic = 2*k - 2*loglik
            results.append((name, aic))

        results_sorted = sorted(results, key=lambda x: x[1])
        print(results_sorted)
        #La que más queda es lognormal. 

    elif menu == "2":
        print("La ejecución de esta función es tardada")
        graficasNumericas(df_final, cols_num, cols_cat)

    elif menu == "3":
        print("Variables categoricas")
        grafico_barras_categorica(
            df_final,
            'CLAUNI',
            titulo="Distribución del Régimen Económico"
        )

        grafico_barras_categorica(
            df_final,
            'ESCHOM',
            titulo="Distribución del Escolaridad en Hombres"
        )

        grafico_barras_categorica(
            df_final,
            'ESCMUJ',
            titulo="Distribución del Escolaridad en Mujeres"
        )


    elif menu == "4":
        # Frecuencia de matrimonios por año de ocurrencia (AÑOOCU)
        print("Frecuencia por año de Ocurrencia")
        tabla1 = frecuenciaVSvariable(df_final, 'AÑOOCU', titulo="Frecuencia por Año de Ocurrencia")
        print(tabla1)

        # -------------------------
        # Frecuencia de matrimonios por año de ocurrencia (AÑOOCU) 
        print("==== MESOCU vs AÑOOCU ====")
        tabla3 = mapaCalorCruce(df_final, 'MESOCU', 'AÑOOCU', normalizar=True, titulo="Heatmap MESOCU vs AÑOOCU")
        print(tabla3)


        # -------------------------
        # 
        print("==== DIAOCU vs AÑOOCU ====")
        tabla4 = frecuenciaCruzadaBarras(df_final, 'DIAOCU', 'AÑOOCU', normalizar=True,titulo="DIAOCU vs AÑOOCU (Porcentaje)")
        print(tabla4)

        # -------------------------
        # DIAOCU vs MESOCU
        # -------------------------
        print("==== DIAOCU vs MESOCU ====")
        tabla7 = mapaCalorCruce(df_final, 'DIAOCU', 'MESOCU', normalizar=True,titulo="Heatmap DIAOCU vs MESOCU")
        print(tabla7)


        # -------------------------
        # DEPOCU vs AÑOOCU
        # -------------------------
        print("==== DEPOCU vs AÑOOCU ====")
        tabla8 = frecuenciaCruzadaBarras(df_final, 'DEPOCU', 'AÑOOCU', normalizar=True,titulo="DEPOCU vs AÑOOCU (Porcentaje)", top_n=10)
        print(tabla8)

        # -------------------------
        # CLAUNI vs AÑOOCU
        # -------------------------
        print("==== CLAUNI vs AÑOOCU ====")
        tabla_clauni = tendencia_categorica(df_final,col_categoria='CLAUNI',col_tiempo='AÑOOCU',top_n=5,)  # para que no se vea saturadotitulo="Tendencia de Tipo de Unión por Añ"
        print(tabla_clauni)


        # -------------------------
        # EDADMUJ vs AÑOOCU
        # -------------------------
        print("==== EDADMUJ vs AÑOOCU ====")
        cajaBigotesPorGrupo(df_final, 'AÑOOCU', 'EDADMUJ', titulo="Edad Mujer por Año de Ocurrencia")
        serie1 = tendencia(df_final, 'AÑOOCU', 'EDADMUJ', estadistico='median', titulo="Mediana Edad Mujer por Año de Ocurrencia")
        print(serie1)


        # -------------------------
        # EDADHOM vs AÑOOCU
        # -------------------------
        print("==== EDADHOM vs AÑOOCU ====")
        cajaBigotesPorGrupo(df_final, 'AÑOOCU', 'EDADHOM', titulo="Edad Hombre por Año de Ocurrencia")
        serie2 = tendencia(df_final, 'AÑOOCU', 'EDADHOM', estadistico='median',titulo="Mediana Edad Hombre por Año de Ocurrencia")
        print(serie2)


        # -------------------------
        # ESCMUJ vs AÑOOCU
        # -------------------------
        print("==== ESCMUJ vs AÑOOCU ====")
        tabla13 = lineasCategoria(df_final, 'ESCMUJ', 'AÑOOCU', normalizar=True, titulo="Tendencia Escolaridad Mujer por Año")
        print(tabla13)


        # -------------------------
        # ESCHOM vs AÑOOCU
        # -------------------------
        print("==== ESCHOM vs AÑOOCU ====")
        tabla15 = lineasCategoria(df_final, 'ESCHOM', 'AÑOOCU', normalizar=True,titulo="Tendencia Escolaridad Hombre por Año")
        print(tabla15)


        # -------------------------
        # NACMUJ vs AÑOOCU
        # -------------------------
        print("==== NACMUJ vs AÑOOCU ====")
        tabla_nacmuj = tendencia_categorica(
            df_final,
            col_categoria='NACMUJ',
            col_tiempo='AÑOOCU',
            top_n=6,
            titulo="Tendencia de Nacionalidad de Mujeres por Año"
        )
        print(tabla_nacmuj)

        # -------------------------
        # NACHOM vs AÑOOCU
        # -------------------------
        print("==== NACHOM vs AÑOOCU ====")
        tabla_nachom = tendencia_categorica(
            df_final,
            col_categoria='NACHOM',
            col_tiempo='AÑOOCU',
            top_n=6,
            titulo="Tendencia de Nacionalidad de hombres por Año"
        )
        print(tabla_nachom)


        # -------------------------
        # DEPOCU vs DEPREG
        # -------------------------
        print("==== DEPOCU vs DEPREG ====")
        tabla21 = mapaCalorCruce(df_final, 'DEPOCU', 'DEPREG', normalizar=True, titulo="Heatmap DEPOCU vs DEPREG")
        print(tabla21)

        # -------------------------
        # EDAD VS CLAUDI
        # -------------------------
        print("==== EDADMUJ y TIPOUNION ====")
        edad_por_tipo_union(df_final, 'EDADMUJ')
        boxplot_edad_tipo_union(df_final, 'EDADMUJ')

        print("==== EDADHOM y TIPOUNION ====")
        edad_por_tipo_union(df_final, 'EDADHOM')
        boxplot_edad_tipo_union(df_final, 'EDADHOM')

    elif menu == "5":
        print("==== EDADMUJ vs AÑOOCU ====")
        grafico_dispersion(
            df_final,
            'AÑOOCU',
            'EDADMUJ',
            titulo="Edad Mujer vs Año de Ocurrencia"
        )

        print("==== EDADHOM vs AÑOOCU ====")
        grafico_dispersion(
            df_final,
            'AÑOOCU',
            'EDADHOM',
            titulo="Edad Hombre vs Año de Ocurrencia"
        )

        

        print("==== EDADHOM vs EDADMUJ ====")
        grafico_dispersion(
            df_final,
            'EDADHOM',
            'EDADMUJ',
            titulo="Edad Hombre vs Edad Mujer"
        )

        
    elif menu == "6":
                
        matriz = analisis_correlaciones(df_final, cols_num, umbral=0.5)
    elif menu == "7":
        clustering(df_final)

    elif menu == "0":
        print("Gracias por utilizar")

    else:
        print("Seleccione una opción")
