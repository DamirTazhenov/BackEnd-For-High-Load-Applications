# Django Load Balancer Project

## Описание

Этот проект демонстрирует, как настроить балансировку нагрузки для Django-приложения с помощью **NGINX** и **Docker**. В проекте используются два экземпляра Django-приложений, которые обрабатывают запросы, поступающие через NGINX, работающий в качестве балансировщика нагрузки. В конфигурации также можно использовать Redis для кэширования сессий или данных.

## Стек технологий

- **Django**: Веб-фреймворк Python.
- **NGINX**: Веб-сервер и балансировщик нагрузки.
- **Redis**: Опционально для хранения сессий и кэша.
- **Docker**: Среда контейнеризации для упаковки и развертывания приложений.
- **Docker Compose**: Инструмент для работы с многоконтейнерными приложениями Docker.

## Файлы проекта

- **Dockerfile**: Dockerfile для Django-приложения.
- **Dockerfile.nginx**: Dockerfile для NGINX.
- **nginx.conf**: Конфигурационный файл для NGINX, настроенный на балансировку нагрузки между двумя экземплярами Django.
- **docker-compose.yml**: Файл Docker Compose для сборки и запуска всех контейнеров (Django, NGINX, Redis).
- **requirements.txt**: Список Python-зависимостей для Django-приложения.

## Установка и запуск проекта

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/ваш-репозиторий/django-load-balancer.git
cd django-load-balancer
```

### Шаг 2: Создание образов и запуск контейнеров

Для сборки и запуска всех контейнеров (Django, NGINX, Redis) выполните команду:

```bash
docker-compose up --build
```

Эта команда выполнит сборку образов для Django и NGINX, а также запустит все необходимые контейнеры.

### Шаг 3: Доступ к приложению

После запуска контейнеров приложение будет доступно по адресу:

```bash
http://localhost/
```

NGINX выполняет балансировку запросов между двумя контейнерами Django, работающими на портах `8001` и `8002`.

## Конфигурация контейнеров

### Django (два экземпляра)

Два контейнера Django, которые работают независимо друг от друга и принимают запросы от NGINX:

- **django1**: работает на порту `8001`.
- **django2**: работает на порту `8002`.

Каждый контейнер использует стандартный `Dockerfile` для Python/Django.

### NGINX

Контейнер NGINX настроен для выполнения балансировки нагрузки по принципу "round-robin" с поддержкой sticky-сессий (с помощью директивы `ip_hash`). Конфигурация NGINX также выполняет health-check серверов и перенаправляет запросы только на здоровые экземпляры.

### Redis (опционально)

Контейнер Redis используется для хранения сессий и кэширования данных. Он доступен на порту `6379`.

## Тестирование производительности

Чтобы протестировать производительность и распределение нагрузки, можно использовать инструмент **Apache Benchmark (ab)**:

```bash
C:\Apache24\bin>ab -n 1000 -c 100 http://localhost/
```

### Результаты тестирования:

```bash
This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests

Server Software:        nginx/1.27.1
Server Hostname:        localhost
Server Port:            80

Document Path:          /
Document Length:        584 bytes

Concurrency Level:      100
Time taken for tests:   3.530 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      936014 bytes
HTML transferred:       584000 bytes
Requests per second:    283.32 [#/sec] (mean)
Time per request:       352.963 [ms] (mean)
Time per request:       3.530 [ms] (mean, across all concurrent requests)
Transfer rate:          258.97 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.4      0       1
Processing:    13  230 574.5     51    3356
Waiting:       13  230 574.6     51    3356
Total:         13  230 574.5     51    3357

Percentage of the requests served within a certain time (ms)
  50%     51
  66%     63
  75%     72
  80%     82
  90%   1039
  95%   1140
  98%   3110
  99%   3167
 100%   3357 (longest request)
```

### Анализ результатов:

- **Requests per second**: Сервер обрабатывает **283.32 запросов в секунду**.
- **Time per request**: В среднем обработка одного запроса занимает **352.963 ms**.
- **Concurrency Level**: Мы тестировали с 100 параллельными соединениями.
- **Failed requests**: Все запросы успешно завершились, нет ошибок.

**Процентиль запросов**:
- 50% запросов завершились за 51 ms.
- 95% запросов завершились за 1140 ms или быстрее.
- Максимальное время обработки одного запроса: 3357 ms.

Эти результаты показывают, что приложение стабильно обрабатывает большое количество запросов даже при высоком уровне параллелизма.

## Логи контейнеров

Чтобы просмотреть логи для каждого контейнера, используйте следующие команды:

- Логи для первого Django контейнера:
  ```bash
  docker logs django1
  ```
- Логи для второго Django контейнера:
  ```bash
  docker logs django2
  ```
- Логи для NGINX:
  ```bash
  docker logs nginx_lb
  ```

## Настройка конфигурации NGINX

Конфигурация NGINX для балансировки нагрузки находится в файле `nginx.conf`. В нем настроены два сервера Django и используется директива `ip_hash` для sticky-сессий:

```nginx
upstream django_servers {
    ip_hash;
    server django1:8000;
    server django2:8000;
}

server {
    listen 80;

    location / {
        proxy_pass http://django_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Остановка контейнеров

Чтобы остановить все запущенные контейнеры, выполните команду:

```bash
docker-compose down
```

Эта команда остановит и удалит все запущенные контейнеры.

## Примечания

- Если вы используете Redis для кэширования или хранения сессий, убедитесь, что в настройках Django (`settings.py`) настроено использование Redis как кэш-бэкенд.
  
  Пример настройки Redis:

  ```python
  CACHES = {
      'default': {
          'BACKEND': 'django_redis.cache.RedisCache',
          'LOCATION': 'redis://redis:6379/1',
          'OPTIONS': {
              'CLIENT_CLASS': 'django_redis.client.DefaultClient',
          }
      }
  }
  ```

## Заключение

Этот проект демонстрирует, как настроить балансировку нагрузки для Django-приложений с помощью NGINX и Docker. Использование контейнеров позволяет легко масштабировать приложение и распределять нагрузку между несколькими серверами.

---
