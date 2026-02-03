Backend – Flask

Procesamiento de Datos – Pandas & NumPy
<div style="display:flex; gap:20px;"> <img src="https://upload.wikimedia.org/wikipedia/commons/e/ed/Pandas_logo.svg" height="80"/> <img src="https://upload.wikimedia.org/wikipedia/commons/3/31/NumPy_logo_2020.svg" height="80"/> </div>
Visualización – Matplotlib & Seaborn
<div style="display:flex; gap:20px;"> <img src="https://matplotlib.org/stable/_images/sphx_glr_logos2_003.png" height="80"/> <img src="https://seaborn.pydata.org/_images/logo-mark-lightbg.svg" height="80"/> </div>
Base de Datos – xaampp

Frontend – HTML & CSS
<div style="display:flex; gap:20px;"> <img src="https://upload.wikimedia.org/wikipedia/commons/6/61/HTML5_logo_and_wordmark.svg" height="80"/> <img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/CSS3_logo_and_wordmark.svg" height="80"/> </div>



📊 Dashboard de Análisis de Ventas Automotrices

Sistema web para registro, limpieza y análisis de ventas de vehículos con visualización interactiva de métricas clave.

🧩 Descripción del Proyecto

Aplicación web desarrollada con Flask que permite gestionar y analizar ventas de vehículos mediante dos canales:

Registro manual por formulario.

Procesamiento masivo de archivos CSV / Excel.

Incluye un módulo de limpieza de datos automática que detecta y corrige:

Duplicados

Valores nulos

Formatos incorrectos

Antes de persistir la información en la base de datos y mostrarla en un dashboard de estadísticas interactivas.

⚙️ Tecnologías Utilizadas
Capa	Tecnología	Propósito
Backend	Flask	Framework web
Procesamiento	Pandas, NumPy	Limpieza y análisis de datos
Visualización	Matplotlib, Seaborn	Gráficos estadísticos
Base de Datos	SQLite	Persistencia
Frontend	HTML5, CSS3	Interfaz de usuario
🗃️ Estructura de la Base de Datos

Tabla: ventas

Campo	Tipo	Descripción
referencia	TEXT	Marca/modelo (ej: Toyota Corolla)
version	TEXT	Versión (ej: Limited, SE)
anio	INTEGER	Año del vehículo
fecha_venta	DATE	Fecha de venta
monto_total	REAL	Valor total
🔄 Flujo Funcional
flowchart LR
A[Formulario / CSV] --> B[Limpieza de datos]
B --> C[Base de datos]
C --> D[Dashboard]

🚀 Pasos de Uso
1️⃣ Pantalla de inicio

Accede al sistema y selecciona el método de carga.

2️⃣ Registro manual

Formulario con validación en tiempo real.
Los datos se almacenan directamente en la base de datos.

3️⃣ Carga de archivo CSV / Excel

Se ejecuta automáticamente el pipeline de limpieza:

Eliminación de duplicados

Eliminación de nulos críticos

Validación numérica (monto_total > 0)

Normalización de texto

Validación de fechas

4️⃣ Análisis de calidad de datos

Ejemplo de salida:

Métrica	Resultado
Registros originales	35
Registros descartados	5
Registros válidos	30
Eficiencia	85.7%
5️⃣ Visualización de estadísticas
Gráfico	Tipo	Insight
Ventas por referencia	Barras	Modelos más vendidos
Ingresos totales	Barras horizontales	Impacto económico
Distribución por versión	Circular	Proporciones
Años más vendidos	Línea	Tendencias
💡 Caso de Uso Real: Limpieza de Dataset

Archivo: ventas_automotrices.csv

Problema	Cantidad	Acción
Duplicados	3	Eliminados
Monto inválido	1	Filtrado
Fecha futura	1	Descartada
Registros finales	30	Guardados

Resultado:
Dataset limpio, consistente y listo para análisis.
Mejora de calidad: +14.3% (nada mal para un CSV rebelde).

🧠 Valor del Proyecto

Este dashboard permite:

Automatizar limpieza de datos reales.

Centralizar ventas.

Detectar tendencias.

Tomar decisiones basadas en métricas, no en corazonadas.

En otras palabras: menos Excel infinito, más inteligencia. 📈
