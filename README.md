# SimpleSignageProxy

This project creates a simple management interface, which allows to dynamically generate proxies (on subdomains) for Traefik. It is intended for a simple digital signage solution, in order to create a central management interface for all screens.

A screen is setup as a (e.g. Raspberry Pi) endpoint device running a browser in kiosk mode. This browser displays the URL https://<screen_id>.<domain>/

The <screen_id> can be setup through the management interface, located at <domain>. This <domain> can be configured using the SSP_DOMAIN environment variable located in the docker-compose.yml file.

# Installation
Use the following docker-compose.yml file for installation (the one in the repo is for development purposes)
```
services:
  ssp:
    image: tttttx2/simplesignageproxy:main
    volumes:
      - ./data:/data
    environment:
      - SSP_DOMAIN=screens.example.com

  traefik:
    image: "traefik:v2.10"
    command:
      - "--api.insecure=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--providers.http.endpoint=http://ssp:8080/plugins/traefik/api_provider?id=api"
    ports:
      - "80:80"
      - "443:443"
```

# Development
This project is based on a "hacky" framework - all non-framework related code is located in the `app/plugins` directory!
