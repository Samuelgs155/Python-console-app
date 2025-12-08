# Gestor de clientes-productos-ventas

# autor: Samuel García

# Estructura
tienda/
│── database.py                     # Conexión y creación de tablas
│── models.py                       # Clases para acceder a la BD (productos, clientes, ventas)
│── Samuel_Garcia_app.py            # Interfaz de consola
│── data                            # carpeta donde se almacena de manera persistente la base de datos SQLite de docker
    │── tienda.db                   # Contiene la base de datos
│── Readme.txt                      # opcional pero necesaria para explicar su instalación, uso y arranque


# Requisitos

# Versión de Pyton 3.11.1 en local
# Tener instalado Docker en local

# instalación
# El entregable se da en un archivo .zip
# Descargar el fichero en una carpeta del escritorio creada por el usuario
# Descomprimir el fichero anterior dentro de esa carpeta
# Compruebe que tiene la estructura de ficheros expuesta más arriba

# Utilizacion

# Paso 1 - Arrancar docker
# Se requiere el uso de docker que contiene la base de datos SQLite
# arrancar desde un CMD
docker run -it --rm -v %cd%:/data keinos/sqlite3

# Paso 2 - Comprobar que este contenedor docker está arrancado 
# Ejecuta el siguiente comando y busca ese contenedor
docker ps

# Otra opción es buscarlo desde Docker Desktop

# Paso 3 - Arrancar la aplicación
# Una vez ejecutado el comando anterior se podrá arrancar esta aplicación
# y funcionará correctamente.
# Opción 1
# Se puede arrancar la aplicación desde Visual Studio
# Opción 2
# Dentro de la carpeta donde está el fichero Samuel_Garcia_app.py, ejecutar este comando "python .\Samuel_Garcia_app.py" en la Terminal o en un CMD

# Ejecutar el docker-compose
# docker-compose up -d
# Entra al contenedor de la app
# docker exec -it tienda_app bash
# Ejecuta tu app manualmente
# python Samuel_Garcia_app.py


docker tag tienda_app samuelgs15/python_tienda_terminal_app:1.0
docker push samuelgs15/python_tienda_terminal_app:1.0



