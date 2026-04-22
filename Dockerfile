# Dockerfile
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency list first (layer caching optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Create a directory for the persistent database volume
RUN mkdir -p /app/data

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]