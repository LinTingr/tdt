from flask import *
import mysql.connector.pooling
import dbbase

dbconfig={
    "database":"taipeitravel",
    "user":"root",
    "password":dbbase.password(),
    "host":'127.0.0.1',
    "port":"3306"
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="poolname",
                                                        pool_size=1, 
                                                        pool_reset_session=True, 
                                                        **dbconfig)

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False

app.secret_key="any"

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")
	
@app.route("/api/attractions")
def api_attractions():
	try:
		page = request.args.get("page", 0)
		number_of_page = 12
		keyword = request.args.get("keyword", None)
		viewpoint = []
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor()

		if keyword == None:
			query = "select * from attraction limit %s, %s;"
			cursor.execute(query, ((int(page) * number_of_page), number_of_page+1))
			viewpoint_data = cursor.fetchall()
			if len(viewpoint_data) == 13:
				data_length = len(viewpoint_data)-1
			else:
				data_length = len(viewpoint_data)
			for i in range(data_length):
				# images = viewpoint_data[i][9]
				# image = images.split(",")
				data = {
						"id": viewpoint_data[i][0],
						"name": viewpoint_data[i][1],
						"category": viewpoint_data[i][2],
						"description": viewpoint_data[i][3],
						"address": viewpoint_data[i][4],
						"transport": viewpoint_data[i][5],
						"mrt": viewpoint_data[i][6],
						"lat": viewpoint_data[i][7],
						"lng": viewpoint_data[i][8],
						"images": [
							viewpoint_data[i][9]
							]
					}
				viewpoint.append(data)
		else :
			query = "select * from attraction where LOCATE(%s, name) OR category = %s limit %s, %s;"
			cursor.execute(query, (keyword, keyword, (int(page) * number_of_page), number_of_page+1))
			viewpoint_data = cursor.fetchall()
			if len(viewpoint_data) == 13:
				data_length = len(viewpoint_data)-1
			else:
				data_length = len(viewpoint_data)
			for i in range(data_length):
				# images = viewpoint_data[i][9]
				# image = images.split(",")
				data = {
					"id": viewpoint_data[i][0],
					"name": viewpoint_data[i][1],
					"category": viewpoint_data[i][2],
					"description": viewpoint_data[i][3],
					"address": viewpoint_data[i][4],
					"transport": viewpoint_data[i][5],
					"mrt": viewpoint_data[i][6],
					"lat": viewpoint_data[i][7],
					"lng": viewpoint_data[i][8],
					"images": [
						viewpoint_data[i][9]
						]
				}
				viewpoint.append(data)
		if len(viewpoint_data) <= 12:
			nextpage = None
		else: 
			nextpage = 1
		alldata = {
			"nextPage": nextpage,
			"data" : viewpoint
		}
		res = make_response(alldata, 200)
		return res
	except:
		data={
				"error": True,
				"message": "server error"
			}
		res = make_response(data, 500)
		return res
	finally:
		cursor.close()  
		cnx.close()


@app.route("/api/attraction/<id>")
def api_attraction_id(id):
	try:
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor()
		query = "select * from attraction where id = %s;"
		cursor.execute(query, (id,))
		viewpoint_data = cursor.fetchone()
		if viewpoint_data != None:
			# images = viewpoint_data[9]
			# image = images.split(",")
			data = {
				"data": [
					{
						"id": viewpoint_data[0],
						"name": viewpoint_data[1],
						"category": viewpoint_data[2],
						"description": viewpoint_data[3],
						"address": viewpoint_data[4],
						"transport": viewpoint_data[5],
						"mrt": viewpoint_data[6],
						"lat": viewpoint_data[7],
						"lng": viewpoint_data[8], 
						"images": [
							viewpoint_data[9]
						]
					}
				]
			}
						
			res = make_response(data, 200)
			return res
		else:
			data={
				"error": True,
				"message": "no such number"
			}
			res = make_response(data, 400)
			return res
	except:
		data={
				"error": True,
				"message": "server error"
			}
		res = make_response(data, 500)
		return res
	finally:
		cursor.close()  
		cnx.close()

@app.route("/api/categories")
def api_categories():
	try:
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor()
		query = "select category from attraction;"
		cursor.execute(query)
		allcat = cursor.fetchall()
		cat = []
		for i in set(allcat):
			cat.append(i[0])
		data = {
			"data":cat
		}
		res = make_response(jsonify(data), 200)
		return res
	except:
		data = {
			"error": True,
			"message": "server error"
		}
		res = make_response(jsonify(data), 500)
		return res
	finally:
		cursor.close()  
		cnx.close()

app.run("host=0.0.0.0", port=3000)
