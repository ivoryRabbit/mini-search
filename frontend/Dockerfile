FROM python:3.9.4-slim

WORKDIR /opt/frontend/

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY src .

EXPOSE 8501

ENV is_docker 1

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port", "8501"]