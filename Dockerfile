# Using a Python image
FROM python:3.9-slim

# Installing required build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    make \
    cmake \
    libmagic-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrading pip
RUN pip install --upgrade pip

# Copying all the files locally into the app directory of the image
COPY . /app

# Accessing the app directory of the image
WORKDIR /app

# Installing precompiled pyarrow
RUN pip install pyarrow

# Installing the dependencies
RUN pip install -r requirements.txt

# Set the Metaflow user environment variable
ENV METAFLOW_USER=ml_user

# Exposing the port in the container
EXPOSE 5001

# Executing the application
CMD python src/app.py