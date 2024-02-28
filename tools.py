## FUNCIONES DE UTILIDAD PARA EL ETL Y EDA
# Importaciones
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


def ver_duplicados(df, columna):
    '''
    Examina y presenta las filas duplicadas en un DataFrame según una columna específica.

    Esta función requiere un DataFrame y el nombre de una columna en particular como entrada.
    Posteriormente, identifica las filas duplicadas basándose en el contenido de la columna especificada,
    las filtra y las ordena para facilitar la comparación.

    Parameters:
        df (pandas.DataFrame): El DataFrame donde se buscarán las filas duplicadas.
        columna (str): El nombre de la columna según la cual se evaluarán las duplicaciones.

    Returns:
        pandas.DataFrame o str: Un DataFrame que incluye las filas duplicadas, filtradas y organizadas,
        listo para ser revisado y comparado, o el mensaje "No hay duplicados" si no se encuentran duplicados.
    '''
    # Filtramos las filas duplicadas
    duplicated_rows = df[df.duplicated(subset=columna, keep=False)]
    if duplicated_rows.empty:
        return "No hay duplicados"
    
    # Ordemos las filas duplicadas para comparar entre sí
    duplicated_rows_sorted = duplicated_rows.sort_values(by=columna)
    return duplicated_rows_sorted

def ver_variables(df):
    '''
    Conduce un análisis de los tipos de datos y la existencia de valores nulos en un DataFrame.

    Esta función acepta un DataFrame como entrada y produce un resumen que abarca detalles sobre
    los tipos de datos presentes en cada columna.

    Parámetros:
        df (pandas.DataFrame): El DataFrame que será objeto de análisis.

    Retorna:
        - pandas.DataFrame: Un DataFrame que proporciona una visión general de cada columna, incluyendo:
        - "nombre_campo": Denominación de cada columna.
        - "tipo_datos":   Tipos de datos distintos presentes en cada columna.
    '''

    dict = {"nombre_campo": [], "tipo_datos": []}

    for columna in df.columns:
        dict["nombre_campo"].append(columna)
        dict["tipo_datos"].append(df[columna].apply(type).unique())
    info = pd.DataFrame(dict)
        
    return info

def convertir_a_time(h):
    '''
    Transforma un valor en un objeto de tiempo (time) de Python si es factible.

    Esta función acepta diversas formas de entrada y procura convertirlas en objetos de tiempo (time) de Python.
    Si la conversión no es factible, retorna None.

    Parámetros:
        x (str, datetime u otro): El valor que se desea convertir a un objeto de tiempo (time).

    Retorna:
        datetime.time or None: Un objeto de tiempo (time) de Python en caso de éxito en la conversión, 
                                o None si la transformación no es posible.
    '''
    if isinstance(h, str):
        try:
            return datetime.strptime(h, "%H:%M:%S").time()
        except ValueError:
            return None
    elif isinstance(h, datetime):
        return h.time()
    return h

def imputa_valor_frecuente(df, columna):
    '''
    Completa los valores ausentes en una columna de un DataFrame utilizando el valor más común.

    Este procedimiento sustituye los valores "SD" con NaN en la columna especificada,
    posteriormente calcula el valor más frecuente en dicha columna y emplea ese valor
    para llenar los espacios vacíos (NaN).

    Parámetros:
        df (pandas.DataFrame): El DataFrame que contiene la columna que se desea completar.
        columna (str): El nombre de la columna donde se llevará a cabo la imputación.

    Retorna:
        None
    '''
    # Reemplazamos "SD" con NaN en la columna
    df[columna] = df[columna].replace("SD", pd.NA)

    # Calculamos el valor más frecuente en la columna
    valor_mas_frecuente = df[columna].mode().iloc[0]
    print(f"El valor mas frecuente es: {valor_mas_frecuente}")

    # Imputamos los valores NaN con el valor más frecuente
    df[columna].fillna(valor_mas_frecuente, inplace=True)
    
