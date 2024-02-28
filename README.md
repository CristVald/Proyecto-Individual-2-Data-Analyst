# Homicidios por siniestros viales en la Ciudad Autónoma de Buenos Aires

## Introducción
En este proyecto simulado, asumimos el rol de un Analista de Datos, parte del equipo de una empresa consultora. La solicitud proviene del Observatorio de Movilidad y Seguridad Vial (OMSV), un centro de estudios bajo la Secretaría de Transporte del Gobierno de la Ciudad Autónoma de Buenos Aires (CABA). La tarea consiste en desarrollar un proyecto de análisis de datos utilizando un conjunto de datos sobre homicidios en siniestros viales ocurridos en la Ciudad de Buenos Aires entre 2016 y 2021.

El objetivo central de este proyecto es proporcionar información útil a las autoridades locales para tomar medidas efectivas que reduzcan el número de víctimas fatales en los incidentes de tráfico en CABA. Como productos finales, se espera la entrega de un informe detallado sobre las tareas realizadas, las metodologías empleadas y las conclusiones clave. Además, se planea la creación y presentación de un dashboard interactivo diseñado para facilitar la interpretación de la información y el análisis de los datos.


## Contexto
Los siniestros viales, también conocidos como accidentes de tráfico, son eventos que involucran vehículos en las vías públicas y pueden derivar de diversas causas, como colisiones entre automóviles, motocicletas, bicicletas o peatones, atropellos, choques con objetos fijos o caídas de vehículos. Estos incidentes pueden resultar en daños materiales, lesiones graves o incluso en fatalidades para las personas involucradas.

La Ciudad Autónoma de Buenos Aires, ubicada en la provincia de Buenos Aires, Argentina, no escapa a esta problemática, ya que los siniestros viales representan una preocupación significativa debido al elevado volumen de tráfico y la densidad poblacional en la región. Estos incidentes tienen un impacto considerable en la seguridad de los residentes y visitantes, así como en la infraestructura vial y los servicios de emergencia.

