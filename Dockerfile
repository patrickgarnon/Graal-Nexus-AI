FROM python:3.11-slim
WORKDIR /app
COPY support_assistant/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY support_assistant/ /app
EXPOSE 5000
CMD ["python", "app.py"]
