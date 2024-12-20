# Wallet Service

Это проект для управления кошельками с возможностью проведения операций (депозит, вывод средств) и просмотр баланса.
Сервис построен с использованием FastAPI, SQLAlchemy и Alembic для миграций, а также Docker для контейнеризации.

## Стек технологий

- **FastAPI** — веб-фреймворк для Python, использующий асинхронную обработку запросов.
- **SQLAlchemy** — ORM для работы с базой данных.
- **Alembic** — инструмент для миграций базы данных.
- **PostgreSQL** — СУБД для хранения данных.
- **Docker** — контейнеризация приложения и базы данных.

## Описание проекта

Проект реализует API для работы с кошельками. Каждый кошелек содержит баланс, который можно посмотреть, и можно
проводить операции:

- **Депозит** — пополнение счета.
- **Вывод** — снятие средств.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/aleksgrekov/wallet_service.git
   cd wallet_service
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Для Windows используйте .venv\Scripts\activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте .env файл с параметрами для подключения к базе данных. Пример:
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname

## Развертывание с Docker

Для запуска приложения и базы данных с использованием Docker, выполните следующие шаги:

1. Сначала создайте сеть и контейнеры:
   ```bash
   docker-compose up -d
   ```

2. После этого база данных и сервис будут работать на портах, указанных в docker-compose.yml.
3. Чтобы выполнить миграции базы данных, выполните:
   ```bash
   docker-compose exec app alembic upgrade head
   ```

4. Приложение будет доступно по адресу http://localhost:8000.

## Миграции

Для создания миграций с помощью Alembic используйте следующие команды:

1. Создание миграции:
   ```bash
   alembic revision --autogenerate -m "Описание изменений"
   ```

2. Применение миграций
   ```bash
   alembic upgrade head
   ```

## Тестирование

Для тестирования API используйте pytest:

1. Установите зависимости для тестирования:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Запустите тесты:
   ```bash
   pytest
   ```

## API

Получить баланс кошелька

- URL: /api/v1/wallets/{uuid}
- Метод: GET
- Ответ:
   ```json
   {
     "uuid": "wallet-uuid",
     "balance": 100.0,
     "message": "Operation successful"
   }
  ```

Операция с кошельком (Депозит/Вывод)

- URL: /api/v1/wallets/{uuid}/operation
- Метод: POST
- Тело запроса:

   ```json
   {
     "operationType": "DEPOSIT" or "WITHDRAW",
     "amount": 50.0
   }
   ```

- Тело запроса:

   ```json   
   {
      "message": "Operation successful"
   }
   ```

## Ошибки

- Недостаточно средств:
    ```json
    {
      "detail": "No enough money"
    }
    ```
- Кошелек не найден:
    ```json
    {
      "detail": "Wallet not found"
    }
    ```
  
- Неверный тип операции:
    ```json
    {
      "detail": "Invalid operation type"
    }
    ```
