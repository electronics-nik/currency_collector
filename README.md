

### Python version
```
Python 3.12
```

### Update PIP
```shell
pip install --upgrade pip
```

### requirements.txt
```
beautifulsoup4==4.13.5
lxml==6.0.2
psycopg2==2.9.10
python-dotenv==1.1.1
requests==2.32.5
selenium==4.35.0
SQLAlchemy==2.0.43
```

### Запуск Docker контейнера в интерактивном режиме для тестирования
```shell
docker run -it --rm python-base /bin/sh
```

---

### Несколько проверенных лайфхаков для удобной отладки Celery в Docker
#### 1️⃣ Логи прямо в консоль

В `docker-compose.yml` укажи:

```yaml
worker:
  build: ./app
  command: celery -A app worker --loglevel=info
  depends_on:
    - redis
  environment:
    - C_FORCE_ROOT=true  # если запускаешь от root
```

- `--loglevel=info` — покажет выполнение задач.
- Если хочешь больше деталей, можно `--loglevel=debug`.

---

#### 2️⃣ Использовать docker-compose logs -f worker

Чтобы наблюдать __живые логи worker__:

```shell
docker-compose logs -f worker
```
Так ты увидишь, когда Celery получает задачу от beat и выполняет её.

---

#### 3️⃣ Проверка очередей Redis

Можно подключиться к Redis контейнеру и посмотреть, что там за задачи:
```shell
docker exec -it redis redis-cli
> keys *
> lrange celery 0 -1  # посмотреть, есть ли задачи в очереди
```

---

#### 4️⃣ Быстрая проверка Beat

Для того, чтобы убедиться, что __Beat реально шлёт задачи__, запусти его в отдельном терминале:
```shell
docker-compose logs -f beat
```
- Ты увидишь, что Beat планирует задачи по расписанию:
```arduino
Scheduler: Sending due task run-my-job-every-1-minute (app.my_job)
```

---

#### 5️⃣ Запуск вручную для отладки

Если нужно протестировать задачу без планировщика, можно прямо из контейнера вызвать:
```shell
docker-compose run --rm worker python -c "from app import my_job; my_job.delay()"
```
- .delay() ставит задачу в очередь Redis, worker её выполнит.
- Отличный способ проверить, что задача работает.

---

### Несколько практических приёмов, чтобы логи Celery и отладка задач в Docker были максимально удобными

#### 1️⃣ Полные логи worker

В `docker-compose.yml` можно указать для worker:

```yaml
worker:
  build: ./app
  command: celery -A app worker --loglevel=debug
  environment:
    - C_FORCE_ROOT=true
```
- `--loglevel=debug` показывает все события, включая получение и выполнение задач.
- `C_FORCE_ROOT=true` нужен, если запускаешь контейнер от root (часто в Docker).

---

#### 2️⃣ Логи Beat

Beat тоже можно запустить с логами:

```yaml
beat:
  build: ./app
  command: celery -A app beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
- Для обычного Celery без Django можно опустить `--scheduler`, достаточно `--loglevel=info`.
- Beat будет писать в stdout, что именно планирует запускать.

---

#### 3️⃣ Одновременный просмотр логов

В отдельном терминале:

```shell
docker-compose logs -f worker
docker-compose logs -f beat
```

- `-f` — follow, т.е. потоки в реальном времени.
- Удобно, чтобы сразу видеть, что задачи ставятся и выполняются.

---

#### 4️⃣ Проверка очереди Redis

Можно зайти в контейнер Redis:

```shell
docker exec -it redis redis-cli
> keys *
> llen celery  # количество задач в очереди
> lrange celery 0 -1  # посмотреть задачи
```

Если очередь пуста → значит Beat/Worker не отправляют или не получают задачи.

---

#### 5️⃣ Тестовая задача напрямую

Чтобы проверить Worker без Beat:

```shell
docker-compose run --rm worker python -c "from app import my_job; my_job.delay()"
```
- `.delay()` ставит задачу в очередь, Worker её выполнит.
- Это быстрый способ убедиться, что задача работает.

---

#### 6️⃣ Рекомендация: вывод задач в лог

В самой задаче:

```python
@app.task
def my_job():
    print("🔥 Задача выполнена!")
```
- Print идёт в stdout, отображается в docker-compose logs.
- Можно использовать logging для более гибкого логирования:
```python
import logging

logger = logging.getLogger(__name__)

@app.task
def my_job():
    logger.info("🔥 Задача выполнена!")
```
- Тогда логи можно конфигурировать (файлы, уровень, формат).

### Вот пример настройки логирования в Celery, чтобы логи шли и в консоль, и в файл.

```python
# app/celery_app.py
import logging
from celery import Celery

app = Celery(
    'app',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

# Настройка логирования
logger = logging.getLogger('celery_app')
logger.setLevel(logging.INFO)

# Консольный обработчик
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Файловый обработчик
file_handler = logging.FileHandler('/logs/celery.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(console_formatter)

# Добавляем обработчики к логгеру
logger.addHandler(console_handler)
logger.addHandler(file_handler)

@app.task
def my_job():
    logger.info("🔥 Задача выполнена!")
```

##### Пояснения:
1. `StreamHandler` → логи в консоль (выводятся в `docker-compose logs`).
2. `FileHandler` → логи в файл `/logs/celery.log`.

- В Docker можно примонтировать volume, чтобы видеть логи на хосте:

```yaml
volumes:
  - ./logs:/logs
```

3. В самой задаче используем `logger.info(...)`, вместо `print()`. Так удобно отлавливать ошибки 
и видеть точное время выполнения.

### Развёртывание
1. Загружаем все `docker-compose` файлы на сервер;
```shell

```

2. Устанавливаем [`Portainer`](https://docs.portainer.io/start/install-ce/server/docker/linux)
```shell
docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:lts
```

3. Создаём Docker сеть
```shell
docker network create currency_collector_net
```
и проверяем её
```shell
docker network inspect currency_collector_net
```
4. Запускаем `Redis`
```shell
cd redis
docker compose up -d
```

5. Запускаем `PstgreSQL`
```shell
cd postgres
docker compose up -d
```

6. Открываем порт в AWS
7. Подключаемся клиентом и инициализируем базу
8. Запускаем приложение
```shell
docker compose -f prod-docker-compose.yml up -d
```
9. Проверяем что все контейнера подключились к сети
```shell
docker network inspect currency_collector_net
```

10. Запускаем `Grafana`
```shell
cd grafana
doucer compose up -d
```



git remote add origin git@github.com:electronics-nik/currency_collector.git
git branch -M main
git push -u origin main