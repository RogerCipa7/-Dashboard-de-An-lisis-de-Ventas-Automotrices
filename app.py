from flask import Flask, render_template, request, jsonify
from flask import send_file
import tempfile
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Configurar el backend no interactivo
import matplotlib.pyplot as plt
import seaborn as sns  
import os
import shutil
from database import conectar_db, insertar_venta


app = Flask(__name__)


def limpiar_graficos():
    graficos_dir = os.path.join(os.getcwd(), 'static', 'graficos')
    if os.path.exists(graficos_dir):
        shutil.rmtree(graficos_dir)  
    os.makedirs(graficos_dir, exist_ok=True)  


def calcular_total_ingresos(df):
    total_ingresos = df['monto_total'].sum()  



def limpiar_datos(df):
    try:
        # Logs para depuración
        print(f"Filas iniciales: {len(df)}")

        # 1. Eliminar filas duplicadas
        df = df.drop_duplicates()
        print(f"Filas después de eliminar duplicados: {len(df)}")

        # 2. Manejar valores nulos
        df = df.dropna(subset=['referencia', 'version', 'anio', 'monto_total'])
        print(f"Filas después de eliminar nulos: {len(df)}")

        # 3. Validar tipos de datos
        df['monto_total'] = pd.to_numeric(df['monto_total'], errors='coerce')
        df = df.dropna(subset=['monto_total'])  # Eliminar filas con valores no numéricos
        df = df[df['monto_total'] > 0]  # Validar que monto_total sea mayor que cero

        # 4. Normalizar texto
        df['referencia'] = df['referencia'].str.lower().str.capitalize()
        df['version'] = df['version'].str.lower().str.capitalize()

        # 5. Validar fechas
        df['fecha_venta'] = pd.to_datetime(df['fecha_venta'], errors='coerce')  # Convertir a datetime
        df = df.dropna(subset=['fecha_venta'])  # Eliminar filas con fechas inválidas
        df = df[df['fecha_venta'] <= pd.Timestamp.today()]  # No permitir fechas futuras

        # Logs finales
        print(f"Filas limpias: {len(df)}")
        return df

    except pd.errors.EmptyDataError:
        raise ValueError("El DataFrame está vacío.")
    except pd.errors.ParserError:
        raise ValueError("Error al analizar los datos.")
    except Exception as e:
        raise ValueError(f"Error inesperado durante la limpieza de datos: {str(e)}")

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')


@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    mensaje = None
    if request.method == 'POST':
        try:

            referencia = request.form['carro']
            version = request.form['version']
            anio = int(request.form['anioCarro'])
            fecha_venta = request.form['fechaVenta']
            monto_total = float(request.form['montoTotalHidden'])

            
            insertar_venta(referencia, version, anio, fecha_venta, monto_total)

            mensaje = "La venta se ha registrado correctamente."
        except Exception as e:
            mensaje = f"Ocurrió un error al registrar la venta: {e}"
        return render_template('formulario.html', mensaje=mensaje)
    return render_template('formulario.html', mensaje=None)

@app.route('/estadisticas')
def estadisticas():
    try:
        # Conectar a la base de datos y obtener los datos
        conn = conectar_db()
        query = """
        SELECT 
            referencia, 
            version, 
            anio, 
            fecha_venta, 
            monto_total
        FROM ventas
        """
        df_bd = pd.read_sql(query, conn)
        conn.close()

        # Verificar si hay datos disponibles
        if df_bd.empty:
            # Renderizar la página con un mensaje indicando que no hay datos
            return render_template('estadisticas.html', 
                                   total_ingresos=0,
                                   mensaje="No hay datos disponibles para mostrar estadísticas.")
        
        # Calcular el total de ingresos
        total_ingresos = df_bd['monto_total'].sum()

        # Generar los gráficos
        generar_grafico_ventas_por_referencia(df_bd)
        generar_grafico_ingresos_totales(df_bd)
        generar_grafico_distribucion_versiones(df_bd)
        generar_grafico_anios_mas_vendidos(df_bd)

        # Renderizar la página con los datos y gráficos generados
        return render_template('estadisticas.html', 
                               total_ingresos=total_ingresos,
                               mensaje=None)  # No hay mensaje de error

    except Exception as e:
        # En caso de error, mostrar un mensaje de error
        return render_template('estadisticas.html', 
                               total_ingresos=0,
                               mensaje=f"Ocurrió un error al cargar las estadísticas: {e}")


@app.route('/procesar_csv', methods=['POST'])
def procesar_csv():
    try:
        
        archivo = request.files['archivo']
        
        
        df = pd.read_csv(archivo)
        
        
        if df.empty:
            return jsonify({"error": "El archivo CSV está vacío"}), 400
        
       
        df = limpiar_datos(df)

        
        conn = conectar_db()
        cursor = conn.cursor()

        for _, fila in df.iterrows():
            referencia = fila['referencia']
            version = fila['version']
            anio = int(fila['anio'])
            fecha_venta = fila['fecha_venta'].strftime('%Y-%m-%d')  # Formatear fecha
            monto_total = float(fila['monto_total'])

            
            insertar_venta(referencia, version, anio, fecha_venta, monto_total)

        conn.commit()
        cursor.close()
        conn.close()

        
        total_ventas = int(len(df))
        promedio_precios = float(df['monto_total'].mean())
        referencia_mas_vendida = str(df['referencia'].mode()[0])
        version_mas_vendida = str(df['version'].mode()[0])
        valor_total_ventas = float(df['monto_total'].sum())

        
        estadisticas_csv = {
            "total_ventas": total_ventas,
            "promedio_precios": round(promedio_precios, 2),
            "referencia_mas_vendida": referencia_mas_vendida,
            "version_mas_vendida": version_mas_vendida,
            "valor_total_ventas": round(valor_total_ventas, 2)
        }

        
        return jsonify(estadisticas_csv)
    
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error: {str(e)}"}), 500


