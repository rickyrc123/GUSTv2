FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /home/GUSTv2
COPY . /home/GUSTv2/

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    postgresql \
    git

RUN pip install \
    numpy \
    scipy \
    matplotlib \
    sqlalchemy \
    fastapi \
    pydantic \
    psycopg2-binary

CMD ["bash"]