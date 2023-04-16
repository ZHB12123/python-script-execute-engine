# coding:utf-8
from flask import Flask
from flask import jsonify
from flask import request

import sys
import os
import json
import multiprocessing
import traceback
import zipfile
import binascii
import time
from datetime import datetime

import run_script

from db.dao import ModulesDao

sys.path.append("../scripts")
sys.path.append("../modules")

ModulesDao.create_table()

app = Flask(__name__)


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


@app.route("/run_module", methods=["POST"])
def run_module():
    payload_dict = json.loads(request.data.decode("utf-8"))
    try:
        pass
    except Exception as e:
        pass


@app.route("/upload_module", methods=["POST"])
def upload_module():
    file_upload = request.files["file"]
    # 判断文件格式是否为.zip
    data = file_upload.stream.read(1024 * 1024 * 10 + 1)
    if len(data) > 1024 * 1024 * 10:
        return "上传的文件太大了！"

    if binascii.hexlify(data[:4]).upper() != b'504B0304':
        return "上传文件格式错误！"

    file_path = "../modules/" + file_upload.filename
    with open(file_path, "wb") as fd:
        fd.write(data)

    zip_file = zipfile.ZipFile(file_path)
    timestamp = int(time.time())
    for file in zip_file.namelist():
        zip_file.extract(file, f"../modules/{file_upload.filename}_{timestamp}")
    zip_file.close()

    os.remove(file_path)

    module_info = {
        "package_name": request.form["package_name"],
        "enter_func": request.form["enter_func"],
        "params": request.form["params"],
        "name": file_upload.filename,
        "upload_time": datetime.now()
    }
    ModulesDao.insert(module_info)

    return "upload success!"


@app.route("/query_all_modules", methods=["GET"])
def query_all_modules():
    return jsonify(ModulesDao.query_all())


if __name__ == '__main__':
    if os.name == "nt":
        multiprocessing.set_start_method("spawn")
    if os.name == "posix":
        multiprocessing.set_start_method("fork")

    app.config['JSON_AS_ASCII'] = False
    # 以调试模式启动,host=0.0.0.0 ,则可以使用127.0.0.1、localhost以及本机ip来访问
    app.run(host="0.0.0.0", port=8899, debug=False)
