from database import init_db

def menu():
    print('')
    print("Bienvenido a la Aplicacion de gestión de la tienda online")
    print('=' * 50)
    print("Por favor, elige una opción:")
    print("1. Administrar items")
    print("2. Consultas y Estadísticas")
    print("3. Salir")
    print('=' * 50)
    print('')

def listar_productos():
    from models import listar_productos
    from itertools import islice
    productos = listar_productos()
    page_size = 10
    it = iter(productos)
    print("Lista de Productos:")
    while True:
        bloque = list(islice(it, page_size))
        if not bloque:
            print("\nNo hay más productos.")
            break
        for p in bloque:
            print(f"ID: {p[0]}, Nombre: {p[1]}, Precio: {p[2]}")
        opcion = input("\nPresiona ENTER para continuar o escribe 'q' para salir: ").strip().lower()
        if opcion == "q":
            print("\nSalida solicitada por el usuario.")
            break

def agregar_producto():
    from models import agregar_producto
    try:
        nombre = input("Nombre del producto: ")
        precio = float(input("Precio del producto: "))
        print(f"Agregando producto... {nombre} - ${precio}")
        seAgrega = bool(input("Confirma agregar el producto? (s/n): ").lower() == 's')
        if seAgrega:
            agregar_producto(nombre, precio)
            print("Producto agregado exitosamente.")
        else:
            print("Operación cancelada. El producto no fue agregado.")
    except Exception as e:
        print(f"Error al agregar el producto: {e}")
        
def actualizar_producto():
    from models import actualizar_producto, listar_productos, buscar_producto_por_id
    productos = listar_productos()    
    if len(productos) == 0:
        print("No hay productos para actualizar.")
        return    
    try:
        producto_id = int(input("Escribe el ID del producto que deseas actualizar: "))
        producto = buscar_producto_por_id(producto_id)
        if not producto:
            print("No se pudo actualizar, producto no encontrado.")   
            return
        print(f"Producto seleccionado: ID: {producto[0]}, Nombre: {producto[1]}, Precio: {producto[2]}")
        nuevo_nombre = input("Nuevo nombre (dejar en blanco para no cambiar): ")   
        nuevo_precio_input = input("Nuevo precio (dejar en blanco para no cambiar): ")
        nuevo_precio = float(nuevo_precio_input) if nuevo_precio_input else None   
        seActualiza = bool(input("Confirma actualizar el producto? (s/n): ").lower() == 's')  
        if not seActualiza:
            print("Operación cancelada. El producto no fue actualizado.")
            return 
        actualizar_producto(producto_id, nuevo_nombre or None, nuevo_precio)
    except Exception as e:
        print(f"Error al actualizar el producto: {e}")
        return
    

def borrrar_producto():
    from models import borrar_producto_por_id, buscar_producto_por_nombre, buscar_producto_por_id  
    try:
        producto_id = int(input("Escribe el ID del producto que deseas borrar: "))    
        producto = buscar_producto_por_id(producto_id)
        print(f"Producto a borrar: ID: {producto[0]}, Nombre: {producto[1]}, Precio: {producto[2]}")
        if not producto:
            print("No se pudo borrar, producto no encontrado.")   
            return 
        seBorra = bool(input("Confirma borrar el producto? (s/n): ").lower() == 's')
        if not seBorra:
            print("Operación cancelada. El producto no fue borrado.")
            return  
        borrar_producto_por_id(producto_id)
    except Exception as e:
        print(f"Error al borrar el producto: {e}")
        return
    

def listar_clientes():
    from models import listar_clientes
    from itertools import islice
    clientes = listar_clientes()
    page_size = 10
    it = iter(clientes)
    print("Lista de Clientes:")
    while True:
        bloque = list(islice(it, page_size))
        if not bloque:
            print("\nNo hay más clientes.")
            break
        for p in bloque:
            print(f"ID: {p[0]}, Nombre: {p[1]}, Email: {p[2]}")
        opcion = input("\nPresiona ENTER para continuar o escribe 'q' para salir: ").strip().lower()
        if opcion == "q":
            print("\nSalida solicitada por el usuario.")
            break

