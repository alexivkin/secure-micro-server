#!/bin/bash

docker run -d --name secure-micro-server --restart unless-stopped -v "$PWD/ba.key":/server/ba.key -v "$PWD/server.pem":/server/server.pem -v "$PWD/server.key":/server/server.key -v "$PWD/public/":/server/public/ -p 8443:8443 alexivkin/secure-micro-server
