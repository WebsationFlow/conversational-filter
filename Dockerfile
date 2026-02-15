FROM python:3.11-slim

WORKDIR /app

# Copy package files
COPY pyproject.toml README.md LICENSE.md ./
COPY src ./src

# Install dependencies
RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir flask gunicorn

# Copy API service
COPY api_service.py .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/api/v1/health')"

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "api_service:app"]
