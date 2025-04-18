### Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose default Streamlit port and set it via ENV
ENV PORT=8501
EXPOSE 8501

# (Optional) Install curl for healthcheck
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Healthcheck to ensure the app is running
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl --fail http://localhost:8501/ || exit 1

# Launch the Streamlit app
CMD ["sh", "-c", "streamlit run frontend.py \
  --server.port $PORT \
  --server.address 0.0.0.0 \
  --server.headless true"]


