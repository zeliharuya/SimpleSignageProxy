import json
import os
import glob
#todo input sanitization

def create(id): # POST
    os.system("mkdir -p /data/screens")
    configpath = "/data/screens/{}".format(id)
    if os.path.isfile(configpath) == True:
        return {"error":'Screen already exists'}

    else:
        f = open(configpath, "w+")
        content = {"id":id, "headers":"{}", "url":"https://example.com"}
        f.write(json.dumps(content))
        f.close()
        return {'ok':'Screen endpoint created'}

def read(id=False): # GET
    if id == False or id == "": # return all screens
        content = []
        for screen_id in glob.glob('/data/screens/*'):
            f = open(screen_id, "r")
            screen_content = f.read()
            f.close()
            content += [json.loads(screen_content)]
        return {'table':content}
    else: #return specific screen
        configpath = "/data/screens/{}".format(id)
        if os.path.isfile(configpath) == False:
            return {"error":'Screen does not exist'}

        else:
            f = open(configpath, "r")
            content = f.read()
            f.close()
            return {'form':json.loads(content)}

def update(id, headers, url): # POST
    configpath = "/data/screens/{}".format(id)
    if os.path.isfile(configpath) == False:
        return {"error":'Screen does not exist'}

    else:
        f = open(configpath, "w+")
        content = {"id":id, "headers":headers, "url":url}
        f.write(json.dumps(content))
        f.close()
        return {'ok':'Screen config updated'}

def delete(id):
    configpath = "/data/screens/{}".format(id)
    if os.path.isfile(configpath) == False:
        return {"error":'Screen does not exist'}

    else:
        os.unlink(configpath)
        return {'ok':'Screen endpoint deleted'}
