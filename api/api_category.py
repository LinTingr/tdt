from flask import *
from api.taipeidb import cnxpool, category_query

category = Blueprint('category', __name__, static_folder="static", static_url_path="/")

@category.route("/api/categories")
def api_categories():
	try:
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor()
		cursor.execute(category_query)
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