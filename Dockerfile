# start from a builder
FROM python:3-slim AS builder
COPY server.py /server/server.py

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/server requests

# start from distroless
FROM gcr.io/distroless/python3-debian10

COPY --from=builder /server /server

# make all prints show up immediately
ENV PYTHONUNBUFFERED=1

EXPOSE 8443
WORKDIR /server/
ENTRYPOINT ["python","server.py"]