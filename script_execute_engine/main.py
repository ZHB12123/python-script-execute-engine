# coding:utf-8
from flask import Flask
from flask import jsonify
from flask import request

import sys
import json
import importlib
import multiprocessing

import traceback
import uuid
import os

original_lib_paths = sys.path.copy()
original_lib_paths.remove(os.getcwd())

sys.path.append("../scripts")
#

# 创建对象
app = Flask(__name__)


def load_module(module_name):
    before_load_modules = set(sys.modules.keys())
    run_module = importlib.import_module(module_name)
    after_load_modules = set(sys.modules.keys())

    # 把新引入的三方库通知主进程
    new_import_modules = []
    for module_key in after_load_modules - before_load_modules:
        module = sys.modules.get(module_key)
        if not module:
            continue
        try:
            for original_lib_path in original_lib_paths:
                if original_lib_path in module.__file__:
                    new_import_modules.append(module_key)
        except Exception as e:
            new_import_modules.append(module_key)

    return run_module, new_import_modules


def run_script(payload_dict, conn):
    entrance_func_name = payload_dict.get("entrance_func")
    code = payload_dict.get("code")

    code_file_name = f"c0dE_{str(uuid.uuid1())}"

    with open(f"../scripts/{code_file_name}.py", "w") as fd:
        fd.write(code)
    try:
        module, new_import_modules = load_module(code_file_name)

        execute_func = getattr(module, entrance_func_name, None)
        execute_result = execute_func()

        conn.send({"result": execute_result, "new_modules": new_import_modules})
    except Exception as e:
        conn.send({"result": str(e), "new_modules": []})
    finally:
        if os.path.exists(f"../scripts/{code_file_name}.py"):
            os.remove(f"../scripts/{code_file_name}.py")
        if os.path.exists(f"../scripts/__pycache__/{code_file_name}.cpython-37.pyc"):
            os.remove(f"../scripts/__pycache__/{code_file_name}.cpython-37.pyc")


# 编写路由，构建url与函数的映射关系（将函数与url绑定）
@app.route("/execute", methods=["POST"])
def users():
    payload_dict = json.loads(request.data.decode("utf-8"))
    try:
        parent_conn, child_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(target=run_script, args=(payload_dict, child_conn,))
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


if __name__ == '__main__':
    # 默认方式启动
    # app.run()
    # 解决jsonify中文乱码问题
    multiprocessing.set_start_method("fork")

    app.config['JSON_AS_ASCII'] = False
    # 以调试模式启动,host=0.0.0.0 ,则可以使用127.0.0.1、localhost以及本机ip来访问
    app.run(host="0.0.0.0", port=8899, debug=False)
