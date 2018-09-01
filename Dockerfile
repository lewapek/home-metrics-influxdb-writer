FROM python:3.7.0-slim
WORKDIR /app
ADD . /app
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 8080
CMD ["python3", "collector.py"]