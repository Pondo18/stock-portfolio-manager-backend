import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/users', methods=['POST'])
def add_user():
	try:
		_json = request.json
		_hashcode = _json['hashcode']
		_username = _json['username']
		_credits = _json['credits']
		if _hashcode and _username and _credits and request.method == 'POST':
			sqlQuery = "INSERT INTO userdata(hashcode, username, credits) VALUES(%s, %s, %s)"
			bindData = (_hashcode, _username, _credits)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			response = jsonify({"hashcode": _hashcode, "username": _username, "credits": _credits})
			response.status_code = 201
			return response
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/users/<string:username>', methods=['GET'])
def get_user(username):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT hashcode, username, credits FROM userdata WHERE username =%s", username)
		userdataRow = cursor.fetchone()
		response = jsonify(userdataRow)
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()



#Credits aktualisieren

@app.route('/users/<string:username>', methods=['PUT'])
def update_user(username):
	try:
		_json = request.json
		_credits = _json['credits']
		if _credits and request.method == 'PUT':
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("UPDATE userdata SET credits=%s WHERE username=%s", (_credits, username))
			conn.commit()
			response = jsonify('User updated successfully!')
			response.status_code = 200
			return response
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/users/<string:username>', methods=['DELETE'])
def delete_user(username):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM userdata WHERE username =%s", (username,))
		conn.commit()
		response = jsonify('User deleted successfully!')
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

if __name__ == "__main__":
    app.run(debug=True)
