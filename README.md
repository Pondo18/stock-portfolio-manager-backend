# Backend zum Portfolio Manager

## Dependencys
Das Backend liegt auf einem Heroku Server, kann aber auch lokal gestartet werden. 
~~~~Bash
heroku local web
~~~~
Um dies zu tuen, müssen zuerst alle verwendeten Librarys installiert werden:
~~~~Bash
pip install -m requirements.txt
~~~~
Die API kommuniziert mit einer MySQL Datenbank, welche ebenfalls lokal gestarten werden kann.

Dafür muss jedoch auch eine Datenbank lokal laufen.
Über Docker lässt sich dies jedoch leicht machen. 

Dafür muss zuerst ein Docker Container gestartet werden:
~~~~Bash
docker-compose up -d
~~~~

Über `docker-compose.yml` werden dem Docker Container nun Informationen über die Datenbank, wie der Port, mitgeteilt.

Der Docker Container lässt sich nun wie folgt neustarten:
~~~~Bash
docker-compose down 
docker-compose up -d
~~~~

Über folgenden Befehl kann er und alle gespeicherten Daten gelöscht werden:
~~~~Bash
docker-compose down -v
~~~~

Wird die Datenbank erstmalig gestartet, müssen jedoch vor der Benutzung die Tabellen erstellt werden: 
~~~~SQL
CREATE TABLE `holdings` (
  `id` int NOT NULL,
  `username` varchar(20) NOT NULL,
  `holding` varchar(100) NOT NULL,
  `number` int NOT NULL,
  `buyIn` double NOT NULL,
  `buyDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
ALTER TABLE `holdings`
  ADD PRIMARY KEY (`id`);
ALTER TABLE `holdings`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

CREATE TABLE `userdata` (
  `hashcode` varchar(32) NOT NULL,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `credits` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
ALTER TABLE `userdata`
  ADD PRIMARY KEY (`username`);
~~~~

Nun kann zwischen der lokalen Datenbank, sowie der Datenbank auf dem Server gewechselt werden.
~~~~Bash
source local.env
~~~~
oder:
~~~~Bash
source scalegrid.env
~~~~

Es kommuniziert mit einer MySQL Datenbank.
Indem die unterschiedlichen .env Dateien geladen werden, lässt sich auch auf eine lokale Datenbank wechseln.
~~~~Bash
source local.env
~~~~


### Backend total lines of Code 
386