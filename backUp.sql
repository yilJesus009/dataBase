-- Crear la base de datos
CREATE DATABASE ExamenBase2;
USE ExamenBase2;

-- tabla Estudiante
CREATE TABLE Estudiante (
    ID_Estudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombreCompleto VARCHAR(255) NOT NULL,
    fechaNacimiento DATE NOT NULL,
    carrera VARCHAR(255) NOT NULL
);

-- tabla Materia
CREATE TABLE Materia (
    codigo_Materia VARCHAR(50),
    nombre VARCHAR(255) NOT NULL,
    creditos INT NOT NULL,
    PRIMARY KEY (codigo_Materia)
);


-- tabla Nota
CREATE TABLE Nota (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Estudiante INT,
    nombreEstudiante VARCHAR(255),
    codigo_Materia VARCHAR(50),
    valor FLOAT NOT NULL,
    FOREIGN KEY (ID_Estudiante) REFERENCES Estudiante(ID_Estudiante),
    FOREIGN KEY (codigo_Materia) REFERENCES Materia(codigo_Materia)
);

select * from Estudiante;
select * from Materia;
select * from Nota;