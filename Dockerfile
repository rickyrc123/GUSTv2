FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip install \
    numpy \
    scipy \
    matplotlib \
    fastapi \
    folium \
    websockets \
    uvicorn \
    pydantic \
    psycopg2-binary \
    sqlalchemy
    
COPY . .

