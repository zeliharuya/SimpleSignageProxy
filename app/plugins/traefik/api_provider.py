import json
import os
import requests



#todo input sanitization

def read(id=False): # GET
    if id == False or id == "":
        return {"text": "This is the API Endpoint for traefik, <br>which implements the proxying for the screens. <br>Nothing else to do here. <br>To get the traefik config, use <br><br><a href=\"/plugins/traefik/api_provider?id=api\">THIS</a>"}
    else:
        provider = {"http":{"routers":{},"services":{}, "middlewares":{}}}

        r = requests.get('http://localhost:8080/plugins/screens/manage_screen')
        data = json.loads(r.text)

        # add ssp admin panel
        provider['http']['routers']['admin']={'entryPoints':['web', 'websecure'], 'service':'admin', 'rule':'PathPrefix(`/admin`)', 'middlewares':["chain"]}
        provider['http']['services']['admin']={"loadBalancer":{"servers":[{'url':"http://ssp:8080"}] } }

        provider['http']['middlewares']['chain']={"chain":{"middlewares":["redirect", "strip"]} }
        provider['http']['middlewares']['redirect']={"redirectregex":{"regex":"^(https?://[^/]+/[a-z0-9_]+)$", "replacement":"${1}/"} }
        provider['http']['middlewares']['strip']={"stripprefixregex":{"regex":"/[a-z0-9_]+"} }


        # add configured screens
        for screen in data['table']:
            provider['http']['routers']['router_'+screen['id']]={'entryPoints':['web', 'websecure'], 'service':'service_'+screen['id'], 'rule':'PathPrefix(`/'+screen['id']+'`)', 'middlewares':['chain']}
            provider['http']['services']['service_'+screen['id']]={"loadBalancer":{"servers":[{'url':screen['url']}], "passHostHeader": False } }

        return provider
