# Лабораторная работа №3: Оркестрация контейнеров в Kubernetes

- ФИО: Ильина Алина
- Группа: АДЭУ-221
- Вариант №8: Python ML API + Redis
- Задача: Счетчик запросов в Redis

## Цель работы
Освоить развертывание связки сервисов в Kubernetes, управление Deployment и Service.

## Ход выполнения

### 1. Создание YAML-манифестов
Файл [redis-deployment.yaml](k/redis-deployment.yaml)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  labels:
    app: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          limits:
            memory: "256Mi"
            cpu: "250m"
```

Пояснение ключевых строк:
- image: redis:7-alpine — официальный легковесный образ Redis версии 7
- containerPort: 6379 — стандартный порт Redis
- replicas: 1 — запускаем один под с Redis
- labels: app: redis — метка для идентификации пода (используется в Service selector)

Файл [python-app-deployment.yaml](k/python-app-deployment.yaml)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-ml-api
  labels:
    app: python-ml-api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: python-ml-api
  template:
    metadata:
      labels:
        app: python-ml-api
    spec:
      containers:
      - name: python-app
        image: python:3.11-slim
        ports:
        - containerPort: 5000
        env:
        - name: REDIS_HOST
          value: "redis-service"
        command: ["/bin/bash", "-c"]
        args:
        - |
          pip install flask redis --quiet
          cat > /app.py << 'EOF'
          # ... код приложения ...
          EOF
          python /app.py
```
Пояснение ключевых строк:
- image: python:3.11-slim — минимальный образ Python 3.11
- containerPort: 5000 — порт Flask-приложения
- env: REDIS_HOST=redis-service — переменная окружения для подключения к Redis. Важный момент: значение redis-service — это имя Kubernetes Service, которое автоматически резолвится в DNS кластера
- command и args — переопределение команды запуска контейнера для установки зависимостей и запуска приложения без сборки собственного Docker-образа

Файл [services.yaml](k/services.yaml)
```yaml
# Сервис для Python-приложения
apiVersion: v1
kind: Service
metadata:
  name: python-ml-api-service
spec:
  selector:
    app: python-ml-api
  type: NodePort
  ports:
    - port: 80
      targetPort: 5000
      nodePort: 30500
---
# Сервис для Redis
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  type: ClusterIP
  ports:
    - port: 6379
      targetPort: 6379
### 2. Скриншоты
![Pods](img/pods.png)
![Services](img/services.png)
![App](img/app-working.png)
```
Пояснение ключевых строк:
- selector: app: python-ml-api — сервис находит поды по метке app=python-ml-api
- type: NodePort — открывает доступ к приложению извне через порт 30500 на IP-адресе ноды
- port: 80 — порт внутри кластера
- targetPort: 5000 — порт контейнера, на который перенаправляется трафик
- nodePort: 30500 — внешний порт для доступа к приложению (диапазон 30000-32767)
- type: ClusterIP для Redis — сервис доступен только внутри кластера, что безопасно для базы данных

### 2. Развёртывание в кластере
Применение манифестов:

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_3/img/d33_0.PNG)

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_3/img/d33_1.PNG)

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_3/img/d33_2.PNG)


Проверка состояния подов:

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_3/img/d33_3.PNG)

Два пода в статусе Running
Колонка READY показывает 1/1 (один контейнер в поде запущен)
Проверка сервисов:

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_3/img/d33_4.PNG)

python-ml-api-service с типом NodePort и портом 80:30500/TCP
redis-service с типом ClusterIP и портом 6379/TCP
CLUSTER-IP — внутренние IP-адреса сервисов в кластере
### 3. Проверка работоспособности приложения

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_3/img/d3_3.PNG)

Тестирование через браузер:
Открыт URL: http://192.168.1.18:30500/counter

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_3/img/d3_1.PNG)

При обновлении страницы счётчик увеличивается на 1

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_3/img/d3_2.PNG)


### 3. Проверка взаимодействия компонентов
Логи Python-приложения:

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_3/img/d33_5.PNG)

Проверка связи с Redis:

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_3/img/d33_6.PNG)

Это подтверждает, что:
- Python-приложение успешно подключается к Redis
- Данные сохраняются в базе между запросами
- Сетевое взаимодействие между сервисами работает через DNS-имя redis-service

### Выводы
В процессе выполнения лабораторной работы было развёрнуто два связанных сервиса в Kubernetes:
Python ML API — веб-приложение на Flask
Redis — база данных для хранения счётчика

- Ключевые моменты:
Сервисы взаимодействуют через DNS-имена Kubernetes (redis-service)
NodePort обеспечивает внешний доступ к приложению
ClusterIP изолирует базу данных внутри кластера (безопасность)
Environment variables (REDIS_HOST) позволяют гибко конфигурировать подключение
- Трудности:
Первоначальная настройка kubectl и алиасов для MicroK8s
Отладка YAML-синтаксиса (отступы, двоеточия)
Ожидание запуска подов (статус ContainerCreating)
- Результат: Приложение работает, счётчик увеличивается при каждом запросе, связка Python + Redis функционирует корректно. 
