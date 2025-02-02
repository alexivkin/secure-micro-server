#!/bin/bash

if [[ ! -f server.key ]];
    openssl req -new -x509 -keyout server.key -out server.pem -days 3650 -nodes -subj "/C=AU/ST=Some-State/O=Internet Widgits Pty Ltd"
fi

docker run -d --name secure-micro-server --restart unless-stopped -v "$PWD/ba.key":/server/ba.key -v "$PWD/server.pem":/server/server.pem -v "$PWD/server.key":/server/server.key -v "$PWD/public/":/server/public/ -p 4545:8443 alexivkin/secure-micro-server