Según el censo poblacional del año 2022, la población de la Ciudad Autónoma de Buenos Aires es de 3,121,707 habitantes en una superficie de 200 km², lo que resulta en una densidad poblacional de alrededor de 15,609 personas por kilómetro cuadrado [(Fuente)](https://www.argentina.gob.ar/caba#:~:text=Poblaci%C3%B3n%3A%203.120.612%20habitantes%20(Censo%202022).). Además, en julio de 2023, se registraron 12,437,735 vehículos transitando por los peajes de las autopistas de acceso a la ciudad [(Fuente)](https://www.estadisticaciudad.gob.ar/eyc/?cat=377). En este contexto, la prevención de siniestros viales y la implementación de políticas efectivas se vuelven esenciales para abordar este problema de manera adecuada.

## Datos

Para este proyecto, se utilizó la Base de Víctimas Fatales en Siniestros Viales, la cual está en formato Excel y consta de dos pestañas de datos:

* HECHOS: Contiene una fila por incidente con un id único y variables temporales, espaciales y de participantes asociadas a cada suceso.
* VICTIMAS: Cuenta con una fila por cada víctima de los incidentes, incluyendo variables como edad, sexo y modo de desplazamiento. Se establece una vinculación con la pestaña de HECHOS a través del id único de cada hecho.


Este [documento](https://github.com/CristVald/Proyecto-Individual-2-Data-Analyst/blob/main/datasets/NOTAS_HOMICIDIOS_SINIESTRO_VIAL.pdf) proporciona definiciones detalladas de los datos utilizados y del desarrollo del proyecto. Además, los datos utilizados en el análisis están disponibles en este [enlace](https://github.com/CristVald/Proyecto-Individual-2-Data-Analyst/blob/main/datasets/homicidios.xlsx).


## Tecnologías utilizadas

Para llevar a cabo este proyecto, se empleó Python y la biblioteca Pandas para llevar a cabo los procesos de extracción, transformación y carga de los datos, así como para realizar el análisis exploratorio de los mismos. Los resultados de este análisis se detallan en el siguiente apartado.

Posteriormente, para obtener datos adicionales necesarios para calcular la población en el año 2021, se realizó webscraping utilizando la biblioteca BeautifulSoup. Todos los pormenores de este proceso se explican de manera exhaustiva en este [enlace](https://github.com/CristVald/Proyecto-Individual-2-Data-Analyst/blob/main/WEBSCRAPING.ipynb).

Por último, para la creación de un dashboard interactivo, se optó por utilizar Power BI, cuyo acceso se encuentra disponible [aquí](https://github.com/CristVald/Proyecto-Individual-2-Data-Analyst/blob/main/PI2.pbix).

## ETL
En una primera etapa, se llevó a cabo un proceso de extracción, transformación y carga de los datos (ETL) para los conjuntos "HECHOS" y "VÍCTIMAS". Durante este proceso, se realizaron diversas tareas como la estandarización de los nombres de las variables, la evaluación de valores nulos y duplicados en los registros, y la eliminación de columnas redundantes o con una cantidad significativa de valores faltantes. Tras completar este proceso para ambos conjuntos de datos relacionados con "Homicidios", se procedió a fusionarlos en un único conjunto denominado "df_homicidios" y se guardó en un formato csv con el nombre "homicidios_cleaned", pueden encontrar la información [aqui](https://github.com/CristVald/Proyecto-Individual-2-Data-Analyst/blob/main/ETL.ipynb).  


## EDA
En esta fase, se llevó a cabo un análisis exploratorio datos (EDA) con el objetivo de identificar patrones que pudieran proporcionar información útil para que las autoridades locales tomen medidas orientadas a reducir la cantidad de víctimas fatales en los siniestros viales. Todos los detalles de este análisis se encuentran detallados en este [enlace](https://github.com/CristVald/Proyecto-Individual-2-Data-Analyst/blob/main/EDA.ipynb).

## Análisis de los Datos

En el análisis inicial, se examinó el perfil de la víctima, encontrando que el 77% son hombres y casi el 50% se encuentra en el rango de 25 a 44 años, siendo el 84% de ellos hombres. 

En cuanto al rol de la víctima, el 48% eran conductores, distribuidos en un 77% de víctimas que se desplazaban en moto y 19% en auto. Respecto al medio de transporte al momento del hecho, el 42% de las víctimas son conductores de moto, y el 88% de ellos son hombres.

Al analizar la responsabilidad en el hecho, el 29% de los casos involucraba a autos, mientras que el 75% eran responsabilidad de vehículos como autos, colectivos y camiones.

En la búsqueda de patrones en la distribución espacial de los hechos, se destacó que en todas las comunas de CABA, las avenidas, vías anchas de al menos 13 metros, fueron un factor común en los accidentes. El 62% de las víctimas perdieron la vida en avenidas, y en el 82% de estos casos, ocurrió en el cruce de avenidas con otras calles. Este patrón se mantuvo consistente a lo largo de los años. En cuanto al rol de la víctima al momento del hecho, varió entre moto y peatón en distintas comunas.

Posteriormente, se examinó la variable temporal para comprender la distribución de los homicidios en diferentes escalas temporales. La distribución anual de víctimas fatales mostró alrededor del 60% en los primeros tres años del conjunto de datos, con una disminución significativa en 2020 debido a las medidas de cuarentena por COVID-19. A lo largo del año, la variación mensual fue marcada, con un pico en diciembre, influenciado por la flexibilización de las medidas de cuarentena.

Descendiendo en la escala temporal, se observó que el 70% de las víctimas perdieron la vida entre lunes y viernes, sugiriendo una relación con los desplazamientos diarios al trabajo. Sin embargo, en la distribución semanal, no se encontraron diferencias significativas entre los distintos días, indicando que la cantidad de víctimas los sábados y domingos es aproximadamente la misma para el conjunto de datos.

Al analizar las franjas horarias, las mayores víctimas (12%) ocurrieron entre las 6 y las 8 de la mañana, asociadas posiblemente al horario de ingreso al trabajo. Sin embargo, se notó que el 55% de estas víctimas resultaron de incidentes ocurridos durante el fin de semana.

## KPI

A partir del análisis previo, se establecieron tres objetivos orientados a reducir la cantidad de víctimas fatales en siniestros viales, junto con la propuesta de tres indicadores clave de rendimiento (KPI).

* Reducir en un 10% la tasa de homicidios en siniestros viales de los últimos seis meses, en CABA, en comparación con la tasa de homicidios en siniestros viales del semestre anterior
  
La tasa de homicidios en siniestros viales se define como el número de víctimas fatales en accidentes de tránsito por cada 100,000 habitantes durante un período específico. Para el año 2021, esta tasa fue de 1.77 en los primeros seis meses. El objetivo propuesto era reducir esto en un 10%, alcanzando 1.60. El KPI calculado para el segundo semestre de 2021 fue de 1.35, cumpliendo con la meta establecida.

* ![KPI 1](https://github.com/CristVald/Proyecto-Individual-2-Data-Analyst/blob/main/im%C3%A1genes/kpi_1.png)


* Reducir en un 7% la cantidad de accidentes mortales de motociclistas en el último año, en CABA, respecto al año anterior

Dado que el 42% de las víctimas mortales se desplazaban en moto, se propuso monitorear la cantidad de accidentes mortales de motociclistas. La fórmula utilizada considera la diferencia absoluta entre el número de accidentes mortales en el año actual (2021) y el año anterior(2020). A pesar del objetivo de reducción del 7%, la cantidad de accidentes mortales de motociclistas para el año 2021 aumentó en un 64%, siendo 64.29.

* Reducir en un 10% la tasa de homicidios en las avenidas en el último año, en CABA, respecto al año anterior:

Dado que el 62% de las víctimas mortales transitaban por avenidas, se propuso reducir la tasa de homicidios en estas vías en un 10%. La tasa calculada para el año 2020 fue de 1.68, y el objetivo para el 2021 fue 1.51(una reducción del 10%). Sin embargo, la tasa real para el 2021 resultó en 1.97, superando la meta y representando un aumento de la tasa de homicidios con respecto al año anterior.



## Conclusiones y recomendaciones

En cuanto al perfil de las víctimas, el 77% eran de sexo masculino, y casi la mitad se encontraba en el rango de edad de 25 a 44 años. Los motociclistas representaron el 42% de los casos. Las avenidas de CABA fueron escenario del 62% de los homicidios, siendo el 82% de estos en cruces con otras calles. Además, el 75% de los eventos ocurrieron en intersecciones viales.

Durante el período comprendido entre 2016 y 2021, se documentaron 717 casos de víctimas fatales en accidentes de tránsito. La mayoría de estos incidentes, un 70%, tuvieron lugar durante la semana, y aproximadamente el 12% ocurrió entre las 6 y las 8 de la mañana durante los fines de semana. Diciembre destacó como el mes con el mayor número de fallecimientos en el análisis.

A pesar de cumplir con el objetivo de reducir la tasa de homicidios en siniestros viales en el segundo semestre de 2021, no se lograron alcanzar las metas propuestas para disminuir la cantidad de accidentes mortales en motociclistas ni en avenidas durante el año 2021 en comparación con el año 2020.

En vista de lo anterior, se formulan las siguientes recomendaciones:

* Mantener la vigilancia de los objetivos establecidos mediante campañas específicas, con un enfoque especial en conductores de motocicletas y usuarios de las avenidas.

* Reforzar las campañas de seguridad vial, especialmente desde los días viernes hasta los lunes, con una intensificación particular durante el mes de diciembre.

* Concentrar las campañas de concienciación en prácticas de conducción segura en avenidas y cruces de calles.

* Orientar las campañas de seguridad hacia el sexo masculino, enfocándose especialmente en la conducción de motocicletas, dirigidas a la franja etaria de 25 a 44 años.












