FROM python:3.13-alpine

# Встановлюємо pip, оновлюємо setuptools та wheel
RUN pip install --upgrade pip setuptools wheel

# Робоча директорія всередині контейнера
WORKDIR /usr/src/app

# Копіюємо лише requirements для окремої кешованої стадії
COPY requirements.txt ./

# Встановлення залежностей
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо інші файли
COPY . .

# Відкриваємо порт
EXPOSE 8000

# Команда за замовчуванням
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

