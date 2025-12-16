# Интернет-магазин на Django

## 1. НАЗНАЧЕНИЕ ПРОГРАММЫ

Создание веб-платформы для размещения и продажи товаров в интернете. Программа предоставляет полный цикл взаимодействия между продавцом и покупателем: от просмотра каталога товаров до оформления заказа и оставления отзывов.

## 2. ФУНКЦИОНАЛЬНЫЕ ВОЗМОЖНОСТИ

### Для покупателей:
- **Регистрация и аутентификация** - создание учетной записи, вход/выход из системы
- **Просмотр каталога товаров** - навигация по категориям и брендам
- **Фильтрация и поиск** - поиск товаров по названию, фильтрация по цене, рейтингу, наличию
- **Управление корзиной** - добавление/удаление товаров, изменение количества
- **Оформление заказов** - создание заказа с указанием деталей доставки
- **Отслеживание заказов** - просмотр истории заказов и их текущего статуса
- **Оставление отзывов** - написание отзывов и оценка купленных товаров
- **Личный кабинет** - управление профилем, просмотр корзины, быстрые действия

### Для администраторов:
- **Управление товарами** - добавление, редактирование, удаление товаров
- **Управление заказами** - изменение статусов заказов, обработка оплат
- **Управление пользователями** - просмотр и управление учетными записями
- **Управление категориями** - создание и редактирование категорий товаров
- **Статистика** - просмотр статистики по продажам и пользователям

## 3. СПОСОБЫ УСТАНОВКИ

### Требования:
- **Python 3.13.7**
- **Django 6.0**
- **PostgreSQL 16.0** (база данных)
- **pip** (менеджер пакетов Python)

### Установка PostgreSQL 16.0:
```bash
# Для Ubuntu/Debian:
sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update
sudo apt install postgresql-16 postgresql-contrib-16

# Для CentOS/RHEL:
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm
sudo dnf install -y postgresql16-server postgresql16-contrib

# Для Windows:
# Скачайте установщик с официального сайта: https://www.postgresql.org/download/windows/

# Запуск и настройка PostgreSQL:
sudo systemctl start postgresql-16
sudo systemctl enable postgresql-16

# Создание базы данных и пользователя:
sudo -u postgres psql
CREATE DATABASE shopdb;
CREATE USER shopuser WITH PASSWORD 'ваш_надежный_пароль';
ALTER ROLE shopuser SET client_encoding TO 'UTF8';
ALTER ROLE shopuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE shopuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE shopdb TO shopuser;
\q