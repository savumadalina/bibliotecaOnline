CREATE SCHEMA bibliotecaOnline;

USE bibliotecaOnline;

--------  creare tabele 
CREATE TABLE Utilizatori 
( ID INT PRIMARY KEY AUTO_INCREMENT, 
Nume VARCHAR(100) NOT NULL, 
Email VARCHAR(100) NOT NULL, 
Parola VARCHAR(100) NOT NULL, 
Rol VARCHAR(100) NOT NULL );

CREATE TABLE Autori
( ID INT AUTO_INCREMENT PRIMARY KEY,
Nume VARCHAR(100) NOT NULL,
Nationalitate VARCHAR(100)
);

CREATE TABLE Genuri
( ID INT AUTO_INCREMENT PRIMARY KEY,
Nume VARCHAR(100) NOT NULL,
Descriere VARCHAR(200)
);

CREATE TABLE Carti
( ID INT AUTO_INCREMENT PRIMARY KEY,
Titlu VARCHAR(100) NOT NULL,
Disponibilitate INT NOT NULL,
PG INT,
Limba VARCHAR(50),
ID_Genuri INT NOT NULL,
ID_Autori INT NOT NULL,
Imagine VARCHAR(100),
FOREIGN KEY (ID_Genuri) REFERENCES Genuri(ID),
FOREIGN KEY (ID_Autori) REFERENCES Autori(ID));

CREATE TABLE Rezervari
( ID INT AUTO_INCREMENT PRIMARY KEY,
ID_Utilizator INT NOT NULL,
ID_Carte INT NOT NULL,
DataRezervare DATETIME NOT NULL,
FOREIGN KEY (ID_Utilizator) REFERENCES Utilizatori(ID),
FOREIGN KEY (ID_Carte) REFERENCES Carti(ID) );

CREATE TABLE Imprumuturi
( ID INT AUTO_INCREMENT PRIMARY KEY,
ID_Utilizator INT NOT NULL,
ID_Carte INT NOT NULL,
DataImprumut DATE NOT NULL,
DataReturnare DATE,
FOREIGN KEY (ID_Utilizator) REFERENCES Utilizatori(ID),
FOREIGN KEY (ID_Carte) REFERENCES Carti(ID) );


INSERT INTO Genuri VALUES
(1, 'Tehnic', 'test'),
(2, 'Dragoste', 'test'),
(3, 'Fantasy', 'test');

INSERT INTO Genuri VALUES
(4, 'Social', 'test');
INSERT INTO Autori VALUES
(3, 'J.K.Rowling', "Englez");
INSERT INTO Autori VALUES
(4, 'Marin Preda', "Român");
INSERT INTO Carti VALUES
(1, '101 Ways To Be A Software Engineer', 1 , 13, 'Engleza',1,1,'/static/images/bg.jpg'),
(2, 'Fluturi', 1, 12, 'Romana', 2,2,'/static/images/fluturi.jpg'),
(3, 'Harry Potter', 0, 9, 'Romana', 3,3,'/static/images/harry.jpg');

commit;


