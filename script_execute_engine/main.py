# coding:utf-8
from flask import Flask
from flask import jsonify
from flask import request

import sys
import json
import importlib

sys.path.append("../scripts")
#

# 创建对象
app = Flask(__name__)


# 编写路由，构建url与函数的映射关系（将函数与url绑定）
@app.route("/execute", methods=["POST"])
def users():
    payload_dict = json.loads(request.data.decode("utf-8"))

    entrance_func_name = payload_dict.get("entrance_func")
    code = payload_dict.get("code")
    with open("../scripts/code_zhb.py", "w") as fd:
        fd.write(code)
    module = importlib.import_module("code_zhb")

    execute_func = getattr(module, entrance_func_name, None)
    execute_result = execute_func()
    return jsonify({"code": 10000, "message": "success", "result": execute_result})


if __name__ == '__main__':
    # 默认方式启动
    # app.run()
    # 解决jsonify中文乱码问题
    app.config['JSON_AS_ASCII'] = False
    # 以调试模式启动,host=0.0.0.0 ,则可以使用127.0.0.1、localhost以及本机ip来访问
    app.run(host="0.0.0.0", port=8899, debug=True)


'''
import requests
import json

url = "127.0.0.1:8899/execute"

payload = json.dumps({
  "entrance_func": "test_main",
  "code": "def test_main():\n    return \"adsada###3212313251dfasasd\""
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
'''
