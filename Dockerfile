# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /workspace
ENV PYTHONPATH=/workspace/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model and app code
# The model is expected in NER/SecureBert-NER
COPY NER/ ./NER/
COPY app/ ./app/

# Create a non-root user for security
RUN useradd -m appuser
RUN chown -R appuser:appuser /workspace
USER appuser

# Expose the port FastAPI runs on (internally)
EXPOSE 8000

# Healthcheck to ensure the backend is running correctly
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Command to run the FastAPI server
ENTRYPOINT ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
