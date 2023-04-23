FROM python:3.10
WORKDIR /app
COPY Requierment.txt .
RUN pip install --no-cache-dir -r Requierment.txt
COPY .. .
EXPOSE 8050
CMD ["python","app.py"]