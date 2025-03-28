from flask import Flask, request,json
from flask_cors import CORS, cross_origin
import imgtopath as itp


app = Flask(__name__)

@app.after_request
def cors(environ):#解决跨域问题
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ

#@cross_origin(origins='*', methods=['POST'])

@app.route('/')
def hello(): #just for test
    data='This is Python'
    return data

@app.route('/getImg',methods=['POST'])
def getImg():
    print('getImg...')
    data = request.get_json()
    url = data['img']
    # url=request.form['img']
    #print(f'url:{url}')
    contour_url,cnt_num=itp.get_light_contour(url)
    datadic={'url':contour_url,'piece':cnt_num}
    jsonData=json.dumps(datadic)
    return jsonData

@app.route('/getPath',methods=['GET'])
def getPath():
    return json.dumps(itp.contour_to_path())

@app.route('/makeAdjacencyMatrix',methods=['GET'])
def getAM():
    print('getAM...')
    return json.dumps(itp.compute_adjacency_matrix())

@app.route('/AntOptimize',methods=['GET'])
def getOptimizedEulerLoop():
    print('antseek')
    return json.dumps(itp.antseek())

@app.route('/fftResult',methods=['GET'])
def getFftResult():
    print('fft')
    return json.dumps(itp.optim_and_fft())

@app.route('/resample',methods=['POST'])
def resamplefft():
    print('refft')
    data = request.get_json()
    downrate = data['downrate']
    print(f'Downrate:{downrate}')
    # downrate=request.form['downrate']
    return json.dumps({'result':itp.path_fft(downrate).tolist()})

if __name__ == '__main__':
   app.run()
   CORS(app) 