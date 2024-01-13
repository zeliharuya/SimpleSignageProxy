import json
import os
import glob
#todo input sanitization

def read(id=False): # GET
    if id == False or id == "":
        return {"text": "This is the API Endpoint for traefik, <br>which implements the proxying for the screens. <br>Nothing else to do here. <br>To get the traefik config, use <br><br><a href=\"/plugins/traefik/api_provider?id=api\">THIS</a>"}
    else:
        return "asdf"
