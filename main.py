import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request


# USERDATA


@app.route('/users', methods=['POST'])
def add_user():
    try:
        _json = request.json
        _hashcode = _json['hashcode']
        _username = _json['username']
        if _hashcode and _username and request.method == 'POST':
            sqlQuery = "INSERT INTO userdata(hashcode, username, credits) VALUES(%s, %s, %s)"
            bindData = (_hashcode, _username, 100000)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify({"hashcode": _hashcode, "username": _username, "credits": 100000})
            response.status_code = 201
            return response
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users', methods=['GET'])
def get_all_user():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if "hashcode" in request.args:
            cursor.execute("SELECT username FROM userdata WHERE hashcode=%s", (request.args.get('hashcode'),))
        else:
            cursor.execute("SELECT * FROM userdata")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
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


# Credits aktualisieren

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


# HOLDINGS


@app.route('/users/<string:username>/holdings', methods=['POST'])
def add_holding(username):
    try:
        _json = request.json
        _holding = _json['holding']
        _number = _json['number']
        _buy_in = _json['buyIn']
        if _holding and _number and _buy_in and request.method == 'POST':
            sqlQuery = "INSERT INTO holdings(username, holding, number, buyIn) VALUES(%s, %s, %s, %s)"
            bindData = (username, _holding, _number, _buy_in)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify({"username": username, "holding": _holding, "number": _number, "buyIn": _buy_in})
            response.status_code = 201
            return response
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/holdings', methods=['GET'])
def get_all_holdings():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM holdings")
        userdataRow = cursor.fetchone()
        response = jsonify(userdataRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users/<string:username>/holdings', methods=['GET'])
def get_all_holdings_from_user(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM holdings WHERE username =%s", username)
        userdataRow = cursor.fetchone()
        response = jsonify(userdataRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users/<string:username>/holdings/<string:holding>', methods=['GET'])
def get_holding_from_user(username, holding):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM holdings WHERE username =%s and holding =%s", (username, holding))
        userdataRow = cursor.fetchone()
        response = jsonify(userdataRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users/<string:username>/holdings/<string:holding>', methods=['DELETE'])
def delete_holding(username, holding):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM holdings WHERE username =%s and holding =%s", (username, holding))
        conn.commit()
        response = jsonify('Holding deleted successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users/<string:username>/holdings/<string:holding>', methods=['PUT'])
def update_holding(username, holding):
    try:
        _json = request.json
        _number = _json['number']
        _buy_in = _json['buyIn']

        if _number and _buy_in and request.method == 'PUT':
            sqlQuery = "UPDATE holdings SET number=%s, buyIn=%s WHERE username=%s and holding =%s"
            bindData = (_number, _buy_in, username, holding)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Holding updated successfully!')
            response.status_code = 200
            return response
        else:
            return not_found()
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
