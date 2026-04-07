FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Add the root directory to PYTHONPATH so imports like "app.database" work if needed
ENV PYTHONPATH=/app
EXPOSE 5000
CMD ["python", "api/app.py"]
