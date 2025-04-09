# FROM python:3.10-slim

# WORKDIR /
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8501
# CMD ["streamlit", "run", "frontend.py", \ "server.port=8501", \ "--server.address=0.0.0.0"]


FROM python:3.10-slim

WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# (optional but good documentation)
EXPOSE 8501

# ensure Streamlit listens on all interfaces
CMD ["streamlit", "run", "frontend.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]
