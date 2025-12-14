import sqlite3

# (1) Función para conectar con BD.
def conectar():
    return sqlite3.connect("myERP.db")

# (2) Función para insertar registros tabla Clientes.
def insertar_cliente(nombre, nit, edad, telefono, email, plazo_cobro):
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO clientes (nombre, nit, edad, telefono, email, plazo_cobro) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (nombre, nit, int(edad), telefono, email, plazo_cobro))
        conn.commit()
    except sqlite3.IntegrityError as error:
        error_msg = str(error)
        if "clientes.nit" in error_msg:
            raise Exception("El NIT ya está registrado en otro cliente")
        elif "clientes.telefono" in error_msg:
            raise Exception("El teléfono ya está registrado en otro cliente")
        elif "clientes.email" in error_msg:
            raise Exception("El email ya está registrado en otro cliente")
        else:
            raise Exception(f"Error de datos duplicados: {error_msg}")
    except Exception as error:
        raise Exception(f"Error al insertar cliente: {str(error)}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# (3) Función para insertar registros tabla Productos.
def insertar_producto(nombre, descripcion, categoria, costo, precio_venta, stock, stock_min, unidad):
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
        """INSERT INTO productos (nombre, descripcion, categoria, costo, precio_venta, stock, stock_min, unidad) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (nombre, descripcion, categoria, float(costo), float(precio_venta), float(stock), float(stock_min), unidad))
        conn.commit()
    except Exception as error:
        raise Exception(f"Error al insertar producto: {str(error)}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# (4) Función para insertar registros tabla Proveedores.
def insertar_proveedor(nombre, nit, contacto, telefono, email, plazo_pago):
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO proveedores (nombre, nit, contacto, telefono, email, plazo_pago) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (nombre, nit, contacto, telefono, email, plazo_pago))
        conn.commit()
    except sqlite3.IntegrityError as error:
        error_msg = str(error)
        if "proveedores.nit" in error_msg:
            raise Exception("El NIT ya está registrado en otro proveedor")
        elif "proveedores.telefono" in error_msg:
            raise Exception("El teléfono ya está registrado en otro proveedor")
        elif "proveedores.email" in error_msg:
            raise Exception("El email ya está registrado en otro proveedor")
        else:
            raise Exception(f"Error de datos duplicados: {error_msg}")
    except Exception as error:
        raise Exception(f"Error al insertar proveedor: {str(error)}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# (5) Función para obtener registros de la tabla Proveedores.
def obtener_proveedores():
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, nit, plazo_pago FROM proveedores ORDER BY nombre")
        proveedores = cursor.fetchall()
        return proveedores
    except sqlite3.OperationalError as error:
        if "no such table" in str(error).lower():
            raise Exception("La tabla proveedores no existe")
        else:
            raise Exception(f"Error en la base de datos {str(error)}")
    except Exception as error:
        raise Exception(f"Error al obtener proveedores: {str(error)}")
    finally:
        if conn:
            conn.close()

# (6) Función para obtener registros de la tabla Productos.
def obtener_productos():
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM productos ORDER BY nombre")
        productos = cursor.fetchall()
        return productos
    except sqlite3.OperationalError as error:
        if "no such table" in str(error).lower():
            raise Exception("La tabla productos no existe")
        else:
            raise Exception(f"Error en la base de datos {str(error)}")
    except Exception as error:
        raise Exception(f"Error al obtener productos: {str(error)}")
    finally:
        if conn:
            conn.close()