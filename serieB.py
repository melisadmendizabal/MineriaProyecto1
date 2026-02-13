
import seaborn as sns
import matplotlib.pyplot as plt
import pandas 

def graficasNumericas(df_final, cols_num, cols_cat):
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
    # de cierto modo, se asemeja a una logarítmica invertida en Y (quitando el hecho de que la gráfica no empieza en 0

    boxplot_numericos = ['EDADHOM', 'EDADMUJ']
    print("Estadística descriptiva general para edades de mujeres y hombres ",df_final[cols_num].describe())
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



# Función que genera la tabla y gráfica de frecuencia
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


#Función que genera el grafico de caja y bigotes en conjunto
def cajaBigotesPorGrupo(df, x_col, y_col, titulo=None, xlabel=None, ylabel=None):
    plt.figure(figsize=(14,6))
    sns.boxplot(x=x_col, y=y_col, data=df)
    plt.title(titulo or f'{y_col} por {x_col}')
    plt.xlabel(xlabel or x_col)
    plt.ylabel(ylabel or y_col)
    plt.xticks(rotation=45)
    plt.show()


#Fución que grafica la tendencia entrevarias variables
def tendencia(df, x_col, y_col, estadistico='median', titulo=None, xlabel=None, ylabel=None):

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


#función que genera graficos de barras
def frecuenciaCruzadaBarras(df, col_x, col_grupo, normalizar=True, titulo=None, xlabel=None, ylabel=None, top_n=None):
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


def mapaCalorCruce(df, col_y, col_x, normalizar=True, titulo=None, cmap='viridis'):

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


def lineasCategoria(df, col_categoria, col_tiempo, normalizar=True, titulo=None):

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

def tendencia_categorica(df, col_categoria, col_tiempo, normalizar=True, titulo=None, xlabel=None, ylabel=None, top_n=None):
    
    # Grafica la tendencia de una variable categórica a través del tiempo.
    # Muestra % por categoría en cada periodo.
    # top_n: si se quiere limitar a las top N categorías
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

