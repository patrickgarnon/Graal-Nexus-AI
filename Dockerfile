# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY support_assistant/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY support_assistant/ ./

# Runtime configuration
ARG PORT=5000
ENV PORT=${PORT}
EXPOSE ${PORT}

# Start the application
CMD ["python", "app.py"]
