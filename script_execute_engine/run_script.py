import importlib
import sys
import os
import uuid

import builtins

original_lib_paths = sys.path.copy()
original_lib_paths.remove(os.getcwd())

user_log = ""


def print_new(*args):
    global user_log
    for arg in args:
        user_log += str(arg)+"\n"


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


def run(payload_dict, conn):
    # 如果要替换builtins里面的函数应该这么换
    builtins.print = print_new
    entrance_func_name = payload_dict.get("entrance_func")
    code = payload_dict.get("code")

    code_file_name = f"c0dE_{str(uuid.uuid1())}"

    with open(f"../scripts/{code_file_name}.py", "w") as fd:
        fd.write(code)
    try:
        module, new_import_modules = load_module(code_file_name)

        execute_func = getattr(module, entrance_func_name, None)
        execute_result = execute_func()

        conn.send({"result": execute_result, "new_modules": new_import_modules, "log": user_log})
    except Exception as e:
        conn.send({"result": str(e), "new_modules": [], "log": user_log})
    finally:
        if os.path.exists(f"../scripts/{code_file_name}.py"):
            os.remove(f"../scripts/{code_file_name}.py")
        if os.path.exists(f"../scripts/__pycache__/{code_file_name}.cpython-37.pyc"):
            os.remove(f"../scripts/__pycache__/{code_file_name}.cpython-37.pyc")