#gráfico de ventas por referencia
def generar_grafico_ventas_por_referencia(df):
    ventas_por_referencia = df.groupby('referencia').size().reset_index(name='total_ventas')
    
    #colores vibrantes bright▬ ("Set2", n_colors): Colores pastel."deep", n_colors): Colores profundos.
    colores = sns.color_palette("bright", len(ventas_por_referencia))  # Paleta "husl" con colores únicos
    
    plt.figure(figsize=(10, 6))
    barras = plt.bar(
        ventas_por_referencia['referencia'], 
        ventas_por_referencia['total_ventas'], 
        color=colores,  # colores  a cada barra
        edgecolor='black'
    )
    
    #etiquetas encima de las barras
    for bar in barras:
        altura = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, altura, f'{int(altura)}', ha='center', va='bottom', fontsize=10)
    
    plt.title('Ventas por Referencia', fontsize=16)
    plt.xlabel('Referencia', fontsize=12)
    plt.ylabel('Total de Ventas', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    
    graficos_dir = os.path.join(os.getcwd(), 'static', 'graficos')
    os.makedirs(graficos_dir, exist_ok=True)
    plt.savefig(os.path.join(graficos_dir, 'ventas_por_referencia.png'))
    plt.close()



#gráfico de ingresos totales por referencia
def generar_grafico_ingresos_totales(df):
    ingresos_por_referencia = df.groupby('referencia')['monto_total'].sum().reset_index()
    
    
    colores = sns.color_palette("bright", len(ingresos_por_referencia))  
    
    plt.figure(figsize=(10, 6))
    barras = plt.barh(
        ingresos_por_referencia['referencia'], 
        ingresos_por_referencia['monto_total'], 
        color=colores,  #colores únicos a cada barra
        edgecolor='black'
    )
    
    #etiquetas al lado de las barras
    for bar in barras:
        ancho = bar.get_width()
        plt.text(ancho + 1000, bar.get_y() + bar.get_height() / 2, f'${ancho:,.0f}', va='center', fontsize=10)
    
    plt.title('Ingresos Totales por Referencia', fontsize=16)
    plt.xlabel('Ingresos Totales ($)', fontsize=12)
    plt.ylabel('Referencia', fontsize=12)
    plt.tight_layout()
    
   
    graficos_dir = os.path.join(os.getcwd(), 'static', 'graficos')
    os.makedirs(graficos_dir, exist_ok=True)
    plt.savefig(os.path.join(graficos_dir, 'ingresos_totales.png'))
    plt.close()



def generar_grafico_distribucion_versiones(df):
    distribucion_por_version = df.groupby('version').size().reset_index(name='total_ventas')
    
    
    colores = sns.color_palette("bright", len(distribucion_por_version))  
    
    plt.figure(figsize=(8, 8))
    plt.pie(
        distribucion_por_version['total_ventas'], 
        labels=distribucion_por_version['version'], 
        autopct='%1.1f%%',  #porcentajes
        startangle=90,  #inicial para mejorar la disposición
        colors=colores,  
        textprops={'fontsize': 10},  #tamaño fuente para las etiquetas
        wedgeprops={'edgecolor': 'black'}  #bordes negros a las secciones
    )
    plt.title('Distribución de Ventas por Versión', fontsize=16)
    plt.axis('equal')  # circulo perfecto
    
    
    graficos_dir = os.path.join(os.getcwd(), 'static', 'graficos')
    os.makedirs(graficos_dir, exist_ok=True)
    plt.savefig(os.path.join(graficos_dir, 'distribucion_versiones.png'))
    plt.close()

def generar_grafico_anios_mas_vendidos(df):
    anios_mas_vendidos = df.groupby('anio').size().reset_index(name='total_ventas')
    anios_mas_vendidos = anios_mas_vendidos.sort_values(by='total_ventas', ascending=False)
    plt.figure(figsize=(10, 6))
    plt.plot(anios_mas_vendidos['anio'], anios_mas_vendidos['total_ventas'], marker='o', color='green', linestyle='-', linewidth=2)
    for i, row in anios_mas_vendidos.iterrows():
        plt.text(row['anio'], row['total_ventas'], f'{row["total_ventas"]}', ha='center', va='bottom', fontsize=10)
    plt.title('Años de Carros Más Vendidos', fontsize=16)
    plt.xlabel('Año del Carro', fontsize=12)
    plt.ylabel('Total de Ventas', fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    graficos_dir = os.path.join(os.getcwd(), 'static', 'graficos')
    os.makedirs(graficos_dir, exist_ok=True)
    plt.savefig(os.path.join(graficos_dir, 'anios_mas_vendidos.png'))
    plt.close()

#aplicación principal
if __name__ == '__main__':
    limpiar_graficos()  #limpiar gráficos
    app.run(debug=True)