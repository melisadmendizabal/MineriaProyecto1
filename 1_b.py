from proyecto import df_final,pandas
import seaborn as sns
import matplotlib.pyplot as plt
import unicodedata

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


#GRAFICAS NUMERICOS (tarda algo en ejecutar jaja)
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18,10)) 
for ax, col in zip(axes.flatten(), cols_num):
    sns.histplot(df_final[col], kde=True, bins=20, ax=ax)
    ax.set_title(f'Distribución de {col}')
    ax.set_xlabel(col)
    ax.set_ylabel('Frecuencia')
plt.tight_layout()
plt.show()
# No tienen una distribución normal. 
# En cuanto a la gráfica de años, tal parece que fuera bastante constante, con una clara 
# disminución en 2020, deduciéndose a causa de la pandemia; por consiguiente, hubo un gran aumento en 2021, por las bodas atrasadas. 
# En los meses, se observa hay más matrimonios en noviembre-diciembre. Posiblemente, para no colisionar con horarios de trabajo. 
# En cuanto a la edad, existe un gran sesgo positivo, debido a la presencia de numerables datos atípicos (personas con 50+ años), 
# los cuales no fueron eliminados, dado que sí pueden existir personas las cuales a esa edad contraigan matrimonio. Se eliminaron 
# únicamente los datos de 99 de edad, ya que el excel del INE indicaba que dichos datos eran para "no especificado". La gráfica de este,
# de cierto modo, se asemeja a una logarítmica invertida en Y (quitando el hecho de que la gráfica no empieza en 0, debido a que los 
# menores de edad no pueden contraer matrimonio). 

boxplot_numericos = ['EDADHOM', 'EDADMUJ']
for col in boxplot_numericos:
    plt.figure(figsize=(8,2))
    sns.boxplot(x=df_final[col])
    plt.title(f'Boxplot de {col}')
    plt.show()

##FRECUENCIAS categoricos
for col in cols_cat:
    print(f"\nFrecuencia de '{col}':")
    print(df_final[col].value_counts(normalize=True, dropna=False).mul(100).round(2).astype(str) + '%')

##Guatemala (departamento y municipio) son donde más se registran datos. 
## La gran mayoría elige comunidad de gananciales como régimen económico de matrimonio
## Casi la totalidad es guatemalteco de nacionalidad (H y M)
## Más del 30%, tanto en hombres como mujeres, han terminado la primaria antes de casarse
## Casi nadie se casa en día 31 o 1. 





# c-----------------------------------------------------------------------------------------
# Frecuencia de matrimonios por año de ocurrencia
def frecuenciaVSvariable(df, col_tiempo, titulo=None, xlabel=None):
    freq = df[col_tiempo].value_counts().sort_index()
    total = freq.sum()

    tabla = pandas.DataFrame({
        col_tiempo: freq.index,
        'frecuencia': freq.values,
        'porcentaje': (freq.values / total) * 100
    })

    tabla['porcentaje'] = tabla['porcentaje'].map(lambda x: f"{x:.2f}%")

    plt.figure(figsize=(10,5))
    sns.lineplot(x=freq.index, y=freq.values, marker='o')
    plt.title(titulo or f'Frecuencia por {col_tiempo}')
    plt.xlabel(xlabel or col_tiempo)
    plt.ylabel('Número de registros')
    plt.grid(True)
    plt.show()

    return tabla


def cajaBigotesPorGrupo(df, x_col, y_col, titulo=None, xlabel=None, ylabel=None):
    plt.figure(figsize=(14,6))
    sns.boxplot(x=x_col, y=y_col, data=df)
    plt.title(titulo or f'{y_col} por {x_col}')
    plt.xlabel(xlabel or x_col)
    plt.ylabel(ylabel or y_col)
    plt.xticks(rotation=45)
    plt.show()


def tendencia(df, x_col, y_col, estadistico='median',
              titulo=None, xlabel=None, ylabel=None):

    if estadistico == 'median':
        serie = df.groupby(x_col)[y_col].median()
    elif estadistico == 'mean':
        serie = df.groupby(x_col)[y_col].mean()
    else:
        raise ValueError("estadistico debe ser 'median' o 'mean'")

    serie = serie.sort_index()

    plt.figure(figsize=(10,5))
    sns.lineplot(x=serie.index, y=serie.values, marker='o')
    plt.title(titulo or f'{estadistico.capitalize()} de {y_col} por {x_col}')
    plt.xlabel(xlabel or x_col)
    plt.ylabel(ylabel or y_col)
    plt.grid(True)
    plt.show()

    return serie


