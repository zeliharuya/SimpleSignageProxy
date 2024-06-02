import json
import os
import requests
import re
import bcrypt

#todo input sanitization

def read(id=False): # GET
    if id == False or id == "":
        return {"text": "This is the API Endpoint for traefik, <br>which implements the proxying for the screens. <br>Nothing else to do here. <br>To get the traefik config, use <br><br><a href=\"/plugins/traefik/api_provider?id=api\">THIS</a>"}
    else:
        provider = {"http":{"routers": {},"services": {}, "middlewares": {}}}

        r = requests.get('http://localhost:8080/plugins/screens/manage_screen')
        data = json.loads(r.text)

        # add ssp admin panel
        provider['http']['routers']['admin'] = {'entryPoints': ['web', 'websecure'], 'service': 'admin', 'rule': 'HOST(`'+os.environ['SSP_DOMAIN']+'`)', 'tls': {'certResolver': 'myresolver'}, 'middlewares': ['ssp-auth']}
        provider['http']['services']['admin'] = {'loadBalancer': {"servers": [ {'url': 'http://ssp:8080'} ] } }

        # add ssp HTTP Basic Auth
        salt = bcrypt.gensalt()
        basicauth_password = bcrypt.hashpw(os.environ['SSP_PASSWORD'].encode('utf-8'), salt)

        provider['http']['middlewares']['ssp-auth'] = {
            'basicAuth': {
                'users': [ os.environ['SSP_USERNAME'] + ":" + basicauth_password.decode() ]
            }
        }

        # provider['http']['middlewares']['chain']={"chain":{"middlewares":["redirect", "strip"]} }
        # provider['http']['middlewares']['redirect']={"redirectregex":{"regex":"^(https?://[^/]+/[a-z0-9_]+)$", "replacement":"${1}/"} }
        provider['http']['middlewares']['strip'] = {"stripprefixregex":{"regex":"/[a-z0-9_]+"} }

#^(https?://[^/]+/?)$
        # add configured screens
        for screen in data['table']:
            try:
                screen_host = re.match("^(https?://[^/]+)/(.*)$", screen['url']).groups()[0]
                screen_path = re.match("^(https?://[^/]+)/(.*)$", screen['url']).groups()[1]

                provider['http']['routers']['router_'+screen['id']] = {'entryPoints':['web', 'websecure'], 'service':'service_'+screen['id'], 'rule':'HOST(`'+screen['id']+'.'+os.environ["SSP_DOMAIN"]+'`)', 'middlewares':['service_'+screen['id']], 'tls':{'certResolver':'myresolver'}}
                provider['http']['services']['service_'+screen['id']] = {"loadBalancer":{"servers":[{'url':screen_host}], "passHostHeader": False } }
                provider['http']['middlewares']['service_'+screen['id']] = {"redirectregex":{"regex":"^(https?://[^/]+/?)$", "replacement":"${1}"+screen_path} }
            except:
                print("error parsing URL")

        return provider
