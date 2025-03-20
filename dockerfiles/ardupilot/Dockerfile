# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set environment variables to avoid interactive installation prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    g++ \
    make \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    libtool \
    libxml2-dev \
    libprotobuf-dev \
    protobuf-compiler \
    libsqlite3-dev \
    libboost-all-dev \
    cmake \
    gawk \
    libcurl4-openssl-dev \
    libtool \
    pkg-config \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    python3-pyqt5 \
    libjpeg-dev \
    libpng-dev \
    libeigen3-dev \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*


# Update package list and install python3-pip
RUN apt-get update && apt-get install -y python3-pip

RUN python3 -m pip install empy==3.3.4
# Download the Waf script
RUN curl -O https://waf.io/waf-2.0.22 && \
    chmod +x waf-2.0.22 && \
    mv waf-2.0.22 /usr/local/bin/waf

# Clone the ArduPilot repository
RUN git clone --recursive https://github.com/ArduPilot/ardupilot.git /ardupilot

# Set the working directory to the cloned ArduPilot repository
WORKDIR /ardupilot

# Explicitly initialize and update the submodules, especially the 'waf' submodule
RUN git submodule update --init --recursive

# Build ArduPilot (now that submodules are correctly initialized)
RUN ./waf configure --board sitl && ./waf
