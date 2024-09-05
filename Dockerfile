# Use a Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code from the host into the container
COPY . .

# Define the command to run your application
CMD [ "python", "app.py"]
