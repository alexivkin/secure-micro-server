# start from distroless
FROM gcr.io/distroless/python3-debian10

COPY server.py /server/server.py

# make all prints show up immediately
ENV PYTHONUNBUFFERED=1

EXPOSE 8443
WORKDIR /server/
ENTRYPOINT ["python","server.py"]