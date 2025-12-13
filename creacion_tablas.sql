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