def imputa_edad_media_segun_sexo(df):
    '''
    Rellena los valores ausentes en la columna 'Edad' utilizando la edad promedio según el género.

    Este proceso sustituye los valores "SD" con NaN en la columna 'Edad', calcula el promedio de edad
    para cada grupo de género (Femenino y Masculino), muestra los promedios calculados y
    posteriormente completa los valores faltantes en la columna 'Edad' utilizando el promedio
    correspondiente al género de cada fila en el DataFrame.

    Parámetros:
        df (pandas.DataFrame): El DataFrame que contiene la columna 'Edad' que se desea imputar.

    Retorna:
        None    
    '''
    
    # Reemplazamos "SD" con NaN en la columna 'edad'
    df["Edad"] = df["Edad"].replace("SD", pd.NA)

    # Calculamos el promedio de edad para cada grupo de género
    promedio_por_genero = df.groupby("Sexo")["Edad"].mean()
    print(f'La edad promedio de Femenino es {round(promedio_por_genero["FEMENINO"])} y de Masculino es {round(promedio_por_genero["MASCULINO"])}')

    # Llenamos los valores NaN en la columna 'edad' utilizando el promedio correspondiente al género
    df["Edad"] = df.apply(lambda row: promedio_por_genero[row["Sexo"]] if pd.isna(row["Edad"]) else row["Edad"], axis=1)
    # Convertimos a entero
    df["Edad"] = df["Edad"].astype(int)
    
def ver_tipo_datos(df):
    '''
    Lleva a cabo un análisis detallado de los tipos de datos y la existencia de valores nulos en un DataFrame.

    Esta función toma un DataFrame como entrada y genera un resumen integral que abarca información sobre
    los tipos de datos presentes en cada columna, el porcentaje de valores no nulos y nulos, así como la
    cantidad exacta de valores nulos por columna.

    Parámetros:
        df (pandas.DataFrame): El DataFrame que será objeto de análisis.

    Retorna:
        pandas.DataFrame: Un DataFrame que proporciona una visión global de cada columna, incluyendo:
        - "nombre_campo": Denominación de cada columna.
        - "tipo_datos": Tipos de datos distintos presentes en cada columna.
        - "no_nulos_%": Porcentaje de valores no nulos en cada columna.
        - "nulos_%": Porcentaje de valores nulos en cada columna.
        - "nulos": Cantidad de valores nulos en cada columna.
    '''

    my_dict = {"nombre_campo": [], "tipo_datos": [], "no_nulos_%": [], "nulos_%": [], "nulos": []}

    for columna in df.columns:
        porcentaje_no_nulos = (df[columna].count() / len(df)) * 100
        my_dict["nombre_campo"].append(columna)
        my_dict["tipo_datos"].append(df[columna].apply(type).unique())
        my_dict["no_nulos_%"].append(round(porcentaje_no_nulos, 2))
        my_dict["nulos_%"].append(round(100-porcentaje_no_nulos, 2))
        my_dict["nulos"].append(df[columna].isnull().sum())

    df_info = pd.DataFrame(my_dict)
        
    return df_info


def distribucion_edad(df):
    '''
    Genera un gráfico con un histograma y un boxplot que muestran la distribución de la edad de los involucrados en los accidentes.

    Parameters:
        df: El conjunto de datos de accidentes.

    Returns:
        Un gráfico con un histograma y un boxplot.
    '''
    # creamos una figura con un solo eje x compartido
    fig, ax = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    
    # Graficamos el histograma de la edad
    sns.histplot(df["Edad"], kde=True, ax=ax[0], color="green", edgecolor="black")
    ax[0].set_title("Histograma de Edad") ; ax[0].set_ylabel("Frecuencia")
    
    # Graficamos el boxplot de la edad
    sns.boxplot(x=df["Edad"], ax=ax[1], color = "skyblue")
    ax[1].set_title("Boxplot de Edad") ; ax[1].set_xlabel("Edad")
    
    # Ajustamos y mostramos el gráfico
    plt.tight_layout()
    plt.show()
    
def distribucion_edad_por_anio(df):
    '''
    Genera un gráfico de boxplot que muestra la distribución de la edad de las víctimas de accidentes por año.

    Parameters:
        df: El conjunto de datos de accidentes.

    Returns:
        Un gráfico de boxplot.
    '''
    # Creamos el gráfico de boxplot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Año", y="Edad", data=df, palette="Set3")
    
    plt.title("Boxplot de Edades de Víctimas por Año") ; plt.xlabel("Año") ; plt.ylabel("Edad de las Víctimas")
     

    plt.show()

