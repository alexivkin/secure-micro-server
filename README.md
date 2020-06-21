# Minimal HTTPS server with basic auth

Based on a distroless image for extra security. Serves content out of /server/public folder mapped into the container on the internal port 8443

## Running

Generate a server key, or provide your own

	openssl req -new -x509 -keyout server.pem -out server.pem -days 3650 -nodes

Generate Basic Auth Key:

	echo -n "<username>:<password>" | base64 > ba.key

Run

 	docker run --rm -it -v "$PWD/ba.key":/server/ba.key -v "$PWD/server.pem":/server/server.pem -v "$PWD/public/":/server/public/ -p 4545:8443 alexivkin/secure-micro-server
