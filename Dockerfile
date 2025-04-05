# Pythong
#FROM python:3.9-slim

#WORKDIR /app

#COPY requirements.txt .

#RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

#EXPOSE 8000

#CMD ["python", "main.py"]

#PHP
FROM php:8.0-cli

WORKDIR /app

COPY composer.json ./

RUN apt-get update && apt-get install -y \
    libzip-dev \
    && docker-php-ext-install zip \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && composer install --no-interaction --no-dev --optimize-autoloader

COPY . .

EXPOSE 8000

CMD ["php", "-S", "0.0.0.0:8000", "-t", "templates"]