def accidentes_por_anio_y_sexo(df):
    '''
    Genera un gráfico de barras que muestra la cantidad de accidentes por año y sexo.

    Parameters:
        df: El conjunto de datos de accidentes.

    Returns:
        Un gráfico de barras.
    '''
    # Creamos el gráfico de barras
    plt.figure(figsize=(12, 4))
    sns.barplot(x="Año", y="Edad", hue="Sexo", data=df, palette="coolwarm")
    
    plt.title("Accidentes por Año y Sexo")
    plt.xlabel("Año") ; plt.ylabel("Edad de las víctimas") ; plt.legend(title="Sexo")
    
    plt.show()
    
def cohen(group1, group2):
    '''
    Calcula el tamaño del efecto de la d de Cohen para dos grupos.

    Parameters:
        grupo1: El primer grupo.
        grupo2: El segundo grupo.

    Returns:
        El tamaño del efecto de la d de Cohen.
    '''
    diff = group1.mean() - group2.mean()
    var1, var2 = group1.var(), group2.var()
    n1, n2 = len(group1), len(group2)
    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    d = diff / np.sqrt(pooled_var)
    return d

def cohen_por_año(df):
    '''
    Calcula el tamaño del efecto de la d de Cohen para dos grupos para los años del Dataframe.

    Parameters:
        df (pandas.DataFrame): El DataFrame que se va a analizar.

    Returns:
        El tamaño del efecto de la d de Cohen.
    '''
    # Obtenemos los años del conjunto de datos
    años_unicos = df["Año"].unique()
    # Creamos una lista vacía para guardar los valores de Cohen
    cohen_lista = []
    # Iteramos por los años y guardamos Cohen para cada grupo
    for a in años_unicos:
        grupo1 = df[((df["Sexo"] == 'MASCULINO') & (df["Año"] == a))]["Edad"]
        grupo2 = df[((df["Sexo"] == 'FEMENINO')& (df["Año"] == a))]["Edad"]
        d = cohen(grupo1, grupo2)
        cohen_lista.append(d)

    # Creamos un Dataframe
    cohen_df = pd.DataFrame()
    cohen_df["Año"] = años_unicos
    cohen_df["Estadistico de Cohen"] = cohen_lista
    cohen_df
    
    # Se grafica los valores de Cohen para los años
    plt.figure(figsize=(8, 4))
    plt.bar(cohen_df["Año"], cohen_df['Estadistico de Cohen'], color="LightSalmon")
    plt.xlabel("Año") ; plt.ylabel("Estadístico de Cohen") ; plt.title("Estadístico de Cohen por Año")
    plt.xticks(años_unicos)
    plt.show()

def edad_y_rol_victimas(df):
    '''
    Genera un gráfico de la distribución de la edad de las víctimas por rol.

    Parameters:
        df (pandas.DataFrame): El DataFrame que se va a analizar.

    Returns:
        None
    '''
    plt.figure(figsize=(8, 4))
    sns.boxplot(y="Rol", x="Edad", data=df, palette="tab20")
    plt.title("Edades por Condición")
    plt.show()
    
def distribucion_edad_por_victima(df):
    '''
    Genera un gráfico de la distribución de la edad de las víctimas por tipo de vehículo.

    Parameters:
        df (pandas.DataFrame): El DataFrame que se va a analizar.

    Returns:
        None
    '''
    # Creamos el gráfico de boxplot
    plt.figure(figsize=(14, 6))
    sns.boxplot(x="Víctima", y="Edad", data=df, palette = "Set2")
    
    plt.title("Vehículo usado en relación a la edad de la víctima") ; plt.xlabel("Tipo de vehiculo") ; plt.ylabel("Edad")
     
    plt.show()
    
