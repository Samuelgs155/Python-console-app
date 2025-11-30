import sqlite3

# En este caso la base de datos se encuentra en la carpeta data
# Asegúrate de que la carpeta data exista antes de ejecutar el código
# Si no existe, créala porque es la que utiliza el contenedor Docker para montar el volumen
DB_NAME = "data/tienda.db"

def get_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        # Mejor manejo con foreign keys activadas
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        print(f"❗ Error conectando a la base de datos: {e}")
        return None


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            cliente_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY(producto_id) REFERENCES productos(id),
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        );
    """)

    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente")

def productos_mas_vendidos(limit=5):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.id, p.nombre, SUM(v.cantidad) AS total_vendido
            FROM ventas v
            JOIN productos p ON v.producto_id = p.id
            GROUP BY p.id, p.nombre
            ORDER BY total_vendido DESC
            LIMIT ?
        """, (limit,))

        return cursor.fetchall()

    except sqlite3.Error as e:
        print("Error obteniendo productos más vendidos:", e)
        return []
    finally:
        conn.close()


def clientes_con_mas_compras(limit=5):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, c.nombre, c.email, COUNT(v.id) AS compras
            FROM clientes c
            JOIN ventas v ON c.id = v.cliente_id
            GROUP BY c.id, c.nombre, c.email
            ORDER BY compras DESC
            LIMIT ?
        """, (limit,))

        return cursor.fetchall()

    except sqlite3.Error as e:
        print("Error obteniendo clientes con más compras:", e)
        return []
    finally:
        conn.close()

def clientes_sin_compras():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, c.nombre, c.email
            FROM clientes c
            LEFT JOIN ventas v ON c.id = v.cliente_id
            WHERE v.id IS NULL
        """)

        return cursor.fetchall()

    except sqlite3.Error as e:
        print("Error obteniendo clientes sin compras:", e)
        return []
    finally:
        conn.close()

def ingresos_totales():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(v.cantidad * p.precio) AS total_ingresos
            FROM ventas v
            JOIN productos p ON p.id = v.producto_id
        """)
        
        total = cursor.fetchone()[0]
        return total if total is not None else 0

    except sqlite3.Error as e:
        print("Error calculando ingresos:", e)
        return 0
    finally:
        conn.close()


