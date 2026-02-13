import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def edad_por_tipo_union(df, edad_col, tipo_union_col='CLAUNI'):
    
    datos = df[[edad_col, tipo_union_col]].dropna()

    resumen = datos.groupby(tipo_union_col)[edad_col].agg(
        media='mean',
        mediana='median',
        std='std',
        conteo='count'
    ).sort_values('media')

    print(resumen.round(2))
    return resumen



def boxplot_edad_tipo_union(df, edad_col, tipo_union_col='CLAUNI'):
    
    datos = df[[edad_col, tipo_union_col]].dropna()

    plt.figure(figsize=(8,6))
    sns.boxplot(data=datos, x=tipo_union_col, y=edad_col)
    plt.xticks(rotation=45)
    plt.title(f'{edad_col} por Tipo de Unión')
    plt.tight_layout()
    plt.show()



def grafico_dispersion(df, x_col, y_col, hue=None, 
                       linea_regresion=True,
                       titulo=None):

    # Eliminar NA en las columnas necesarias
    columnas = [x_col, y_col]
    if hue:
        columnas.append(hue)

    datos = df[columnas].dropna()

    plt.figure(figsize=(8,6))

    # Scatter
    sns.scatterplot(data=datos, x=x_col, y=y_col, hue=hue, alpha=0.6)

    # Línea de regresión (sin hue para que no se distorsione)
    if linea_regresion and not hue:
        sns.regplot(data=datos, x=x_col, y=y_col,
                    scatter=False, color='red')

    plt.title(titulo or f'{y_col} vs {x_col}')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.tight_layout()
    plt.show()

    # Correlación de Pearson
    correlacion = datos[x_col].corr(datos[y_col])
    print(f"Coeficiente de correlación (Pearson): {correlacion:.4f}")

    return correlacion




def analisis_correlaciones(df, columnas, umbral=0.7):

    # 1 Filtrar solo columnas numéricas y eliminar NA
    datos = df[columnas].dropna()

    # 2️Matriz de correlación
    matriz_corr = datos.corr()

    # 3️ Heatmap
    plt.figure(figsize=(8,6))
    sns.heatmap(matriz_corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de Correlación")
    plt.tight_layout()
    plt.show()

    # 4️ Detectar correlaciones fuertes
    print(f"\nCorrelaciones fuertes (|r| >= {umbral}):\n")

    fuertes = []

    for i in range(len(matriz_corr.columns)):
        for j in range(i+1, len(matriz_corr.columns)):
            col1 = matriz_corr.columns[i]
            col2 = matriz_corr.columns[j]
            valor = matriz_corr.iloc[i, j]

            if abs(valor) >= umbral:
                fuertes.append((col1, col2, valor))

    if fuertes:
        fuertes = sorted(fuertes, key=lambda x: abs(x[2]), reverse=True)
        for col1, col2, valor in fuertes:
            print(f"{col1} vs {col2} → r = {valor:.4f}")
    else:
        print("No se encontraron correlaciones fuertes.")

    return matriz_corr



def grafico_barras_categorica(df, columna, top_n=None, titulo=None):

    freq = df[columna].value_counts(normalize=True) * 100
    
    if top_n:
        freq = freq.head(top_n)

    plt.figure(figsize=(8,5))
    sns.barplot(x=freq.values, y=freq.index)
    plt.xlabel("Porcentaje (%)")
    plt.ylabel(columna)
    plt.title(titulo or f'Distribución de {columna}')
    plt.tight_layout()
    plt.show()

    print((freq.round(2)).astype(str) + "%")






