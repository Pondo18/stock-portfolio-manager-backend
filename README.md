# Backend zum Portfolio Manager

## Aufgabe des Backends
Das Backend dient, als Rest-API Schnittstelle zwischen Client und Daten. 
Es ermöglicht einen sicheren Zugriff auf die Datenbank,
ohne die Credentials im Client Code hinterlegen zu müssen.

[Frontend Repository](https://github.com/Pondo18/AktienPython)

## Funktion der API
Mithilfe von URL-Routing über Flask werden der in der API bestimmte Funktionen definiert. 
Anschließend wird der SQL-Befehl ausgeführt und die Antwort als Response ausgegeben.

### Wichtige Status Codes
* 200: Ok. Request war erfolgreich
* 201: Ok. Neuer Eintrag erstellt
* 400: Client Error - Bad Request
* 404: Not found. Eintrag nicht gefunden
* 500: Internal Server Error


## Dependencies
Das Backend liegt auf einem Server, welcher z.B. über [Heroku](https://www.heroku.com/) gehostet werden kann. 
Es kann jedoch ebenfalls lokal gestartet werden: 
~~~~Bash
heroku local web
~~~~
Um dies zu tun, müssen zuerst alle verwendeten Libraries installiert werden:
~~~~Bash
pip install -m requirements.txt
~~~~
Die API kommuniziert mit einer MySQL Datenbank,
welche sowohl auf einem eigenen Server als auch lokal bereitgestellt werden kann.
Ich hab sie bei dem Hosting-Anbieter [Scalegrid](https://scalegrid.io/) hosten lassen,
wo sie für 30 Tage kostenlos ist.

Eine lokale Entwicklung bringt trotzdem einige Vorteile mit sich, 
deshalb empfiehlt es sich z.B. über Docker eine lokal, aufzusetzen.

Dafür muss zuerst ein Docker Container gestartet werden:
~~~~Bash
docker-compose up -d
~~~~

Über `docker-compose.yml` werden dem Docker Container nun Informationen über die Datenbank, wie der Port, mitgeteilt.
Außerdem stellt es eine phpmyadmin Benutzeroberfläche bereit. 
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

Die Informationen über die Datenbank bekommt das Programm aus Umgebungsvariablen, welche in den `.env` Dateien hinterlegt sind.
~~~~Bash
DBHOST
DBUSER
DBNAME
DBPASS
~~~~

Mithilfe dem Folgenden kann zwischen lokaler und nicht lokaler Datenbank gewechselt werden.
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

## Hinweise
Die API befindet sich im Development Zustand und ist nicht über http-authentication,
oder weitere Verfahren geschützt.

## Links

Server:
[Heroku](https://www.heroku.com/) - [Heroku Doku](https://devcenter.heroku.com/categories/reference)

Datenbank: [Scalegrid](https://scalegrid.io/) - [Docker](https://www.docker.com/)

Rest-API: [Flask Doku](https://flask.palletsprojects.com/en/1.1.x/)