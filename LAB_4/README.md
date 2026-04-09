# Лабораторная работа №4: Создание и развертывание полнофункционального приложения

- ФИО: Ильина Алина
- Группа: АДЭУ-221
- Вариант №8: название системы - Support Tickets.	Бизнес-задача - система техподдержки.	Данные - описание проблемы, уровень срочности, автор, статус решения.

## Описание архитектуры

### Выбранный технологический стек:
| Компонент | Технология | Назначение |
|-----------|-----------|------------|
| **Backend** | FastAPI (Python 3.11) | REST API для CRUD-операций с тикетами |
| **Frontend** | Streamlit | Веб-интерфейс для создания и просмотра тикетов |
| **Database** | PostgreSQL 15 | Хранение данных о тикетах поддержки |
| **Container** | Docker | Изоляция и переносимость сервисов |
| **Orchestration** | Kubernetes (MicroK8s) | Управление жизненным циклом подов |

## Ход выполнения

### Создаем необходимые папки и файлы:

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_4/img/d4_1.PNG)

### Сборка Docker-образов

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_4/img/d4_2.PNG)
![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_4/img/d4_3.PNG)
![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_4/img/d4_4.PNG)

Команды docker build выполнены успешно, образы my-backend:v1 и my-frontend:v1 созданы.

### Статус подов в Kubernetes

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_4/img/d4_6.PNG)

Все поды находятся в статусе Running, READY 1/1. Ошибок перезапуска нет.

Проверяем хост и IP-адрес ВМ.
![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_4/img/d4_7.PNG)
![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_4/img/d4_8.PNG)

### Работающее приложение в браузере (форма ввода и отображение таблицы):

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_4/img/d4_res.PNG)

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_4/img/d4_res1.PNG)

![](https://github.com/IlinaAS/analytics-docker-labs/blob/main/LAB_4/img/d4_res2.PNG)

Интерфейс доступен по http://192.168.1.18:30080. Форма создания тикета работает, данные отображаются в таблице.

### Выводы
- В ходе выполнения лабораторной работы успешно реализовано и развёрнуто трёхзвенное приложение Support Tickets в кластере Kubernetes.
- Написан REST API на FastAPI с валидацией входных данных и CRUD-операциями.
- Создан интерактивный веб-интерфейс на Streamlit для работы с заявками.
- Сервисы контейнеризированы через Docker и корректно импортированы в MicroK8s.
- Написаны YAML-манифесты с правильным использованием ClusterIP для внутренних сервисов и NodePort для внешнего доступа.
- Приложение стабильно работает, данные сохраняются в PostgreSQL, взаимодействие между компонентами настроено через переменные окружения и DNS-имена сервисов K8s.
