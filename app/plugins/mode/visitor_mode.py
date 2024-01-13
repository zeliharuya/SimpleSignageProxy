import json
import os
#todo input sanitization

def create(id): # POST
    os.system("mkdir -p /data/modes")
    configpath = "/data/modes/visitormode"
    if os.path.isfile(configpath) == True:
        return {"error":'Visitormode already exists'}

    else:
        f = open(configpath, "w+")
        content = {"id":"visitormode", "enabled":False}
        f.write(json.dumps(content))
        f.close()
        return {'ok':'Visitor Mode Created'}

def read(id=False): # GET
    configpath = "/data/modes/visitormode"
    if os.path.isfile(configpath) == False:
        create('visitormode')
    if id == False or id == "":
        content = []
        f = open(configpath, "r")
        mode_content = f.read()
        f.close()
        content += [json.loads(mode_content)]
        return {'table':content}

    else: #return specific mode
        configpath = "/data/modes/visitormode"
        if os.path.isfile(configpath) == False:
            return {"error":'Mode does not exist'}

        else:
            f = open(configpath, "r")
            content = f.read()
            f.close()
            return {'form':json.loads(content)}

def update(id, enabled): # POST
    configpath = "/data/modes/visitormode"
    if os.path.isfile(configpath) == False:
        return {"error":'Mode does not exist'}

    else:
        f = open(configpath, "w+")
        content = {"id":"visitormode", "enabled":enabled}
        f.write(json.dumps(content))
        f.close()
        return {'ok':'Mode config updated'}

def delete(id):
    configpath = "/data/modes/visitormode"
    if os.path.isfile(configpath) == False:
        return {"error":'Mode does not exist'}

    else:
        os.unlink(configpath)
        return {'ok':'Mode endpoint deleted'}
