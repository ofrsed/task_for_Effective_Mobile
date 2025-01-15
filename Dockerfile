# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /effective_cafe


# Копируем весь проект
COPY . /effective_cafe
COPY requirements.txt /effective_cafe/

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Устанавливаем зависимости
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt


# Открываем порт для Django
EXPOSE 8000

# Запускаем сервер Django
CMD python manage.py migrate && python manage.py populate_db && python manage.py runserver 0.0.0.0:8000