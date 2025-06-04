# Use an official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY src/app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY src/app /app

# Expose the port Flask runs on
EXPOSE 5000

# Run the app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]