FROM gcr.io/distroless/python3-debian10

COPY server.py /server/server.py

EXPOSE 8443
WORKDIR /server/
ENTRYPOINT ["python","server.py"]