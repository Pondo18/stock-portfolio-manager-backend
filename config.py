from app import app
import os
from flaskext.mysql import MySQL



mysql = MySQL()
"""app.config['MYSQL_DATABASE_USER'] = 'moritz'
app.config['MYSQL_DATABASE_PASSWORD'] = 'secret'
app.config['MYSQL_DATABASE_DB'] = 'finance'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
"""

app.config['MYSQL_DATABASE_USER'] = os.environ.get('DBUSER', 'moritz')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('DBPASS', 'secret')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('DBNAME', 'finance')
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('DBHOST', 'localhost')


mysql.init_app(app)
print(app.config)