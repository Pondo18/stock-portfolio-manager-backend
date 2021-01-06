# Backend zum Portfolio Manager

## Dependenys
Das Backend liegt auf einem Heroku Server, kann aber auch lokal gestartet werden. 
~~~~Bash
heroku local web
~~~~
Es kommuniziert mit einer MySQL Datenbank.
Indem die unterschiedlichen .env Dateien geladen werden, kann aber auch auf eine lokale Docker Datenbank gewechselt werden.
~~~~Bash
read local.env
~~~~

Die verwendeten Library können wie folgt installiert werden: 
~~~~Bash
pip install -m requirements.txt
~~~~













docker run --rm -it mysql mysql -h $DBHOST -u $DBUSER -p"$DBPASS" $DBNAME