CREATE TABLE IF NOT EXISTS usuarios (
    id_discord TEXT PRIMARY KEY,
    nombre_usuario TEXT NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS progreso_cuestionario (
    usuario_id TEXT PRIMARY KEY,
    respuestas TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_discord)
);

CREATE TABLE IF NOT EXISTS inversiones (
    id_inversion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_discord TEXT,
    nombre_inversion TEXT,
    tipo_inversion TEXT,
    valor_perfil_inversor REAL,  -- Cambié de INTEGER a REAL para permitir decimales
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
    expectativa_rendimiento TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_discord)
);