def frecuenciaCruzadaBarras(df, col_x, col_grupo, normalizar=True,
                            titulo=None, xlabel=None, ylabel=None, top_n=None):
    tabla = pandas.crosstab(df[col_x], df[col_grupo])

    if top_n:
        tabla = tabla.loc[:, tabla.sum().sort_values(ascending=False).head(top_n).index]

    if normalizar:
        tabla = tabla.div(tabla.sum(axis=0), axis=1) * 100
        tabla = tabla.round(2)

    tabla = tabla.sort_index()

    tabla.plot(kind='bar', figsize=(14,6), stacked=True)
    plt.title(titulo or f'{col_x} vs {col_grupo}')
    plt.xlabel(xlabel or col_x)
    plt.ylabel(ylabel or ('Porcentaje' if normalizar else 'Frecuencia'))
    plt.legend(title=col_grupo, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    if normalizar:
        tabla = tabla.applymap(lambda x: f"{x:.2f}%")

    return tabla


def mapaCalorCruce(df, col_y, col_x, normalizar=True,
                   titulo=None, cmap='viridis'):

    tabla = pandas.crosstab(df[col_y], df[col_x])

    if normalizar:
        tabla = tabla.div(tabla.sum(axis=0), axis=1) * 100
        tabla = tabla.round(2)

    plt.figure(figsize=(14,6))
    sns.heatmap(tabla, cmap=cmap, annot=True, fmt=".2f")
    plt.title(titulo or f'{col_y} vs {col_x}')
    plt.xlabel(col_x)
    plt.ylabel(col_y)
    plt.tight_layout()
    plt.show()

    if normalizar:
        tabla = tabla.applymap(lambda x: f"{x:.2f}%")

    return tabla


def lineasCategoria(df, col_categoria, col_tiempo,
                    normalizar=True, titulo=None):

    tabla = pandas.crosstab(df[col_tiempo], df[col_categoria])

    if normalizar:
        tabla = tabla.div(tabla.sum(axis=1), axis=0) * 100
        tabla = tabla.round(2)

    plt.figure(figsize=(12,6))
    for col in tabla.columns:
        plt.plot(tabla.index, tabla[col], marker='o', label=col)

    plt.title(titulo or f'{col_categoria} a través del tiempo')
    plt.xlabel(col_tiempo)
    plt.ylabel('Porcentaje' if normalizar else 'Frecuencia')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    if normalizar:
        tabla = tabla.applymap(lambda x: f"{x:.2f}%")

    return tabla

def tendencia_categorica(df, col_categoria, col_tiempo,
                         normalizar=True, titulo=None,
                         xlabel=None, ylabel=None, top_n=None):
    """
    Grafica la tendencia de una variable categórica a través del tiempo.
    Muestra % por categoría en cada periodo.

    top_n: si se quiere limitar a las top N categorías
    """

    # 1) tabla cruzada
    tabla = pandas.crosstab(df[col_tiempo], df[col_categoria])

    # 2) normalizar a porcentaje por fila (por cada año)
    if normalizar:
        tabla = tabla.div(tabla.sum(axis=1), axis=0) * 100

    # 3) elegir top_n categorías (por frecuencia total)
    if top_n:
        top_cols = tabla.sum(axis=0).sort_values(ascending=False).head(top_n).index
        tabla = tabla[top_cols]

    # 4) plot de líneas
    plt.figure(figsize=(12,6))
    for col in tabla.columns:
        plt.plot(tabla.index, tabla[col], marker='o', label=col)

    plt.title(titulo or f'{col_categoria} a través del tiempo')
    plt.xlabel(xlabel or col_tiempo)
    plt.ylabel(ylabel or ('Porcentaje' if normalizar else 'Frecuencia'))
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return tabla



# Frecuencia de matrimonios por año de ocurrencia (AÑOOCU)
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


