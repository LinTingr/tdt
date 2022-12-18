from flask import *
from model.taipeidb import cnxpool
 
attraction = Blueprint("attraction", __name__, static_folder="static", static_url_path="/")

def push_data(viewpoint_data, viewpoint):
	if len(viewpoint_data) == 13:
		data_length = len(viewpoint_data)-1
	else:
		data_length = len(viewpoint_data)
	for i in range(data_length):
		images = viewpoint_data[i][9]
		image = images.split(", ")
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
				"images": image
			}
		viewpoint.append(data)

@attraction.route("/api/attractions")
def api_attractions():
	try:
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor()
		page = request.args.get("page", 0)
		number_of_page = 12
		keyword = request.args.get("keyword", None)
		viewpoint = []

		if keyword == None:
			query = "select * from attraction limit %s, %s;"
			cursor.execute(query, ((int(page) * number_of_page), number_of_page+1))
			viewpoint_data = cursor.fetchall()
			push_data(viewpoint_data, viewpoint)
		else :
			query = "select * from attraction where LOCATE(%s, name)>0 OR category = %s limit %s, %s;"
			cursor.execute(query, (keyword, keyword, (int(page) * number_of_page), number_of_page+1))
			viewpoint_data = cursor.fetchall()
			push_data(viewpoint_data, viewpoint)
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


@attraction.route("/api/attraction/<id>")
def api_attraction_id(id):
	try:
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor()
		query = "select * from attraction where id = %s;"
		cursor.execute(query, (id,))
		viewpoint_data = cursor.fetchone()
		if viewpoint_data != None:
			images = viewpoint_data[9]
			image = images.split(", ")
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
						"images": image
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
