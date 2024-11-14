-- Crear base de datos
CREATE DATABASE sistema_inversiones;

-- Usar la base de datos
USE sistema_inversiones;

-- Crear tabla de usuarios con ID de Discord
CREATE TABLE usuarios (
    id_discord VARCHAR(50) PRIMARY KEY,
    nombre_usuario VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de inversiones, relacionada con los usuarios
CREATE TABLE inversiones (
    id_inversion INTEGER PRIMARY KEY,
    id_discord VARCHAR(50),
    nombre_inversion VARCHAR(255),
    tipo_inversion VARCHAR(50),
    valor_perfil_inversor INTEGER,
    FOREIGN KEY (id_discord) REFERENCES usuarios(id_discord)
);

CREATE TABLE IF NOT EXISTS respuestas_perfil (
    usuario_id TEXT PRIMARY KEY,
    objetivo_inversion TEXT,
    horizonte_temporal TEXT,
    tiempo_mantener TEXT,
    nivel_experiencia TEXT,
    capital_inicial TEXT,
    ingreso_anual TEXT,
    nivel_deuda TEXT,
    porcentaje_ingresos_invertir TEXT,
    tolerancia_riesgo TEXT,
    inversiones_activas TEXT,
    ingresos_o_crecimiento TEXT,
    reaccion_perdida TEXT,
    productos_financieros TEXT,
    preferencias_sector TEXT,
    mercados_nacionales_o_internacionales TEXT,
    conocimiento_mercado TEXT,
    volatilidad_mercado TEXT,
    sostenibilidad TEXT,
    preocupaciones_inversiones TEXT,
    expectativa_rendimiento TEXT
);
