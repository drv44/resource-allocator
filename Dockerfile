FROM python:3.10-slim
WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# (Optional) document a default, but Railway will override
ENV PORT=8501

# Expose is only documentation here
EXPOSE 8501

# Shell form so $PORT is evaluated at runtime
CMD ["sh", "-c", "streamlit run frontend.py \
  --server.port $PORT \
  --server.address 0.0.0.0 \
  --server.headless true"]
