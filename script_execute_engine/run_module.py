import importlib
import json
import sys
import os
import uuid

from db.dao import ModulesDao

original_lib_paths = sys.path.copy()
original_lib_paths.remove(os.getcwd())


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
    run_info = ModulesDao.query_by_id(payload_dict.get("id"))

    package_name = run_info.get("package_name")
    enter_func = run_info.get("enter_func")
    params = run_info.get("params")
    package_path = run_info.get("package_path")

    try:
        sys.path.append(f"../modules/{package_path}")
        module, new_import_modules = load_module(package_name)

        execute_func = getattr(module, enter_func, None)

        kwargs = json.loads(params)
        execute_result = execute_func(**kwargs)
        conn.send({"result": execute_result, "new_modules": new_import_modules})
    except Exception as e:
        conn.send({"result": str(e), "new_modules": []})