def cant_accidentes_sexo(df):
    '''
    Produce un resumen de la cantidad de accidentes por sexo de los conductores.

    Esta función acepta un DataFrame como entrada y produce un resumen que abarca:

    * Un gráfico de barras que representa la cantidad de accidentes por sexo de los conductores en orden descendente.
    * Un DataFrame que exhibe la cantidad y el porcentaje de accidentes por sexo de los conductores.

    Parámetros:
        df (pandas.DataFrame): El DataFrame que se analizará.

    Retorna:
        None
    '''
    # Convertimos la columna "fecha" a tipo de dato datetime
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    
    # Extraemos el día de la semana (0 = lunes, 6 = domingo)
    df["Dia semana"] = df["Fecha"].dt.dayofweek
    
    # Creamos una columna 'tipo_dia' para diferenciar entre semana y fin de semana
    df["Tipo de día"] = df["Dia semana"].apply(lambda x: "Fin de Semana" if x >= 5 else "Semana")
    
    # Contamos la cantidad de accidentes por tipo de día
    data = df["Tipo de día"].value_counts().reset_index()
    data.columns = ["Tipo de día", "Cantidad de accidentes"]
    
    # Creamos el gráfico de barras
    plt.figure(figsize=(6, 4))
    ax = sns.barplot(x="Tipo de día", y="Cantidad de accidentes", data=data)
    
    ax.set_title("Cantidad de accidentes por tipo de día") ; ax.set_xlabel("Tipo de día") ; ax.set_ylabel("Cantidad de accidentes")
    
    # Agregamos las cantidades en las barras
    for index, row in data.iterrows():
        ax.annotate(f'{row["Cantidad de accidentes"]}', (index, row["Cantidad de accidentes"]), ha="center", va="bottom")
    
    plt.show()

def victimas_sexo_rol_victima(df):
    '''
    Produce un resumen de la cantidad de víctimas por sexo, rol y tipo de vehículo en un accidente de tráfico.

    Esta función acepta un DataFrame como entrada y genera un resumen que incluye:

    * Gráficos de barras que presentan la cantidad de víctimas por sexo, rol y tipo de vehículo en orden descendente.
    * DataFrames que muestran la cantidad y el porcentaje de víctimas por sexo, rol y tipo de vehículo.

    Parámetros:
        df (pandas.DataFrame): El DataFrame que será objeto de análisis.

    Retorna:
        None
    '''
    nuevos_colores = ["dodgerblue", "y"]
    sns.set_palette(sns.color_palette(nuevos_colores))
    # Creamos el gráfico
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Gráfico 1: Sexo
    sns.countplot(data=df, x="Sexo", ax=axes[0])
    axes[0].set_title("Víctimas por sexo") ; axes[0].set_ylabel("Cantidad de víctimas")

    # Definimos una paleta de colores personalizada (invierte los colores)
    colores_por_defecto = sns.color_palette()
    colores_invertidos = [colores_por_defecto[1], colores_por_defecto[0]]
    
    # Gráfico 2: Rol
    df_rol = df.groupby(["Rol", "Sexo"]).size().unstack(fill_value=0)
    df_rol.plot(kind="bar", stacked=True, ax=axes[1], color=colores_invertidos)
    axes[1].set_title("Víctimas por rol") ; axes[1].set_ylabel("Cantidad de víctimas") ; axes[1].tick_params(axis='x', rotation=45)
    axes[1].legend().set_visible(False)
    
    # Gráfico 3: Tipo de vehículo
    df_victima = df.groupby(["Víctima", "Sexo"]).size().unstack(fill_value=0)
    df_victima.plot(kind="bar", stacked=True, ax=axes[2], color=colores_invertidos)
    axes[2].set_title("Víctimas por tipo de vehículo") ; axes[2].set_ylabel("Cantidad de víctimas") ; axes[2].tick_params(axis='x', rotation=45)
    axes[2].legend().set_visible(False)


    plt.show()
    

def victimas_participantes(df):
    '''
    Produce un resumen de la cantidad de víctimas por número de participantes en un accidente de tráfico.

    Esta función toma un DataFrame como entrada y genera un resumen que incluye:

    * Un gráfico de barras que representa la cantidad de víctimas por número de participantes en orden descendente.
    * Un DataFrame que exhibe la cantidad y el porcentaje de víctimas por número de participantes.

    Parámetros:
        df (pandas.DataFrame): El DataFrame que se analizará.

    Retorna:
        None
    '''
    # Ordenamos los datos por "Participantes" en orden descendente por cantidad
    ordenado = df["Participantes"].value_counts().reset_index()
    ordenado = ordenado.rename(columns={"Cantidad": "Participantes"})
    ordenado = ordenado.sort_values(by="count", ascending=False)
    
    plt.figure(figsize=(15, 4))
    
    # Creamos el gráfico de barras
    ax = sns.barplot(data=ordenado, x="Participantes", y="count", order=ordenado["Participantes"], palette="Set3")
    ax.set_title("Víctimas por participantes")
    ax.set_ylabel("Cantidad de víctimas")
    # Rotamos las etiquetas del eje x a 45 grados
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment="right")

    plt.show()
    
    
