# Minimal HTTPS server with basic auth


Serves content out of /server/public folder, over HTTPS, mapped into the container on the internal port 8443.
Supports running custom python server-side code. To do this set an execute bit on the file you'd like the server to run. The code will have "filename" variable passed to it and "result" and "error" expected from it.

Based on a distroless image for extra security.

Building: `docker build -t <image tag> .`

## Running

Generate a server key, or provide your own

	openssl req -new -x509 -keyout server.key -out server.pem -days 3650 -nodes

Generate Basic Auth Key:

	echo -n "<username>:<password>" | base64 > ba.key

Run

```bash
docker run --rm -it -v "$PWD/ba.key":/server/ba.key -v "$PWD/server.pem":/server/server.pem -v "$PWD/server.key":/server/server.key  -v "$PWD/public/":/server/public/ -p 4545:8443 alexivkin/secure-micro-server
```
