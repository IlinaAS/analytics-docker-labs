Ильина Алина, группа АДЭУ-221
### Вариант 8
## Описание задачи
**Бизнес-метрика:** Анализ стоимости логистических маршрутов в разных валютах.  
**Данные:** Реальные курсы валют (api.exchangerate.host) + синтетические данные по маршрутам.  
**Технологии:** Python 3.9+, requests, pandas, Docker.

## Цель работы
Научиться разрабатывать воспроизводимые аналитические инструменты: пройти полный цикл от написания Python-скрипта для обработки бизнес-данных до его упаковки в Docker-образ и запуска в изолированной среде.  

## Ход работы:

### 1. Создание папки проекта

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_2/img/dd2.PNG)

### 2. Создание файлов

Файл 1: app.py (Основной скрипт)
Для чего нужен:
Это главный файл программы. Он выполняет всю аналитическую работу.  
![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_2/img/app.PNG)

Файл 2: requirements.txt (Зависимости)
Это список всех Python-библиотек, которые нужны для работы программы.  
![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_2/img/requr.PNG)

Файл 3: Dockerfile (Инструкция сборки)
Это «рецепт» для Docker. По этим инструкциям Docker создаёт образ с твоим приложением.  
![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_2/img/dockerfile.PNG)

Файл 4: .dockerignore (Исключения для Docker)
Это файл-инструкция для Docker: «Не копируй эти файлы в образ».  
![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_2/img/dockerignore.PNG)

### 3. Проверка файлов
Проверяем, что все 4 файла созданы   
![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_2/img/проверка_файлов.PNG)

### 4. Сборка Docker-образа

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_2/img/dd3.PNG)

Docker читает Dockerfile  
Скачивает базовый образ python:3.9-slim  
Копирует requirements.txt и устанавливает библиотеки  
Копирует app.py  
Создаёт образ с именем supply-lab и тегом v1  

### 5. Запуск контейнера

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_2/img/dd4.PNG)

Docker создаёт контейнер из образа supply-lab:v1  
Выполняет команду python app.py  
Выводит результат в терминал  
Флаг --rm автоматически удаляет контейнер после завершения (не мусорит)  