def agregar_cliente():
    from models import agregar_cliente
    nombre = input("Nombre del cliente: ")
    email = input("Email del cliente: ")
    print(f"Agregando cliente... {nombre} - {email}")
    seAgrega = bool(input("Confirma agregar el cliente? (s/n): ").lower() == 's')
    if seAgrega:
        agregar_cliente(nombre, email)
        print("Cliente agregado exitosamente.")
    else:
        print("Operación cancelada. El cliente no fue agregado.")

def actualizar_cliente():
    from models import buscar_cliente_por_email
    email = input("Escribe el email del cliente a actualizar: ")
    cliente = buscar_cliente_por_email(email)
    if cliente:
        from models import actualizar_cliente
        print(f"Cliente encontrado: ID: {cliente[0]}, Nombre: {cliente[1]}, Email: {cliente[2]}")
        nuevo_nombre = input("Nuevo nombre (dejar en blanco para no cambiar): ")
        nuevo_email = input("Nuevo email (dejar en blanco para no cambiar): ")
        print('')
        print(f"Actualizando cliente... {cliente[1]} - {cliente[2]}")
        seActualiza = bool(input("Confirma actualizar el cliente? (s/n): ").lower() == 's')
        if not seActualiza:
            print("Operación cancelada. El cliente no fue actualizado.")
            return
        actualizar_cliente(cliente[0], nuevo_nombre or None, nuevo_email or None)
    else:
        print("No se pudo actualizar, cliente no encontrado.")

def borrrar_cliente():
    from models import buscar_cliente_por_email
    email = input("Escribe el email del cliente a actualizar: ")
    cliente = buscar_cliente_por_email(email)
    if cliente:
        from models import borrar_cliente_por_email
        print(f"Cliente encontrado: ID: {cliente[0]}, Nombre: {cliente[1]}, Email: {cliente[2]}")
        print('')
        print(f"Borrando cliente... {cliente[1]} - {cliente[2]}")
        seBorra = bool(input("Confirma borrar el cliente? (s/n): ").lower() == 's')
        if not seBorra:
            print("Operación cancelada. El cliente no fue borrado.")
            return
        borrar_cliente_por_email(email)
        print("Cliente eliminado exitosamente.")
    else:
        print("No se pudo borrar, cliente no encontrado.")

def registrar_venta():
    from models import registrar_venta, buscar_producto_por_id, buscar_cliente_por_email    
    from models import listar_productos
    
    try:
        productos = listar_productos()
        if len(productos) == 0:
            print("No hay productos para registrar una venta.")
            return      
        
        producto_id = int(input("ID del producto: "))
        productoSeleccionado = buscar_producto_por_id(producto_id)
        if not productoSeleccionado:
            print("No se pudo registrar la venta, producto no encontrado.")   
        
        cliente_email = input("Email del cliente: ")
        clienteDB = buscar_cliente_por_email(cliente_email)
        if not clienteDB:
            print("No se pudo registrar la venta, cliente no encontrado.")
                
        cantidad = int(input("Cantidad: "))
        cliente_id = clienteDB[0]
        registrar_venta(producto_id, cliente_id, cantidad)
        print("Venta registrada exitosamente.")
   
    except Exception as e:  
        print(f"Error al registrar la venta: {e}")
        return 

    

def listar_ventas():
    from models  import listar_ventas
    from itertools import islice
    ventas = listar_ventas()   
    if len(ventas) == 0:
        print("No hay ventas registradas.")   

    page_size = 10
    it = iter(ventas)      
    print("Lista de Ventas:")
    while True:
        bloque = list(islice(it, page_size))
        if not bloque:
            print("\nNo hay más Ventas.")
            break
        for venta in bloque:
            print(f"ID: {venta[0]}, Producto Nombre: {venta[1]}, Cliente Nombre: {venta[2]}, Cantidad: {venta[3]}, Fecha: {venta[4]}")
        opcion = input("\nPresiona ENTER para continuar o escribe 'q' para salir: ").strip().lower()
        if opcion == "q":
            print("\nSalida solicitada por el usuario.")
            break
    print('')
    
