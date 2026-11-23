# Use an official lightweight Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file first to leverage Docker's caching mechanism
COPY backend_files/requirements.txt /app/backend_files/requirements.txt

# Install system dependencies and Python requirements
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r /app/backend_files/requirements.txt

# Copy all application files and subfolders into the container working directory
COPY . /app

# Expose port 8501 for the default Streamlit application
EXPOSE 8501

# Run the Streamlit application on container startup
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
