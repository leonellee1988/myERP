-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
	nit TEXT NOT NULL UNIQUE,
    edad INTEGER NOT NULL CHECK (edad >= 0 AND edad <= 120),
    telefono TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
	plazo_cobro TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT (datetime('now', 'localtime'))
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    categoria TEXT NOT NULL,
    costo REAL NOT NULL CHECK (costo >= 0),
    precio_venta REAL NOT NULL CHECK (precio_venta >= 0),
    stock REAL NOT NULL DEFAULT 0 CHECK (stock >= 0),
    stock_min REAL NOT NULL DEFAULT 0 CHECK (stock_min >= 0),
    unidad TEXT NOT NULL DEFAULT 'Unidad',
    fecha_registro TIMESTAMP DEFAULT (datetime('now', 'localtime'))
);

-- Tabla de proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    nit TEXT NOT NULL UNIQUE,
    contacto TEXT NOT NULL,
    telefono TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    plazo_pago TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT (datetime('now', 'localtime'))
);

-- Tabla de órdenes de compra
CREATE TABLE IF NOT EXISTS ordenes_compra (
    numero_oc VARCHAR(20) PRIMARY KEY,
    proveedor_id INTEGER NOT NULL,
    proveedor_nombre VARCHAR(100) NOT NULL,
    nit VARCHAR(20) NOT NULL,
    fecha_emision DATE NOT NULL,
    fecha_entrega DATE NOT NULL,
    plazo_pago VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
);

-- Tabla detalle de órdenes de compra
CREATE TABLE IF NOT EXISTS ordenes_compra_detalle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    no_item INTEGER NOT NULL,
    numero_oc VARCHAR(20) NOT NULL,
    producto_id INTEGER NOT NULL,
    producto_nombre VARCHAR(100) NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (numero_oc) REFERENCES ordenes_compra(numero_oc) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);