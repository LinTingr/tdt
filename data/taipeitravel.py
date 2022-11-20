import json
import mysql.connector

cnx = mysql.connector.connect(user='root', 
                              password='ragic08051228', 
                              host='127.0.0.1',
                              port=3306,
                              database='taipeitravel',
                              buffered= True,  
)

cursor = cnx.cursor()

path = 'taipei-attractions.json'

with open(path, encoding='UTF-8') as response:
    data = json.load(response)
# query = "INSERT into attraction(id) VALUES(%s);"
# print(data)
taipeilist = data["result"]["results"]
# print(taipeilist)
for i in taipeilist:
    query = "INSERT into attraction(id, name, category, description, address, transport, mrt, lat, lng, images) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    id = i["_id"]
    name = i["name"]
    category = i["CAT"]
    description = i["description"]
    address = i["address"]
    transport = i["direction"]
    mrt = i["MRT"]
    lat = i["latitude"]
    lng = i["longitude"]
    files = i["file"].split("https")
    images = []
    for j in files:
        if j.endswith("jpg")  or j[-3:] == "JPG":
            images.append("https" + j )
    images = ", ".join(images)
    cursor.execute(query, (id, name, category, description, address, transport, mrt, lat, lng, images))
    cnx.commit()
    # print(images)



cursor.close()  
cnx.close()