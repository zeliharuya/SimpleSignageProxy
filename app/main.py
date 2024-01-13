from flask import Flask, request, render_template, redirect
import glob
import json
import sys
import importlib
import os

app = Flask(__name__)




# Setup redirect and hosting of frontend

@app.route('/')
def base():
    return render_template('index.html')

@app.route('/plugins')
def list_plugins():
    plugin_dirs = [i.split('/')[-2] for i in glob.glob("/app/plugins/*/", recursive=False)]
    return json.dumps(plugin_dirs)

@app.route('/plugins/<path:plugin>')
def list_plugin_features(plugin):
    feature_files = [i.split('/')[-1].split('.')[-2] for i in glob.glob("/app/plugins/{}/*.py".format(plugin), recursive=False)]
    return json.dumps(feature_files)

@app.route('/plugins/<path:plugin>/<path:feature>', methods = ['POST','GET','PUT','DELETE'])
def exec_feature(plugin,feature):
#    data=request.args.get('data')
    mod = importlib.import_module('plugins.{}.{}'.format(plugin,feature))

    if request.method == 'POST' and hasattr(mod, "create"):
        data=request.args.to_dict()
        return mod.create(**data)

    elif request.method == 'GET' and hasattr(mod, "read"):
        data=request.args.to_dict()
        return mod.read(**data)

    elif request.method == 'PUT' and hasattr(mod, "update"):
        data=request.args.to_dict()
        return mod.update(**data)

    elif request.method == 'DELETE' and hasattr(mod, "delete"):
        data=request.args.to_dict()
        return mod.delete(**data)

    else:
        return "Invalid Request"


@app.route('/swagger')
def swagger():
    return redirect("static/swagger/index.html", code=302)

@app.route('/swagger.json')
def swaggerjson():
    swagger_json = {"swagger":"2.0","info":None,"host":None,"basePath":None,"tags":None,"schemes":None,"paths":None,"securityDefinitions":{"api_key":{"type": "apiKey","name": "api_key","in": "header"}},"definitions":{"response": {"type": "object", "properties":{"raw":{"type": "object"},"pretty":{"type": "object"}}}},"externalDocs":{"description":"github","url":os.environ['DOC_PROJECT_URL']}}
    swagger_json["info"] = {"description": "undefined", "version": "undefined", "title": os.environ['DOC_PROJECT_NAME']}
    swagger_json["host"] = "localhost:8080"
    swagger_json["basePath"] = "/plugins"
    swagger_json["tags"] = [{"name":i} for i in [i.split('/')[-2] for i in glob.glob("/app/plugins/*/", recursive=False)]]
    swagger_json["schemes"] = ["http", "https"]
    swagger_json["paths"] = {}
    for plugin in [i.split('/')[-2] for i in glob.glob("/app/plugins/*/", recursive=False)]:
        for feature in [i.split('/')[-1].split('.')[-2] for i in glob.glob("/app/plugins/{}/*.py".format(plugin), recursive=False)]:
            mod = importlib.import_module('plugins.{}.{}'.format(plugin,feature))
            paths = {}            
            if hasattr(mod, "create"):
                params = [{"name":i, "in":"query", "type":"string"} for i in mod.create.__code__.co_varnames[:mod.create.__code__.co_argcount]]
                paths["post"] = {"tags":[plugin], "parameters":params, "responses":{'200':{"description":"API Call succeded", "schema":{"$ref": "#/definitions/response"}}}}

            if hasattr(mod, "read"):
                params = [{"name":i, "in":"query", "type":"string"} for i in mod.read.__code__.co_varnames[:mod.read.__code__.co_argcount]]
                paths["get"] = {"tags":[plugin], "parameters":params, "responses":{'200':{"description":"API Call succeded", "schema":{"$ref": "#/definitions/response"}}}}

            if hasattr(mod, "update"):
                params = [{"name":i, "in":"query", "type":"string"} for i in mod.update.__code__.co_varnames[:mod.update.__code__.co_argcount]]
                paths["put"] = {"tags":[plugin], "parameters":params, "responses":{'200':{"description":"API Call succeded", "schema":{"$ref": "#/definitions/response"}}}}

            if hasattr(mod, "delete"):
                params = [{"name":i, "in":"query", "type":"string"} for i in mod.delete.__code__.co_varnames[:mod.delete.__code__.co_argcount]]
                paths["delete"] = {"tags":[plugin], "parameters":params, "responses":{'200':{"description":"API Call succeded", "schema":{"$ref": "#/definitions/response"}}}}

            swagger_json["paths"]["/{}/{}".format(plugin,feature)] = paths
    return swagger_json



if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, host="0.0.0.0")