def borrar_venta():
    from models import borrar_venta_por_id, listar_ventas,buscar_venta_por_id
    ventas = listar_ventas()   
    if len(ventas) == 0:
        print("No hay ventas registradas.")  
        return      
    try:
        venta_id = int(input("Escribe el ID de la venta que deseas borrar: "))  
        venta = buscar_venta_por_id(venta_id)
        if not venta:
            print("No se pudo borrar, venta no encontrada.")   
            return
        print(f"Venta a borrar: ID: {venta[0]}, Producto ID: {venta[1]}, Cliente ID: {venta[2]}, Cantidad: {venta[3]}, Fecha: {venta[4]}")
        seBorra = bool(input("Confirma borrar la venta? (s/n): ").lower() == 's')
        if not seBorra:
            print("Operación cancelada. La venta no fue borrada.")
            return
        borrar_venta_por_id(venta_id)
        print("Venta eliminada exitosamente.")
    except Exception as e:
        print(f"Error al borrar la venta: {e}")
        return
    
def clientes_con_mas_compras():
    from database import clientes_con_mas_compras
    limit = int(input("¿Cuántos clientes deseas ver?: "))
    clientes = clientes_con_mas_compras(limit)
    print('')
    print(f"Top {limit} Clientes con más compras:")
    for cli in clientes:
        print(f"ID: {cli[0]}, Nombre: {cli[1]}, Email: {cli[2]}, Compras: {cli[3]}")  
    print('') 

def clientes_sin_compras():
    from database import clientes_sin_compras
    clientes = clientes_sin_compras()
    print("Clientes sin compras:")
    for cli in clientes:
        print(f"ID: {cli[0]}, Nombre: {cli[1]}, Email: {cli[2]}") 
    print('') 

def ingresos_totales():
    from database import ingresos_totales
    total = ingresos_totales()
    print(f"Ingresos totales de la tienda: ${total:.2f}")
    print('') 

def gestionar_items():
    while True:
        print('')
        print("Gestión de Items")
        print('-' * 30)
        print("1. Listar Productos")
        print("2. Insertar Producto")
        print("3. Actualizar Producto")
        print("4. Borrar Producto")
        print("5. Listar Clientes")
        print("6. Insertar Cliente")
        print("7. Actualizar Cliente")
        print("8. Borrar Cliente")
        print("9. Listar Ventas")
        print("10. Registrar Venta")
        print("11. Borrar Venta")
        print("12. Volver al Menú Principal")
        print('-' * 30)
        choice = input("Ingresa el número de la opción deseada: ")
        print('')
        if choice == '1':
            listar_productos()
        elif choice == '2':
            agregar_producto()
        elif choice == '3':
            actualizar_producto()            
        elif choice == '4':
            borrrar_producto()
        elif choice == '5':
            listar_clientes()          
        elif choice == '6':
            agregar_cliente()
        elif choice == '7':
            actualizar_cliente()
        elif choice == '8':
            borrrar_cliente()
        elif choice == '9':
            listar_ventas()            
        elif choice == '10':
            registrar_venta()
        elif choice == '11':
            borrar_venta()
        elif choice == '12':
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
    

def gestionar_consultas_y_estadisticas():
    print("Funcionalidad de consultas y estadísticas aún no implementada.")
    while True:
        print('')
        print("Consultas y Estadísticas")
        print('-' * 30)
        print("1. Clientes con más compras")
        print("2. Clientes sin compras")
        print("3. Ingresos totales")
        print("4. Volver al Menú Principal")
        print('-' * 30)
        choice = input("Ingresa el número de la opción deseada: ")
        print('')
        if choice == '1':
            clientes_con_mas_compras()
        elif choice == '2':
            clientes_sin_compras()
        elif choice == '3':
            ingresos_totales()
        elif choice == '4':
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    #inicializar la base de datos
    init_db()

    while True:
        menu()
        choice = input("Ingresa el número de la opción deseada: ")
        print('')
        if choice == '1':
            print("Redirigiendo a la gestión de items...")
            gestionar_items()
        elif choice == '2':
            print("Redirigiendo a consultas y estadísticas...")
            gestionar_consultas_y_estadisticas()
        elif choice == '3':
            print("Saliendo de la aplicación. Por favor, que tenga un buen día.")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
    