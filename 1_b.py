from proyecto import df_final,pandas
import seaborn as sns
import matplotlib.pyplot as plt

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
    df_final[col] = pandas.to_numeric(df_final[col], errors='coerce').astype('Int64')


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
