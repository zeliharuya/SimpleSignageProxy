import base64
import json
import os
#todo input sanitization

def create(id): # POST
    os.system("mkdir -p /data/modes")
    configpath = "/data/modes/visitormode"
    if os.path.isfile(configpath) == True:
        return {"error":'Visitormode already exists'}

    else:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Construct the full path to the image file
        sample_image_path = os.path.join(script_dir, "visitor_mode_sample.png")
        
        with open(sample_image_path, "rb") as image_file:
            encoded_sample_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        f = open(configpath, "w+")
        content = {"id":"visitormode", "is_enabled":False, "base64_placeholder_image": encoded_sample_image}
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

    elif id == "visitor_mode_image":
        return '<html><body style="margin: 0px; height: 100vh; background-position: center; background-size: contain; background-color: black; background-image: url(data:image/png;base64,' + json.loads(open(configpath, "r").read())['base64_placeholder_image'] + '"></body></html>'

    else: #return specific mode
        configpath = "/data/modes/visitormode"
        if os.path.isfile(configpath) == False:
            return {"error":'Mode does not exist'}

        else:
            f = open(configpath, "r")
            content = f.read()
            f.close()
            return {'form':json.loads(content)}

def update(id, is_enabled, base64_placeholder_image): # POST
    configpath = "/data/modes/visitormode"
    if os.path.isfile(configpath) == False:
        return {"error":'Mode does not exist'}

    else:
        f = open(configpath, "w+")
        content = {"id":"visitormode", "is_enabled":is_enabled, "base64_placeholder_image": base64_placeholder_image}
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
