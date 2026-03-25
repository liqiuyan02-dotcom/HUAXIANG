FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create data directory
RUN mkdir -p data

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "backend/app.py"]
