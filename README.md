# reminder_bot

## Описание
`reminder_bot` - это бот, который отправляет напоминания о чем-либо через определенное время или в конкретное время путем отправки сообщения в чат бота. Программа использует API OpenAI для обработки запросов и отправляет уведомления с использованием Celery и Redis.

## Требования
Все зависимости указаны в файле `requirements.txt`.

## Установка и запуск

### 1. Установка Redis
Убедитесь, что у вас установлен Redis. Инструкции по установке можно найти [здесь](https://redis.io/download).

### 2. Установка зависимостей
Установите все необходимые зависимости, выполнив команду:
```bash
pip install -r requirements.txt
```

### 3. Запуск Celery
Запустите Celery из корневой папки с виртуальным окружением с помощью следующей команды:
```bash
celery -A celery1.celery_app worker -l info -E
```

### 4. Запуск бота
Запустите бота:
```bash
python bot.py
```

## Структура проекта

- `celery1/` - Папка, содержащая задачи для расписания и выполнения отправки сообщений по заданному расписанию.
- `db/` - Папка для создания, редактирования и просмотра базы данных. Используется SQLite, так как это тестовый проект без нагрузок, и она не требует дополнительных манипуляций для подключения и уже предустановлена в Python.
- `config/` - Папка, содержащая файлы с токенами, которые представлены в виде констант.
- `function/` - Папка, содержащая файл с функциями, вынесенными из основного файла проекта для улучшения читабельности кода.
- В корневой папке находятся основные файлы:
  - `bot.py` - Отвечает за взаимодействие с пользователем.
  - `ai.py` - Отвечает за работу с API OpenAI, запись в базу данных и отправку уведомлений в очередь Celery на исполнение.


## Контакты
https://t.me/artdmsav