def cantidad_acusados(df):
    '''
    Produce un resumen de la cantidad de acusados en un accidente de tráfico.

    Esta función toma un DataFrame como entrada y genera un resumen que abarca:

    * Un gráfico de barras que presenta la cantidad de acusados en orden descendente.
    * Un DataFrame que exhibe la cantidad y el porcentaje de acusados.

    Parámetros:
        df (pandas.DataFrame): El DataFrame que será objeto de análisis.

    Retorna:
        None
    '''
    # Ordenamos los datos por 'Participantes' en orden descendente por cantidad
    ordenado = df["Acusado"].value_counts().reset_index()
    ordenado = ordenado.rename(columns={"Cantidad": "Acusado"})
    ordenado = ordenado.sort_values(by="count", ascending=False)
    
    plt.figure(figsize=(15, 4))
    
    # Creamos el gráfico de barras
    ax = sns.barplot(data=ordenado, x="Acusado", y="count", order=ordenado["Acusado"])
    ax.set_title("Cantidad de acusados en los hechos") ; ax.set_ylabel("Cantidad de acusados") 
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment="right")

    
    plt.show()
    

def tipo_de_calle(df):
    '''
    Produce un resumen de los accidentes de tráfico por tipo de calle y cruce.

    Esta función toma un DataFrame como entrada y genera un resumen que abarca:

    * Un gráfico de barras que exhibe la cantidad de víctimas por tipo de calle.
    * Un gráfico de barras que muestra la cantidad de víctimas en cruces.
    * Un DataFrame que presenta la cantidad y el porcentaje de víctimas por tipo de calle.
    * Un DataFrame que muestra la cantidad y el porcentaje de víctimas en cruces.

    Parámetros:
        df (pandas.DataFrame): El DataFrame que será objeto de análisis.

    Retorna:
        None
    '''
    # Creamos el gráfico
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    sns.countplot(data=df, x="Tipo de calle", ax=axes[0], palette="Set2")
    axes[0].set_title("Víctimas por tipo de calle") ; axes[0].set_ylabel("Cantidad de víctimas")

    sns.countplot(data=df, x="Cruce", ax=axes[1], palette="Set2")
    axes[1].set_title("Víctimas en cruces") ; axes[1].set_ylabel("Cantidad de víctimas")
    
    plt.show()
    
    

def accidentes_mensuales(df):
    '''
    Genera gráficos de línea que muestran la cantidad de víctimas de accidentes mensuales por año.

    Esta función toma un DataFrame que incluye datos de accidentes, identifica los años únicos
    presentes en la columna 'Año', y produce gráficos de línea para visualizar la cantidad de víctimas
     por mes en cada año. Los gráficos se organizan en una cuadrícula de subgráficos de 2x3.

    Parámetros:
        df (pandas.DataFrame): El DataFrame que contiene los datos de accidentes, con una columna "Año".

    Retorna:
    None
    '''
    # Obtenemos una lista de años únicos
    años = df["Año"].unique()

    # Definimos el número de filas y columnas para la cuadrícula de subgráficos
    n_filas = 3
    n_columnas = 2

    # Creamos una figura con subgráficos en una cuadrícula de 2x3
    fig, axes = plt.subplots(n_filas, n_columnas, figsize=(14, 8))

    # Iteramos a través de los años y creamos un gráfico por año
    for i, year in enumerate(años):
        fila = i // n_columnas
        columna = i % n_columnas
            
    # Filtramos los datos para el año actual y agrupamos por mes
        data_mensual = (df[df["Año"] == year]
                        .groupby("Mes")
                        .agg({"Cantidad víctimas":"sum"}))
            
        # Configuramos el subgráfico actual
        ax = axes[fila, columna]
        data_mensual.plot(ax=ax, kind="bar")
        ax.set_title("Año " + str(year)) ; ax.set_xlabel("Mes") ; ax.set_ylabel("Cantidad de Víctimas")
        ax.legend_ = None
            
    # Mostramos y acomodamos el gráfico
    plt.tight_layout()
    plt.show()

