from database import get_connection
import sqlite3

def buscar_producto_por_nombre(nombre):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
        productos = cursor.fetchall()

        if productos:
            return productos
        else:
            print("No se encontraron productos con ese nombre.")
            return []
    except sqlite3.Error as e:
        print("Error buscando producto:", e)
        return []
    finally:
        conn.close()

def buscar_producto_por_id(producto_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()

        if producto:
            return producto
        else:
            print("No se encontró un producto con ese ID.")
            return None
    except sqlite3.Error as e:
        print("Error buscando producto por ID:", e)
        return None
    finally:
        conn.close()


def agregar_producto(nombre, precio):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos(nombre, precio) VALUES (?, ?)", (nombre, precio))
        conn.commit()
    except sqlite3.Error as e:
        print("Error agregando producto:", e)
    finally:
        conn.close()

def actualizar_producto(producto_id, nuevo_nombre=None, nuevo_precio=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Verificar si el producto existe
        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()

        if not producto:
            print("No existe un producto con ese ID.")
            return

        # Crear la query dinámicamente (solo actualiza lo que envías)
        campos = []
        valores = []

        if nuevo_nombre:
            campos.append("nombre = ?")
            valores.append(nuevo_nombre)

        if nuevo_precio is not None:
            campos.append("precio = ?")
            valores.append(nuevo_precio)

        if not campos:
            print("No hay datos para actualizar.")
            return

        valores.append(producto_id)

        query = f"UPDATE productos SET {', '.join(campos)} WHERE id = ?"
        cursor.execute(query, tuple(valores))
        conn.commit()

        print("Producto actualizado correctamente")

    except sqlite3.Error as e:
        print("Error actualizando producto:", e)
    finally:
        conn.close()

def buscar_producto_por_id(producto_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()

        if producto:
            return producto
        else:
            print("No se encontró un producto con ese ID.")
            return None
    except sqlite3.Error as e:
        print("Error buscando producto por ID:", e)
        return None
    finally:
        conn.close()

def listar_productos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error listando productos:", e)
    finally:
        conn.close()

def buscar_cliente_por_email(email):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM clientes WHERE email = ?", (email,))
        cliente = cursor.fetchone()

        if cliente:
            return cliente
        else:
            print("No se encontró un cliente con ese email.")
            return None

    except sqlite3.Error as e:
        print("Error buscando cliente:", e)
        return None
    finally:
        conn.close()

def borrar_producto_por_id(producto_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Verificar si el producto existe
        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()

        if not producto:
            print("No existe un producto con ese ID.")
            return

        # Comprobar ventas asociadas
        cursor.execute("SELECT COUNT(*) FROM ventas WHERE producto_id = ?", (producto_id,))
        ventas_asociadas = cursor.fetchone()[0]

        if ventas_asociadas > 0:
            print("No se puede eliminar. El producto tiene ventas registradas.")
            return

        # Borrar producto
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conn.commit()

        print("Producto eliminado correctamente")

    except sqlite3.Error as e:
        print("Error eliminando producto:", e)
    finally:
        conn.close()



def agregar_cliente(nombre, email):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes(nombre, email) VALUES (?, ?)", (nombre, email))
        conn.commit()
    except sqlite3.IntegrityError:
        print("El email ya está registrado.")
    except sqlite3.Error as e:
        print("Error agregando cliente:", e)
    finally:
        conn.close()

def actualizar_cliente(cliente_id, nuevo_nombre=None, nuevo_email=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Verificar si el cliente existe
        cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
        existente = cursor.fetchone()

        if not existente:
            print("No existe un cliente con ese ID.")
            return

        # Construimos la query dinámicamente
        campos = []
        valores = []

        if nuevo_nombre:
            campos.append("nombre = ?")
            valores.append(nuevo_nombre)

        if nuevo_email:
            campos.append("email = ?")
            valores.append(nuevo_email)

        if not campos:
            print("No hay datos para actualizar.")
            return

        valores.append(cliente_id)

        query = f"UPDATE clientes SET {', '.join(campos)} WHERE id = ?"
        cursor.execute(query, tuple(valores))
        conn.commit()

        print("Cliente actualizado correctamente")

    except sqlite3.IntegrityError:
        print("Ese email ya está registrado por otro cliente.")
    except sqlite3.Error as e:
        print("Error actualizando cliente:", e)
    finally:
        conn.close()

def borrar_cliente_por_email(email):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Verificar si el cliente existe
        cursor.execute("SELECT id FROM clientes WHERE email = ?", (email,))
        cliente = cursor.fetchone()

        if not cliente:
            print("No existe un cliente con ese email.")
            return

        cliente_id = cliente[0]

        # Comprobar ventas asociadas
        cursor.execute("SELECT COUNT(*) FROM ventas WHERE cliente_id = ?", (cliente_id,))
        ventas_asociadas = cursor.fetchone()[0]

        if ventas_asociadas > 0:
            print("No se puede eliminar. El cliente tiene ventas registradas.")
            return

        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conn.commit()

        print("Cliente eliminado correctamente")

    except sqlite3.Error as e:
        print("❗ Error eliminando cliente:", e)
    finally:
        conn.close()




def listar_clientes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error listando clientes:", e)
    finally:
        conn.close()

from datetime import datetime

def registrar_venta(producto_id, cliente_id, cantidad):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
        INSERT INTO ventas(producto_id, cliente_id, cantidad, fecha)
        VALUES (?, ?, ?, ?)
        """, (producto_id, cliente_id, cantidad, fecha))

        conn.commit()
    except sqlite3.IntegrityError:
        print("Producto o Cliente no existen.")
    except sqlite3.Error as e:
        print("❗ Error registrando venta:", e)
    finally:
        conn.close()

def listar_ventas():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT v.id, p.nombre, c.nombre, cantidad, fecha
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        JOIN clientes c ON v.cliente_id = c.id
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error listando ventas:", e)
    finally:
        conn.close()

def borrar_venta_por_id(venta_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Verificar si la venta existe
        cursor.execute("SELECT * FROM ventas WHERE id = ?", (venta_id,))
        venta = cursor.fetchone()

        if not venta:
            print("No existe una venta con ese ID.")
            return

        cursor.execute("DELETE FROM ventas WHERE id = ?", (venta_id,))
        conn.commit()

        print("Venta eliminada correctamente")

    except sqlite3.Error as e:
        print("Error eliminando venta:", e)
    finally:
        conn.close()

def buscar_venta_por_id(venta_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT v.id, p.nombre, c.nombre, cantidad, fecha
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        JOIN clientes c ON v.cliente_id = c.id
        WHERE v.id = ?
        """, (venta_id,))

        venta = cursor.fetchone()

        if venta:
            return venta
        else:
            print("No se encontró una venta con ese ID.")
            return None

    except sqlite3.Error as e:
        print("Error buscando venta por ID:", e)
        return None
    finally:
        conn.close()
