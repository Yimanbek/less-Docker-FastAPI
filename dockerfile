FROM python:3.10-slim

ENV TZ=Asia/Bishkek
RUN apt-get update && apt-get install -y tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /usr/src/app

# Копируем файл зависимостей
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем 8000 порт (FastAPI по умолчанию)
EXPOSE 8000

# Запускаем приложение (главный процесс)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