def victimas_mensuales(df):
    '''
    Genera un gráfico de barras que exhibe la cantidad de víctimas de accidentes por mes.

    Esta función toma un DataFrame con información de accidentes, agrupa los datos por mes,
    y calcula la suma total de víctimas por mes. Posteriormente, crea un gráfico de barras que
    representa la cantidad de víctimas para cada mes.

    Parámetros:
        df (pandas.DataFrame): El DataFrame que contiene los datos de accidentes con una columna 'Mes'.

    Retorna:
        None
    '''
    # Agrupamos por la cantidad de víctimas por mes
    data = df.groupby("Mes").agg({"Cantidad víctimas":"sum"}).reset_index()
    
    plt.figure(figsize=(6,4))
    ax = sns.barplot(x="Mes", y="Cantidad víctimas", data=data, palette="Set2")
    ax.set_title("Cantidad de víctimas mensuales")
    ax.set_xlabel("Mes") ; ax.set_ylabel("Cantidad de accidentes")
    
    
    print(f"El mes con menor cantidad de víctimas tiene {data.min()[1]} víctimas")
    print(f"El mes con mayor cantidad de víctimas tiene {data.max()[1]} víctimas")
    
    plt.show()

def victimas_por_dia_semana(df):
    '''
    Genera un gráfico de barras que ilustra la cantidad de víctimas de accidentes por día de la semana.

    Esta función toma un DataFrame que incluye datos de accidentes, verifica si la columna 'Fecha'
    ya está en formato datetime y, en caso contrario, la convierte. Posteriormente, extrae el día de la semana
    (donde 0 representa el lunes y 6 el domingo), asigna el nombre correspondiente a cada día de la semana,
    cuenta la cantidad de accidentes por día de la semana y finalmente, crea un gráfico de barras que muestra
    la cantidad de víctimas para cada día de la semana.

    Parámetros:
        df (pandas.DataFrame): El DataFrame que contiene los datos de accidentes con una columna 'Fecha'.

    Retorna:
        None
    '''
    # Convertimos la columna "fecha" a tipo de dato datetime
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    
    # Extraemos el día de la semana (0 = lunes, 6 = domingo)
    df["Día semana"] = df["Fecha"].dt.dayofweek
    
    # Mapeamos el número del día de la semana a su nombre
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    df["Nombre día"] = df["Día semana"].map(lambda x: dias_semana[x])
    
    # Contamos la cantidad de accidentes por día de la semana
    data = df.groupby("Nombre día").agg({"Cantidad víctimas":"sum"}).reset_index()
      
    # Creamos el gráfico de barras
    plt.figure(figsize=(6, 3))
    ax = sns.barplot(x="Nombre día", y="Cantidad víctimas", data=data, order=dias_semana, palette="Set3")
    
    ax.set_title("Accidentes por Día de la Semana") ; ax.set_xlabel("Día de la Semana") ; ax.set_ylabel("Cantidad de Accidentes")
    plt.xticks(rotation=45)
    
    # Mostramos el resumen de los datos
    print(f"El día de la semana con menor cantidad de víctimas tiene {data.min()[1]} víctimas")
    print(f"El día de la semana con mayor cantidad de víctimas tiene {data.max()[1]} víctimas")
    print(f"La diferencia porcentual es de {round((data.max()[1] - data.min()[1]) / data.min()[1] * 100,2)}")
    

    plt.show()

def categoria_momento_dia(hora):
  """
  Devuelve la categoría de tiempo correspondiente a la hora proporcionada.

  Parameters:
    hora: La hora a clasificar.

  Returns:
    La categoría de tiempo correspondiente.
  """
  if hora.hour >= 6 and hora.hour <= 10:
    return "Mañana"
  elif hora.hour >= 11 and hora.hour <= 13:
    return "Mediodía"
  elif hora.hour >= 14 and hora.hour <= 18:
    return "Tarde"
  elif hora.hour >= 19 and hora.hour <= 23:
    return "Noche"
  else:
    return "Madrugada"

