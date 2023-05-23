import flask
import requests

app = flask.Flask(__name__)

controllers = {} #dict

@app.route('/api/controllers/<controller_id>/rpc/<path:sub_path>', methods = ['GET', 'POST'])
def rpc_request(controller_id: str, sub_path: str):
    
    if controller_id not in controllers.keys():
        return 'Invalid id', 404

     
    adress = controllers[controller_id]['address']
    response = requests.request(
        method=flask.request.method, 
        url=f'http://{adress}/{sub_path}',
        headers=flask.request.headers, 
        data=flask.request.data    
    )

    status = response.status_code
    data = response.content
    headers = dict(response.headers)

    return flask.Response(
        status=status,
        response=data,
        headers=headers               
    )
    
@app.post('/api/register')
def register_controller():  
    data = flask.request.json 
    #store ip adress into data
    data['address'] = flask.request.remote_addr 
    controllers[data['id']] = data
    # print(controllers)
    return 'Controller registered successfully', 201

@app.get('/api/controllers')
def get_list_controllers():  
    return {
        "controllers": list(controllers.values())  #refer postman
    }