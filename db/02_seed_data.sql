-- ============================================
-- 🚚 PROYECTO: RUTAS DE ENTREGA - DATOS INICIALES
-- Archivo 2/2: Inserción de datos de prueba
-- Este script inserta datos de ejemplo en las tablas existentes.
-- ============================================

USE ruta_de_entrega;

-- 🔹 DATOS DE EJEMPLO

-- CLIENTES
INSERT INTO clientes (nombre, direccion, telefono, correo, latitud, longitud)
VALUES
('Supermercado A', 'Av. Central 123, Aguascalientes', '4491112233', 'contacto@supera.mx', 21.8853, -102.2916),
('Ferretería B', 'Calle 5 de Mayo 456, Jesús María', '4492223344', 'ventas@ferreb.mx', 21.9617, -102.3432),
('Panadería C', 'Av. Siglo XXI 789, Aguascalientes', '4493334455', 'pedido@panaderiac.mx', 21.8765, -102.2955);

-- CONDUCTORES
INSERT INTO conductores (nombre, telefono, licencia)
VALUES
('Luis Pérez', '4495556677', 'LIC12345'),
('Ana Torres', '4496667788', 'LIC67890');

-- VEHÍCULOS
INSERT INTO vehiculos (marca, modelo, placas, capacidad)
VALUES
('Nissan', 'NP300', 'AGX-123', 1200),
('Toyota', 'Hiace', 'AGZ-456', 1500);

-- RUTAS
INSERT INTO rutas (nombre_ruta, id_conductor, id_vehiculo, fecha)
VALUES
('Ruta Norte', 1, 1, '2025-10-17'),
('Ruta Sur', 2, 2, '2025-10-17');

-- ENTREGAS
INSERT INTO entregas (id_ruta, id_cliente, estado, fecha_entrega, hora_entrega, observaciones)
VALUES
(1, 1, 'pendiente', '2025-10-17', '10:00:00', 'Pedido listo para entrega'),
(1, 2, 'en camino', '2025-10-17', '11:00:00', 'Cliente confirmado'),
(2, 3, 'retrasado', '2025-10-17', '12:00:00', 'Retraso por tráfico');

-- PAQUETES
INSERT INTO paquetes (id_entrega, descripcion, peso, valor)
VALUES
(1, 'Caja con productos de limpieza', 25.5, 850.00),
(2, 'Herramientas eléctricas', 40.0, 2300.00),
(3, 'Pan y repostería', 15.0, 600.00);

-- SEGUIMIENTO
INSERT INTO seguimiento (id_entrega, estado, comentario)
VALUES
(1, 'pendiente', 'Pedido cargado en almacén'),
(2, 'en camino', 'Vehículo salió a ruta'),
(3, 'retrasado', 'Demora por cierre de calle');