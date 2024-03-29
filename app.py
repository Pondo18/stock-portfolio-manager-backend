from flask import Flask
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

import pymysql
from config import mysql
from flask import jsonify, request


# USERDATA


@app.route('/users', methods=['POST'])
def add_user():
    _json = request.get_json()
    _hashcode = _json['hashcode']
    _username = _json['username']
    parameters = [_hashcode, _username]
    if _hashcode and _username:
        try:
            sqlQuery = "INSERT INTO userdata(hashcode, username, credits) VALUES(%s, %s, %s)"
            bindData = (_hashcode, _username, 100000)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify({"hashcode": _hashcode, "username": _username, "credits": 100000})
            response.status_code = 201
            cursor.close()
            return response
        except Exception as e:
            print(e)
            return server_error(e)
        finally:
            conn.close()
    else:
        return bad_request(parameters)


@app.route('/users', methods=['GET'])
def get_all_user():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if "hashcode" in request.args:
            cursor.execute("SELECT username FROM userdata WHERE hashcode=%s", (request.args.get('hashcode'),))
        else:
            cursor.execute("SELECT * FROM userdata")
        userdata_row = cursor.fetchall()
        response = jsonify(userdata_row)
        if userdata_row is None:
            response.status_code = 404
        else:
            response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return server_error(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users/<string:username>', methods=['GET'])
def get_user(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT hashcode, username, credits FROM userdata WHERE username =%s", username)
        userdata_row = cursor.fetchone()
        response = jsonify(userdata_row)
        if userdata_row is None:
            response.status_code = 404
        else:
            response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return server_error(e)
    finally:
        cursor.close()
        conn.close()


# update Credits

@app.route('/users/<string:username>', methods=['PUT'])
def update_user_credits(username):
    try:
        _json = request.json
        _credits = _json['credits']
        if _credits:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE userdata SET credits=%s WHERE username=%s", (_credits, username))
            conn.commit()
            response = jsonify('Credits updated successfully!')
            response.status_code = 200
            return response
        else:
            return not_found()
    except Exception as e:
        print(e)
        return server_error(e)
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
        return server_error(e)
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
        parameters = [_holding, _number, _buy_in]

        if _holding and _number and _buy_in:
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
            return bad_request(parameters)
    except Exception as e:
        print(e)
        return server_error(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/holdings', methods=['GET'])
def get_all_holdings():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM holdings")
        holdings_row = cursor.fetchall()
        response = jsonify(holdings_row)
        response.status_code = 200
        return response
    except Exception as e:
        return server_error(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users/<string:username>/holdings', methods=['GET'])
def get_all_holdings_from_user(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM holdings WHERE username =%s", username)
        holdings_row = cursor.fetchall()
        response = jsonify(holdings_row)
        if not holdings_row:
            response.status_code = 204
        else:
            response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return server_error(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users/<string:username>/holdings/<string:holding>', methods=['GET'])
def get_holding_from_user(username, holding):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM holdings WHERE username =%s and holding =%s", (username, holding))
        holdings_row = cursor.fetchone()
        response = jsonify(holdings_row)
        if holdings_row is None:
            return not_found()
        else:
            response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return server_error(e)
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
        return server_error(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users/<string:username>/holdings/<string:holding>', methods=['PUT'])
def update_holding(username, holding):
    try:
        _json = request.json
        _number = _json['number']
        _buy_in = _json['buyIn']
        parameters = [_number, _buy_in]

        if _number and _buy_in:
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
            return bad_request(parameters)
    except Exception as e:
        return server_error(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found():
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@app.errorhandler(400)
def bad_request(parameters=None):
    missing_parameters = []
    for parameter in parameters:
        if not parameter:
            missing_parameters.append(parameter)
    message = {
        'status': 400,
        'message': 'Client error - bad request: ' + str(missing_parameters) + ' missing',
    }
    response = jsonify(message)
    response.status_code = 400
    return response


@app.errorhandler(500)
def server_error(error=None):
    message = {
        'status': 500,
        'message': "Server Error:" + str(error) + " " + request.url,
    }
    response = jsonify(message)
    response.status_code = 500
    return response


if __name__ == "__main__":
    app.run(debug=False)
