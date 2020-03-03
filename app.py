from flask import Flask, request, jsonify, abort, Response

app = Flask(__name__)


parts = [
    {'id' : 0,
     'manufacturer': 'AMD',
     'name': 'Ryzen 7 3800x',
     'type': 'CPU'
     },
    {'id': 1,
     'manufacturer': 'AMD',
     'name': 'Ryzen 5 3600',
     'type': 'CPU'
     },
    {'id': 2,
     'manufacturer': 'ASRock',
     'name': 'AB350M PRO4',
     'type': 'Motherboard'
     }
]

new_id = 3
#GET
#POST - Create/Add
#DELETE
#PUT - Update/Modify

@app.route('/')
def home():
    return "<h1>PC parts list</h1>"

@app.route('/api/parts', methods = ['GET', 'POST'])
def api_parts():
    if request.method == 'GET':
        if 'name' in request.args:
            temp_parts = []
            for part in parts:
                temp_parts.append({'id' : (part.get('id')), 'name': part.get('name')})
            return jsonify(temp_parts)
        return jsonify(parts)
    if request.method == 'POST':
        if 'name' in request.args and 'manufacturer' in request.args and 'type' in request.args and len(request.args) == 3:
            global new_id
            new_part = {
                'id': new_id,
                'manufacturer': request.args.get('manufacturer'),
                'name': request.args.get('name'),
                'type': request.args.get('type')
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
                return Response(status=204)
    
    elif request.method == 'PUT':
        if 'name' in request.args:
            part[0]['name'] = request.args.get('name')
            return Response(status=201)
        if 'manufacturer' in request.args:
            part[0]['manufacturer'] = request.args.get('manufacturer')
            return Response(status=201)
        if 'type' in request.args:
            part[0]['type'] = request.args.get('type')
            return Response(status=201)
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
