import flask
import requests

app = flask.Flask(__name__)

controllers = {} #dict

@app.route('/api/controllers/<controller_id:str>/rpc/<sub_path:path>')
def rpc_request(controller_id: str, sub_path: str):
    """
    send http request to controller

    1. get address of controller with id controllrt_id
    2. send request to said controller address containing
        - incoming request method
        - incoming headers
        - incoming subpath
        - incoming payload
    3. return controller response containing
        - response status code 
        - response data
        - response headers
    """
    adress = controllers[controller_id]['address']
    response = requests.request(
        method=flask.request.method, 
        url=f'{adress}/{sub_path}',
        headers=flask.request.headers, 
        data=flask.request.data    
    )

    status = response.status_code
    data = response.content
    headers = response.headers
   
    return flask.Response(
        status=status,
        data=data,
        headers=headers               
    )

@app.post('/api/register')
def register_controller():  
    data = flask.request.json 
    #store ip adress into data
    data['adress'] = flask.request.remote_addr 
    controllers[data['id']] = data

@app.get('/api/controllers')
def get_list_controllers():  
    return {
        "controllers": controllers.values()  #refer postman
    }
