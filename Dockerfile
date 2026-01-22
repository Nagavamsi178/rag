FROM python:3.11.9


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

EXPOSE 8501

CMD ["python", "main.py"]
