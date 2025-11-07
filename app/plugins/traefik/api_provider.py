import json
import os
import requests
import re
import bcrypt

#todo input sanitization

def read(id=False): # GET
    if id == False or id == "":
        return {"text": "This is the API Endpoint for traefik, which implements the proxying for the screens. <br>Nothing else to do here. <br><br><a target=\"_blank\" href=\"/plugins/traefik/api_provider?id=api\">Open traefic Config</a>"}
    else:
        provider = {"http":{"routers": {},"services": {}, "middlewares": {}}}

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
        provider['http']['middlewares']['strip'] = {"stripPrefixRegex":{"regex":"/[a-z0-9_]+"} }

        mode_data = json.loads((requests.get('http://localhost:8080/plugins/mode/visitor_mode')).text)
        screen_data = json.loads((requests.get('http://localhost:8080/plugins/screens/manage_screen')).text)
        
        # add configured screens
        for screen in screen_data['table']:
            try:
                if len(mode_data['table']) > 0 and mode_data['table'][0]['is_enabled'] == 'true':
                    screen_host = 'http://ssp:8080'
                    screen_path = 'plugins/mode/visitor_mode?id=visitor_mode_image'
                else:
                    screen_host = re.match("^(https?://[^/]+)/(.*)$", screen['url']).groups()[0]
                    screen_path = re.match("^(https?://[^/]+)/(.*)$", screen['url']).groups()[1]

                provider['http']['routers']['router_'+screen['id']] = {'entryPoints':['web', 'websecure'], 'service':'service_'+screen['id'], 'rule':'HOST(`'+screen['id']+'.'+os.environ["SSP_DOMAIN"]+'`)', 'middlewares':['redirect_'+screen['id']], 'tls':{'certResolver':'myresolver'}}

                provider['http']['services']['service_'+screen['id']] = {"loadBalancer":{"servers":[{'url':screen_host}], "passHostHeader": False } }
                provider['http']['middlewares']['redirect_'+screen['id']] = {"redirectRegex":{"regex":"^(https?://[^/]+/?)$", "replacement":"${1}"+screen_path} }

                upstream_headers = {}
                raw_headers = screen.get('headers', '')
                if isinstance(raw_headers, str) and raw_headers.strip():
                    try:
                        parsed = json.loads(raw_headers)
                        if isinstance(parsed, dict):
                            upstream_headers = {str(k): str(v) for k, v in parsed.items() if v is not None}
                    except Exception:
                        pass

                if upstream_headers:
                    provider['http']['routers']['router_'+screen['id']]['middlewares'].append('header_'+screen['id'])
                    provider['http']['middlewares']['header_'+screen['id']] = {"headers": {"customRequestHeaders" : upstream_headers} }
            except:
                print("error parsing URL")

        return provider

