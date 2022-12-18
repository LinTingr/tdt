from flask import *
from api.taipeidb import cnxpool
import jwt

booking = Blueprint("booking", __name__, static_folder="static", static_url_path="/")

@booking.route("/api/booking", methods=["POST"])
def schedule():
	try :
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor()
		cookies = request.cookies.get('token')
		userdata = jwt.decode(cookies, "secret", algorithms=["HS256"])
		print(userdata)
		data = {
			"error": True,
			"message": "未登入系統"
		}
		response = make_response(jsonify(data),403)
		if cookies:
			schedule = request.get_json()
			if schedule["date"] :
				query = "select * from order_booking where userid = %s;"
				cursor.execute(query, (userdata["userid"],)) 
				repeat = cursor.fetchone()
				if repeat:
					query = "delete from order_booking where userid = %s;"
					cursor.execute(query, (userdata["userid"],))
				query = "INSERT INTO order_booking(userid, attractionId, date, time, price) VALUES (%s, %s, %s, %s, %s);"
				order = (userdata["userid"], schedule["attractionId"], schedule["date"], schedule["time"], schedule["price"])
				cursor.execute(query, order)
				cnx.commit()
				data = {"ok": True}
				response = make_response(jsonify(data),200)
			else:
				data = {
					"error": True,
					"message": "請選擇日期"
				}
				response = make_response(jsonify(data),400)
			# print(schedule["date"])
		return response
	except :
		data = {
			"error": True,
			"message": "伺服器錯誤"
		}
		response = make_response(jsonify(data),500)
		return response
	finally:
		cursor.close()
		cnx.close()	

@booking.route("/api/booking", methods=["GET"])
def schedule__():
	try :
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor()
		data = {
			"data":None
		}
		cookies = request.cookies.get('token')
		userdata = jwt.decode(cookies, "secret", algorithms=["HS256"])
		query = "select * from order_booking where userid = %s"
		cursor.execute(query, (userdata["userid"], ))
		booking = cursor.fetchone()
		if booking:
			query = "select id, name, address, images from attraction where id = %s;"
			cursor.execute(query, (booking[2],))
			attraction = cursor.fetchone()
			images = attraction[3]
			image = images.split(", ")
			data = {
				"data": {
					"attraction": {
						"id": attraction[0],
						"name": attraction[1],
						"address": attraction[2],
						"image": image[0]
					},
					"date": booking[3],
					"time": booking[4],
					"price": booking[5]
					}
			}
		response = make_response(jsonify(data),200)
		return response
	except :
		data = {
			"error": True,
			"message": "伺服器錯誤"
		}
		response = make_response(jsonify(data),500)
		return response
	finally:
		cursor.close()
		cnx.close()	

@booking.route("/api/booking", methods=["DELETE"])
def schedule___():
	try :
		print(1)
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor()
		print(2)
		cookies = request.cookies.get('token')
		print(3)
		userdata = jwt.decode(cookies, "secret", algorithms=["HS256"])
		print(4)
		print(userdata["userid"])
		query = "DELETE FROM order_booking WHERE userid = %s;"
		cursor.execute(query, (userdata["userid"],))
		cnx.commit()
		data = {"ok":True}
		response = make_response(jsonify(data),200)
		return response
	except :
		data = {
			"error": True,
			"message": "請按照情境提供對應的錯誤訊息"
		}
		response = make_response(jsonify(data),500)
		return response
	finally:
		cursor.close()
		cnx.close()