# Base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy app files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port FastAPI will run on
EXPOSE 8000

# Run the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
