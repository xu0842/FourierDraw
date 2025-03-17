from flask import Flask, request

app = Flask(__name__)

@app.after_request
def cors(environ):#解决跨域问题
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ

@app.route('/api/endpoint', methods=['POST'])
def endpoint():
    data = request.get_json()
    print(f'data:{data}')
    return {'message': 'Received data: {}'.format(data)}

if __name__ == '__main__':
    app.run()
