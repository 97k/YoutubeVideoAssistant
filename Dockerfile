FROM python:3.11-slim

WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src .
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
