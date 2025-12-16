import sqlite3

class ConexionBD():

    # Método para conectar con BD.
    @staticmethod
    def conectar():
        return sqlite3.connect("myERP.db")

    # Método para insertar registros tabla Clientes.
    @staticmethod
    def insertar_cliente(nombre, nit, edad, telefono, email, plazo_cobro):
        conn = None
        try:
            conn = ConexionBD.conectar()
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

    # Método para insertar registros tabla Productos.
    @staticmethod
    def insertar_producto(nombre, descripcion, categoria, costo, precio_venta, stock, stock_min, unidad):
        conn = None
        try:
            conn = ConexionBD.conectar()
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

    # Método para insertar registros tabla Proveedores.
    @staticmethod
    def insertar_proveedor(nombre, nit, contacto, telefono, email, plazo_pago):
        conn = None
        try:
            conn = ConexionBD.conectar()
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

    # Método para obtener registros de la tabla Proveedores.
    @staticmethod
    def obtener_proveedores():
        conn = None
        try:
            conn = ConexionBD.conectar()
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

    # Método para obtener registros de la tabla Productos.
    @staticmethod
    def obtener_productos():
        conn = None
        try:
            conn = ConexionBD.conectar()
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
        
    # Método para obtener último correlativo.
    @staticmethod
    def obtener_ultimo_numero_oc():
        try:
            conexion = sqlite3.connect('myERP.db')
            cursor = conexion.cursor()
            cursor.execute("SELECT numero_oc FROM ordenes_compra ORDER BY numero_oc DESC LIMIT 1")
            resultado = cursor.fetchone()
            conexion.close()
            
            if resultado:
                return resultado[0]  
            return None
            
        except sqlite3.Error as error:
            raise Exception("Error, no se pudo obtener el último número de OC")
    
    # Método para insertar registros tabla Orden Compra.
    @staticmethod
    def insertar_orden_compra(numero_oc, proveedor_id, proveedor_nombre, nit, fecha_emision, fecha_entrega, plazo_pago, total):
        conn = None
        try:
            conn = ConexionBD.conectar()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO ordenes_compra (numero_oc, proveedor_id, proveedor_nombre, nit, fecha_emision, fecha_entrega, plazo_pago, total) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                (numero_oc, proveedor_id, proveedor_nombre, nit, fecha_emision, fecha_entrega, plazo_pago, float(total)))
            conn.commit()
        except sqlite3.IntegrityError as error:
            error_msg = str(error)
            if "ordenes_compra.numero_oc" in error_msg:
                raise Exception("El número OC ya está registrado en otra Orden de Compra")
            else:
                raise Exception(f"Error de datos duplicados: {error_msg}")
        except Exception as error:
            raise Exception(f"Error al insertar la orden de compra: {str(error)}")
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    # Método para insertar registros tabla Orden Compra (Detalle).
    @staticmethod
    def insertar_oc_detalle(no_item, numero_oc, producto_id, producto_nombre, cantidad, precio_unitario, subtotal):
        conn = None
        try:
            conn = ConexionBD.conectar()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO ordenes_compra_detalle (no_item, numero_oc, producto_id, producto_nombre, cantidad, precio_unitario, subtotal) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                (no_item, numero_oc, producto_id, producto_nombre, float(cantidad), float(precio_unitario), float(subtotal)))
            conn.commit()
        except sqlite3.IntegrityError as error:
            error_msg = str(error)
            if "FOREIGN KEY constraint failed" in error_msg:
                raise Exception(f"El número OC: {numero_oc} no existe")
            elif "ordenes_compra_detalle.numero_oc" in error_msg:
                raise Exception("Error de integridad referencial con la orden de compra")
            else:
                raise Exception(f"Error de datos duplicados: {error_msg}")
        except Exception as error:
            raise Exception(f"Error al insertar el detalle de orden de compra: {str(error)}")
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass