# Stage 1: Build stage
FROM python:3.13-slim AS builder
 
RUN mkdir /app
 
WORKDIR /app
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
 
# Stage 2: Production stage
FROM python:3.13-slim

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Create a non-root user, -m: create home directory, -r: create system user
# Change the directory ownership, -R: recursively
# RUN useradd -m -r appuser && \
# mkdir /app && \
# chown -R appuser /app
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Copy application code with permissions for the non-root user
# COPY --chown=appuser:appuser . .
COPY . .

# Switch to non-root user
# USER appuser
 
# Expose the application port
EXPOSE 8000