def accidentes_por_tiempo_del_dia(df):
    '''
    Calcula la cantidad de accidentes por categoría de tiempo y visualiza un gráfico de barras.

    Esta función toma un DataFrame con una columna 'Hora' y emplea la función 'crea_categoria_momento_dia'
    para añadir la columna 'Categoria tiempo'. Posteriormente, cuenta la cantidad de accidentes para cada
    categoría de tiempo, calcula los porcentajes y genera un gráfico de barras que ilustra la distribución
    de accidentes por categoría de tiempo.

    Parámetros:
        df (pandas.DataFrame): El DataFrame que contiene la información de los accidentes.

    Retorna:
        None
    '''
    # Aplicamos la función crea_categoria_momento_dia para crear la columna 'categoria_tiempo'
    df["Categoria tiempo"] = pd.to_datetime(df["Hora"]).apply(categoria_momento_dia)

    # Contamos la cantidad de accidentes por categoría de tiempo
    data = df["Categoria tiempo"].value_counts().reset_index()
    data.columns = ["Categoria tiempo", "Cantidad accidentes"]

    # Calculamos los porcentajes
    total_accidentes = data["Cantidad accidentes"].sum()
    data["Porcentaje"] = (data["Cantidad accidentes"] / total_accidentes) * 100
    
    # Creamos el gráfico de barras
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x="Categoria tiempo", y="Cantidad accidentes", data=data, palette="YlGn")

    ax.set_title("Accidentes por Momento del Día") ; ax.set_xlabel("Momento del día") ; ax.set_ylabel("Cantidad")

    # Agregamos las cantidades en las barras
    for index, row in data.iterrows():
        ax.annotate(f'{row["Cantidad accidentes"]}', (index, row["Cantidad accidentes"]), ha="center", va="bottom")

    
    plt.show()

def accidentes_por_horas_del_dia(df):
    '''
    Genera un gráfico de barras que muestra la cantidad de accidentes por hora del día.

    Parameters:
        df: El conjunto de datos de accidentes.

    Returns:
        Un gráfico de barras.
    '''
    # Extraemos la hora del día de la columna 'hora'
    df["Hora del día"] = pd.to_datetime(df["Hora"]).apply(lambda x: x.hour)

    # Contamos la cantidad de accidentes por hora del día
    data = df["Hora del día"].value_counts().reset_index()
    data.columns = ["Hora del día", "Cantidad de accidentes"]

    # Ordenamos los datos por hora del día
    data = data.sort_values(by="Hora del día")

    # Creamos el gráfico de barras
    plt.figure(figsize=(15, 6))
    ax = sns.barplot(x="Hora del día", y="Cantidad de accidentes", data=data, palette="Set3")

    ax.set_title("Accidentes por Hora del Día") ; ax.set_xlabel("Hora del día") ; ax.set_ylabel("Cantidad de accidentes")

    # Se agrega las cantidades en las barras
    for index, row in data.iterrows():
        ax.annotate(f'{row["Cantidad de accidentes"]}', (row["Hora del día"], row["Cantidad de accidentes"]), ha="center", va="bottom")

    # Se muestra el gráfico
    plt.show()

def accidentes_fin_de_semana(df):
    '''
    Genera un gráfico de barras que muestra la cantidad de accidentes por tipo de día (semana o fin de semana).

    Parameters:
        df: El conjunto de datos de accidentes.

    Returns:
        Un gráfico de barras.
    '''
    # Convertimos la columna "fecha" a tipo de dato datetime
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    
    # Extraemos el día de la semana (0 = lunes, 6 = domingo)
    df["Dia semana"] = df["Fecha"].dt.dayofweek
    
    # Creamos una columna "tipo_dia" para diferenciar entre semana y fin de semana
    df["Tipo de día"] = df["Dia semana"].apply(lambda x: "Fin de Semana" if x >= 5 else "Semana")
    
    # Contamos la cantidad de accidentes por tipo de día
    data = df["Tipo de día"].value_counts().reset_index()
    data.columns = ["Tipo de día", "Cantidad de accidentes"]
    
    # Creamos el gráfico de barras
    plt.figure(figsize=(6, 4))
    ax = sns.barplot(x="Tipo de día", y="Cantidad de accidentes", data=data, palette="RdBu")
    
    ax.set_title("Accidentes por tipo de día") ; ax.set_xlabel("Tipo de día") ; ax.set_ylabel("Cantidad")
    
    # Agregamos las cantidades en las barras
    for index, row in data.iterrows():
        ax.annotate(f'{row["Cantidad de accidentes"]}', (index, row["Cantidad de accidentes"]), ha='center', va='bottom')
    
    plt.show()