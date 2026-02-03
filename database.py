import mysql.connector


def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="",  
        database="ventas_autos"
    )


def insertar_venta(referencia, version, anio, fecha_venta, monto_total):
    conn = conectar_db()
    cursor = conn.cursor()
    query = """
    INSERT INTO ventas (referencia, version, anio, fecha_venta, monto_total)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (referencia, version, anio, fecha_venta, monto_total))
    conn.commit()
    cursor.close()
    conn.close()
#leer csv pasar a bd o lee solo csv- o bd 

"""
-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS ventas_autos;
USE ventas_autos;

-- Crear la tabla 'ventas'
CREATE TABLE IF NOT EXISTS ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    referencia VARCHAR(50) NOT NULL,
    version VARCHAR(50) NOT NULL,
    anio INT NOT NULL,
    fecha_venta DATE NOT NULL,
    monto_total DECIMAL(15, 2) NOT NULL
);

"""