import json
import os

#todo input sanitization

def create(name): # POST
    configpath = "/data/{}".format(name)
    if os.path.isfile(configpath) == True:
        return {"error":'Screen already exists'}

    else:
        f = open(configpath, "w+")
        content = {"name":name, "headers":{}, "url":"https://example.com"}
        f.write(json.dumps(content))
        return {'raw':'Screen endpoint created', 'pretty':''}

def read(name): # GET
    configpath = "/data/{}".format(name)
    if os.path.isfile(configpath) == False:
        return {"error":'Screen does not exist'}

    else:
        f = open(configpath, "r")
        content = f.read()
        return {'raw':json.dumps(content), 'pretty':''}

def update(name, headers, url): # PUT
    return name
    response = {"error":'not implemented'}
    return response

def delete(name):
    configpath = "/data/{}".format(name)
    if os.path.isfile(configpath) == False:
        return {"error":'Screen does not exist'}

    else:
        os.unlink(configpath)
        return {'raw':'Screen endpoint deleted', 'pretty':''}
