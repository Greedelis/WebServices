from flask import Flask, request, jsonify, abort, Response
import json
import requests 
app = Flask(__name__)

URL = "http://arnweb:5000/"

parts = [
    {"id" : 0,
     "manufacturer": "AMD",
     "name": "Ryzen 7 3800x",
     "type": "CPU",
     "price": "331.90",
     "phone_id" : "1"
     },
    {"id": 1,
     "manufacturer": "AMD",
     "name": "Ryzen 5 3600",
     "type": "CPU",
     "price": "181.00",
     "phone_id" : "2"
     },
    {"id": 2,
     "manufacturer": "ASRock",
     "name": "AB350 PRO4",
     "type": "Motherboard",
     "price": "74.69",
     "phone_id" : "4"
     }
]

new_id = 3
#GET
#POST - Create/Add
#DELETE
#PUT - Update/Modify

@app.route("/")
def home():
    return "<h1>PC parts list</h1><a href='http://localhost:5000/api/parts'>All parts</a>"



@app.route("/api/parts", methods = ["GET", "POST"])
def api_parts():
    if request.method == "GET":
        if "name" in request.args:
            temp_parts = []
            for part in parts:
                temp_parts.append({"id" : (part.get("id")), "name": part.get("name")})
            return jsonify(temp_parts)
        return jsonify(parts)

    elif request.method == "POST":
        new_data = request.get_json("force=True")
        if "name" in new_data and "manufacturer" in new_data and "type" in new_data and "price" in new_data and "phone_id" in new_data:
            global new_id
            new_part = {
                "id": new_id,
                "manufacturer": new_data["manufacturer"],
                "name": new_data["name"],
                "type": new_data["type"],
                "price": new_data["price"],
                "phone_id": new_data["phone_id"]
            }
            parts.append(new_part)
            new_id+=1
            return Response(response=(json.dumps({"Success":"Part was added"})), status=201, headers={"location": "/api/parts/"+str(new_id-1)}, mimetype="application/json")
        else:
            error_msg = "no "
            if "name" not in new_data:
                error_msg += "name "
            if "manufacturer" not in new_data:
                error_msg += "manufacturer "
            if "type" not in new_data:
                error_msg += "type "
            if "price" not in new_data:
                error_msg += "price "
            if "phone_id" not in new_data:
                error_msg += "phone_id "
            error_msg += "have been declared"

            return Response(json.dumps({"Failure" : error_msg}),status=400,mimetype="application/json")
    else:
        abort(404)

@app.route("/api/test", methods = ["GET", "DELETE", "PUT"])
def test():
    res = (requests.get(URL+"phones"))
    return jsonify(res.json())

@app.route("/api/parts/<int:part_id>", methods = ["GET", "DELETE", "PUT"])
def api_part_id(part_id):
    part = [part for part in parts if part["id"] == part_id]
    if len(part) == 0:
        abort(404)
    
    if request.method == "GET":
        return jsonify(part)

    elif request.method == "DELETE":
        for party in parts:
            if party["id"] == part_id:
                parts.remove(party)
                return Response(json.dumps({"Success" : "Deleted"}),status=204, mimetype="application/json")
    
    elif request.method == "PUT":
        new_data = request.get_json("force=True")
        response = ""
        if "name" in new_data:
            part[0]["name"] = new_data["name"]
            response += "name "
        if "manufacturer" in new_data:
            part[0]["manufacturer"] = new_data["manufacturer"]
            response += "manufacturer "
        if "type" in new_data:
            part[0]["type"] = new_data["type"]
            response += "type "
        if "price" in new_data:
            part[0]["price"] = new_data["price"]
            response += "price "
        if "phone_id" in new_data:
            part[0]["phone_id"] = new_data["phone_id"]
            response += "phone_id "
        response += "have been changed"
       

        if "name" not in new_data and "manufacturer" not in new_data and "type" not in new_data and "price" not in new_data and "phone_id" not in new_data:
            return Response(json.dumps({"Failed" : "no "}))

        return Response(json.dumps(part),status=200, mimetype="application/json")

@app.route("/api/phones", methods = ["GET", "POST"])
def api_phones():
    if request.method == "GET":  
        req = requests.get(URL + "phones/")
        return jsonify(req.json())
    elif request.method == "POST":
        new_data = request.get_json("force=True")
        resp = requests.post(URL+"phones", json = (new_data), )
        #return new_data
        if str(resp.status_code) == "400" or str(resp.status_code) == "404":
            return Response(json.dumps({"Failure" : resp.text}),status=resp.status_code,mimetype="application/json")
        else:
             return Response(json.dumps({"Success" : resp.text}),status=resp.status_code,mimetype="application/json")

@app.route("/api/parts/<int:part_id>/phone", methods = ["GET"])
def api_phone_info(part_id):
    part = [part for part in parts if part["id"] == part_id]
    if len(part) == 0:
        abort(404)
    
    if request.method == "GET":
        req = requests.get(URL+"phones/"+str(part[0]["phone_id"]))
        #print (part[0]["phone_id"])
        return jsonify(req.json())

        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
