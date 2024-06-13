# SimpleSignageProxy

This project creates a simple management interface, which allows to dynamically generate proxies (on subdomains) for Traefik. It is intended for a simple digital signage solution, in order to create a central management interface for all screens.

A screen is setup as a (e.g. Raspberry Pi) endpoint device running a browser in kiosk mode. This browser displays the URL https://<screen_id>.<domain>/

The <screen_id> can be setup through the management interface, located at <domain>. This <domain> can be configured using the SSP_DOMAIN environment variable located in the environment file.

Clone the example environment file with:
```
cp example.env .env
```

# Installation
Use the following docker-compose.yml file for installation. Adjust the example.env and save it to .env (the one in the repo is for development purposes)
```
services:
  ssp:
    image: tttttx2/simplesignageproxy:main
    restart:
      always
    volumes:
      - ./data:/data
    environment:
      - SSP_USERNAME=${SSP_USERNAME}
      - SSP_DOMAIN=${SSP_DOMAIN}
      - SSP_PASSWORD=${SSP_PASSWORD}

  traefik:
    image: "traefik:v2.10"
    restart:
      always
    volumes:
      - ./traefikdata:/data
#    environment:
#      - LEGO_CA_CERTIFICATES=/data/custom.crt
    command:
      - "--api.insecure=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--providers.http.endpoint=http://${SSP_USERNAME}:${SSP_PASSWORD}@ssp:8080/plugins/traefik/api_provider?id=api"
      - "--providers.http.pollInterval=60s"
      # ACME
      - '--certificatesresolvers.myresolver.acme.email=tech@kastgroup.com'
      - '--certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web'
      - '--certificatesresolvers.myresolver.acme.httpchallenge=true'
      - '--certificatesresolvers.myresolver.acme.caserver=https://acme-v02.api.letsencrypt.org/directory'
      - '--certificatesresolvers.myresolver.acme.storage=/data/acme.json'
      - '--entrypoints.web.http.redirections.entrypoint.to=websecure'
      - '--entrypoints.web.http.redirections.entrypoint.scheme=https'

    ports:
      - "80:80"
      - "443:443"

```

# Development
This project is based on a "hacky" framework - all non-framework related code is located in the `app/plugins` directory!
