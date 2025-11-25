# Dev container for ts-segmentation
# Use the official Dev Container Python image for python 3.10
FROM mcr.microsoft.com/devcontainers/python:1-3.10

ENV DEBIAN_FRONTEND=noninteractive

# Install system packages commonly required by the project
# Add packages that are required for creating virtualenvs and building numeric
# packages (numpy / scipy) when pre-built wheels are not available.
RUN apt-get update \
  && apt-get -y install --no-install-recommends \
  build-essential \
  libsndfile1 \
  git \
  curl \
  python3-venv \
  python3-pip \
  libatlas-base-dev \
  libopenblas-dev \
  liblapack-dev \
  gfortran \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Switch back to the default non-root user from the base image
USER ${USERNAME}

WORKDIR /workspace

# Ensure pip cache isn't huge in container
ENV PIP_NO_CACHE_DIR=1

# Keep it lean: actual Python deps are installed in postCreateCommand (via
# `.devcontainer/post-create.sh`).
