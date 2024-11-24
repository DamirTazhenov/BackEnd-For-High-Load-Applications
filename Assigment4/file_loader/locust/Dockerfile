# Dockerfile для Locust
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /locust

# Копируем только файлы, необходимые для Locust
COPY locustfile.py /locust/
COPY requirements.txt /locust/

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Открываем порт для веб-интерфейса Locust
EXPOSE 8089

# Указываем команду по умолчанию для Locust
ENTRYPOINT ["locust"]
