from flask import Flask, request, jsonify, abort, Response
import json

app = Flask(__name__)


parts = [
    {'id' : 0,
     'manufacturer': 'AMD',
     'name': 'Ryzen 7 3800x',
     'type': 'CPU',
     'price': '331.90'
     },
    {'id': 1,
     'manufacturer': 'AMD',
     'name': 'Ryzen 5 3600',
     'type': 'CPU',
     'price': '181.00'
     },
    {'id': 2,
     'manufacturer': 'ASRock',
     'name': 'AB350 PRO4',
     'type': 'Motherboard',
     'price': '74.69'
     }
]

new_id = 3
#GET
#POST - Create/Add
#DELETE
#PUT - Update/Modify

@app.route('/')
def home():
    return "<h1>PC parts list</h1><a href='http://localhost:5000/api/parts'>All parts</a>"

@app.route('/api/parts', methods = ['GET', 'POST'])
def api_parts():
    if request.method == 'GET':
        if 'name' in request.args:
            temp_parts = []
            for part in parts:
                temp_parts.append({'id' : (part.get('id')), 'name': part.get('name')})
            return jsonify(temp_parts)
        return jsonify(parts)
    elif request.method == 'POST':
        if 'name' in request.args and 'manufacturer' in request.args and 'type' in request.args and 'price' in request.args and len(request.args) == 4:
            global new_id
            new_part = {
                'id': new_id,
                'manufacturer': request.args.get('manufacturer'),
                'name': request.args.get('name'),
                'type': request.args.get('type'),
                'price': request.args.get('price')
            }
            parts.append(new_part)
            new_id+=1
            return Response('Part was added to http://localhost:5000/api/parts/'+str(new_id-1),status=201)
        else:
            abort(400)
    else:
        abort(404)


@app.route('/api/parts/<int:part_id>', methods = ['GET', 'DELETE', 'PUT'])
def api_part_id(part_id):
    part = [part for part in parts if part['id'] == part_id]
    if len(part) == 0:
        abort(404)
    
    if request.method == 'GET':
        return jsonify(part)

    elif request.method == 'DELETE':
        for party in parts:
            if party['id'] == part_id:
                parts.remove(party)
                return Response(json.dumps({'Success' : 'Deleted'}),status=204, mimetype='application/json')
    
    elif request.method == 'PUT':
        if 'name' in request.args:
            part[0]['name'] = request.args.get('name')
            return Response(json.dumps({'Success' : 'name has been changed'}), status=201,mimetype='application/json')
        if 'manufacturer' in request.args:
            part[0]['manufacturer'] = request.args.get('manufacturer')
            return Response(json.dumps({'Success' : 'manufacturer has been changed'}), status=201,mimetype='application/json')
        if 'type' in request.args:
            part[0]['type'] = request.args.get('type')
            return Response(json.dumps({'Success' : 'type has been changed'}), status=201,mimetype='application/json')
        if 'price' in request.args:
            part[0]['price'] = request.args.get('price')
            return Response(json.dumps({'Success' : 'price has been changed'}), status=201,mimetype='application/json')
        else:
            abort(400)
        
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
