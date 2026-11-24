CREATE TABLE IF NOT EXISTS ventas (
    id_venta INTEGER PRIMARY KEY,
    fecha DATE NOT NULL,
    producto VARCHAR(100) NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(12,2) NOT NULL
        CHECK (precio_unitario > 0),
    ciudad VARCHAR(100) NOT NULL,
    total NUMERIC(14,2) GENERATED ALWAYS AS
        (cantidad * precio_unitario) STORED
);