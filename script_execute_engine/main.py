# coding:utf-8
from flask import Flask
from flask import jsonify
from flask import request

import sys
import json
import multiprocessing
import traceback
import zipfile
import binascii
import time

import run_script

sys.path.append("../scripts")
sys.path.append("../modules")

app = Flask(__name__)

type_dict = {
    b'424D': 'bmp',
    b'FFD8FF': 'jpg',
    b'2E524D46': 'rm',
    b'4D546864': 'mid',
    b'89504E47': 'png',
    b'47494638': 'gif',
    b'49492A00': 'tif',
    b'41433130': 'dwg',
    b'38425053': 'psd',
    b'2142444E': 'pst',
    b'FF575043': 'wpd',
    b'AC9EBD8F': 'qdf',
    b'E3828596': 'pwl',
    b'504B0304': 'zip',
    b'52617221': 'rar',
    b'57415645': 'wav',
    b'41564920': 'avi',
    b'2E7261FD': 'ram',
    b'000001BA': 'mpg',
    b'000001B3': 'mpg',
    b'6D6F6F76': 'mov',
    b'7B5C727466': 'rtf',
    b'3C3F786D6C': 'xml',
    b'68746D6C3E': 'html',
    b'D0CF11E0': 'doc/xls',
    b'255044462D312E': 'pdf',
    b'CFAD12FEC5FD746F': 'dbx',
    b'3026B2758E66CF11': 'asf',
    b'5374616E64617264204A': 'mdb',
    b'252150532D41646F6265': 'ps/eps',
    b'44656C69766572792D646174653A': 'eml'
}

@app.route("/execute", methods=["POST"])
def execute():
    payload_dict = json.loads(request.data.decode("utf-8"))
    try:
        parent_conn, child_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(target=run_script.run, args=(payload_dict, child_conn,))
        p.start()
        result = parent_conn.recv()
        execute_result = result.get("result")
        new_modules = result.get("new_modules")
        for module_name in new_modules:
            try:
                m = __import__(module_name)
                globals()[module_name] = m
            except Exception as e:
                pass
        p.terminate()
        p.kill()
        p.join()

        return jsonify({"code": 0, "message": "success", "result": execute_result})
    except Exception as e:
        return jsonify({"code": 1, "message": "fail", "result": traceback.format_exc()})

@app.route("/upload_module",methods=["POST"])
def upload_module():
    file_upload=request.files["file"]
    # 判断文件格式是否为.zip
    data=file_upload.stream.read(1024*1024*10+1)
    if len(data)>1024*1024*10:
        return "上传的文件太大了！"
    
    if binascii.hexlify(data[:4]).upper()!=b'504B0304':
        return "上传文件格式错误！"
    
    file_path = "../modules/"+file_upload.filename
    with open(file_path,"wb") as fd:
        fd.write(data)

    zip_file=zipfile.ZipFile(file_path)
    timestamp=int(time.time())
    for file in zip_file.namelist():
        zip_file.extract(file,f"../modules/{file_upload.filename}_{timestamp}")
    zip_file.close()

    return "upload success!"

if __name__ == '__main__':
    # 默认方式启动
    # app.run()
    # 解决jsonify中文乱码问题
    # multiprocessing.set_start_method("fork")

    app.config['JSON_AS_ASCII'] = False
    # 以调试模式启动,host=0.0.0.0 ,则可以使用127.0.0.1、localhost以及本机ip来访问
    app.run(host="0.0.0.0", port=8899, debug=False)
