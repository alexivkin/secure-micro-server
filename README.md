# Secure minimal web server with Basic authentication

A small HTTPS server written in python to serve sensitive data over TLS after basic authentication. Designed to run in a docker container for additional security.

* Runs natively or inside a distroless container image for extra security.
* Serves content out of /server/public folder, over HTTPS, mapped into the container on the internal port 8443.
* Supports running custom python server-side code. A file that has an execute bit will be run after receiving the GET request. The code will have "filename" variable passed to it and "result" and "error" expected from it.

Building the docker image: `docker build -t <image tag> .`

## Running

Create a folder `public` and put your contents into it. Generate the basic auth key:

	echo -n "<username>:<password>" | base64 > ba.key

Then

	./run.sh

If you don't have a TLS in a `server.key` file, one will be generated for you on the first run.

To run interactively execute

	python server.py

or

```bash
docker run --rm -it -v "$PWD/ba.key":/server/ba.key -v "$PWD/server.pem":/server/server.pem -v "$PWD/server.key":/server/server.key  -v "$PWD/public/":/server/public/ -p 4545:8443 alexivkin/secure-micro-server
```
