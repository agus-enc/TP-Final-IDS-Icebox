FROM python:3.14
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
RUN chmod +x init_docker.sh
EXPOSE 5000
CMD ["./init_docker.sh"]