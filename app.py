import flask
import requests

app = flask.Flask(__name__)

controllers = {} #dict

@app.route('/api/controllers/<controller_id>/rpc/<path:sub_path>', methods = ['GET', 'POST'])
def rpc_request(controller_id: str, sub_path: str):
    
    if(controller_id in controllers.keys()):
        adress = controllers[controller_id]['address']
        response = requests.request(
            method=flask.request.method, 
            url=f'http://{adress}/{sub_path}',
            headers=flask.request.headers, 
            data=flask.request.data    
        )

    else: 
     return 'Invalid id'

    status = response.status_code
    data = response.content
    # headers = response.headers
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
    return 'Controller registered successfully'

@app.get('/api/controllers')
def get_list_controllers():  
    return {
        "controllers": list(controllers.values())  #refer postman
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 8082)