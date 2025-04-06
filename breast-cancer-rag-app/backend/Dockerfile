# Stage 1: Builder with build dependencies
FROM python:3.11-slim as builder

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    gcc \
    python3-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime image
FROM python:3.11-slim

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Application setup
WORKDIR /app
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]