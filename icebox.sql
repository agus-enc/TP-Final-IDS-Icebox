CREATE DATABASE IF NOT EXISTS ICEBOX;
USE ICEBOX;

CREATE TABLE usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(20) DEFAULT 'user' -- rol user o admin para acceso
);

CREATE TABLE paises (
    id_pais INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    continente VARCHAR(50) NOT NULL -- sacar en caso de no ser necesaria
);

CREATE TABLE ciudades (
    id_ciudad INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_pais INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    latitud DECIMAL(10, 8), -- (M (Precisión), D (Escala))
    longitud DECIMAL(11, 8),
    FOREIGN KEY (id_pais) REFERENCES paises(id_pais) ON DELETE CASCADE
);

CREATE TABLE viajes (
    id_viaje INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    fecha_viaje DATE, -- puede ser null si el usuario no quiere poner fecha
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE paradas (
    id_parada INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_viaje INT NOT NULL,
    id_ciudad INT NOT NULL,
    orden_en_ruta INT NOT NULL, -- saber el orden de las paradas
    relato_texto JSON,
    FOREIGN KEY (id_viaje) REFERENCES viajes(id_viaje) ON DELETE CASCADE,
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad)
);

CREATE TABLE imanes (
    id_iman INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_ciudad INT, -- saber que ciudad es para el predeterminado (relación con país) 
    id_parada INT NOT NULL, 
    imagen_url VARCHAR(255),
    predeterminado BOOLEAN DEFAULT FALSE, -- iman predeterminado
    ubicación_heladera BOOLEAN DEFAULT FALSE, -- control de vista en heladera o en cajon
    posicion_x FLOAT DEFAULT 0, -- necesario para que se guarde la posición del Drag and Drop
    posicion_y FLOAT DEFAULT 0,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad) ON DELETE SET NULL,
    FOREIGN KEY (id_parada) REFERENCES paradas(id_parada) ON DELETE CASCADE
);